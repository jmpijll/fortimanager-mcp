"""MCP tools for system configuration and administration."""

import logging
from typing import Any

from fortimanager_mcp.api.system import SystemAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_system_api() -> SystemAPI:
    """Get System API instance with FortiManager client."""
    client = get_fmg_client()
    if client is None:
        raise RuntimeError("FortiManager client not initialized")
    return SystemAPI(client)


# =============================================================================
# Admin User Tools
# =============================================================================


@mcp.tool()
async def list_admin_users() -> dict[str, Any]:
    """List all administrator users on FortiManager.
    
    Returns information about all admin accounts including:
    - Username
    - Profile (permissions level)
    - Trusted hosts
    - Authentication method
    - Last login information
    - Account status
    
    This is useful for:
    - Security audits
    - Access control reviews
    - User management
    - Compliance reporting
    
    Returns:
        Dictionary with status and list of admin users
    """
    api = _get_system_api()
    users = await api.list_admin_users()
    return {
        "status": "success",
        "count": len(users),
        "users": users,
    }


@mcp.tool()
async def get_admin_user(username: str) -> dict[str, Any]:
    """Get detailed information about a specific administrator user.
    
    Args:
        username: Admin username
    
    Returns:
        Dictionary with status and user details
    """
    api = _get_system_api()
    user = await api.get_admin_user(username=username)
    return {
        "status": "success",
        "user": user,
    }


# =============================================================================
# System Settings Tools
# =============================================================================


@mcp.tool()
async def get_system_global_settings() -> dict[str, Any]:
    """Get global system settings for FortiManager.
    
    Returns comprehensive system configuration including:
    - Admin timeout settings
    - Hostname and domain
    - Timezone configuration
    - GUI preferences
    - API access settings
    - Certificate settings
    - Database settings
    
    This is useful for:
    - System configuration review
    - Compliance verification
    - Troubleshooting
    - Configuration backups
    
    Returns:
        Dictionary with status and global settings
    """
    api = _get_system_api()
    settings = await api.get_system_global_settings()
    return {
        "status": "success",
        "settings": settings,
    }


@mcp.tool()
async def get_system_status() -> dict[str, Any]:
    """Get comprehensive FortiManager system status.
    
    Returns detailed status information including:
    - Software version and build
    - License information
    - System uptime
    - CPU and memory usage
    - Disk space usage
    - Database status
    - Process information
    - Network connectivity
    
    This is the primary tool for:
    - Health monitoring
    - Capacity planning
    - Troubleshooting
    - Status dashboards
    
    Returns:
        Dictionary with status and system information
    """
    api = _get_system_api()
    status = await api.get_system_status()
    return {
        "status": "success",
        "system": status,
    }


# =============================================================================
# High Availability Tools
# =============================================================================


@mcp.tool()
async def get_ha_configuration() -> dict[str, Any]:
    """Get High Availability (HA) configuration.
    
    Returns HA configuration including:
    - Cluster ID and mode
    - Primary/secondary roles
    - Heartbeat interface settings
    - Failover settings
    - File quota settings
    - Load balancing mode
    
    FortiManager HA provides:
    - Redundancy and failover
    - Configuration synchronization
    - Load distribution
    - High availability for management
    
    Returns:
        Dictionary with status and HA configuration
    """
    api = _get_system_api()
    ha_config = await api.get_ha_config()
    return {
        "status": "success",
        "ha_config": ha_config,
    }


@mcp.tool()
async def get_ha_status() -> dict[str, Any]:
    """Get current High Availability (HA) status.
    
    Returns real-time HA status including:
    - Current HA health status
    - Cluster member status
    - Synchronization status
    - Failover status
    - Connection status between members
    
    Use this to monitor:
    - HA cluster health
    - Synchronization progress
    - Potential failover issues
    - Member connectivity
    
    Returns:
        Dictionary with status and current HA state
    """
    api = _get_system_api()
    ha_status = await api.get_ha_status()
    return {
        "status": "success",
        "ha_status": ha_status,
    }


# =============================================================================
# System Interface Tools
# =============================================================================


