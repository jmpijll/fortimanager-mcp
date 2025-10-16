"""Database cache operations API module."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient


class DBCacheAPI:
    """Database cache operations for performance optimization."""

    def __init__(self, client: FortiManagerClient) -> None:
        """Initialize DB Cache API.

        Args:
            client: FortiManager client instance
        """
        self.client = client

    async def clear_db_cache(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Clear database cache for an ADOM.

        Clears cached database queries to force fresh data retrieval.
        Use this when you suspect stale data or after major configuration changes.

        Args:
            adom: ADOM name

        Returns:
            Operation result
        """
        url = f"/cache/adom/{adom}/clear"
        return await self.client.execute(url, {})

    async def get_db_cache_status(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get database cache statistics and status.

        Retrieves cache hit rates, size, and performance metrics.

        Args:
            adom: ADOM name

        Returns:
            Cache statistics
        """
        url = f"/cache/adom/{adom}/status"
        return await self.client.get(url)


