"""FortiManager MCP Server implementation."""

import logging
from contextlib import asynccontextmanager
from typing import AsyncIterator

from mcp.server.fastmcp import FastMCP

from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.utils.config import get_settings

logger = logging.getLogger(__name__)

# Get settings
settings = get_settings()
settings.configure_logging()

# Create FortiManager client (will be initialized on lifespan)
fmg_client: FortiManagerClient | None = None


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
    return "FortiManager MCP Server is healthy"


# Import tools (registers them with the server)
from fortimanager_mcp.tools import additional_object_tools, advanced_object_tools, device_tools, fortiguard_tools, monitoring_tools, object_tools, policy_tools, provisioning_tools, script_tools, sdwan_tools, security_tools, system_tools, vpn_tools, workspace_tools  # noqa: E402, F401


def main() -> None:
    """Entry point for the MCP server."""
    import uvicorn
    from contextlib import asynccontextmanager
    from starlette.applications import Starlette
    from starlette.routing import Mount
    
    logger.info(f"Starting MCP server on {settings.MCP_SERVER_HOST}:{settings.MCP_SERVER_PORT}")

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
            finally:
                logger.info("Closing FortiManager connection")
                await fmg_client.disconnect()
    
    # Create app with MCP mounted and proper lifespan
    app = Starlette(
        routes=[
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

