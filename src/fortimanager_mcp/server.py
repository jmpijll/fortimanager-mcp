"""FortiManager MCP Server implementation."""

import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncIterator

from mcp.server.fastmcp import FastMCP

from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.utils.config import get_settings

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()
settings.configure_logging()

# Create FortiManager client (will be initialized on lifespan)
fmg_client: FortiManagerClient | None = None


# Dynamic mode: lightweight discovery tools
def register_dynamic_tools(mcp_server: FastMCP) -> None:
    """Register discovery tools for dynamic mode only."""
    # Import here to avoid heavy imports at module import time
    from fortimanager_mcp.utils.tool_registry import (  # noqa: E402
        execute_tool_dynamic,
        get_tool_metadata,
        populate_registry,
    )

    # Ensure registry is populated (idempotent)
    populate_registry()

    @mcp_server.tool()
    async def find_fortimanager_tool(operation: str) -> dict[str, Any]:
        """Discover FortiManager tools by operation name/keywords."""
        # Basic metadata-driven search
        op = operation.lower().strip()
        results: list[dict[str, Any]] = []
        # get_tool_metadata(None) is not supported; rely on registry introspection
        # Pull a small, representative set for now; full index search is handled inside registry helpers if available
        candidates = [
            "list_devices",
            "list_adoms",
            "list_firewall_policies",
            "get_system_status",
        ]
        for name in candidates:
            meta = get_tool_metadata(name)
            if not meta:
                continue
            hay = f"{name} {getattr(meta, 'module', '')} {getattr(meta, 'description', '')}".lower()
            if all(tok in hay for tok in op.split()):
                results.append(
                    {
                        "name": name,
                        "category": getattr(meta, "module", "unknown"),
                        "description": getattr(meta, "description", name.replace("_", " ")),
                        "how_to_use": f"execute_advanced_tool(tool_name='{name}', ...)",
                    }
                )
        return {
            "status": "success" if results else "not_found",
            "operation": operation,
            "found": len(results),
            "tools": results,
        }

    @mcp_server.tool()
    async def execute_advanced_tool(
        tool_name: str,
        parameters: dict | None = None,
        kwargs: dict | None = None,
    ) -> Any:
        """Execute a FortiManager operation dynamically by tool name.

        Supports both flat kwargs and a nested 'parameters' dict from some MCP clients.
        """
        merged: dict[str, Any] = {}
        if parameters and isinstance(parameters, dict):
            merged.update(parameters)
        if kwargs and isinstance(kwargs, dict):
            merged.update(kwargs)
        return await execute_tool_dynamic(tool_name, **merged)

    @mcp_server.tool()
    def list_fortimanager_categories() -> dict[str, Any]:
        """List high-level FortiManager operation categories (metadata-only)."""
        # Keep in sync with utils.tool_registry registry summary if available
        return {
            "status": "success",
            "note": "Categories summary provided in dynamic mode",
        }




def get_fmg_client() -> FortiManagerClient | None:
    """Get the global FortiManager client instance.
    
    Returns:
        FortiManager client or None if not initialized
    """
    return fmg_client


@asynccontextmanager
async def server_lifespan(server: FastMCP) -> AsyncIterator[dict]:
    """Manage server startup and shutdown.

    Args:
        server: FastMCP server instance

    Yields:
        Dictionary with FortiManager client
    """
    global fmg_client

    logger.info("Starting FortiManager MCP server")

    # Initialize and connect FortiManager client
    fmg_client = FortiManagerClient.from_settings(settings)
    await fmg_client.connect()

    logger.info("FortiManager MCP server started successfully")

    try:
        yield {"fmg_client": fmg_client}
    finally:
        # Cleanup on shutdown
        logger.info("Shutting down FortiManager MCP server")
        if fmg_client:
            await fmg_client.disconnect()
        logger.info("FortiManager MCP server shut down")


# Create FastMCP server
mcp = FastMCP(
    "FortiManager API Server",
    stateless_http=True,  # Stateless for Docker deployment
    lifespan=server_lifespan,
)


# Health check resource
@mcp.resource("health://status")
def health_check() -> str:
    """Health check resource for monitoring.

    Returns:
        Health status message
    """
    mode = settings.FMG_TOOL_MODE
    if mode == "full":
        tool_info = "590 tools loaded"
    else:
        tool_info = "3 discovery tools + 590+ operations via dynamic execution"
    return f"FortiManager MCP Server is healthy (mode: {mode}, {tool_info})"




# Conditional tool loading based on FMG_TOOL_MODE
if settings.FMG_TOOL_MODE == "dynamic":
    # Dynamic mode: register discovery tools only
    logger.info("Loading in DYNAMIC mode - discovery tools only")
    register_dynamic_tools(mcp)
    