@mcp.tool()
async def list_system_interfaces() -> dict[str, Any]:
    """List all system interfaces on FortiManager.
    
    Returns information about management interfaces including:
    - Interface name
    - IP address and netmask
    - Status (up/down)
    - Speed and duplex
    - Description
    - Access settings (HTTP, HTTPS, SSH, etc.)
    - VLAN configuration
    
    System interfaces are used for:
    - Management access (GUI, API, CLI)
    - Device communication
    - HA heartbeat
    - Log forwarding
    - Backup operations
    
    Returns:
        Dictionary with status and list of interfaces
    """
    api = _get_system_api()
    interfaces = await api.list_system_interfaces()
    return {
        "status": "success",
        "count": len(interfaces),
        "interfaces": interfaces,
    }


@mcp.tool()
async def get_system_interface(name: str) -> dict[str, Any]:
    """Get detailed information about a specific system interface.
    
    Args:
        name: Interface name (e.g., "port1", "port2")
    
    Returns:
        Dictionary with status and interface details
    """
    api = _get_system_api()
    interface = await api.get_system_interface(name=name)
    return {
        "status": "success",
        "interface": interface,
    }


# =============================================================================
# Logging Configuration Tools
# =============================================================================


@mcp.tool()
async def get_log_settings() -> dict[str, Any]:
    """Get logging configuration settings.
    
    Returns logging configuration including:
    - Log storage settings
    - Log forwarding configuration
    - Log retention policies
    - Custom field definitions
    - Log filtering settings
    - Alert settings
    
    FortiManager logging handles:
    - Device logs from managed FortiGates
    - FortiManager system logs
    - Audit logs
    - Event logs
    - Analytics and reporting data
    
    Returns:
        Dictionary with status and log settings
    """
    api = _get_system_api()
    log_settings = await api.get_log_settings()
    return {
        "status": "success",
        "log_settings": log_settings,
    }


# =============================================================================
# Backup Configuration Tools
# =============================================================================


@mcp.tool()
async def get_backup_settings() -> dict[str, Any]:
    """Get backup configuration settings.
    
    Returns backup settings including:
    - Backup schedule configuration
    - Backup destination settings
    - Retention policies
    - Encryption settings
    - Directory paths
    - FTP/SFTP server settings
    
    FortiManager backups include:
    - System configuration
    - ADOM configurations
    - Device configurations
    - Database content
    - Certificates and keys
    
    Regular backups are critical for:
    - Disaster recovery
    - Configuration rollback
    - System migration
    - Compliance requirements
    
    Returns:
        Dictionary with status and backup settings
    """
    api = _get_system_api()
    backup_settings = await api.get_backup_settings()
    return {
        "status": "success",
        "backup_settings": backup_settings,
    }


# ============================================================================
# Phase 20: FMG System Operations - Certificate Management
# ============================================================================


@mcp.tool()
async def list_system_certificates() -> dict[str, Any]:
    """List all system certificates.
    
    Retrieves all local certificates installed on the FortiManager.
    Certificates are used for HTTPS, API access, and secure communication.
    
    Returns:
        Dictionary with list of certificates including:
        - Certificate name
        - Subject and issuer information
        - Validity period (not before/not after dates)
        - Status (valid, expired, expiring soon)
        - Usage (web, API, etc.)
    
    Example:
        result = list_system_certificates()
    """
    api = _get_system_api()
    certificates = await api.list_certificates()
    return {
        "status": "success",
        "count": len(certificates),
        "certificates": certificates,
    }


@mcp.tool()
async def list_ca_certificates() -> dict[str, Any]:
    """List CA certificates.
    
    Retrieves all Certificate Authority (CA) certificates installed on FortiManager.
    CA certificates are used to verify the identity of devices and other systems.
    
    Returns:
        Dictionary with list of CA certificates including:
        - CA certificate name
        - Issuer information
        - Validity period
        - Certificate chain details
    
    Example:
        result = list_ca_certificates()
    """
    api = _get_system_api()
    ca_certs = await api.list_ca_certificates()
    return {
        "status": "success",
        "count": len(ca_certs),
        "ca_certificates": ca_certs,
    }


