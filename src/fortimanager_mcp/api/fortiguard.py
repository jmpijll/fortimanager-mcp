"""FortiGuard management API client for FortiManager."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient


class FortiGuardAPI:
    """API client for FortiGuard management operations."""

    def __init__(self, client: FortiManagerClient):
        """Initialize FortiGuard API client."""
        self.client = client

    # ============================================================================
    # FortiGuard Database Versions
    # ============================================================================

    async def get_fortiguard_versions(self) -> dict[str, Any]:
        """Get FortiGuard database versions.
        
        Returns version information for all FortiGuard objects:
        - Antivirus
        - Webfilter
        - GeoIP
        - IPS
        - etc.
        
        Returns:
            FortiGuard database versions
        """
        url = "/um/misc/fgd_db_ver"
        data = {"flags": 0}
        return await self.client.get(url, data=data)

    async def get_fortiguard_servers(self) -> dict[str, Any]:
        """Get list of FortiGuard upstream servers.
        
        Returns:
            List of FortiGuard servers with connection status
        """
        url = "/um/misc/server_list"
        return await self.client.get(url)

    # ============================================================================
    # Firmware Management
    # ============================================================================

    async def list_firmware_images(
        self,
        platform: str | None = None,
    ) -> list[dict[str, Any]]:
        """List available firmware images.
        
        Args:
            platform: Platform filter (e.g., "FortiGate", "FortiSwitch")
            
        Returns:
            List of firmware images
        """
        url = "/um/image/version/list"
        params = {}
        if platform:
            params["platform"] = platform
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def get_firmware_image_info(
        self,
        product: str,
        version: str,
    ) -> dict[str, Any]:
        """Get information about a specific firmware image.
        
        Args:
            product: Product name (e.g., "FortiGate")
            version: Firmware version
            
        Returns:
            Firmware image information
        """
        url = f"/um/image/version/{product}/{version}"
        return await self.client.get(url)

    async def download_firmware_image(
        self,
        product: str,
        version: str,
    ) -> dict[str, Any]:
        """Download a firmware image to FortiManager.
        
        Args:
            product: Product name
            version: Firmware version
            
        Returns:
            Download task information
        """
        url = "/um/image/download"
        data = {
            "product": product,
            "version": version,
        }
        return await self.client.exec(url, data=data)

    # ============================================================================
    # Device Contracts & Licenses
    # ============================================================================

    async def get_device_contracts(
        self,
        device: str | None = None,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get FortiGuard contracts for managed devices.
        
        Args:
            device: Specific device name (optional)
            adom: ADOM name
            
        Returns:
            List of device contracts
        """
        url = "/um/misc/fmg_license/devices"
        params = {"adom": adom}
        if device:
            params["device"] = device
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def get_device_license_status(
        self,
        device: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get license status for a specific device.
        
        Args:
            device: Device name
            adom: ADOM name
            
        Returns:
            License status information
        """
        url = f"/dvmdb/device/{device}/license/status"
        params = {"adom": adom}
        return await self.client.get(url, **params)

    # ============================================================================
    # FortiGuard Update History
    # ============================================================================

    async def get_update_history(
        self,
        category: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get FortiGuard update history.
        
        Args:
            category: FortiGuard category (e.g., "av", "wf", "ips")
            
        Returns:
            Update history records
        """
        url = "/um/misc/fgd_update_history"
        params = {}
        if category:
            params["category"] = category
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def get_downloaded_objects(self) -> list[dict[str, Any]]:
        """Get list of FortiGuard objects downloaded by FortiManager.
        
        Returns:
            List of downloaded FortiGuard objects
        """
        url = "/um/misc/fgd_object_list"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # ============================================================================
    # External Resources
    # ============================================================================

    async def list_external_resources(
        self,
        resource_type: str = "local",
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List external resources (threat feeds, custom lists, etc.).
        
        Args:
            resource_type: Resource type ("local" or "remote")
            adom: ADOM name
            
        Returns:
            List of external resources
        """
        if resource_type == "local":
            url = f"/pm/config/adom/{adom}/obj/system/external-resource"
        else:
            url = f"/pm/config/adom/{adom}/obj/system/external-resource"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_external_resource(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get external resource details.
        
        Args:
            name: Resource name
            adom: ADOM name
            
        Returns:
            External resource details
        """
        url = f"/pm/config/adom/{adom}/obj/system/external-resource/{name}"
        return await self.client.get(url)

    async def create_external_resource(
        self,
        name: str,
        resource_url: str,
        resource_type: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create an external resource (threat feed, custom URL list).
        
        Args:
            name: Resource name
            resource_url: URL of the external resource
            resource_type: Type (e.g., "address", "domain", "malware")
            adom: ADOM name
            **kwargs: Additional parameters (update-method, refresh-rate, etc.)
            
        Returns:
            Created resource
            
        Example:
            create_external_resource(
                name="threat-feed-1",
                resource_url="https://example.com/feed.txt",
                resource_type="address",
                adom="production"
            )
        """
        data = {
            "name": name,
            "resource": resource_url,
            "type": resource_type,
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/obj/system/external-resource"
        return await self.client.add(url, data=data)

    async def delete_external_resource(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete an external resource.
        
        Args:
            name: Resource name
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/system/external-resource/{name}"
        return await self.client.delete(url)

    async def refresh_external_resource(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Manually refresh an external resource.
        
        Args:
            name: Resource name
            adom: ADOM name
            
        Returns:
            Refresh task result
        """
        url = f"/pm/config/adom/{adom}/obj/system/external-resource/{name}"
        data = {"action": "refresh"}
        return await self.client.exec(url, data=data)

    # ============================================================================
    # Phase 22: FortiGuard Update Operations
    # ============================================================================

    async def trigger_fortiguard_update(
        self,
        update_type: str = "all",
    ) -> dict[str, Any]:
        """Trigger manual FortiGuard update.
        
        Manually triggers FortiManager to check for and download
        FortiGuard updates for databases, signatures, and firmware.
        
        Args:
            update_type: Update type ("all", "av", "ips", "wf", "geoip", etc.)
            
        Returns:
            Update task information
        """
        url = "/um/misc/trigger_fgd_update"
        data = {"type": update_type}
        return await self.client.exec(url, data=data)

    async def get_fortiguard_update_status(self) -> dict[str, Any]:
        """Get FortiGuard update status.
        
        Retrieves current status of FortiGuard updates including:
        - Update in progress
        - Last update time
        - Next scheduled update
        - Update errors if any
        
        Returns:
            Update status information
        """
        url = "/um/misc/fgd_update_status"
        return await self.client.get(url)

    async def get_fortiguard_update_schedule(self) -> dict[str, Any]:
        """Get FortiGuard update schedule configuration.
        
        Returns the configured schedule for automatic FortiGuard updates.
        
        Returns:
            Update schedule configuration
        """
        url = "/cli/global/system/fortiguard"
        data = await self.client.get(url)
        # Extract update schedule info
        if isinstance(data, dict):
            return {
                "update-server-location": data.get("update-server-location"),
                "auto-update-schedule": data.get("auto-update-schedule"),
                "update-frequency": data.get("update-frequency"),
                "update-day": data.get("update-day"),
                "update-time": data.get("update-time"),
            }
        return data if isinstance(data, dict) else {}

    # ============================================================================
    # Phase 22: FortiGuard Database Queries
    # ============================================================================

    async def query_fortiguard_outbreak(
        self,
        query_type: str = "latest",
    ) -> dict[str, Any]:
        """Query FortiGuard outbreak information.
        
        Retrieves current outbreak and threat intelligence from FortiGuard:
        - Latest malware outbreaks
        - Botnet activity
        - Vulnerability alerts
        - Zero-day threats
        
        Args:
            query_type: Query type ("latest", "critical", "trending")
            
        Returns:
            Outbreak information
        """
        url = "/um/misc/fgd_outbreak"
        params = {"type": query_type}
        return await self.client.get(url, **params)

    async def get_fortiguard_category_override(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get FortiGuard web filter category overrides.
        
        Returns custom category assignments that override FortiGuard's
        default categorization of websites.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of category overrides
        """
        url = f"/pm/config/adom/{adom}/obj/webfilter/ftgd-local-cat"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # ============================================================================
    # Phase 25: Complete FortiGuard Management
    # ============================================================================

    async def test_fortiguard_connection(self) -> dict[str, Any]:
        """Test connectivity to FortiGuard servers.
        
        Performs a connectivity test to FortiGuard servers to verify:
        - Network connectivity
        - DNS resolution
        - Server availability
        - Authentication status
        
        Returns:
            Connection test results
        """
        url = "/um/misc/test_fgd_connection"
        return await self.client.exec(url, data={})

    async def get_fortiguard_service_status(self) -> dict[str, Any]:
        """Get comprehensive FortiGuard service status.
        
        Returns detailed status information for all FortiGuard services:
        - Subscription status
        - Service availability
        - Last successful update per service
        - Connection status to update servers
        - License expiration dates
        
        Returns:
            FortiGuard service status information
        """
        url = "/um/misc/fgd_service_status"
        return await self.client.get(url)

    # ============================================================================
    # Phase 46: FortiGuard Advanced Operations
    # ============================================================================

    async def get_fortiguard_upstream_servers(self) -> dict[str, Any]:
        """Get FortiGuard upstream server configuration.
        
        Retrieves the configuration for upstream FortiGuard servers that
        FortiManager uses for updates and threat intelligence.
        
        Returns:
            FortiGuard server configuration including:
            - protocol: Connection protocol (http/https)
            - port: Connection port
            - service_account_id: FortiGuard service account ID
            - update_server_location: Geographic server preference
            - fortiguard_anycast: Anycast configuration
            - fortiguard_anycast_source: Anycast source setting
            
        Example Response:
            {
                "protocol": "https",
                "port": 443,
                "service-account-id": "FG-123456",
                "update-server-location": "usa",
                "fortiguard-anycast": "enable"
            }
        """
        url = "/cli/global/system/fortiguard"
        return await self.client.get(url)

    async def get_device_package_versions(
        self,
        platform: str = "FortiGate",
        current_version: str | None = None,
    ) -> list[dict[str, Any]]:
        """Get available package versions for managed devices.
        
        Queries available firmware and update packages for specific
        device platforms, optionally filtered by current version to
        show upgrade paths.
        
        Args:
            platform: Device platform (e.g., "FortiGate", "FortiSwitch", "FortiAP")
            current_version: Current device version for upgrade path analysis
            
        Returns:
            List of available packages with:
            - version: Package version number
            - build: Build number
            - release_date: Package release date
            - platform: Target platform
            - size_mb: Package size in megabytes
            - upgrade_path: Whether this is a valid upgrade
            
        Example:
            get_device_package_versions(
                platform="FortiGate",
                current_version="7.0.10"
            )
        """
        url = "/um/image/package/list"
        params = {"platform": platform}
        if current_version:
            params["current_version"] = current_version
        
        data = await self.client.get(url, data=params)
        return data if isinstance(data, list) else [data] if data else []

    async def export_fortiguard_objects(
        self,
        object_types: list[str],
        adom: str = "root",
        export_format: str = "json",
    ) -> dict[str, Any]:
        """Export FortiGuard objects for backup or migration.
        
        Exports specified object types from an ADOM in a portable format
        that can be imported into another ADOM or FortiManager instance.
        
        Args:
            object_types: List of object paths to export (e.g., ["firewall/address", "firewall/service/custom"])
            adom: Source ADOM name
            export_format: Export format - "json" or "xml"
            
        Returns:
            Exported data structure
            
        Example:
            export_fortiguard_objects(
                object_types=[
                    "firewall/address",
                    "firewall/service/custom",
                    "firewall/addrgrp"
                ],
                adom="production",
                export_format="json"
            )
            
        Note:
            Exported data should be stored securely as it may contain
            sensitive configuration information.
        """
        data = {
            "scope": {"name": adom, "type": "adom"},
            "objects": [{"type": obj_type} for obj_type in object_types],
            "format": export_format,
        }
        
        url = "/sys/api/export"
        return await self.client.exec(url, data=data)

    async def import_fortiguard_objects(
        self,
        import_data: str,
        adom: str = "root",
        conflict_action: str = "merge",
    ) -> dict[str, Any]:
        """Import FortiGuard objects from exported data.
        
        Imports previously exported objects into an ADOM. Supports
        multiple conflict resolution strategies.
        
        Args:
            import_data: Exported JSON or XML data to import
            adom: Target ADOM name
            conflict_action: How to handle conflicts:
                - "merge": Merge with existing objects
                - "replace": Replace existing objects
                - "skip": Skip objects that already exist
            
        Returns:
            Import results including:
            - imported_count: Number of objects imported
            - skipped_count: Number skipped due to conflicts
            - errors: Any import errors encountered
            
        Example:
            import_fortiguard_objects(
                import_data=exported_json,
                adom="disaster-recovery",
                conflict_action="merge"
            )
            
        Warning:
            Import operations can significantly modify ADOM configuration.
            Always test in a non-production ADOM first.
        """
        data = {
            "scope": {"name": adom, "type": "adom"},
            "data": import_data,
            "conflict_action": conflict_action,
        }
        
        url = "/sys/api/import"
        return await self.client.exec(url, data=data)

