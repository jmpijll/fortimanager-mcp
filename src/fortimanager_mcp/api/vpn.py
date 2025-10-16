"""FortiManager VPN API operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class VPNAPI:
    """VPN management operations.
    
    Handles IPsec, SSL-VPN, and certificate management.
    """

    def __init__(self, client: Any) -> None:
        """Initialize VPNAPI.
        
        Args:
            client: FortiManager API client
        """
        self.client = client

    # =========================================================================
    # IPsec Phase1 Interface Methods
    # =========================================================================

    async def list_ipsec_phase1(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List IPsec Phase1 interfaces in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of IPsec Phase1 interfaces
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/phase1-interface"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_ipsec_phase1(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get IPsec Phase1 interface details.
        
        Args:
            name: Phase1 interface name
            adom: ADOM name
            
        Returns:
            Phase1 interface details
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/phase1-interface/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_ipsec_phase1(
        self,
        name: str,
        interface: str,
        remote_gw: str,
        adom: str = "root",
        psk: str | None = None,
        certificate: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create IPsec Phase1 interface.
        
        Args:
            name: Phase1 interface name
            interface: Physical/logical interface name
            remote_gw: Remote gateway IP address
            adom: ADOM name
            psk: Pre-shared key (for PSK authentication)
            certificate: Certificate name (for certificate authentication)
            **kwargs: Additional Phase1 parameters
            
        Returns:
            Created Phase1 interface
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/phase1-interface"
        
        data: dict[str, Any] = {
            "name": name,
            "interface": interface,
            "remote-gw": remote_gw,
        }
        
        if psk:
            data["authmethod"] = "psk"
            data["psksecret"] = psk
        elif certificate:
            data["authmethod"] = "signature"
            data["certificate"] = certificate
        
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def update_ipsec_phase1(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update IPsec Phase1 interface.
        
        Args:
            name: Phase1 interface name
            adom: ADOM name
            **kwargs: Fields to update
            
        Returns:
            Updated Phase1 interface
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/phase1-interface/{name}"
        result = await self.client.update(url, kwargs)
        return result if isinstance(result, dict) else {}

    async def delete_ipsec_phase1(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete IPsec Phase1 interface.
        
        Args:
            name: Phase1 interface name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/phase1-interface/{name}"
        return await self.client.delete(url)

    # =========================================================================
    # IPsec Phase2 Interface Methods
    # =========================================================================

    async def list_ipsec_phase2(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List IPsec Phase2 interfaces in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of IPsec Phase2 interfaces
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/phase2-interface"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_ipsec_phase2(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get IPsec Phase2 interface details.
        
        Args:
            name: Phase2 interface name
            adom: ADOM name
            
        Returns:
            Phase2 interface details
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/phase2-interface/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_ipsec_phase2(
        self,
        name: str,
        phase1name: str,
        adom: str = "root",
        src_subnet: str | None = None,
        dst_subnet: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create IPsec Phase2 interface.
        
        Args:
            name: Phase2 interface name
            phase1name: Associated Phase1 interface name
            adom: ADOM name
            src_subnet: Source subnet (CIDR format, e.g., "192.168.1.0/24")
            dst_subnet: Destination subnet (CIDR format)
            **kwargs: Additional Phase2 parameters
            
        Returns:
            Created Phase2 interface
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/phase2-interface"
        
        data: dict[str, Any] = {
            "name": name,
            "phase1name": phase1name,
        }
        
        if src_subnet:
            data["src-subnet"] = src_subnet
        if dst_subnet:
            data["dst-subnet"] = dst_subnet
        
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def delete_ipsec_phase2(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete IPsec Phase2 interface.
        
        Args:
            name: Phase2 interface name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/phase2-interface/{name}"
        return await self.client.delete(url)

    # =========================================================================
    # SSL-VPN Portal Methods
    # =========================================================================

    async def list_sslvpn_portals(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List SSL-VPN portals in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of SSL-VPN portals
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ssl/web/portal"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_sslvpn_portal(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get SSL-VPN portal details.
        
        Args:
            name: Portal name
            adom: ADOM name
            
        Returns:
            Portal details
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ssl/web/portal/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_sslvpn_portal(
        self,
        name: str,
        adom: str = "root",
        tunnel_mode: bool = True,
        web_mode: bool = True,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create SSL-VPN portal.
        
        Args:
            name: Portal name
            adom: ADOM name
            tunnel_mode: Enable tunnel mode
            web_mode: Enable web mode
            **kwargs: Additional portal parameters
            
        Returns:
            Created portal
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ssl/web/portal"
        
        data: dict[str, Any] = {
            "name": name,
            "tunnel-mode": "enable" if tunnel_mode else "disable",
            "web-mode": "enable" if web_mode else "disable",
        }
        data.update(kwargs)
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def delete_sslvpn_portal(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete SSL-VPN portal.
        
        Args:
            name: Portal name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ssl/web/portal/{name}"
        return await self.client.delete(url)

    # =========================================================================
    # VPN Certificate Methods
    # =========================================================================

    async def list_vpn_certificates_ca(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List VPN Certificate Authorities in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of CA certificates
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/certificate/ca"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_vpn_certificate_ca(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get VPN CA certificate details.
        
        Args:
            name: CA certificate name
            adom: ADOM name
            
        Returns:
            CA certificate details
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/certificate/ca/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def list_vpn_certificates_remote(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List VPN remote certificates in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of remote certificates
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/certificate/remote"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_vpn_certificate_remote(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get VPN remote certificate details.
        
        Args:
            name: Remote certificate name
            adom: ADOM name
            
        Returns:
            Remote certificate details
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/certificate/remote/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # SSL-VPN Host Check Software Methods
    # =========================================================================

    async def list_sslvpn_host_check_software(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List SSL-VPN host check software in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of host check software configurations
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ssl/web/host-check-software"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_sslvpn_host_check_software(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get SSL-VPN host check software details.
        
        Args:
            name: Host check software name
            adom: ADOM name
            
        Returns:
            Host check software details
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ssl/web/host-check-software/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # Phase 23: IPsec Advanced Operations
    # =========================================================================

    async def list_ipsec_concentrators(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List IPsec VPN concentrator configurations.
        
        Concentrators allow a single FortiGate to aggregate multiple
        IPsec tunnels from remote sites.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of IPsec concentrator configs
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/concentrator"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_ipsec_forticlient_templates(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List FortiClient IPsec VPN templates.
        
        Templates define FortiClient VPN connection settings that can be
        distributed to end users for consistent VPN configuration.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of FortiClient IPsec templates
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/forticlient"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def list_ipsec_manualkey_interfaces(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List IPsec manual-key interfaces.
        
        Manual-key IPsec uses pre-configured keys instead of IKE for
        establishing tunnels (less common, used for specific scenarios).
        
        Args:
            adom: ADOM name
            
        Returns:
            List of manual-key IPsec interfaces
        """
        url = f"/pm/config/adom/{adom}/obj/vpn/ipsec/manualkey-interface"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    # =========================================================================
    # Phase 23: VPN Monitoring
    # =========================================================================

    async def get_ipsec_tunnel_status(
        self,
        device: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get IPsec tunnel status for a specific device.
        
        Retrieves real-time status of all IPsec tunnels on a device:
        - Tunnel up/down status
        - Phase 1 and Phase 2 status
        - Peer information
        - Traffic statistics
        
        Args:
            device: Device name
            adom: ADOM name
            
        Returns:
            List of tunnel status entries
        """
        url = f"/dvmdb/adom/{adom}/device/{device}/vd/root/vpn/ipsec/status"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_sslvpn_tunnel_status(
        self,
        device: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get SSL-VPN tunnel status for a specific device.
        
        Retrieves active SSL-VPN connections:
        - Connected users
        - Connection duration
        - Data transferred
        - Client IP addresses
        - Authentication method
        
        Args:
            device: Device name
            adom: ADOM name
            
        Returns:
            List of active SSL-VPN sessions
        """
        url = f"/dvmdb/adom/{adom}/device/{device}/vd/root/vpn/ssl/status"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_vpn_statistics(
        self,
        device: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get VPN statistics for a device.
        
        Retrieves comprehensive VPN statistics:
        - Total tunnels configured
        - Active tunnels
        - Data throughput
        - Packet counts
        - Error statistics
        
        Args:
            device: Device name
            adom: ADOM name
            
        Returns:
            VPN statistics
        """
        url = f"/dvmdb/adom/{adom}/device/{device}/vd/root/vpn/statistics"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