@mcp.tool()
async def get_certificate_details(name: str) -> dict[str, Any]:
    """Get detailed information about a specific certificate.
    
    Retrieves comprehensive details about a certificate including validity,
    subject, issuer, and usage information.
    
    Args:
        name: Certificate name
    
    Returns:
        Dictionary with certificate details including:
        - Subject DN (Distinguished Name)
        - Issuer DN
        - Serial number
        - Validity dates
        - Key algorithm and size
        - Signature algorithm
        - Subject Alternative Names (SANs)
    
    Example:
        result = get_certificate_details(name="Fortinet_SSL")
    """
    api = _get_system_api()
    cert = await api.get_certificate_details(name)
    return {
        "status": "success",
        "certificate": cert,
    }


# ============================================================================
# Phase 20: FMG System Operations - System Status
# ============================================================================


@mcp.tool()
async def get_license_status() -> dict[str, Any]:
    """Get FortiManager license status.
    
    Retrieves license information including:
    - License type (VM, hardware, etc.)
    - License validity and expiration
    - Licensed features
    - FortiCare support status
    - Number of managed devices allowed
    
    This is useful for:
    - Monitoring license expiration
    - Capacity planning
    - Compliance verification
    - Support contract validation
    
    Returns:
        Dictionary with license status information
    
    Example:
        result = get_license_status()
    """
    api = _get_system_api()
    license = await api.get_license_status()
    return {
        "status": "success",
        "license": license,
    }


@mcp.tool()
async def get_system_performance() -> dict[str, Any]:
    """Get system performance metrics.
    
    Retrieves real-time performance statistics including:
    - CPU usage (overall and per-core)
    - Memory utilization (RAM, swap)
    - Disk I/O statistics
    - Network throughput
    - Process information
    
    Use this to:
    - Monitor system health
    - Identify performance bottlenecks
    - Plan capacity upgrades
    - Troubleshoot slowdowns
    
    Returns:
        Dictionary with performance metrics
    
    Example:
        result = get_system_performance()
    """
    api = _get_system_api()
    performance = await api.get_system_performance()
    return {
        "status": "success",
        "performance": performance,
    }


@mcp.tool()
async def get_disk_usage() -> dict[str, Any]:
    """Get disk usage information.
    
    Retrieves disk space usage statistics including:
    - Total disk capacity
    - Used space
    - Available space
    - Usage percentage
    - Partition information
    
    Critical for:
    - Preventing disk full conditions
    - Planning storage upgrades
    - Monitoring log growth
    - Database management
    
    Returns:
        Dictionary with disk usage information
    
    Example:
        result = get_disk_usage()
    """
    api = _get_system_api()
    disk_info = await api.get_disk_usage()
    return {
        "status": "success",
        "disk_usage": disk_info,
    }


# ============================================================================
# Phase 20: FMG System Operations - Admin Operations
# ============================================================================


@mcp.tool()
async def list_admin_sessions() -> dict[str, Any]:
    """List active admin sessions.
    
    Retrieves information about all currently logged-in administrators:
    - Username
    - Login time
    - Source IP address
    - Session type (GUI, CLI, API)
    - Idle time
    - Session ID
    
    Use this to:
    - Monitor who is logged in
    - Audit administrative access
    - Identify stale sessions
    - Security monitoring
    
    Returns:
        Dictionary with list of active sessions
    
    Example:
        result = list_admin_sessions()
    """
    api = _get_system_api()
    sessions = await api.list_admin_sessions()
    return {
        "status": "success",
        "count": len(sessions),
        "sessions": sessions,
    }


@mcp.tool()
async def get_api_user_info() -> dict[str, Any]:
    """Get current API user information.
    
    Retrieves information about the currently connected API user:
    - Username
    - User profile
    - Permissions and access rights
    - ADOM assignments
    - Login history
    
    Useful for:
    - Verifying API connection
    - Checking permissions
    - Auditing API access
    - Troubleshooting access issues
    
    Returns:
        Dictionary with current API user details
    
    Example:
        result = get_api_user_info()
    """
    api = _get_system_api()
    user_info = await api.get_api_user_info()
    return {
        "status": "success",
        "user": user_info,
    }


