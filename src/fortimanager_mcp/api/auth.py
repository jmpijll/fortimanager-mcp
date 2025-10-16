"""Authentication handlers for FortiManager API."""

import logging
from typing import Protocol

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
) -> AuthProvider:
    """Create appropriate authentication provider based on configuration.

    Args:
        api_token: API token for token-based auth
        username: Username for session-based auth
        password: Password for session-based auth

    Returns:
        Authentication provider instance

    Raises:
        AuthenticationError: If no valid authentication configuration provided
    """
    if api_token:
        logger.info("Selected token-based authentication")
        return TokenAuthProvider(api_token)

    if username and password:
        logger.info("Selected session-based authentication")
        return SessionAuthProvider(username, password)

    raise AuthenticationError(
        "No authentication configuration provided. "
        "Set FORTIMANAGER_API_TOKEN or both FORTIMANAGER_USERNAME and FORTIMANAGER_PASSWORD"
    )

