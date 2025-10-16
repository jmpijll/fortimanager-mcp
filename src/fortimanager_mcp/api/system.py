"""FortiManager System Configuration and Administration API operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class SystemAPI:
    """System configuration and administration operations.
    
    Handles system settings, admin users, HA, interfaces, and backups.
    """

    def __init__(self, client: Any) -> None:
        """Initialize SystemAPI.
        
        Args:
            client: FortiManager API client
        """
        self.client = client

    # =========================================================================
    # Admin User Methods
    # =========================================================================

    async def list_admin_users(self) -> list[dict[str, Any]]:
        """List all admin users.
        
        Returns:
            List of admin users
        """
        url = "/cli/global/system/admin/user"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_admin_user(self, username: str) -> dict[str, Any]:
        """Get admin user details.
        
        Args:
            username: Admin username
            
        Returns:
            User details
        """
        url = f"/cli/global/system/admin/user/{username}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # System Global Settings Methods
    # =========================================================================

    async def get_system_global_settings(self) -> dict[str, Any]:
        """Get system global settings.
        
        Returns:
            Global system settings
        """
        url = "/cli/global/system/global"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_system_status(self) -> dict[str, Any]:
        """Get comprehensive system status.
        
        Returns:
            System status including version, license, and resource usage
        """
        url = "/sys/status"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # High Availability Methods
    # =========================================================================

    async def get_ha_config(self) -> dict[str, Any]:
        """Get HA configuration.
        
        Returns:
            HA configuration settings
        """
        url = "/cli/global/system/ha"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_ha_status(self) -> dict[str, Any]:
        """Get HA status.
        
        Returns:
            Current HA status and health
        """
        url = "/sys/ha/status"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # System Interface Methods
    # =========================================================================

    async def list_system_interfaces(self) -> list[dict[str, Any]]:
        """List all system interfaces.
        
        Returns:
            List of system interfaces
        """
        url = "/cli/global/system/interface"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_system_interface(self, name: str) -> dict[str, Any]:
        """Get system interface details.
        
        Args:
            name: Interface name
            
        Returns:
            Interface details
        """
        url = f"/cli/global/system/interface/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # Logging Settings Methods
    # =========================================================================

    async def get_log_settings(self) -> dict[str, Any]:
        """Get log settings.
        
        Returns:
            Log configuration settings
        """
        url = "/cli/global/system/log/settings"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # Backup Settings Methods
    # =========================================================================

    async def get_backup_settings(self) -> dict[str, Any]:
        """Get backup settings.
        
        Returns:
            Backup configuration settings
        """
        url = "/cli/global/system/backup/all-settings"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # Phase 20: Certificate Management
    # =========================================================================

    async def list_certificates(self) -> list[dict[str, Any]]:
        """List all certificates.
        
        Returns:
            List of system certificates
        """
        url = "/cli/global/system/certificate/local"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_ca_certificates(self) -> list[dict[str, Any]]:
        """List CA certificates.
        
        Returns:
            List of CA certificates
        """
        url = "/cli/global/system/certificate/ca"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_certificate_details(self, name: str) -> dict[str, Any]:
        """Get certificate details.
        
        Args:
            name: Certificate name
            
        Returns:
            Certificate details including validity and subject
        """
        url = f"/cli/global/system/certificate/local/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # Phase 20: System Status Operations
    # =========================================================================

    async def get_license_status(self) -> dict[str, Any]:
        """Get FortiManager license status.
        
        Returns:
            License information and validity
        """
        url = "/sys/license/forticare"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_system_performance(self) -> dict[str, Any]:
        """Get system performance metrics.
        
        Returns:
            CPU, memory, and disk usage statistics
        """
        url = "/sys/performance"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_disk_usage(self) -> dict[str, Any]:
        """Get disk usage information.
        
        Returns:
            Disk space usage details
        """
        url = "/cli/global/system/status"
        data = await self.client.get(url)
        # Extract disk info from status
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # Phase 20: Admin Operations
    # =========================================================================

    async def list_admin_sessions(self) -> list[dict[str, Any]]:
        """List active admin sessions.
        
        Returns:
            List of active administrator sessions
        """
        url = "/sys/session"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_api_user_info(self) -> dict[str, Any]:
        """Get current API user information.
        
        Returns:
            Information about the currently connected API user
        """
        url = "/sys/api/user"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def list_system_admins(self) -> list[dict[str, Any]]:
        """List system administrators with detailed info.
        
        Returns:
            List of administrators with permissions and profiles
        """
        url = "/cli/global/system/admin/user"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Phase 27: Complete FMG System Operations
    # =========================================================================

    async def get_dns_settings(self) -> dict[str, Any]:
        """Get DNS server configuration.
        
        Returns:
            DNS settings including primary and secondary servers
        """
        url = "/cli/global/system/dns"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_ntp_settings(self) -> dict[str, Any]:
        """Get NTP (time synchronization) settings.
        
        Returns:
            NTP configuration including servers and sync status
        """
        url = "/cli/global/system/ntp"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_route_settings(self) -> list[dict[str, Any]]:
        """Get static route configuration.
        
        Returns:
            List of static routes configured on FortiManager
        """
        url = "/cli/global/system/route"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Phase 40: Advanced System Operations & Diagnostics
    # =========================================================================

    async def get_interface_settings(self) -> list[dict[str, Any]]:
        """Get network interface configuration.
        
        Returns:
            List of network interfaces with IP addresses and settings
        """
        url = "/cli/global/system/interface"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_snmp_settings(self) -> dict[str, Any]:
        """Get SNMP configuration.
        
        Returns:
            SNMP settings including communities and trap destinations
        """
        url = "/cli/global/system/snmp/sysinfo"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_syslog_settings(self) -> list[dict[str, Any]]:
        """Get syslog server configuration.
        
        Returns:
            List of configured syslog servers
        """
        url = "/cli/global/system/syslog"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_email_settings(self) -> dict[str, Any]:
        """Get email server configuration for notifications.
        
        Returns:
            Email server settings including SMTP configuration
        """
        url = "/cli/global/system/email-server"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_global_settings(self) -> dict[str, Any]:
        """Get global FortiManager settings.
        
        Returns:
            Global configuration including hostname, timezone, language
        """
        url = "/cli/global/system/global"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_admin_settings(self) -> dict[str, Any]:
        """Get administrative settings including timeout and lockout.
        
        Returns:
            Admin settings including session timeout, lockout policy
        """
        url = "/cli/global/system/admin/setting"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_log_settings(self) -> dict[str, Any]:
        """Get log configuration and retention settings.
        
        Returns:
            Log settings including retention policies and storage
        """
        url = "/cli/global/system/log/settings"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_fmupdate_settings(self) -> dict[str, Any]:
        """Get FortiManager update service configuration.
        
        Returns:
            Update service settings including FortiGuard connection
        """
        url = "/cli/global/fmupdate/service"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_sql_settings(self) -> dict[str, Any]:
        """Get SQL database settings.
        
        Returns:
            SQL configuration including database location and size
        """
        url = "/cli/global/system/sql"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def get_alert_console_settings(self) -> dict[str, Any]:
        """Get alert console configuration.
        
        Returns:
            Alert console settings for system notifications
        """
        url = "/cli/global/system/alertconsole"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # Phase 44: Additional System Operations
    # =========================================================================

    async def get_backup_status(
        self,
    ) -> dict[str, Any]:
        """Get system backup status and history.
        
        Returns:
            Backup status information
        """
        url = "/sys/status/backup"
        return await self.client.get(url)

    async def get_ha_status(
        self,
    ) -> dict[str, Any]:
        """Get FortiManager HA cluster status.
        
        Returns:
            HA cluster status
        """
        url = "/sys/ha/status"
        return await self.client.get(url)

    async def get_auto_update_status(
        self,
    ) -> dict[str, Any]:
        """Get automatic update status and schedule.
        
        Returns:
            Auto-update configuration and status
        """
        url = "/cli/global/system/autoupdate/schedule"
        return await self.client.get(url)

    async def get_workspace_mode_status(
        self,
    ) -> dict[str, Any]:
        """Get workspace mode configuration.
        
        Returns:
            Workspace mode settings
        """
        url = "/cli/global/system/workflow"
        return await self.client.get(url)

    async def list_connector_types(
        self,
    ) -> list[dict[str, Any]]:
        """List available connector types and their capabilities.
        
        Returns:
            List of connector types
        """
        url = "/sys/connector/types"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_gui_settings(
        self,
    ) -> dict[str, Any]:
        """Get GUI display settings.
        
        Returns:
            GUI configuration
        """
        url = "/cli/global/system/global"
        return await self.client.get(url)

    # =========================================================================
    # Phase 50: Final System Operations (The Last 10!)
    # =========================================================================

    async def list_tacacs_servers(
        self,
    ) -> list[dict[str, Any]]:
        """List TACACS+ servers configured on FortiManager.
        
        TACACS+ servers provide centralized AAA (Authentication, Authorization,
        and Accounting) services for administrative access control.
        
        Returns:
            List of TACACS+ server configurations
        """
        url = "/cli/global/system/admin/tacacs"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_tacacs_server(
        self,
        server_name: str,
    ) -> dict[str, Any]:
        """Get specific TACACS+ server configuration.
        
        Args:
            server_name: TACACS+ server name
            
        Returns:
            TACACS+ server details
        """
        url = f"/cli/global/system/admin/tacacs/{server_name}"
        return await self.client.get(url)

    async def get_user_sessions(
        self,
    ) -> list[dict[str, Any]]:
        """Get current user sessions on FortiManager.
        
        Returns information about active administrative sessions including:
        - Username
        - Login time
        - Source IP address
        - Session duration
        - Access method (GUI, CLI, API)
        
        Returns:
            List of active user sessions
        """
        url = "/sys/session"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def create_adom_in_fortianalyzer(
        self,
        adom_name: str,
        description: str = "",
    ) -> dict[str, Any]:
        """Create ADOM in connected FortiAnalyzer.
        
        When FortiManager is integrated with FortiAnalyzer, this creates
        a corresponding ADOM in FAZ for log collection and analysis.
        
        Args:
            adom_name: ADOM name to create
            description: ADOM description
            
        Returns:
            Creation result
            
        Note:
            Requires FortiAnalyzer integration to be configured.
        """
        data = {
            "name": adom_name,
            "desc": description,
        }
        url = "/dvmdb/adom"
        # This creates ADOM with FAZ sync enabled
        result = await self.client.add(url, data=data)
        return result

    async def get_api_user_details(
        self,
    ) -> dict[str, Any]:
        """Get details about the currently connected API user.
        
        Returns information about the API user making the request including:
        - Username
        - User type (API user, admin)
        - Permissions
        - Profile
        - Last login time
        
        Returns:
            Current API user details
        """
        url = "/sys/api/user/current"
        return await self.client.get(url)

    async def reboot_fortimanager(
        self,
        delay: int = 0,
    ) -> dict[str, Any]:
        """Reboot FortiManager system.
        
        Args:
            delay: Delay in seconds before reboot (0 = immediate)
            
        Returns:
            Reboot initiation result
            
        Warning:
            This will reboot the FortiManager and disconnect all users.
            Use with extreme caution in production environments.
        """
        data = {"delay": delay}
        url = "/sys/reboot"
        return await self.client.execute(url, data)

    async def backup_fortimanager_config(
        self,
    ) -> dict[str, Any]:
        """Trigger FortiManager configuration backup.
        
        Creates a full backup of FortiManager configuration including:
        - System configuration
        - ADOM configurations
        - Policy packages
        - Objects
        - Device management data
        
        Returns:
            Backup task details
            
        Note:
            The backup file will be stored in FortiManager's backup location.
            Use download operations to retrieve the backup file.
        """
        url = "/sys/backup"
        return await self.client.execute(url, {})

    async def restore_fortimanager_config(
        self,
        backup_file: str,
    ) -> dict[str, Any]:
        """Restore FortiManager configuration from backup.
        
        Args:
            backup_file: Path to backup file on FortiManager
            
        Returns:
            Restore task details
            
        Warning:
            This will replace current configuration with backup.
            All current settings will be lost. Use with extreme caution.
        """
        data = {"file": backup_file}
        url = "/sys/restore"
        return await self.client.execute(url, data)

    async def get_fortiguard_upstream_servers_list(
        self,
    ) -> list[dict[str, Any]]:
        """Get list of FortiGuard upstream servers.
        
        Returns the configured FortiGuard servers that FortiManager uses
        for updates and threat intelligence, including:
        - Server addresses
        - Connection status
        - Protocol and port
        - Service types
        
        Returns:
            List of upstream FortiGuard servers
        """
        url = "/cli/global/system/fortiguard"
        data = await self.client.get(url)
        # Return as list for consistency
        return [data] if isinstance(data, dict) else data if isinstance(data, list) else []