@mcp.tool()
async def list_system_administrators() -> dict[str, Any]:
    """List all system administrators.
    
    Retrieves detailed information about all administrator accounts:
    - Username and user ID
    - Profile type (Super User, Standard User, etc.)
    - ADOM assignments
    - Permission sets
    - Login status
    - Account status (enabled/disabled)
    - Password expiration
    
    Use this for:
    - User management and auditing
    - Permission verification
    - Security compliance
    - Access control reviews
    
    Returns:
        Dictionary with list of administrators
    
    Example:
        result = list_system_administrators()
    """
    api = _get_system_api()
    admins = await api.list_system_admins()
    return {
        "status": "success",
        "count": len(admins),
        "administrators": admins,
    }


# =============================================================================
# Phase 27: Complete FMG System Operations
# =============================================================================


@mcp.tool()
async def get_system_dns_settings() -> dict[str, Any]:
    """Get FortiManager DNS server configuration.
    
    Retrieves DNS settings including:
    - Primary DNS server
    - Secondary DNS server
    - DNS timeout settings
    - Source IP for DNS queries
    
    Use this to:
    - Verify DNS configuration
    - Troubleshoot name resolution issues
    - Audit network settings
    - Document system configuration
    
    Returns:
        Dictionary with DNS configuration
    
    Example:
        result = get_system_dns_settings()
        # Returns DNS servers and configuration
    """
    api = _get_system_api()
    dns_settings = await api.get_dns_settings()
    return {
        "status": "success",
        "dns_settings": dns_settings,
    }


@mcp.tool()
async def get_system_ntp_settings() -> dict[str, Any]:
    """Get FortiManager NTP (time synchronization) settings.
    
    Retrieves NTP configuration including:
    - NTP server addresses
    - Synchronization status
    - Time zone settings
    - Sync interval
    - Authentication settings
    
    Accurate time is critical for:
    - Log correlation across devices
    - Certificate validation
    - Security event analysis
    - Scheduled tasks execution
    
    Returns:
        Dictionary with NTP configuration and sync status
    
    Example:
        result = get_system_ntp_settings()
        # Returns NTP servers and sync status
    """
    api = _get_system_api()
    ntp_settings = await api.get_ntp_settings()
    return {
        "status": "success",
        "ntp_settings": ntp_settings,
    }


@mcp.tool()
async def get_system_routes() -> dict[str, Any]:
    """Get FortiManager static route configuration.
    
    Retrieves all static routes configured on FortiManager including:
    - Destination network/mask
    - Gateway IP address
    - Interface assignment
    - Administrative distance
    - Route priority
    
    Use this to:
    - Verify network connectivity paths
    - Audit routing configuration
    - Troubleshoot reachability issues
    - Document network topology
    
    Returns:
        Dictionary with list of static routes
    
    Example:
        result = get_system_routes()
        # Returns all configured static routes
    """
    api = _get_system_api()
    routes = await api.get_route_settings()
    return {
        "status": "success",
        "count": len(routes),
        "routes": routes,
    }


# =============================================================================
# Phase 40: Advanced System Configuration & Diagnostics
# =============================================================================


