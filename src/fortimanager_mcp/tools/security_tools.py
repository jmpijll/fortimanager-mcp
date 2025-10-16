"""MCP tools for security profile management operations."""

import logging
from typing import Any

from fortimanager_mcp.api.security_profiles import SecurityProfilesAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_security_api() -> SecurityProfilesAPI:
    """Get SecurityProfilesAPI instance."""
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return SecurityProfilesAPI(client)


# Web Filter Tools

@mcp.tool()
async def list_webfilter_profiles(adom: str = "root") -> dict[str, Any]:
    """List web filter profiles in an ADOM.
    
    Web filter profiles control web access and URL filtering.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of web filter profiles
        
    Example:
        result = list_webfilter_profiles(adom="root")
    """
    try:
        api = _get_security_api()
        profiles = await api.list_webfilter_profiles(adom=adom)
        
        return {
            "status": "success",
            "count": len(profiles),
            "profiles": profiles,
        }
    except Exception as e:
        logger.error(f"Failed to list web filter profiles: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def get_webfilter_profile(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get web filter profile details.
    
    Retrieves detailed configuration of a web filter profile.
    
    Args:
        name: Profile name
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with profile details
        
    Example:
        result = get_webfilter_profile(name="default", adom="root")
    """
    try:
        api = _get_security_api()
        profile = await api.get_webfilter_profile(name=name, adom=adom)
        
        return {
            "status": "success",
            "profile": profile,
        }
    except Exception as e:
        logger.error(f"Failed to get web filter profile: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_url_filters(adom: str = "root") -> dict[str, Any]:
    """List URL filter objects.
    
    URL filters contain lists of URLs to block or allow.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of URL filters
        
    Example:
        result = list_url_filters(adom="root")
    """
    try:
        api = _get_security_api()
        filters = await api.list_url_filters(adom=adom)
        
        return {
            "status": "success",
            "count": len(filters),
            "filters": filters,
        }
    except Exception as e:
        logger.error(f"Failed to list URL filters: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def add_url_to_filter(
    filter_id: int,
    url: str,
    adom: str = "root",
    action: str = "block",
) -> dict[str, Any]:
    """Add URL to a URL filter.
    
    Adds a new URL entry to an existing URL filter list.
    
    Args:
        filter_id: URL filter ID
        url: URL to add (e.g., "www.example.com")
        adom: ADOM name (default: "root")
        action: Action - "block", "allow", or "monitor" (default: "block")
        
    Returns:
        Dictionary with created entry details
        
    Example:
        result = add_url_to_filter(
            filter_id=1,
            url="www.malicious-site.com",
            action="block",
            adom="root"
        )
    """
    try:
        api = _get_security_api()
        entry = await api.create_url_filter_entry(
            filter_id=filter_id,
            url_to_block=url,
            adom=adom,
            action=action,
        )
        
        return {
            "status": "success",
            "entry": entry,
            "message": f"Added URL '{url}' to filter {filter_id}",
        }
    except Exception as e:
        logger.error(f"Failed to add URL to filter: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


# Application Control Tools

@mcp.tool()
async def list_applications(adom: str = "root") -> dict[str, Any]:
    """List all available applications.
    
    Returns the complete application database with details like
    category, risk level, technology, and protocols.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of applications
        
    Example:
        result = list_applications(adom="root")
    """
    try:
        api = _get_security_api()
        apps = await api.list_applications(adom=adom)
        
        return {
            "status": "success",
            "count": len(apps),
            "applications": apps[:100],  # Limit to first 100 for performance
            "note": f"Showing first 100 of {len(apps)} applications" if len(apps) > 100 else None,
        }
    except Exception as e:
        logger.error(f"Failed to list applications: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_application_categories(adom: str = "root") -> dict[str, Any]:
    """List application categories.
    
    Returns application categories like Email, Business, P2P, etc.
    Note: ADOM must contain real devices (not just model devices).
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of application categories
        
    Example:
        result = list_application_categories(adom="root")
    """
    try:
        api = _get_security_api()
        categories = await api.list_application_categories(adom=adom)
        
        return {
            "status": "success",
            "count": len(categories),
            "categories": categories,
        }
    except Exception as e:
        logger.error(f"Failed to list application categories: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_appctrl_profiles(adom: str = "root") -> dict[str, Any]:
    """List application control profiles.
    
    Application control profiles define which applications are allowed or blocked.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of application control profiles
        
    Example:
        result = list_appctrl_profiles(adom="root")
    """
    try:
        api = _get_security_api()
        profiles = await api.list_appctrl_profiles(adom=adom)
        
        return {
            "status": "success",
            "count": len(profiles),
            "profiles": profiles,
        }
    except Exception as e:
        logger.error(f"Failed to list application control profiles: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


# IPS Tools

@mcp.tool()
async def list_ips_sensors(adom: str = "root") -> dict[str, Any]:
    """List IPS sensors in an ADOM.
    
    IPS sensors contain rules for detecting and preventing intrusions.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of IPS sensors
        
    Example:
        result = list_ips_sensors(adom="root")
    """
    try:
        api = _get_security_api()
        sensors = await api.list_ips_sensors(adom=adom)
        
        return {
            "status": "success",
            "count": len(sensors),
            "sensors": sensors,
        }
    except Exception as e:
        logger.error(f"Failed to list IPS sensors: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def get_ips_sensor(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get IPS sensor details including rules.
    
    Retrieves detailed configuration of an IPS sensor including all rules.
    
    Args:
        name: Sensor name
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with sensor details and rules
        
    Example:
        result = get_ips_sensor(name="default", adom="root")
    """
    try:
        api = _get_security_api()
        sensor = await api.get_ips_sensor(name=name, adom=adom)
        
        return {
            "status": "success",
            "sensor": sensor,
        }
    except Exception as e:
        logger.error(f"Failed to get IPS sensor: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def create_ips_sensor(
    name: str,
    adom: str = "root",
    comment: str | None = None,
) -> dict[str, Any]:
    """Create a new IPS sensor.
    
    Creates an IPS sensor that can be populated with rules.
    
    Args:
        name: Sensor name
        adom: ADOM name (default: "root")
        comment: Optional comment
        
    Returns:
        Dictionary with created sensor details
        
    Example:
        result = create_ips_sensor(
            name="my_ips_sensor",
            adom="root",
            comment="Custom IPS sensor for critical systems"
        )
    """
    try:
        api = _get_security_api()
        sensor = await api.create_ips_sensor(
            name=name,
            adom=adom,
            comment=comment,
        )
        
        return {
            "status": "success",
            "sensor": sensor,
            "message": f"IPS sensor '{name}' created successfully",
        }
    except Exception as e:
        logger.error(f"Failed to create IPS sensor: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def add_ips_rule(
    sensor_name: str,
    severity: list[str],
    adom: str = "root",
    action: str = "default",
    log: str = "disable",
) -> dict[str, Any]:
    """Add IPS rule to a sensor.
    
    Adds a new IPS rule to an existing sensor based on severity.
    
    Args:
        sensor_name: IPS sensor name
        severity: List of severities (e.g., ["critical", "high", "medium", "low", "info"])
        adom: ADOM name (default: "root")
        action: Action - "default", "allow", "block", or "quarantine" (default: "default")
        log: Enable logging - "enable" or "disable" (default: "disable")
        
    Returns:
        Dictionary with created rule details
        
    Example:
        result = add_ips_rule(
            sensor_name="my_ips_sensor",
            severity=["critical", "high"],
            action="block",
            log="enable",
            adom="root"
        )
    """
    try:
        api = _get_security_api()
        rule = await api.add_ips_rule(
            sensor_name=sensor_name,
            severity=severity,
            adom=adom,
            action=action,
            log=log,
        )
        
        return {
            "status": "success",
            "rule": rule,
            "message": f"IPS rule added to sensor '{sensor_name}'",
        }
    except Exception as e:
        logger.error(f"Failed to add IPS rule: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def delete_ips_sensor(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete an IPS sensor.
    
    Removes an IPS sensor from FortiManager.
    
    Args:
        name: Sensor name
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with deletion status
        
    Example:
        result = delete_ips_sensor(name="my_ips_sensor", adom="root")
    """
    try:
        api = _get_security_api()
        await api.delete_ips_sensor(name=name, adom=adom)
        
        return {
            "status": "success",
            "message": f"IPS sensor '{name}' deleted successfully",
        }
    except Exception as e:
        logger.error(f"Failed to delete IPS sensor: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


# DLP Tools

@mcp.tool()
async def list_dlp_sensors(adom: str = "root") -> dict[str, Any]:
    """List DLP (Data Loss Prevention) sensors.
    
    DLP sensors detect and prevent sensitive data leakage.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of DLP sensors
        
    Example:
        result = list_dlp_sensors(adom="root")
    """
    try:
        api = _get_security_api()
        sensors = await api.list_dlp_sensors(adom=adom)
        
        return {
            "status": "success",
            "count": len(sensors),
            "sensors": sensors,
        }
    except Exception as e:
        logger.error(f"Failed to list DLP sensors: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def get_dlp_sensor(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get DLP sensor details.
    
    Retrieves detailed configuration of a DLP sensor.
    
    Args:
        name: Sensor name
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with DLP sensor details
        
    Example:
        result = get_dlp_sensor(name="default", adom="root")
    """
    try:
        api = _get_security_api()
        sensor = await api.get_dlp_sensor(name=name, adom=adom)
        
        return {
            "status": "success",
            "sensor": sensor,
        }
    except Exception as e:
        logger.error(f"Failed to get DLP sensor: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_dlp_filepatterns(adom: str = "root") -> dict[str, Any]:
    """List DLP file patterns.
    
    File patterns define file types to monitor for DLP.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of DLP file patterns
        
    Example:
        result = list_dlp_filepatterns(adom="root")
    """
    try:
        api = _get_security_api()
        patterns = await api.list_dlp_filepatterns(adom=adom)
        
        return {
            "status": "success",
            "count": len(patterns),
            "patterns": patterns,
        }
    except Exception as e:
        logger.error(f"Failed to list DLP file patterns: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


# Antivirus Tools

@mcp.tool()
async def list_antivirus_profiles(adom: str = "root") -> dict[str, Any]:
    """List antivirus profiles.
    
    Antivirus profiles define virus scanning settings.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of antivirus profiles
        
    Example:
        result = list_antivirus_profiles(adom="root")
    """
    try:
        api = _get_security_api()
        profiles = await api.list_antivirus_profiles(adom=adom)
        
        return {
            "status": "success",
            "count": len(profiles),
            "profiles": profiles,
        }
    except Exception as e:
        logger.error(f"Failed to list antivirus profiles: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def get_antivirus_profile(
    name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get antivirus profile details.
    
    Retrieves detailed configuration of an antivirus profile.
    
    Args:
        name: Profile name
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with antivirus profile details
        
    Example:
        result = get_antivirus_profile(name="default", adom="root")
    """
    try:
        api = _get_security_api()
        profile = await api.get_antivirus_profile(name=name, adom=adom)
        
        return {
            "status": "success",
            "profile": profile,
        }
    except Exception as e:
        logger.error(f"Failed to get antivirus profile: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


# ============================================================================
# Phase 19: Security Profiles - IPS Advanced Queries
# ============================================================================


@mcp.tool()
async def list_ips_signatures(
    adom: str = "root",
    severity: str | None = None,
) -> dict[str, Any]:
    """List available IPS signatures.
    
    Retrieves the list of custom IPS signatures that can be used in IPS sensors.
    These signatures detect specific attack patterns and vulnerabilities.
    
    Args:
        adom: ADOM name (default: "root")
        severity: Optional severity filter (critical, high, medium, low, info)
        
    Returns:
        Dictionary with list of IPS signatures
        
    Example:
        # List all signatures
        result = list_ips_signatures(adom="root")
        
        # List only critical signatures
        result = list_ips_signatures(adom="root", severity="critical")
    """
    try:
        api = _get_security_api()
        
        filter_criteria = {"severity": severity} if severity else None
        signatures = await api.list_ips_signatures(
            adom=adom,
            filter_criteria=filter_criteria
        )
        
        return {
            "status": "success",
            "count": len(signatures),
            "signatures": signatures,
        }
    except Exception as e:
        logger.error(f"Failed to list IPS signatures: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_ips_protocols(adom: str = "root") -> dict[str, Any]:
    """List IPS protocol decoders.
    
    Retrieves the list of protocol decoders used by IPS for deep packet inspection.
    Protocol decoders analyze specific network protocols for threats.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of protocol decoders
        
    Example:
        result = list_ips_protocols(adom="root")
    """
    try:
        api = _get_security_api()
        protocols = await api.list_ips_protocols(adom=adom)
        
        return {
            "status": "success",
            "count": len(protocols),
            "protocols": protocols,
        }
    except Exception as e:
        logger.error(f"Failed to list IPS protocols: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def query_ips_applications(
    adom: str = "root",
    search_term: str | None = None,
) -> dict[str, Any]:
    """Query IPS application signatures.
    
    Searches for application signatures that IPS can detect and control.
    Application signatures identify specific applications and services.
    
    Args:
        adom: ADOM name (default: "root")
        search_term: Optional search term to filter results
        
    Returns:
        Dictionary with list of application signatures
        
    Example:
        # List all applications
        result = query_ips_applications(adom="root")
        
        # Search for specific application
        result = query_ips_applications(
            adom="root",
            search_term="facebook"
        )
    """
    try:
        api = _get_security_api()
        applications = await api.query_ips_applications(
            adom=adom,
            search_term=search_term
        )
        
        return {
            "status": "success",
            "count": len(applications),
            "applications": applications,
        }
    except Exception as e:
        logger.error(f"Failed to query IPS applications: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


# ============================================================================
# Phase 19: Security Profiles - DLP FortiGuard Queries
# ============================================================================


@mcp.tool()
async def list_dlp_fortiguard_elements(adom: str = "root") -> dict[str, Any]:
    """List FortiGuard DLP data elements.
    
    Retrieves the list of predefined data types from FortiGuard that can be
    detected by DLP sensors (e.g., credit cards, SSN, passport numbers).
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of DLP data elements
        
    Example:
        result = list_dlp_fortiguard_elements(adom="root")
    """
    try:
        api = _get_security_api()
        elements = await api.list_dlp_fortiguard_elements(adom=adom)
        
        return {
            "status": "success",
            "count": len(elements),
            "elements": elements,
        }
    except Exception as e:
        logger.error(f"Failed to list DLP FortiGuard elements: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_dlp_dictionaries(adom: str = "root") -> dict[str, Any]:
    """List DLP dictionaries.
    
    Retrieves custom DLP dictionaries containing patterns and keywords
    for data loss prevention. Dictionaries define sensitive data to detect.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of DLP dictionaries
        
    Example:
        result = list_dlp_dictionaries(adom="root")
    """
    try:
        api = _get_security_api()
        dictionaries = await api.list_dlp_dictionaries(adom=adom)
        
        return {
            "status": "success",
            "count": len(dictionaries),
            "dictionaries": dictionaries,
        }
    except Exception as e:
        logger.error(f"Failed to list DLP dictionaries: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


# =============================================================================
# Phase 30: Complete Security Profiles
# =============================================================================


@mcp.tool()
async def list_ssh_filter_profiles(adom: str = "root") -> dict[str, Any]:
    """List SSH filter profiles.
    
    SSH filter profiles control SSH protocol usage including:
    - Allowed SSH commands
    - File transfer restrictions
    - Shell command filtering
    - SSH version enforcement
    
    Use this to secure SSH access and prevent unauthorized operations.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of SSH filter profiles
        
    Example:
        result = list_ssh_filter_profiles(adom="root")
    """
    try:
        api = _get_security_api()
        profiles = await api.list_ssh_filter_profiles(adom=adom)
        
        return {
            "status": "success",
            "count": len(profiles),
            "profiles": profiles,
        }
    except Exception as e:
        logger.error(f"Failed to list SSH filter profiles: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_email_filter_profiles(adom: str = "root") -> dict[str, Any]:
    """List email filter profiles.
    
    Email filter profiles control email content and attachments:
    - Attachment blocking by type
    - Content inspection
    - Spam filtering integration
    - Phishing detection
    
    Protects against email-borne threats and data leakage.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of email filter profiles
        
    Example:
        result = list_email_filter_profiles(adom="root")
    """
    try:
        api = _get_security_api()
        profiles = await api.list_email_filter_profiles(adom=adom)
        
        return {
            "status": "success",
            "count": len(profiles),
            "profiles": profiles,
        }
    except Exception as e:
        logger.error(f"Failed to list email filter profiles: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_file_filter_profiles(adom: str = "root") -> dict[str, Any]:
    """List file filter profiles.
    
    File filter profiles control file transfers including:
    - File type blocking (executables, scripts, archives)
    - File size limits
    - Protocol-specific filtering (HTTP, FTP, SMTP)
    - Upload/download restrictions
    
    Prevents malware distribution and data exfiltration.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of file filter profiles
        
    Example:
        result = list_file_filter_profiles(adom="root")
    """
    try:
        api = _get_security_api()
        profiles = await api.list_file_filter_profiles(adom=adom)
        
        return {
            "status": "success",
            "count": len(profiles),
            "profiles": profiles,
        }
    except Exception as e:
        logger.error(f"Failed to list file filter profiles: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_icap_profiles(adom: str = "root") -> dict[str, Any]:
    """List ICAP (Internet Content Adaptation Protocol) profiles.
    
    ICAP profiles integrate with external content inspection servers:
    - Third-party DLP engines
    - Advanced antivirus/sandboxing
    - Content filtering services
    - Custom inspection systems
    
    Extends FortiGate security with external scanners.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of ICAP profiles
        
    Example:
        result = list_icap_profiles(adom="root")
    """
    try:
        api = _get_security_api()
        profiles = await api.list_icap_profiles(adom=adom)
        
        return {
            "status": "success",
            "count": len(profiles),
            "profiles": profiles,
        }
    except Exception as e:
        logger.error(f"Failed to list ICAP profiles: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def list_voip_profiles(adom: str = "root") -> dict[str, Any]:
    """List VoIP (Voice over IP) security profiles.
    
    VoIP profiles secure voice communications:
    - SIP (Session Initiation Protocol) inspection
    - SCCP (Skinny Client Control Protocol) protection
    - VoIP attack prevention
    - Call quality monitoring
    - RTP/RTCP validation
    
    Essential for securing VoIP infrastructure and preventing abuse.
    
    Args:
        adom: ADOM name (default: "root")
        
    Returns:
        Dictionary with list of VoIP profiles
        
    Example:
        result = list_voip_profiles(adom="root")
    """
    try:
        api = _get_security_api()
        profiles = await api.list_voip_profiles(adom=adom)
        
        return {
            "status": "success",
            "count": len(profiles),
            "profiles": profiles,
        }
    except Exception as e:
        logger.error(f"Failed to list VoIP profiles: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


# =============================================================================
# Phase 47: Security Profile Batch Operations
# =============================================================================


@mcp.tool()
async def bulk_add_security_profile_entries(
    profile_type: str,
    profile_name: str,
    entries_json: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Add multiple entries to a security profile in one batch operation.
    
    Efficiently adds multiple URLs, signatures, rules, or filters to security
    profiles. Much faster than adding entries one at a time.
    
    Supports: Web Filter, IPS, Application Control, DLP, Antivirus profiles.
    
    Args:
        profile_type: Profile type - "webfilter", "ips", "application", "dlp", "av"
        profile_name: Name of the profile to modify
        entries_json: JSON string array of entries to add
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with operation results and count of entries added
    
    Example:
        result = bulk_add_security_profile_entries(
            profile_type="webfilter",
            profile_name="strict-filter",
            entries_json='[{"url": "badsite1.com", "action": "block"}, {"url": "badsite2.com", "action": "block"}]',
            adom="root"
        )
    """
    try:
        import json
        api = _get_security_api()
        
        # Parse entries from JSON
        entries = json.loads(entries_json)
        
        result = await api.batch_add_profile_entries(
            profile_type=profile_type,
            profile_name=profile_name,
            entries=entries,
            adom=adom,
        )
        
        return {
            "status": "success",
            **result,
        }
    except Exception as e:
        logger.error(f"Failed to batch add profile entries: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def replace_security_profile_entries(
    profile_type: str,
    profile_name: str,
    entries_json: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Replace ALL entries in a security profile with new ones.
    
    WARNING: This removes all existing entries and replaces them with the
    provided list. This operation cannot be undone. Use with caution.
    
    Useful for bulk profile reconfiguration or migration scenarios.
    
    Args:
        profile_type: Profile type - "webfilter", "ips", "application", "dlp"
        profile_name: Name of the profile to modify
        entries_json: JSON string array of complete new entry list
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with operation results
    
    Example:
        result = replace_security_profile_entries(
            profile_type="ips",
            profile_name="production-ips",
            entries_json='[{"signature": "sig1", "action": "block"}, ...]',
            adom="root"
        )
    """
    try:
        import json
        api = _get_security_api()
        
        # Parse entries from JSON
        entries = json.loads(entries_json)
        
        result = await api.replace_all_profile_entries(
            profile_type=profile_type,
            profile_name=profile_name,
            entries=entries,
            adom=adom,
        )
        
        return {
            "status": "success",
            **result,
        }
    except Exception as e:
        logger.error(f"Failed to replace profile entries: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def bulk_update_security_profile_entries(
    profile_type: str,
    profile_name: str,
    updates_json: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Update multiple entries in a security profile.
    
    Updates specific fields in multiple profile entries without replacing
    the entire entry. Each update must include an "id" field plus the
    fields to update.
    
    Args:
        profile_type: Profile type - "webfilter", "ips", "application", "dlp"
        profile_name: Name of the profile to modify
        updates_json: JSON string array of entries with id and fields to update
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with update results
    
    Example:
        result = bulk_update_security_profile_entries(
            profile_type="ips",
            profile_name="default",
            updates_json='[{"id": 1, "action": "block", "severity": "critical"}, {"id": 2, "action": "monitor"}]',
            adom="root"
        )
    """
    try:
        import json
        api = _get_security_api()
        
        # Parse updates from JSON
        updates = json.loads(updates_json)
        
        result = await api.batch_update_profile_entries(
            profile_type=profile_type,
            profile_name=profile_name,
            entry_updates=updates,
            adom=adom,
        )
        
        return {
            "status": "success",
            **result,
        }
    except Exception as e:
        logger.error(f"Failed to batch update profile entries: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def bulk_delete_security_profile_entries(
    profile_type: str,
    profile_name: str,
    entry_ids: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete multiple entries from a security profile.
    
    Removes multiple entries by ID in a single operation. Much more
    efficient than deleting entries one at a time.
    
    Args:
        profile_type: Profile type - "webfilter", "ips", "application", "dlp"
        profile_name: Name of the profile to modify
        entry_ids: Comma-separated list of entry IDs to delete (e.g., "1,2,3")
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with deletion results
    
    Example:
        result = bulk_delete_security_profile_entries(
            profile_type="webfilter",
            profile_name="test-filter",
            entry_ids="10,11,12,13",
            adom="root"
        )
    """
    try:
        api = _get_security_api()
        
        # Parse entry IDs
        ids = [id.strip() for id in entry_ids.split(",")]
        
        result = await api.batch_delete_profile_entries(
            profile_type=profile_type,
            profile_name=profile_name,
            entry_ids=ids,
            adom=adom,
        )
        
        return {
            "status": "success",
            **result,
        }
    except Exception as e:
        logger.error(f"Failed to batch delete profile entries: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def get_security_profile_entry_count(
    profile_type: str,
    profile_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get count and list of entries in a security profile.
    
    Useful for:
    - Monitoring profile complexity
    - Capacity planning
    - Identifying oversized profiles
    - Profile auditing
    
    Args:
        profile_type: Profile type - "webfilter", "ips", "application", "dlp"
        profile_name: Name of the profile
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with entry count and list of entries
    
    Example:
        result = get_security_profile_entry_count(
            profile_type="ips",
            profile_name="production-ips",
            adom="root"
        )
    """
    try:
        api = _get_security_api()
        
        result = await api.get_profile_entry_count(
            profile_type=profile_type,
            profile_name=profile_name,
            adom=adom,
        )
        
        return {
            "status": "success",
            **result,
        }
    except Exception as e:
        logger.error(f"Failed to get profile entry count: {e}")
        return {
            "status": "error",
            "message": str(e),
        }


@mcp.tool()
async def validate_security_profile_entries(
    profile_type: str,
    entries_json: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Validate security profile entries before applying them.
    
    Pre-validates entry syntax, required fields, and value ranges without
    actually creating the entries. Use this in automation workflows to
    catch errors before applying changes.
    
    Validation checks:
    - Required fields present
    - Valid action values
    - Proper syntax
    - Value ranges
    
    Args:
        profile_type: Profile type - "webfilter", "ips", "application", "dlp"
        entries_json: JSON string array of entries to validate
        adom: ADOM name (default: "root")
    
    Returns:
        Dictionary with validation results and any errors found
    
    Example:
        result = validate_security_profile_entries(
            profile_type="webfilter",
            entries_json='[{"url": "test.com", "action": "block"}, {"url": "bad.com"}]',
            adom="root"
        )
    """
    try:
        import json
        api = _get_security_api()
        
        # Parse entries from JSON
        entries = json.loads(entries_json)
        
        result = await api.validate_profile_entries(
            profile_type=profile_type,
            entries=entries,
            adom=adom,
        )
        
        return {
            "status": "success",
            **result,
        }
    except Exception as e:
        logger.error(f"Failed to validate profile entries: {e}")
        return {
            "status": "error",
            "message": str(e),
        }

