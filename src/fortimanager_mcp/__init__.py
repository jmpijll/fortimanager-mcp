"""FortiManager MCP Server - Model Context Protocol server for FortiManager JSON RPC API."""

__version__ = "0.1.0"
__author__ = "Jamie van der Pijll"
__description__ = "MCP server exposing FortiManager API operations as standardized tools"

from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.utils.config import Settings
from fortimanager_mcp.utils.errors import FortiManagerError

__all__ = [
    "FortiManagerClient",
    "Settings",
    "FortiManagerError",
]

