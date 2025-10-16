"""FortiManager Security Profiles API operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class SecurityProfilesAPI:
    """Security Profile management operations.
    
    Handles Web Filter, Application Control, IPS, DLP, and other security profiles.
    """

    def __init__(self, client: Any) -> None:
        """Initialize SecurityProfilesAPI.
        
        Args:
            client: FortiManager API client
        """
        self.client = client

    # Web Filter / URL Filter methods
    
    async def list_webfilter_profiles(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List web filter profiles.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of web filter profiles
        """
        url = f"/pm/config/adom/{adom}/obj/webfilter/profile"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_webfilter_profile(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get web filter profile details.
        
        Args:
            name: Profile name
            adom: ADOM name
            
        Returns:
            Web filter profile details
        """
        url = f"/pm/config/adom/{adom}/obj/webfilter/profile/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def list_url_filters(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List URL filter objects.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of URL filters
        """
        url = f"/pm/config/adom/{adom}/obj/webfilter/urlfilter"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def create_url_filter_entry(
        self,
        filter_id: int,
        url_to_block: str,
        adom: str = "root",
        action: str = "block",
    ) -> dict[str, Any]:
        """Add URL entry to a URL filter.
        
        Args:
            filter_id: URL filter ID
            url_to_block: URL to add
            adom: ADOM name
            action: Action (block, allow, monitor)
            
        Returns:
            Created entry details
        """
        url = f"/pm/config/adom/{adom}/obj/webfilter/urlfilter/{filter_id}/entries"
        data = {
            "url": url_to_block,
            "action": action,
        }
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    # Application Control methods
    
    async def list_applications(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List all available applications.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of applications
        """
        url = f"/pm/config/adom/{adom}/_application/list"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_application_categories(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List application categories.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of application categories
        """
        url = f"/pm/config/adom/{adom}/_category/list"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_appctrl_profiles(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List application control profiles.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of application control profiles
        """
        url = f"/pm/config/adom/{adom}/obj/application/list"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_appctrl_profile(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get application control profile details.
        
        Args:
            name: Profile name
            adom: ADOM name
            
        Returns:
            Profile details
        """
        url = f"/pm/config/adom/{adom}/obj/application/list/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # IPS methods
    
    async def list_ips_sensors(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List IPS sensors.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of IPS sensors
        """
        url = f"/pm/config/adom/{adom}/obj/ips/sensor"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_ips_sensor(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get IPS sensor details.
        
        Args:
            name: Sensor name
            adom: ADOM name
            
        Returns:
            IPS sensor details including rules
        """
        url = f"/pm/config/adom/{adom}/obj/ips/sensor/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_ips_sensor(
        self,
        name: str,
        adom: str = "root",
        comment: str | None = None,
    ) -> dict[str, Any]:
        """Create an IPS sensor.
        
        Args:
            name: Sensor name
            adom: ADOM name
            comment: Optional comment
            
        Returns:
            Created sensor details
        """
        url = f"/pm/config/adom/{adom}/obj/ips/sensor"
        data: dict[str, Any] = {"name": name}
        if comment:
            data["comment"] = comment
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def add_ips_rule(
        self,
        sensor_name: str,
        severity: list[str],
        adom: str = "root",
        action: str = "default",
        status: str = "default",
        log: str = "disable",
    ) -> dict[str, Any]:
        """Add IPS rule to a sensor.
        
        Args:
            sensor_name: IPS sensor name
            severity: List of severities (e.g., ["critical", "high"])
            adom: ADOM name
            action: Action (default, allow, block, quarantine)
            status: Status (default, enable, disable)
            log: Logging (enable, disable)
            
        Returns:
            Created rule details
        """
        url = f"/pm/config/adom/{adom}/obj/ips/sensor/{sensor_name}/entries"
        data = {
            "severity": severity,
            "action": action,
            "status": status,
            "log": log,
            "application": ["all"],
            "location": ["all"],
            "os": ["all"],
            "protocol": ["all"],
        }
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def delete_ips_sensor(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete an IPS sensor.
        
        Args:
            name: Sensor name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/config/adom/{adom}/obj/ips/sensor/{name}"
        result = await self.client.delete(url)
        return result

    # DLP methods
    
    async def list_dlp_sensors(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List DLP sensors.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of DLP sensors
        """
        url = f"/pm/config/adom/{adom}/obj/dlp/sensor"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_dlp_sensor(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get DLP sensor details.
        
        Args:
            name: Sensor name
            adom: ADOM name
            
        Returns:
            DLP sensor details
        """
        url = f"/pm/config/adom/{adom}/obj/dlp/sensor/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def list_dlp_filepatterns(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List DLP file patterns.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of DLP file patterns
        """
        url = f"/pm/config/adom/{adom}/obj/dlp/filepattern"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # Antivirus methods
    
    async def list_antivirus_profiles(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List antivirus profiles.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of antivirus profiles
        """
        url = f"/pm/config/adom/{adom}/obj/antivirus/profile"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_antivirus_profile(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get antivirus profile details.
        
        Args:
            name: Profile name
            adom: ADOM name
            
        Returns:
            Antivirus profile details
        """
        url = f"/pm/config/adom/{adom}/obj/antivirus/profile/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # Phase 19: Advanced Entry Management
    
    async def add_multiple_webfilter_entries(
        self,
        profile_name: str,
        entries: list[dict[str, Any]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Add multiple entries to a web filter profile.
        
        Args:
            profile_name: Web filter profile name
            entries: List of entry dictionaries
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/webfilter/profile/{profile_name}/ftgd-wf/filters"
        result = await self.client.add(url, data=entries)
        return result if isinstance(result, dict) else {}

    async def replace_ips_entries(
        self,
        sensor_name: str,
        entries: list[dict[str, Any]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Replace all entries in an IPS sensor.
        
        Args:
            sensor_name: IPS sensor name
            entries: List of IPS rule entries
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/ips/sensor/{sensor_name}/entries"
        result = await self.client.set(url, data=entries)
        return result if isinstance(result, dict) else {}

    async def batch_update_profile_entries(
        self,
        profile_type: str,
        profile_name: str,
        entry_type: str,
        entries: list[dict[str, Any]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Batch update entries in any profile type.
        
        Args:
            profile_type: Profile type (webfilter, ips, dlp, etc.)
            profile_name: Profile name
            entry_type: Entry type (rules, filters, sensors, etc.)
            entries: List of entries to update
            adom: ADOM name
            
        Returns:
            Operation result
        """
        url = f"/pm/config/adom/{adom}/obj/{profile_type}/{profile_name}/{entry_type}"
        result = await self.client.set(url, data=entries)
        return result if isinstance(result, dict) else {}

    # Phase 19: IPS Advanced Queries
    
    async def list_ips_signatures(
        self,
        adom: str = "root",
        filter_criteria: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """List available IPS signatures.
        
        Args:
            adom: ADOM name
            filter_criteria: Optional filter criteria
            
        Returns:
            List of IPS signatures
        """
        url = f"/pm/config/adom/{adom}/obj/ips/custom"
        data = await self.client.get(url)
        signatures = data if isinstance(data, list) else [data] if data else []
        
        # Apply filters if provided
        if filter_criteria:
            filtered = []
            for sig in signatures:
                match = True
                for key, value in filter_criteria.items():
                    if sig.get(key) != value:
                        match = False
                        break
                if match:
                    filtered.append(sig)
            return filtered
        
        return signatures

    async def list_ips_protocols(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List IPS protocol decoders.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of protocol decoders
        """
        url = f"/pm/config/adom/{adom}/obj/ips/decoder"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def query_ips_applications(
        self,
        adom: str = "root",
        search_term: str | None = None,
    ) -> list[dict[str, Any]]:
        """Query IPS application signatures.
        
        Args:
            adom: ADOM name
            search_term: Optional search term to filter results
            
        Returns:
            List of application signatures
        """
        # Query from application control - IPS uses same app definitions
        url = f"/pm/config/adom/{adom}/obj/application/list"
        data = await self.client.get(url)
        apps = data if isinstance(data, list) else [data] if data else []
        
        if search_term:
            filtered = []
            for app in apps:
                if search_term.lower() in str(app.get("name", "")).lower():
                    filtered.append(app)
            return filtered
        
        return apps

    # Phase 19: DLP FortiGuard Queries
    
    async def list_dlp_fortiguard_elements(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List FortiGuard DLP data elements.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of DLP data elements
        """
        url = f"/pm/config/adom/{adom}/obj/dlp/data-type"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_dlp_dictionaries(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List DLP dictionaries.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of DLP dictionaries
        """
        url = f"/pm/config/adom/{adom}/obj/dlp/dictionary"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Phase 30: Complete Security Profiles
    # =========================================================================

    async def list_ssh_filter_profiles(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List SSH filter profiles.
        
        SSH filter profiles control SSH protocol usage and commands.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of SSH filter profiles
        """
        url = f"/pm/config/adom/{adom}/obj/ssh-filter/profile"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_email_filter_profiles(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List email filter profiles.
        
        Email filter profiles control email content and attachments.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of email filter profiles
        """
        url = f"/pm/config/adom/{adom}/obj/emailfilter/profile"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_file_filter_profiles(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List file filter profiles.
        
        File filter profiles control file transfer and uploads/downloads.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of file filter profiles
        """
        url = f"/pm/config/adom/{adom}/obj/file-filter/profile"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_icap_profiles(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List ICAP profiles.
        
        ICAP profiles integrate with external content inspection servers
        for DLP, antivirus, and content filtering.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of ICAP profiles
        """
        url = f"/pm/config/adom/{adom}/obj/icap/profile"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_voip_profiles(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List VoIP profiles.
        
        VoIP profiles control SIP and SCCP protocol inspection and security.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of VoIP profiles
        """
        url = f"/pm/config/adom/{adom}/obj/voip/profile"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Phase 47: Security Profile Batch Operations
    # =========================================================================

    async def batch_add_profile_entries(
        self,
        profile_type: str,
        profile_name: str,
        entries: list[dict[str, Any]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Add multiple entries to a security profile in one operation.
        
        Efficiently adds multiple entries (URLs, signatures, rules) to security
        profiles like web filter, IPS, application control, etc.
        
        Args:
            profile_type: Profile type - "webfilter", "ips", "application", "dlp", "av"
            profile_name: Profile name
            entries: List of entry dictionaries to add
            adom: ADOM name
            
        Returns:
            Operation result with count of entries added
            
        Example:
            batch_add_profile_entries(
                profile_type="webfilter",
                profile_name="strict-filter",
                entries=[
                    {"url": "example1.com", "action": "block"},
                    {"url": "example2.com", "action": "block"}
                ]
            )
        """
        # Map profile types to their entry endpoints
        entry_paths = {
            "webfilter": f"/pm/config/adom/{adom}/obj/webfilter/profile/{profile_name}/ftgd-wf/filters",
            "ips": f"/pm/config/adom/{adom}/obj/ips/sensor/{profile_name}/entries",
            "application": f"/pm/config/adom/{adom}/obj/application/list/{profile_name}/entries",
            "dlp": f"/pm/config/adom/{adom}/obj/dlp/sensor/{profile_name}/filter",
            "av": f"/pm/config/adom/{adom}/obj/antivirus/profile/{profile_name}/http",
        }
        
        url = entry_paths.get(profile_type)
        if not url:
            raise ValueError(f"Unsupported profile type: {profile_type}")
        
        # Add entries in batch
        results = []
        for entry in entries:
            result = await self.client.add(url, data=entry)
            results.append(result)
        
        return {
            "profile_type": profile_type,
            "profile_name": profile_name,
            "entries_added": len(results),
            "results": results,
        }

    async def replace_all_profile_entries(
        self,
        profile_type: str,
        profile_name: str,
        entries: list[dict[str, Any]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Replace all entries in a security profile.
        
        Removes existing entries and replaces them with new ones. Useful for
        bulk profile reconfiguration or migration.
        
        Args:
            profile_type: Profile type - "webfilter", "ips", "application", "dlp"
            profile_name: Profile name
            entries: Complete list of new entries
            adom: ADOM name
            
        Returns:
            Operation result
            
        Warning:
            This replaces ALL existing entries. Cannot be undone.
        """
        # Map profile types to their entry endpoints
        entry_paths = {
            "webfilter": f"/pm/config/adom/{adom}/obj/webfilter/profile/{profile_name}/ftgd-wf/filters",
            "ips": f"/pm/config/adom/{adom}/obj/ips/sensor/{profile_name}/entries",
            "application": f"/pm/config/adom/{adom}/obj/application/list/{profile_name}/entries",
            "dlp": f"/pm/config/adom/{adom}/obj/dlp/sensor/{profile_name}/filter",
        }
        
        url = entry_paths.get(profile_type)
        if not url:
            raise ValueError(f"Unsupported profile type: {profile_type}")
        
        # Use PUT to replace all entries
        result = await self.client.set(url, data={"entries": entries})
        
        return {
            "profile_type": profile_type,
            "profile_name": profile_name,
            "entries_replaced": len(entries),
            "result": result,
        }

    async def batch_update_profile_entries(
        self,
        profile_type: str,
        profile_name: str,
        entry_updates: list[dict[str, Any]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Update multiple profile entries.
        
        Updates specific fields in multiple entries without replacing entire entries.
        
        Args:
            profile_type: Profile type
            profile_name: Profile name
            entry_updates: List of entries with id and fields to update
            adom: ADOM name
            
        Returns:
            Update results
            
        Example:
            batch_update_profile_entries(
                profile_type="ips",
                profile_name="default",
                entry_updates=[
                    {"id": 1, "action": "block", "severity": "critical"},
                    {"id": 2, "action": "monitor"}
                ]
            )
        """
        entry_paths = {
            "webfilter": f"/pm/config/adom/{adom}/obj/webfilter/profile/{profile_name}/ftgd-wf/filters",
            "ips": f"/pm/config/adom/{adom}/obj/ips/sensor/{profile_name}/entries",
            "application": f"/pm/config/adom/{adom}/obj/application/list/{profile_name}/entries",
            "dlp": f"/pm/config/adom/{adom}/obj/dlp/sensor/{profile_name}/filter",
        }
        
        base_url = entry_paths.get(profile_type)
        if not base_url:
            raise ValueError(f"Unsupported profile type: {profile_type}")
        
        results = []
        for update in entry_updates:
            entry_id = update.pop("id", None)
            if entry_id:
                url = f"{base_url}/{entry_id}"
                result = await self.client.update(url, data=update)
                results.append(result)
        
        return {
            "profile_type": profile_type,
            "profile_name": profile_name,
            "entries_updated": len(results),
            "results": results,
        }

    async def batch_delete_profile_entries(
        self,
        profile_type: str,
        profile_name: str,
        entry_ids: list[int | str],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete multiple entries from a security profile.
        
        Removes multiple entries by ID in a single operation.
        
        Args:
            profile_type: Profile type
            profile_name: Profile name
            entry_ids: List of entry IDs to delete
            adom: ADOM name
            
        Returns:
            Deletion results
        """
        entry_paths = {
            "webfilter": f"/pm/config/adom/{adom}/obj/webfilter/profile/{profile_name}/ftgd-wf/filters",
            "ips": f"/pm/config/adom/{adom}/obj/ips/sensor/{profile_name}/entries",
            "application": f"/pm/config/adom/{adom}/obj/application/list/{profile_name}/entries",
            "dlp": f"/pm/config/adom/{adom}/obj/dlp/sensor/{profile_name}/filter",
        }
        
        base_url = entry_paths.get(profile_type)
        if not base_url:
            raise ValueError(f"Unsupported profile type: {profile_type}")
        
        results = []
        for entry_id in entry_ids:
            url = f"{base_url}/{entry_id}"
            result = await self.client.delete(url)
            results.append(result)
        
        return {
            "profile_type": profile_type,
            "profile_name": profile_name,
            "entries_deleted": len(results),
            "results": results,
        }

    async def get_profile_entry_count(
        self,
        profile_type: str,
        profile_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get count of entries in a security profile.
        
        Useful for monitoring profile size and complexity.
        
        Args:
            profile_type: Profile type
            profile_name: Profile name
            adom: ADOM name
            
        Returns:
            Entry count statistics
        """
        entry_paths = {
            "webfilter": f"/pm/config/adom/{adom}/obj/webfilter/profile/{profile_name}/ftgd-wf/filters",
            "ips": f"/pm/config/adom/{adom}/obj/ips/sensor/{profile_name}/entries",
            "application": f"/pm/config/adom/{adom}/obj/application/list/{profile_name}/entries",
            "dlp": f"/pm/config/adom/{adom}/obj/dlp/sensor/{profile_name}/filter",
        }
        
        url = entry_paths.get(profile_type)
        if not url:
            raise ValueError(f"Unsupported profile type: {profile_type}")
        
        data = await self.client.get(url)
        entries = data if isinstance(data, list) else [data] if data else []
        
        return {
            "profile_type": profile_type,
            "profile_name": profile_name,
            "entry_count": len(entries),
            "entries": entries,
        }

    async def validate_profile_entries(
        self,
        profile_type: str,
        entries: list[dict[str, Any]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Validate profile entries before applying.
        
        Checks entry syntax and values without actually creating them.
        Useful for pre-validation in automation workflows.
        
        Args:
            profile_type: Profile type
            entries: Entries to validate
            adom: ADOM name
            
        Returns:
            Validation results with any errors
        """
        validation_results = []
        
        for idx, entry in enumerate(entries):
            errors = []
            
            # Basic validation
            if profile_type == "webfilter":
                if "url" not in entry:
                    errors.append("Missing required field: url")
                if "action" not in entry:
                    errors.append("Missing required field: action")
                elif entry["action"] not in ["block", "allow", "monitor"]:
                    errors.append(f"Invalid action: {entry['action']}")
            
            elif profile_type == "ips":
                if "signature" not in entry and "rule-id" not in entry:
                    errors.append("Missing signature or rule-id")
                if "action" in entry and entry["action"] not in ["block", "pass", "reset"]:
                    errors.append(f"Invalid action: {entry['action']}")
            
            validation_results.append({
                "index": idx,
                "valid": len(errors) == 0,
                "errors": errors,
                "entry": entry,
            })
        
        valid_count = sum(1 for r in validation_results if r["valid"])
        
        return {
            "profile_type": profile_type,
            "total_entries": len(entries),
            "valid_entries": valid_count,
            "invalid_entries": len(entries) - valid_count,
            "validation_results": validation_results,
        }

