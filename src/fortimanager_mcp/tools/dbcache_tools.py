"""MCP tools for database cache operations."""

import logging
from typing import Any

from fortimanager_mcp.api.dbcache import DBCacheAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_dbcache_api() -> DBCacheAPI:
    """Get DBCacheAPI instance."""
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return DBCacheAPI(client)


@mcp.tool()
async def clear_database_cache(adom: str = "root") -> dict[str, Any]:
    """Clear database cache for an ADOM to force fresh data retrieval.

    Use this when you suspect stale cached data or after major configuration changes.
    The cache will be automatically rebuilt on subsequent queries.

    Args:
        adom: ADOM name (default: root)

    Returns:
        Dictionary with operation status
    """
    try:
        api = _get_dbcache_api()
        result = await api.clear_db_cache(adom=adom)
        return {"status": "success", "message": f"Database cache cleared for ADOM '{adom}'", "result": result}
    except Exception as e:
        logger.error(f"Error clearing database cache: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_database_cache_statistics(adom: str = "root") -> dict[str, Any]:
    """Get database cache statistics and performance metrics.

    Retrieves cache hit rates, memory usage, and efficiency metrics.
    Useful for performance tuning and troubleshooting.

    Args:
        adom: ADOM name (default: root)

    Returns:
        Dictionary with cache statistics
    """
    try:
        api = _get_dbcache_api()
        stats = await api.get_db_cache_status(adom=adom)
        return {"status": "success", "adom": adom, "cache_stats": stats}
    except Exception as e:
        logger.error(f"Error getting cache statistics: {e}")
        return {"status": "error", "message": str(e)}


