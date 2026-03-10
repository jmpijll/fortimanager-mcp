"""Authentication handlers for FortiManager API."""

import logging
from typing import Protocol
from urllib.parse import urlparse

import httpx

from fortimanager_mcp.utils.errors import AuthenticationError

logger = logging.getLogger(__name__)


class AuthProvider(Protocol):
    """Protocol for authentication providers."""

    async def authenticate(self, client: httpx.AsyncClient, base_url: str) -> str | None:
        """Authenticate and return session ID or None for token auth.

        Args:
            client: HTTP client instance
            base_url: FortiManager base URL

        Returns:
            Session ID for session-based auth, None for token-based auth

        Raises:
            AuthenticationError: If authentication fails
        """
        ...

    def get_headers(self) -> dict[str, str]:
        """Get authentication headers for requests.

        Returns:
            Dictionary of HTTP headers
        """
        ...

    async def logout(self, client: httpx.AsyncClient, base_url: str, session: str) -> None:
        """Logout and cleanup session.

        Args:
            client: HTTP client instance
            base_url: FortiManager base URL
            session: Session ID to logout
        """
        ...


class TokenAuthProvider:
    """API token-based authentication provider."""

    def __init__(self, api_token: str) -> None:
        """Initialize token auth provider.

        Args:
            api_token: FortiManager API token
        """
        self.api_token = api_token
        logger.debug("Initialized token-based authentication")

    async def authenticate(self, client: httpx.AsyncClient, base_url: str) -> None:
        """No authentication required for token-based auth.

        Args:
            client: HTTP client instance (unused)
            base_url: FortiManager base URL (unused)

        Returns:
            None (token is sent with each request)
        """
        logger.info("Using token-based authentication")
        return None

    def get_headers(self) -> dict[str, str]:
        """Get authentication headers with bearer token.

        Returns:
            Dictionary with Authorization header
        """
        return {
            "Authorization": f"Bearer {self.api_token}",
            "Content-Type": "application/json",
        }

    async def logout(self, client: httpx.AsyncClient, base_url: str, session: str) -> None:
        """No logout required for token-based auth.

        Args:
            client: HTTP client instance (unused)
            base_url: FortiManager base URL (unused)
            session: Session ID (unused)
        """
        pass


