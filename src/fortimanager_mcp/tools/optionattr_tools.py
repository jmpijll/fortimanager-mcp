"""MCP tools for option attribute operations."""

import logging
from typing import Any

from fortimanager_mcp.api.optionattr import OptionAttributeAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_optionattr_api() -> OptionAttributeAPI:
    """Get OptionAttributeAPI instance."""
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return OptionAttributeAPI(client)


@mcp.tool()
async def get_object_type_option_attributes(
    object_type: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get available option attributes for a FortiManager object type.

    Retrieves metadata about all configurable options and their valid values
    for a specific object type. Useful for understanding what fields can be
    configured and their constraints.

    Common object types:
    - "firewall.policy" - Firewall policy options
    - "firewall.address" - Firewall address options
    - "firewall.service.custom" - Service options
    - "pkg.firewall.policy" - Policy package options

    Args:
        object_type: Object type identifier
        adom: ADOM name (default: root)

    Returns:
        Dictionary with option attributes and definitions
    """
    try:
        api = _get_optionattr_api()
        attributes = await api.get_option_attributes(object_type=object_type, adom=adom)
        return {
            "status": "success",
            "object_type": object_type,
            "adom": adom,
            "attributes": attributes,
        }
    except Exception as e:
        logger.error(f"Error getting option attributes: {e}")
        return {"status": "error", "message": str(e)}

