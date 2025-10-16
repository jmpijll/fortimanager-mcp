"""MCP tools for FortiGuard management."""

import logging
from typing import Any

from fortimanager_mcp.api.fortiguard import FortiGuardAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_fortiguard_api() -> FortiGuardAPI:
    """Get FortiGuard API instance."""
    client = get_fmg_client()
    return FortiGuardAPI(client)


# ============================================================================
# FortiGuard Database & Versions
# ============================================================================

@mcp.tool()
async def get_fortiguard_database_versions() -> dict[str, Any]:
    """Get FortiGuard database versions.
    
    Returns version information for all FortiGuard services:
    - Antivirus signatures
    - Web filtering database
    - IPS signatures
    - GeoIP database
    - Application Control
    - And more
    
    Returns:
        Dictionary with FortiGuard database versions and update times
        
    Example:
        versions = get_fortiguard_database_versions()
        # Returns: {av: {version: X, update_time: Y}, wf: {...}, ...}
    """
    try:
        api = _get_fortiguard_api()
        versions = await api.get_fortiguard_versions()
        return {
            "status": "success",
            "fortiguard_versions": versions,
        }
    except Exception as e:
        logger.error(f"Error getting FortiGuard versions: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fortiguard_servers() -> dict[str, Any]:
    """Get FortiGuard upstream server list and connection status.
    
    Shows which FortiGuard distribution servers the FortiManager
    connects to for updates.
    
    Returns:
        Dictionary with FortiGuard server information
    """
    try:
        api = _get_fortiguard_api()
        servers = await api.get_fortiguard_servers()
        return {
            "status": "success",
            "fortiguard_servers": servers,
        }
    except Exception as e:
        logger.error(f"Error getting FortiGuard servers: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Firmware Management
# ============================================================================

@mcp.tool()
async def list_available_firmware(platform: str | None = None) -> dict[str, Any]:
    """List available firmware images from FortiGuard.
    
    Args:
        platform: Filter by platform (e.g., "FortiGate", "FortiSwitch")
    
    Returns:
        Dictionary with available firmware images
        
    Example:
        firmware = list_available_firmware(platform="FortiGate")
    """
    try:
        api = _get_fortiguard_api()
        images = await api.list_firmware_images(platform=platform)
        return {
            "status": "success",
            "count": len(images),
            "firmware_images": images,
        }
    except Exception as e:
        logger.error(f"Error listing firmware images: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def download_firmware(product: str, version: str) -> dict[str, Any]:
    """Download a firmware image to FortiManager.
    
    Args:
        product: Product name (e.g., "FortiGate")
        version: Firmware version (e.g., "7.4.1")
    
    Returns:
        Dictionary with download task information
        
    Example:
        result = download_firmware(product="FortiGate", version="7.4.1")
    """
    try:
        api = _get_fortiguard_api()
        result = await api.download_firmware_image(product=product, version=version)
        return {
            "status": "success",
            "message": f"Firmware download initiated for {product} {version}",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error downloading firmware {product} {version}: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Device Contracts & Licenses
# ============================================================================

@mcp.tool()
async def get_device_fortiguard_contracts(
    device: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """Get FortiGuard service contracts for managed devices.
    
    Shows which FortiGuard services are licensed for each device
    (Antivirus, Web Filtering, IPS, etc.).
    
    Args:
        device: Specific device name (optional, returns all if not specified)
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with device contract information
        
    Example:
        contracts = get_device_fortiguard_contracts(adom="production")
    """
    try:
        api = _get_fortiguard_api()
        contracts = await api.get_device_contracts(device=device, adom=adom)
        return {
            "status": "success",
            "count": len(contracts) if isinstance(contracts, list) else 1,
            "contracts": contracts,
        }
    except Exception as e:
        logger.error(f"Error getting device contracts: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Update History
# ============================================================================

@mcp.tool()
async def get_fortiguard_update_history(category: str | None = None) -> dict[str, Any]:
    """Get FortiGuard update history.
    
    Shows when FortiGuard databases were last updated.
    
    Args:
        category: Filter by category (e.g., "av", "wf", "ips", "geoip")
    
    Returns:
        Dictionary with update history
        
    Example:
        history = get_fortiguard_update_history(category="av")
    """
    try:
        api = _get_fortiguard_api()
        history = await api.get_update_history(category=category)
        return {
            "status": "success",
            "count": len(history),
            "update_history": history,
        }
    except Exception as e:
        logger.error(f"Error getting update history: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_downloaded_fortiguard_objects() -> dict[str, Any]:
    """Get list of FortiGuard objects downloaded by FortiManager.
    
    Returns:
        Dictionary with downloaded FortiGuard objects
    """
    try:
        api = _get_fortiguard_api()
        objects = await api.get_downloaded_objects()
        return {
            "status": "success",
            "count": len(objects),
            "downloaded_objects": objects,
        }
    except Exception as e:
        logger.error(f"Error getting downloaded objects: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# External Resources (Threat Feeds)
# ============================================================================

@mcp.tool()
async def list_external_threat_feeds(adom: str = "root") -> dict[str, Any]:
    """List external resources (threat feeds, custom URL/IP lists).
    
    External resources allow importing custom threat intelligence feeds
    and IP/domain blocklists from external sources.
    
    Args:
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with external resources list
        
    Example:
        feeds = list_external_threat_feeds(adom="production")
    """
    try:
        api = _get_fortiguard_api()
        resources = await api.list_external_resources(adom=adom)
        return {
            "status": "success",
            "count": len(resources),
            "external_resources": resources,
        }
    except Exception as e:
        logger.error(f"Error listing external resources: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_external_threat_feed(name: str, adom: str = "root") -> dict[str, Any]:
    """Get details of a specific external threat feed.
    
    Args:
        name: Resource name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with external resource details
    """
    try:
        api = _get_fortiguard_api()
        resource = await api.get_external_resource(name=name, adom=adom)
        return {
            "status": "success",
            "external_resource": resource,
        }
    except Exception as e:
        logger.error(f"Error getting external resource '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_external_threat_feed(
    name: str,
    url: str,
    resource_type: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create an external threat feed (IP/domain blocklist).
    
    Args:
        name: Resource name
        url: URL of the external feed
        resource_type: Type ("address", "domain", "malware")
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with creation result
        
    Example:
        result = create_external_threat_feed(
            name="abuse-ch-ipblocklist",
            url="https://sslbl.abuse.ch/blacklist/sslipblacklist.txt",
            resource_type="address",
            adom="production"
        )
    """
    try:
        api = _get_fortiguard_api()
        result = await api.create_external_resource(
            name=name,
            resource_url=url,
            resource_type=resource_type,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"External threat feed '{name}' created",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating external resource '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_external_threat_feed(name: str, adom: str = "root") -> dict[str, Any]:
    """Delete an external threat feed.
    
    Args:
        name: Resource name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_fortiguard_api()
        result = await api.delete_external_resource(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"External threat feed '{name}' deleted",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error deleting external resource '{name}': {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def refresh_external_threat_feed(name: str, adom: str = "root") -> dict[str, Any]:
    """Manually refresh an external threat feed.
    
    Forces an immediate update of the threat feed from its source URL.
    
    Args:
        name: Resource name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with refresh result
    """
    try:
        api = _get_fortiguard_api()
        result = await api.refresh_external_resource(name=name, adom=adom)
        return {
            "status": "success",
            "message": f"External threat feed '{name}' refresh initiated",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error refreshing external resource '{name}': {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 22: FortiGuard Enhancement - Update Operations
# ============================================================================


@mcp.tool()
async def trigger_fortiguard_update(update_type: str = "all") -> dict[str, Any]:
    """Trigger manual FortiGuard update.
    
    Manually triggers FortiManager to check for and download FortiGuard
    updates including:
    - Antivirus signatures
    - IPS signatures  
    - Web filter database
    - GeoIP database
    - Application control signatures
    - All databases (default)
    
    Use this when you need immediate updates rather than waiting for
    the scheduled update window.
    
    Args:
        update_type: Update type - "all", "av", "ips", "wf", "geoip", "app"
            (default: "all")
    
    Returns:
        Dictionary with update task information
    
    Example:
        # Update all databases
        result = trigger_fortiguard_update(update_type="all")
        
        # Update only IPS signatures
        result = trigger_fortiguard_update(update_type="ips")
    """
    try:
        api = _get_fortiguard_api()
        result = await api.trigger_fortiguard_update(update_type=update_type)
        return {
            "status": "success",
            "message": f"FortiGuard update triggered for: {update_type}",
            "task": result,
        }
    except Exception as e:
        logger.error(f"Error triggering FortiGuard update: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fortiguard_update_status() -> dict[str, Any]:
    """Get FortiGuard update status.
    
    Retrieves the current status of FortiGuard updates including:
    - Whether an update is in progress
    - Last successful update timestamp
    - Next scheduled update time
    - Any update errors or warnings
    - Database versions being updated
    
    Use this to monitor update progress and troubleshoot update issues.
    
    Returns:
        Dictionary with update status information
    
    Example:
        result = get_fortiguard_update_status()
    """
    try:
        api = _get_fortiguard_api()
        status = await api.get_fortiguard_update_status()
        return {
            "status": "success",
            "update_status": status,
        }
    except Exception as e:
        logger.error(f"Error getting FortiGuard update status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fortiguard_update_schedule() -> dict[str, Any]:
    """Get FortiGuard automatic update schedule.
    
    Retrieves the configured schedule for automatic FortiGuard updates:
    - Update frequency (daily, weekly)
    - Update day (for weekly updates)
    - Update time
    - Update server location
    - Auto-update enabled/disabled
    
    Use this to verify update scheduling configuration.
    
    Returns:
        Dictionary with update schedule configuration
    
    Example:
        result = get_fortiguard_update_schedule()
    """
    try:
        api = _get_fortiguard_api()
        schedule = await api.get_fortiguard_update_schedule()
        return {
            "status": "success",
            "schedule": schedule,
        }
    except Exception as e:
        logger.error(f"Error getting FortiGuard update schedule: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 22: FortiGuard Enhancement - Database Queries
# ============================================================================


@mcp.tool()
async def query_fortiguard_outbreak(query_type: str = "latest") -> dict[str, Any]:
    """Query FortiGuard outbreak and threat intelligence.
    
    Retrieves real-time threat intelligence from FortiGuard Labs:
    - Latest malware outbreaks and variants
    - Active botnet campaigns
    - Critical vulnerability alerts
    - Zero-day threat notifications
    - Trending attack patterns
    
    This provides situational awareness about current threats that may
    affect your network security posture.
    
    Args:
        query_type: Type of outbreak query:
            - "latest": Most recent outbreaks (default)
            - "critical": Critical severity only
            - "trending": Trending threats
    
    Returns:
        Dictionary with outbreak information
    
    Example:
        # Get latest outbreaks
        result = query_fortiguard_outbreak(query_type="latest")
        
        # Get only critical threats
        result = query_fortiguard_outbreak(query_type="critical")
    """
    try:
        api = _get_fortiguard_api()
        outbreak_info = await api.query_fortiguard_outbreak(query_type=query_type)
        return {
            "status": "success",
            "outbreak_info": outbreak_info,
        }
    except Exception as e:
        logger.error(f"Error querying FortiGuard outbreak: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fortiguard_category_overrides(adom: str = "root") -> dict[str, Any]:
    """Get FortiGuard web filter category overrides.
    
    Retrieves custom category assignments that override FortiGuard's
    default website categorization. Use this to:
    - View websites with custom category assignments
    - Audit category override policies
    - Identify sites moved to more/less restrictive categories
    
    Category overrides allow you to reclassify websites that FortiGuard
    may have categorized incorrectly or that need special handling in
    your environment.
    
    Args:
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with list of category overrides
    
    Example:
        result = get_fortiguard_category_overrides(adom="root")
    """
    try:
        api = _get_fortiguard_api()
        overrides = await api.get_fortiguard_category_override(adom=adom)
        return {
            "status": "success",
            "count": len(overrides),
            "overrides": overrides,
        }
    except Exception as e:
        logger.error(f"Error getting category overrides: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 25: Complete FortiGuard Management
# ============================================================================


@mcp.tool()
async def test_fortiguard_connection() -> dict[str, Any]:
    """Test connectivity to FortiGuard servers.
    
    Performs a comprehensive connectivity test to FortiGuard servers to verify:
    - Network connectivity and routing
    - DNS resolution for FortiGuard domains
    - FortiGuard server availability
    - Authentication and subscription status
    - Port accessibility (HTTPS/443)
    
    Use this to troubleshoot FortiGuard connectivity issues or verify
    network configuration after firewall changes.
    
    Returns:
        Dictionary with connection test results
    
    Example:
        result = test_fortiguard_connection()
        # Returns connection status, latency, and any errors
    """
    try:
        api = _get_fortiguard_api()
        test_result = await api.test_fortiguard_connection()
        return {
            "status": "success",
            "connection_test": test_result,
        }
    except Exception as e:
        logger.error(f"Error testing FortiGuard connection: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fortiguard_service_status() -> dict[str, Any]:
    """Get comprehensive FortiGuard service status.
    
    Retrieves detailed status for all FortiGuard services including:
    - Subscription status (active, expired, trial)
    - Service availability per category (AV, IPS, Web Filter, etc.)
    - Last successful update timestamp for each service
    - Connection status to FortiGuard update servers
    - License expiration dates
    - Service-specific health indicators
    
    This provides a complete health check of all FortiGuard services
    and helps identify subscription or connectivity issues.
    
    Returns:
        Dictionary with comprehensive service status
    
    Example:
        result = get_fortiguard_service_status()
        # Returns detailed status for AV, IPS, WebFilter, GeoIP, etc.
    """
    try:
        api = _get_fortiguard_api()
        service_status = await api.get_fortiguard_service_status()
        return {
            "status": "success",
            "service_status": service_status,
        }
    except Exception as e:
        logger.error(f"Error getting FortiGuard service status: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Phase 46: FortiGuard Advanced Operations
# ============================================================================


@mcp.tool()
async def get_fortiguard_upstream_config() -> dict[str, Any]:
    """Get FortiGuard upstream server configuration.
    
    Retrieves the configuration for upstream FortiGuard servers that
    FortiManager uses for updates and threat intelligence, including:
    - Connection protocol (HTTP/HTTPS)
    - Connection port
    - FortiGuard service account ID
    - Preferred geographic server location
    - Anycast configuration settings
    
    Useful for troubleshooting FortiGuard connectivity and verifying
    server configuration.
    
    Returns:
        Dictionary with upstream server configuration
    
    Example:
        result = get_fortiguard_upstream_config()
        # Returns protocol, port, server location, etc.
    """
    try:
        api = _get_fortiguard_api()
        config = await api.get_fortiguard_upstream_servers()
        return {
            "status": "success",
            "upstream_config": config,
        }
    except Exception as e:
        logger.error(f"Error getting FortiGuard upstream configuration: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_available_package_versions(
    platform: str = "FortiGate",
    current_version: str | None = None,
) -> dict[str, Any]:
    """Get available firmware and update packages for managed devices.
    
    Queries available packages for specific device platforms to:
    - View all available firmware versions
    - Identify upgrade paths from current version
    - Check package release dates and sizes
    - Plan firmware upgrade strategies
    
    Supports multiple platforms including FortiGate, FortiSwitch, FortiAP,
    FortiExtender, and more.
    
    Args:
        platform: Device platform (default: "FortiGate")
            Options: "FortiGate", "FortiSwitch", "FortiAP", "FortiExtender"
        current_version: Current device version (e.g., "7.0.10") for upgrade paths
    
    Returns:
        Dictionary with list of available packages
    
    Example:
        # Get all FortiGate packages
        result = get_available_package_versions(platform="FortiGate")
        
        # Get upgrade paths from current version
        result = get_available_package_versions(
            platform="FortiGate",
            current_version="7.0.10"
        )
    """
    try:
        api = _get_fortiguard_api()
        packages = await api.get_device_package_versions(
            platform=platform,
            current_version=current_version,
        )
        return {
            "status": "success",
            "platform": platform,
            "current_version": current_version,
            "count": len(packages),
            "packages": packages,
        }
    except Exception as e:
        logger.error(f"Error getting package versions: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def export_fortiguard_configuration(
    object_types: str,
    adom: str = "root",
    export_format: str = "json",
) -> dict[str, Any]:
    """Export FortiGuard objects for backup or migration.
    
    Exports specified object types from an ADOM in a portable format.
    Useful for:
    - Configuration backup before major changes
    - Migration between FortiManager instances
    - ADOM cloning and replication
    - Disaster recovery preparation
    
    Args:
        object_types: Comma-separated list of object paths to export
            Examples: "firewall/address", "firewall/service/custom"
        adom: Source ADOM name (default: "root")
        export_format: Export format - "json" or "xml" (default: "json")
    
    Returns:
        Dictionary with exported configuration data
    
    Example:
        result = export_fortiguard_configuration(
            object_types="firewall/address,firewall/service/custom",
            adom="production",
            export_format="json"
        )
    
    Warning:
        Exported data may contain sensitive configuration. Store securely.
    """
    try:
        api = _get_fortiguard_api()
        
        # Parse object types from comma-separated string
        types_list = [t.strip() for t in object_types.split(",")]
        
        exported = await api.export_fortiguard_objects(
            object_types=types_list,
            adom=adom,
            export_format=export_format,
        )
        
        return {
            "status": "success",
            "adom": adom,
            "format": export_format,
            "object_types": types_list,
            "exported_data": exported,
        }
    except Exception as e:
        logger.error(f"Error exporting FortiGuard configuration: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def import_fortiguard_configuration(
    import_data: str,
    adom: str = "root",
    conflict_action: str = "merge",
) -> dict[str, Any]:
    """Import FortiGuard objects from exported configuration data.
    
    Imports previously exported objects into an ADOM with configurable
    conflict resolution. Supports:
    - Disaster recovery restoration
    - Configuration migration between ADOMs
    - Bulk object deployment
    - Configuration synchronization
    
    Args:
        import_data: Exported JSON or XML configuration data
        adom: Target ADOM name (default: "root")
        conflict_action: How to handle existing objects:
            - "merge": Merge with existing (default)
            - "replace": Replace existing objects
            - "skip": Skip objects that already exist
    
    Returns:
        Dictionary with import results and statistics
    
    Example:
        result = import_fortiguard_configuration(
            import_data='{"objects": [...]}',
            adom="disaster-recovery",
            conflict_action="merge"
        )
    
    Warning:
        Import operations can significantly modify ADOM configuration.
        Always test in a non-production ADOM first.
    """
    try:
        api = _get_fortiguard_api()
        
        result = await api.import_fortiguard_objects(
            import_data=import_data,
            adom=adom,
            conflict_action=conflict_action,
        )
        
        return {
            "status": "success",
            "adom": adom,
            "conflict_action": conflict_action,
            "import_result": result,
        }
    except Exception as e:
        logger.error(f"Error importing FortiGuard configuration: {e}")
        return {"status": "error", "message": str(e)}