class FortiCloudAuthProvider:
    """FortiCloud OAuth authentication provider.

    Uses a two-step OAuth flow:
    1. Get access token from FortiCloud IAM
    2. Exchange access token for a FortiManager session
    """

    FORTICLOUD_AUTH_URL = "https://customerapiauth.fortinet.com/api/v1/oauth/token/"

    def __init__(self, username: str, password: str, client_id: str = "FortiManager") -> None:
        """Initialize FortiCloud auth provider.

        Args:
            username: FortiCloud IAM user ID
            password: FortiCloud IAM secret
            client_id: OAuth client_id ('FortiManager' or 'FortiAnalyzer')
        """
        self.username = username
        self.password = password
        self.client_id = client_id
        self._session_id: str | None = None
        logger.debug(f"Initialized FortiCloud authentication for user: {username}")

    async def authenticate(self, client: httpx.AsyncClient, base_url: str) -> str:
        """Authenticate via FortiCloud OAuth and obtain session ID.

        Args:
            client: HTTP client instance
            base_url: FortiManager base URL (e.g. https://host/jsonrpc)

        Returns:
            Session ID

        Raises:
            AuthenticationError: If authentication fails
        """
        logger.info("Authenticating via FortiCloud OAuth")

        # Step 1: Get OAuth access token from FortiCloud IAM
        token_payload = {
            "username": self.username,
            "password": self.password,
            "client_id": self.client_id,
            "grant_type": "password",
        }

        try:
            token_response = await client.post(
                self.FORTICLOUD_AUTH_URL,
                json=token_payload,
                headers={"Content-Type": "application/json"},
            )
            token_response.raise_for_status()
            token_data = token_response.json()

            access_token = token_data.get("access_token")
            if not access_token:
                raise AuthenticationError("No access_token in FortiCloud OAuth response")

            logger.debug("Successfully obtained FortiCloud access token")

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during FortiCloud OAuth: {e}")
            raise AuthenticationError(f"FortiCloud OAuth failed: HTTP {e.response.status_code}") from e
        except httpx.RequestError as e:
            logger.error(f"Request error during FortiCloud OAuth: {e}")
            raise AuthenticationError(f"FortiCloud OAuth connection error: {e}") from e

        # Step 2: Exchange access token for FortiManager session
        # Derive the host from base_url (strip /jsonrpc path)
        parsed = urlparse(base_url)
        login_url = f"{parsed.scheme}://{parsed.netloc}/p/forticloud_jsonrpc_login/"

        login_payload = {"access_token": access_token}

        try:
            login_response = await client.post(
                login_url,
                json=login_payload,
                headers={"Content-Type": "application/json"},
            )
            login_response.raise_for_status()
            login_data = login_response.json()

            session_id = login_data.get("session")
            if not session_id:
                raise AuthenticationError("No session ID in FortiCloud login response")

            self._session_id = session_id
            logger.info("Successfully authenticated via FortiCloud OAuth")
            return session_id

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during FortiCloud login: {e}")
            raise AuthenticationError(f"FortiCloud login failed: HTTP {e.response.status_code}") from e
        except httpx.RequestError as e:
            logger.error(f"Request error during FortiCloud login: {e}")
            raise AuthenticationError(f"FortiCloud login connection error: {e}") from e

    def get_headers(self) -> dict[str, str]:
        """Get authentication headers.

        Returns:
            Dictionary with Content-Type header
        """
        return {"Content-Type": "application/json"}

    async def logout(self, client: httpx.AsyncClient, base_url: str, session: str) -> None:
        """Logout and cleanup session.

        Args:
            client: HTTP client instance
            base_url: FortiManager base URL
            session: Session ID to logout
        """
        if not session:
            return

        logger.info("Logging out FortiCloud session")

        payload = {
            "id": 1,
            "method": "exec",
            "params": [{"url": "sys/logout"}],
            "session": session,
            "verbose": 1,
        }

        try:
            response = await client.post(
                base_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            logger.info("Successfully logged out FortiCloud session")
        except Exception as e:
            logger.warning(f"FortiCloud logout failed (non-critical): {e}")

        self._session_id = None

    @property
    def session_id(self) -> str | None:
        """Get current session ID."""
        return self._session_id


class SessionAuthProvider:
    """Session-based authentication provider."""

    def __init__(self, username: str, password: str) -> None:
        """Initialize session auth provider.

        Args:
            username: FortiManager username
            password: FortiManager password
        """
        self.username = username
        self.password = password
        self._session_id: str | None = None
        logger.debug(f"Initialized session-based authentication for user: {username}")

    async def authenticate(self, client: httpx.AsyncClient, base_url: str) -> str:
        """Authenticate and obtain session ID.

        Args:
            client: HTTP client instance
            base_url: FortiManager base URL

        Returns:
            Session ID

        Raises:
            AuthenticationError: If authentication fails
        """
        logger.info(f"Authenticating user: {self.username}")

        payload = {
            "id": 1,
            "method": "exec",
            "params": [
                {
                    "url": "sys/login/user",
                    "data": {
                        "user": self.username,
                        "passwd": self.password,
                    },
                }
            ],
            "verbose": 1,
        }

        try:
            response = await client.post(
                base_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            data = response.json()

            # Check for errors
            if not data.get("result"):
                raise AuthenticationError("No result in login response")

            result = data["result"][0]
            status = result.get("status", {})

            if status.get("code") != 0:
                error_msg = status.get("message", "Unknown error")
                raise AuthenticationError(f"Login failed: {error_msg}", code=status.get("code"))

            # Extract session ID
            session_id = data.get("session")
            if not session_id:
                raise AuthenticationError("No session ID in login response")

            self._session_id = session_id
            logger.info("Successfully authenticated")
            return session_id

        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error during authentication: {e}")
            raise AuthenticationError(f"HTTP error: {e.response.status_code}") from e
        except httpx.RequestError as e:
            logger.error(f"Request error during authentication: {e}")
            raise AuthenticationError(f"Connection error: {e}") from e
        except KeyError as e:
            logger.error(f"Unexpected response format: {e}")
            raise AuthenticationError("Invalid response format") from e

    def get_headers(self) -> dict[str, str]:
        """Get authentication headers.

        Returns:
            Dictionary with Content-Type header
        """
        return {"Content-Type": "application/json"}

    async def logout(self, client: httpx.AsyncClient, base_url: str, session: str) -> None:
        """Logout and cleanup session.

        Args:
            client: HTTP client instance
            base_url: FortiManager base URL
            session: Session ID to logout
        """
        if not session:
            return

        logger.info("Logging out session")

        payload = {
            "id": 1,
            "method": "exec",
            "params": [{"url": "sys/logout"}],
            "session": session,
            "verbose": 1,
        }

        try:
            response = await client.post(
                base_url,
                json=payload,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            logger.info("Successfully logged out")
        except Exception as e:
            logger.warning(f"Logout failed (non-critical): {e}")

        self._session_id = None

    @property
    def session_id(self) -> str | None:
        """Get current session ID.

        Returns:
            Session ID or None if not authenticated
        """
        return self._session_id


def create_auth_provider(
    api_token: str | None = None,
    username: str | None = None,
    password: str | None = None,
    forticloud: bool = False,
    forticloud_client_id: str = "FortiManager",
) -> AuthProvider:
    """Create appropriate authentication provider based on configuration.

    Args:
        api_token: API token for token-based auth
        username: Username for session-based auth
        password: Password for session-based auth
        forticloud: Use FortiCloud OAuth flow
        forticloud_client_id: FortiCloud OAuth client_id

    Returns:
        Authentication provider instance

    Raises:
        AuthenticationError: If no valid authentication configuration provided
    """
    if api_token:
        logger.info("Selected token-based authentication")
        return TokenAuthProvider(api_token)

    if forticloud:
        if not (username and password):
            raise AuthenticationError(
                "FortiCloud authentication requires both "
                "FORTIMANAGER_USERNAME and FORTIMANAGER_PASSWORD"
            )
        logger.info("Selected FortiCloud OAuth authentication")
        return FortiCloudAuthProvider(username, password, client_id=forticloud_client_id)

    if username and password:
        logger.info("Selected session-based authentication")
        return SessionAuthProvider(username, password)

    raise AuthenticationError(
        "No authentication configuration provided. "
        "Set FORTIMANAGER_API_TOKEN, or both FORTIMANAGER_USERNAME and FORTIMANAGER_PASSWORD, "
        "or enable FORTICLOUD_AUTH with FORTIMANAGER_USERNAME and FORTIMANAGER_PASSWORD"
    )

