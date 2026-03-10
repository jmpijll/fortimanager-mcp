"""Base FortiManager API client with JSON-RPC implementation."""

import logging
from typing import Any, Literal

import httpx

from fortimanager_mcp.api.auth import AuthProvider, create_auth_provider
from fortimanager_mcp.api.models import APIResponse, JSONRPCRequest
from fortimanager_mcp.utils.config import Settings
from fortimanager_mcp.utils.errors import (
    APIError,
    ConnectionError,
    TimeoutError,
    parse_fmg_error,
)

logger = logging.getLogger(__name__)


class FortiManagerClient:
    """Base client for FortiManager JSON RPC API.

    This client handles:
    - Authentication (token-based and session-based)
    - JSON-RPC request/response formatting
    - Error handling and retries
    - Connection pooling
    """

    def __init__(
        self,
        host: str,
        api_token: str | None = None,
        username: str | None = None,
        password: str | None = None,
        verify_ssl: bool = True,
        timeout: int = 30,
        max_retries: int = 3,
        forticloud: bool = False,
        forticloud_client_id: str = "FortiManager",
    ) -> None:
        """Initialize FortiManager client.

        Args:
            host: FortiManager hostname or IP
            api_token: API token for authentication
            username: Username for session-based auth
            password: Password for session-based auth
            verify_ssl: Verify SSL certificates
            timeout: Request timeout in seconds
            max_retries: Maximum retry attempts
            forticloud: Use FortiCloud OAuth flow
            forticloud_client_id: FortiCloud OAuth client_id

        Raises:
            AuthenticationError: If no valid authentication provided
        """
        self.host = host.replace("https://", "").replace("http://", "").rstrip("/")
        self.base_url = f"https://{self.host}/jsonrpc"
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.max_retries = max_retries

        # Create authentication provider
        self.auth = create_auth_provider(
            api_token=api_token,
            username=username,
            password=password,
            forticloud=forticloud,
            forticloud_client_id=forticloud_client_id,
        )

        # HTTP client (created on connect)
        self._client: httpx.AsyncClient | None = None
        self._session_id: str | None = None
        self._request_id = 0

        logger.info(f"Initialized FortiManager client for {self.host}")

    @classmethod
    def from_settings(cls, settings: Settings) -> "FortiManagerClient":
        """Create client from settings.

        Args:
            settings: Application settings

        Returns:
            Configured FortiManager client
        """
        return cls(
            host=settings.FORTIMANAGER_HOST,
            api_token=settings.FORTIMANAGER_API_TOKEN,
            username=settings.FORTIMANAGER_USERNAME,
            password=settings.FORTIMANAGER_PASSWORD,
            verify_ssl=settings.FORTIMANAGER_VERIFY_SSL,
            timeout=settings.FORTIMANAGER_TIMEOUT,
            max_retries=settings.FORTIMANAGER_MAX_RETRIES,
            forticloud=settings.FORTICLOUD_AUTH,
            forticloud_client_id=settings.FORTICLOUD_CLIENT_ID,
        )

    async def connect(self) -> None:
        """Establish connection and authenticate.

        Raises:
            ConnectionError: If connection fails
            AuthenticationError: If authentication fails
        """
        if self._client:
            logger.warning("Client already connected")
            return

        logger.info("Connecting to FortiManager")

        # Create HTTP client
        self._client = httpx.AsyncClient(
            verify=self.verify_ssl,
            timeout=httpx.Timeout(self.timeout),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
        )

        # Authenticate (returns session ID or None for token auth)
        try:
            self._session_id = await self.auth.authenticate(self._client, self.base_url)
            logger.info("Successfully connected to FortiManager")
        except Exception as e:
            await self.disconnect()
            raise

    async def disconnect(self) -> None:
        """Disconnect and cleanup resources."""
        client = self._client
        if not client:
            return

        self._client = None

        logger.info("Disconnecting from FortiManager")

        # Logout if using session auth
        if self._session_id:
            try:
                await self.auth.logout(client, self.base_url, self._session_id)
            except Exception as e:
                logger.warning(f"Logout failed: {e}")
            finally:
                self._session_id = None

        # Close HTTP client
        await client.aclose()
        logger.info("Disconnected from FortiManager")

    async def __aenter__(self) -> "FortiManagerClient":
        """Async context manager entry."""
        await self.connect()
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Async context manager exit."""
        await self.disconnect()

    def _get_next_request_id(self) -> int:
        """Get next request ID.

        Returns:
            Incremented request ID
        """
        self._request_id += 1
        return self._request_id

    async def _request(
        self,
        method: Literal["get", "add", "set", "update", "delete", "exec", "clone", "move"],
        url: str,
        data: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
    ) -> APIResponse:
        """Execute JSON-RPC request.

        Args:
            method: RPC method
            url: API endpoint URL (without /jsonrpc)
            data: Request data
            params: Additional parameters (fields, loadsub, etc.)

        Returns:
            API response

        Raises:
            ConnectionError: If not connected
            APIError: If API returns error
            TimeoutError: If request times out
        """
        if not self._client:
            raise ConnectionError("Not connected. Call connect() first.")

        # Build request params
        request_params: dict[str, Any] = {"url": url}
        if data:
            request_params["data"] = data
        if params:
            request_params.update(params)

        # Build JSON-RPC request
        payload = {
            "id": self._get_next_request_id(),
            "method": method,
            "params": [request_params],
            "verbose": 1,  # Use symbolic values
        }

        # Add session for session-based auth
        if self._session_id:
            payload["session"] = self._session_id

        # Log request (sanitized)
        logger.debug(f"Request: {method} {url}")

        try:
            response = await self._client.post(
                self.base_url,
                json=payload,
                headers=self.auth.get_headers(),
            )
            response.raise_for_status()
            data = response.json()

            # Parse response
            api_response = APIResponse(**data)

            # Check for errors
            if not api_response.is_success:
                error_code = api_response.error_code or -1
                error_msg = api_response.error_message or "Unknown error"
                raise parse_fmg_error(error_code, error_msg, url)

            logger.debug(f"Response: {method} {url} - Success")
            return api_response

        except httpx.TimeoutException as e:
            logger.error(f"Request timeout: {method} {url}")
            raise TimeoutError(f"Request timeout: {url}") from e
        except httpx.HTTPStatusError as e:
            logger.error(f"HTTP error {e.response.status_code}: {method} {url}")
            raise ConnectionError(f"HTTP {e.response.status_code}: {url}") from e
        except httpx.RequestError as e:
            logger.error(f"Request error: {method} {url}: {e}")
            raise ConnectionError(f"Connection error: {url}") from e

    async def get(
        self,
        url: str,
        fields: list[str] | None = None,
        filter: list[Any] | None = None,
        loadsub: int = 1,
        **kwargs: Any,
    ) -> Any:
        """Get object(s) from FortiManager.

        Args:
            url: API endpoint URL
            fields: List of fields to return
            filter: Filter criteria [field, operator, value]
            loadsub: Load sub-objects (0=no, 1=yes)
            **kwargs: Additional parameters

        Returns:
            Retrieved data

        Example:
            # Get all devices
            devices = await client.get("/dvmdb/device")

            # Get specific device fields
            device = await client.get(
                "/dvmdb/device/device-001",
                fields=["name", "ip", "os_ver"]
            )

            # Get with filter
            devices = await client.get(
                "/dvmdb/device",
                filter=["os_ver", "==", "7.0"]
            )
        """
        params = {"loadsub": loadsub, **kwargs}
        if fields:
            params["fields"] = fields
        if filter:
            params["filter"] = filter

        response = await self._request("get", url, params=params)
        return response.data

    async def add(self, url: str, data: dict[str, Any], **kwargs: Any) -> Any:
        """Add new object to FortiManager.

        Args:
            url: API endpoint URL
            data: Object data
            **kwargs: Additional parameters

        Returns:
            Created object data

        Example:
            # Create firewall address
            address = await client.add(
                "/pm/config/adom/root/obj/firewall/address",
                data={
                    "name": "internal_network",
                    "subnet": "10.0.0.0/8",
                    "comment": "Internal network"
                }
            )
        """
        response = await self._request("add", url, data=data, params=kwargs)
        return response.data

    async def set(self, url: str, data: dict[str, Any], **kwargs: Any) -> Any:
        """Set/update object in FortiManager.

        Args:
            url: API endpoint URL (must include object identifier)
            data: Updated object data
            **kwargs: Additional parameters

        Returns:
            Updated object data

        Example:
            # Update firewall address
            address = await client.set(
                "/pm/config/adom/root/obj/firewall/address/internal_network",
                data={"comment": "Updated comment"}
            )
        """
        response = await self._request("set", url, data=data, params=kwargs)
        return response.data

    async def update(self, url: str, data: dict[str, Any], **kwargs: Any) -> Any:
        """Update object in FortiManager (alias for set).

        Args:
            url: API endpoint URL
            data: Updated object data
            **kwargs: Additional parameters

        Returns:
            Updated object data
        """
        return await self.set(url, data, **kwargs)

    async def delete(self, url: str, **kwargs: Any) -> Any:
        """Delete object from FortiManager.

        Args:
            url: API endpoint URL (must include object identifier)
            **kwargs: Additional parameters

        Returns:
            Deletion result

        Example:
            # Delete firewall address
            await client.delete(
                "/pm/config/adom/root/obj/firewall/address/internal_network"
            )
        """
        response = await self._request("delete", url, params=kwargs)
        return response.data

    async def execute(self, url: str, data: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        """Execute operation on FortiManager.

        Args:
            url: API endpoint URL
            data: Operation data
            **kwargs: Additional parameters

        Returns:
            Execution result

        Example:
            # Install device settings
            result = await client.execute(
                "/securityconsole/install/device",
                data={
                    "adom": "root",
                    "scope": [{"name": "device-001", "vdom": "root"}]
                }
            )
        """
        response = await self._request("exec", url, data=data, params=kwargs)
        return response.data

    async def exec(self, url: str, data: dict[str, Any] | None = None, **kwargs: Any) -> Any:
        """Alias for execute() method.
        
        Args:
            url: API endpoint URL
            data: Operation data
            **kwargs: Additional parameters

        Returns:
            Execution result
        """
        return await self.execute(url, data=data, **kwargs)

    async def clone(self, url: str, data: dict[str, Any], **kwargs: Any) -> Any:
        """Clone object in FortiManager.

        Args:
            url: API endpoint URL
            data: Clone configuration
            **kwargs: Additional parameters

        Returns:
            Cloned object data
        """
        response = await self._request("clone", url, data=data, params=kwargs)
        return response.data

    async def move(self, url: str, data: dict[str, Any], **kwargs: Any) -> Any:
        """Move/reorder object in FortiManager.

        Args:
            url: API endpoint URL
            data: Move configuration (target, option)
            **kwargs: Additional parameters

        Returns:
            Move result

        Example:
            # Move policy
            await client.move(
                "/pm/config/adom/root/pkg/default/firewall/policy/10",
                data={"option": "after", "target": 5}
            )
        """
        response = await self._request("move", url, data=data, params=kwargs)
        return response.data