else:
    # Full mode: Load all tools (default behavior)
    logger.info("Loading in FULL mode - all 590 tools")
    logger.info("This consumes ~118K tokens for tool definitions")
    
    # Import all tool modules (registers them with the server)
    from fortimanager_mcp.tools import (  # noqa: E402, F401
        additional_object_tools,
        adom_tools,
        advanced_object_tools,
        connector_tools,
        csf_tools,
        dbcache_tools,
        device_tools,
        docker_tools,
        fmgcloud_tools,
        fortiguard_tools,
        metafield_tools,
        monitoring_tools,
        object_tools,
        optionattr_tools,
        policy_tools,
        provisioning_tools,
        qos_tools,
        script_tools,
        sdwan_tools,
        security_tools,
        subfetch_tools,
        sysproxy_tools,
        system_tools,
        vpn_tools,
        workspace_tools,
    )


def main() -> None:
    """Entry point for the MCP server."""
    import sys
    import os
    
    # Determine server mode from settings
    server_mode = settings.MCP_SERVER_MODE
    
    if server_mode == "auto":
        # Auto-detect mode based on environment
        is_docker = os.path.exists("/.dockerenv") or os.getenv("DOCKER_CONTAINER") == "1"
        
        if is_docker or sys.stdin.isatty():
            # Docker or TTY → HTTP mode
            server_mode = "http"
        else:
            # Pipe stdin → stdio mode (Claude Desktop, etc.)
            server_mode = "stdio"
    
    if server_mode == "stdio":
        # Run in stdio mode for MCP clients (Claude Desktop, LM Studio, etc.)
        logger.info("Starting MCP server in stdio mode")
        run_stdio()
    else:
        # Run in HTTP mode for Docker deployment
        logger.info(f"Starting MCP server in HTTP mode on {settings.MCP_SERVER_HOST}:{settings.MCP_SERVER_PORT}")
        run_http()


def run_stdio() -> None:
    """Run MCP server in stdio mode for LM Studio and similar clients."""
    import asyncio
    
    async def stdio_main():
        """Main coroutine for stdio mode."""
        global fmg_client
        
        # Initialize FortiManager connection
        logger.info("Initializing FortiManager connection")
        fmg_client = FortiManagerClient.from_settings(settings)
        
        try:
            await fmg_client.connect()
            logger.info("FortiManager connection established")
        except Exception as e:
            logger.warning(f"FortiManager connection failed: {e}. Server will still start.")
        
        try:
            # Run FastMCP in stdio mode (use the async version directly)
            await mcp.run_stdio_async()
        finally:
            # Cleanup
            logger.info("Closing FortiManager connection")
            if fmg_client:
                await fmg_client.disconnect()
    
    # Run the async main
    asyncio.run(stdio_main())


def run_http() -> None:
    """Run MCP server in HTTP mode for Docker deployment."""
    import uvicorn
    from contextlib import asynccontextmanager
    from starlette.applications import Starlette
    from starlette.routing import Mount, Route
    from starlette.responses import JSONResponse
    from starlette.requests import Request

    # Health check endpoint
    async def health_endpoint(request: Request) -> JSONResponse:
        """HTTP health check endpoint for Docker health checks."""
        global fmg_client
        
        # Check if client is connected by verifying _client attribute exists
        is_connected = fmg_client is not None and fmg_client._client is not None
        
        health_status = {
            "status": "healthy",
            "service": "fortimanager-mcp",
            "fortimanager_connected": is_connected
        }
        
        return JSONResponse(health_status, status_code=200)

    # Create Starlette app with lifespan
    @asynccontextmanager
    async def app_lifespan(app):
        """Ensure MCP session manager and FortiManager client start."""
        # Start MCP session manager which also runs our server_lifespan
        async with mcp.session_manager.run():
            # Also initialize FortiManager connection manually since stateless mode doesn't trigger lifespan
            global fmg_client
            logger.info("Initializing FortiManager connection")
            fmg_client = FortiManagerClient.from_settings(settings)
            try:
                await fmg_client.connect()
                logger.info("FortiManager connection established")
                yield
            except Exception as e:
                logger.warning(f"FortiManager connection failed: {e}. Server will still start.")
                # Server can still start even if FortiManager is not available
                yield
            finally:
                logger.info("Closing FortiManager connection")
                if fmg_client:
                    await fmg_client.disconnect()
    
    # Create app with MCP mounted and proper lifespan
    app = Starlette(
        routes=[
            Route("/health", health_endpoint, methods=["GET"]),
            Mount("/", app=mcp.streamable_http_app()),
        ],
        lifespan=app_lifespan,
    )
    
    # Run with uvicorn
    uvicorn.run(
        app,
        host=settings.MCP_SERVER_HOST,
        port=settings.MCP_SERVER_PORT,
        log_level=settings.LOG_LEVEL.lower(),
    )


if __name__ == "__main__":
    main()