@mcp.tool()
async def get_system_interfaces() -> dict[str, Any]:
    """Get network interface configuration for FortiManager."""
    try:
        api = _get_system_api()
        interfaces = await api.get_interface_settings()
        return {"status": "success", "interfaces": interfaces}
    except Exception as e:
        logger.error(f"Error getting interfaces: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_snmp_config() -> dict[str, Any]:
    """Get SNMP configuration including communities and trap destinations."""
    try:
        api = _get_system_api()
        snmp = await api.get_snmp_settings()
        return {"status": "success", "snmp": snmp}
    except Exception as e:
        logger.error(f"Error getting SNMP settings: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_syslog_config() -> dict[str, Any]:
    """Get syslog server configuration."""
    try:
        api = _get_system_api()
        syslog = await api.get_syslog_settings()
        return {"status": "success", "syslog_servers": syslog}
    except Exception as e:
        logger.error(f"Error getting syslog settings: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_email_server_config() -> dict[str, Any]:
    """Get email server configuration for system notifications."""
    try:
        api = _get_system_api()
        email = await api.get_email_settings()
        return {"status": "success", "email_server": email}
    except Exception as e:
        logger.error(f"Error getting email settings: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_global_system_config() -> dict[str, Any]:
    """Get global FortiManager system configuration."""
    try:
        api = _get_system_api()
        config = await api.get_global_settings()
        return {"status": "success", "global_config": config}
    except Exception as e:
        logger.error(f"Error getting global settings: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_admin_config() -> dict[str, Any]:
    """Get administrative settings including session timeout and lockout policy."""
    try:
        api = _get_system_api()
        admin = await api.get_admin_settings()
        return {"status": "success", "admin_settings": admin}
    except Exception as e:
        logger.error(f"Error getting admin settings: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_log_config() -> dict[str, Any]:
    """Get log configuration and retention settings."""
    try:
        api = _get_system_api()
        logs = await api.get_log_settings()
        return {"status": "success", "log_settings": logs}
    except Exception as e:
        logger.error(f"Error getting log settings: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_update_service_config() -> dict[str, Any]:
    """Get FortiManager update service configuration."""
    try:
        api = _get_system_api()
        update = await api.get_fmupdate_settings()
        return {"status": "success", "update_service": update}
    except Exception as e:
        logger.error(f"Error getting update service settings: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_sql_config() -> dict[str, Any]:
    """Get SQL database configuration."""
    try:
        api = _get_system_api()
        sql = await api.get_sql_settings()
        return {"status": "success", "sql_settings": sql}
    except Exception as e:
        logger.error(f"Error getting SQL settings: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_alert_console_config() -> dict[str, Any]:
    """Get alert console configuration for system notifications."""
    try:
        api = _get_system_api()
        alerts = await api.get_alert_console_settings()
        return {"status": "success", "alert_console": alerts}
    except Exception as e:
        logger.error(f"Error getting alert console settings: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 44: Additional System Operations
# =============================================================================


@mcp.tool()
async def get_system_backup_status() -> dict[str, Any]:
    """Get system backup status and history.
    
    Returns:
        Dictionary with backup status
    """
    try:
        api = _get_system_api()
        status = await api.get_backup_status()
        return {"status": "success", "backup_status": status}
    except Exception as e:
        logger.error(f"Error getting backup status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fmg_ha_cluster_status() -> dict[str, Any]:
    """Get FortiManager HA cluster status.
    
    Returns:
        Dictionary with HA cluster status
    """
    try:
        api = _get_system_api()
        status = await api.get_ha_status()
        return {"status": "success", "ha_cluster": status}
    except Exception as e:
        logger.error(f"Error getting HA status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_auto_update_configuration() -> dict[str, Any]:
    """Get automatic update status and schedule.
    
    Returns:
        Dictionary with auto-update configuration
    """
    try:
        api = _get_system_api()
        config = await api.get_auto_update_status()
        return {"status": "success", "auto_update": config}
    except Exception as e:
        logger.error(f"Error getting auto-update status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_workspace_mode_configuration() -> dict[str, Any]:
    """Get workspace mode configuration settings.
    
    Returns:
        Dictionary with workspace mode settings
    """
    try:
        api = _get_system_api()
        config = await api.get_workspace_mode_status()
        return {"status": "success", "workspace_mode": config}
    except Exception as e:
        logger.error(f"Error getting workspace mode: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_available_connector_types() -> dict[str, Any]:
    """List available connector types and capabilities.
    
    Returns:
        Dictionary with list of connector types
    """
    try:
        api = _get_system_api()
        types = await api.list_connector_types()
        return {"status": "success", "count": len(types), "connector_types": types}
    except Exception as e:
        logger.error(f"Error listing connector types: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fmg_gui_settings() -> dict[str, Any]:
    """Get GUI display settings and configuration.
    
    Returns:
        Dictionary with GUI configuration
    """
    try:
        api = _get_system_api()
        settings = await api.get_gui_settings()
        return {"status": "success", "gui_settings": settings}
    except Exception as e:
        logger.error(f"Error getting GUI settings: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 50: Final System Operations (TRUE 100% COVERAGE!) 🏁
# =============================================================================


@mcp.tool()
async def list_tacacs_plus_servers() -> dict[str, Any]:
    """List TACACS+ servers configured on FortiManager.
    
    TACACS+ servers provide centralized AAA (Authentication, Authorization,
    and Accounting) services for administrative access control to FortiManager.
    
    Use this to:
    - View configured TACACS+ authentication servers
    - Audit external authentication configuration
    - Verify AAA server connectivity settings
    - Check authentication server priorities
    
    Returns:
        Dictionary with list of TACACS+ servers
    
    Example:
        result = list_tacacs_plus_servers()
        # Returns configured TACACS+ servers with host, port, timeout
    """
    try:
        api = _get_system_api()
        servers = await api.list_tacacs_servers()
        return {
            "status": "success",
            "count": len(servers),
            "tacacs_servers": servers,
        }
    except Exception as e:
        logger.error(f"Error listing TACACS+ servers: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_tacacs_plus_server_details(server_name: str) -> dict[str, Any]:
    """Get specific TACACS+ server configuration details.
    
    Retrieves detailed configuration for a named TACACS+ server including:
    - Server hostname/IP address
    - Port and protocol settings
    - Authentication timeout
    - Authorization settings
    - Accounting configuration
    
    Args:
        server_name: TACACS+ server name to retrieve
    
    Returns:
        Dictionary with TACACS+ server details
    
    Example:
        result = get_tacacs_plus_server_details(
            server_name="corporate-tacacs"
        )
    """
    try:
        api = _get_system_api()
        server = await api.get_tacacs_server(server_name=server_name)
        return {
            "status": "success",
            "server": server,
        }
    except Exception as e:
        logger.error(f"Error getting TACACS+ server details: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_active_user_sessions() -> dict[str, Any]:
    """Get current active user sessions on FortiManager.
    
    Returns information about all active administrative sessions including:
    - Username and authentication method
    - Login time and session duration
    - Source IP address
    - Access method (GUI, CLI, API)
    - Admin profile and permissions
    
    Useful for:
    - Security auditing
    - Session monitoring
    - Troubleshooting access issues
    - Identifying unauthorized access
    
    Returns:
        Dictionary with list of active sessions
    
    Example:
        result = get_active_user_sessions()
        # Returns all active admin sessions with details
    """
    try:
        api = _get_system_api()
        sessions = await api.get_user_sessions()
        return {
            "status": "success",
            "count": len(sessions),
            "sessions": sessions,
        }
    except Exception as e:
        logger.error(f"Error getting user sessions: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_fortianalyzer_adom(
    adom_name: str,
    description: str = "",
) -> dict[str, Any]:
    """Create ADOM in connected FortiAnalyzer for log collection.
    
    When FortiManager is integrated with FortiAnalyzer, this creates
    a corresponding ADOM in FAZ to enable log collection and analysis
    for the specified ADOM.
    
    Use cases:
    - Enable log collection for new ADOM
    - Integrate FortiManager and FortiAnalyzer
    - Centralized log management
    - Compliance and auditing
    
    Args:
        adom_name: ADOM name to create in FortiAnalyzer
        description: ADOM description
    
    Returns:
        Dictionary with creation result
    
    Example:
        result = create_fortianalyzer_adom(
            adom_name="branch-offices",
            description="Branch office log collection"
        )
    
    Note:
        Requires FortiAnalyzer integration to be configured.
    """
    try:
        api = _get_system_api()
        result = await api.create_adom_in_fortianalyzer(
            adom_name=adom_name,
            description=description,
        )
        return {
            "status": "success",
            "message": f"ADOM '{adom_name}' created in FortiAnalyzer",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error creating FortiAnalyzer ADOM: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_current_api_user() -> dict[str, Any]:
    """Get details about the currently connected API user.
    
    Returns information about the API user making this request including:
    - Username and user type
    - Authentication method
    - Permissions and admin profile
    - Last login time
    - Current session details
    
    Useful for:
    - Verifying API credentials
    - Checking user permissions
    - Debugging access issues
    - Security auditing
    
    Returns:
        Dictionary with current API user details
    
    Example:
        result = get_current_api_user()
        # Returns details about the authenticated API user
    """
    try:
        api = _get_system_api()
        user = await api.get_api_user_details()
        return {
            "status": "success",
            "user": user,
        }
    except Exception as e:
        logger.error(f"Error getting API user details: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def reboot_system(delay: int = 0) -> dict[str, Any]:
    """Reboot FortiManager system.
    
    Initiates a system reboot with optional delay. This will:
    - Gracefully shut down all services
    - Disconnect all users
    - Reboot the FortiManager appliance
    - Restart after hardware initialization
    
    Args:
        delay: Delay in seconds before reboot (default: 0 = immediate)
    
    Returns:
        Dictionary with reboot initiation result
    
    Example:
        result = reboot_system(delay=60)  # Reboot in 60 seconds
    
    WARNING:
        This will reboot the entire FortiManager system and disconnect
        all users. Use with extreme caution in production environments.
        Ensure all pending operations are complete before rebooting.
    """
    try:
        api = _get_system_api()
        result = await api.reboot_fortimanager(delay=delay)
        return {
            "status": "success",
            "message": f"System reboot initiated (delay: {delay}s)",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error rebooting system: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def backup_system_config() -> dict[str, Any]:
    """Trigger FortiManager configuration backup.
    
    Creates a full backup of FortiManager configuration including:
    - Global system configuration
    - All ADOM configurations
    - Policy packages and rules
    - Firewall objects
    - Device management data
    - Administrative settings
    
    Use for:
    - Regular backup schedules
    - Pre-change backups
    - Disaster recovery preparation
    - Configuration migration
    
    Returns:
        Dictionary with backup task details
    
    Example:
        result = backup_system_config()
        # Backup file stored in FortiManager
    
    Note:
        The backup file will be stored in FortiManager's backup location.
        Use download operations to retrieve the backup file if needed.
    """
    try:
        api = _get_system_api()
        result = await api.backup_fortimanager_config()
        return {
            "status": "success",
            "message": "System backup initiated",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error backing up system: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def restore_system_config(backup_file: str) -> dict[str, Any]:
    """Restore FortiManager configuration from backup file.
    
    Restores the complete FortiManager configuration from a previously
    created backup file. This operation:
    - Stops all services
    - Replaces current configuration
    - Restores all ADOMs and policies
    - Restores device management data
    - Restarts services
    
    Args:
        backup_file: Path to backup file on FortiManager
    
    Returns:
        Dictionary with restore task details
    
    Example:
        result = restore_system_config(
            backup_file="/var/backup/fmg_backup_2025-10-16.dat"
        )
    
    WARNING:
        This will completely replace the current configuration with the
        backup. All current settings, ADOMs, policies, and objects will
        be lost. This operation cannot be undone. Use with extreme caution.
        
        Best practice: Create a backup before restoring!
    """
    try:
        api = _get_system_api()
        result = await api.restore_fortimanager_config(backup_file=backup_file)
        return {
            "status": "success",
            "message": "System restore initiated",
            "result": result,
        }
    except Exception as e:
        logger.error(f"Error restoring system: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_fortiguard_upstream_servers() -> dict[str, Any]:
    """Get list of FortiGuard upstream servers.
    
    Returns the configured FortiGuard servers that FortiManager uses for:
    - Firmware and signature updates
    - Threat intelligence feeds
    - Web filtering categories
    - Application signatures
    - IPS signatures
    
    Information includes:
    - Server addresses and ports
    - Connection status
    - Protocol configuration
    - Service types available
    
    Returns:
        Dictionary with list of upstream servers
    
    Example:
        result = get_fortiguard_upstream_servers()
        # Returns FortiGuard server configuration
    """
    try:
        api = _get_system_api()
        servers = await api.get_fortiguard_upstream_servers_list()
        return {
            "status": "success",
            "count": len(servers),
            "upstream_servers": servers,
        }
    except Exception as e:
        logger.error(f"Error getting FortiGuard upstream servers: {e}")
        return {"status": "error", "message": str(e)}

