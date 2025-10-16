"""Policy management API module."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient
from fortimanager_mcp.api.models import FirewallPolicy, PolicyPackage


class PolicyAPI:
    """Policy and policy package management operations."""

    def __init__(self, client: FortiManagerClient) -> None:
        """Initialize policy API.

        Args:
            client: FortiManager client instance
        """
        self.client = client

    # Policy Package Operations
    async def list_packages(
        self,
        adom: str = "root",
        fields: list[str] | None = None,
    ) -> list[PolicyPackage]:
        """List policy packages in ADOM.

        Args:
            adom: ADOM name
            fields: Specific fields to return

        Returns:
            List of policy packages
        """
        url = f"/pm/pkg/adom/{adom}"
        data = await self.client.get(url, fields=fields)
        if not isinstance(data, list):
            data = [data] if data else []

        return [PolicyPackage(**item) for item in data]

    async def get_package(self, package: str, adom: str = "root") -> PolicyPackage:
        """Get specific policy package.

        Args:
            package: Package name
            adom: ADOM name

        Returns:
            Policy package details
        """
        url = f"/pm/pkg/adom/{adom}/{package}"
        data = await self.client.get(url)
        return PolicyPackage(**data)

    async def create_package(
        self,
        name: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> PolicyPackage:
        """Create policy package.

        Args:
            name: Package name
            adom: ADOM name
            **kwargs: Additional package parameters

        Returns:
            Created policy package
        """
        data = {
            "name": name,
            "type": "pkg",
            **kwargs,
        }

        url = f"/pm/pkg/adom/{adom}"
        await self.client.add(url, data=data)
        return await self.get_package(name, adom=adom)

    async def delete_package(self, package: str, adom: str = "root") -> None:
        """Delete policy package.

        Args:
            package: Package name
            adom: ADOM name
        """
        url = f"/pm/pkg/adom/{adom}/{package}"
        await self.client.delete(url)

    # Firewall Policy Operations
    async def list_policies(
        self,
        package: str,
        adom: str = "root",
        fields: list[str] | None = None,
        filter: list[Any] | None = None,
    ) -> list[FirewallPolicy]:
        """List firewall policies in package.

        Args:
            package: Policy package name
            adom: ADOM name
            fields: Specific fields to return
            filter: Filter criteria

        Returns:
            List of firewall policies
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy"
        data = await self.client.get(url, fields=fields, filter=filter)
        if not isinstance(data, list):
            data = [data] if data else []

        return [FirewallPolicy(**item) for item in data]

    async def get_policy(
        self,
        policy_id: int,
        package: str,
        adom: str = "root",
    ) -> FirewallPolicy:
        """Get specific firewall policy.

        Args:
            policy_id: Policy ID
            package: Policy package name
            adom: ADOM name

        Returns:
            Firewall policy details
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy/{policy_id}"
        data = await self.client.get(url)
        return FirewallPolicy(**data)

    async def create_policy(
        self,
        package: str,
        srcintf: list[str],
        dstintf: list[str],
        srcaddr: list[str],
        dstaddr: list[str],
        service: list[str],
        action: str = "accept",
        adom: str = "root",
        name: str | None = None,
        schedule: str = "always",
        **kwargs: Any,
    ) -> FirewallPolicy:
        """Create firewall policy.

        Args:
            package: Policy package name
            srcintf: Source interfaces
            dstintf: Destination interfaces
            srcaddr: Source addresses
            dstaddr: Destination addresses
            service: Services
            action: Action (accept/deny)
            adom: ADOM name
            name: Policy name
            schedule: Schedule name
            **kwargs: Additional policy parameters

        Returns:
            Created firewall policy
        """
        data = {
            "srcintf": srcintf,
            "dstintf": dstintf,
            "srcaddr": srcaddr,
            "dstaddr": dstaddr,
            "service": service,
            "action": action,
            "schedule": schedule,
            "status": "enable",
            **kwargs,
        }

        if name:
            data["name"] = name

        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy"
        result = await self.client.add(url, data=data)

        # Get the policy ID from result
        if isinstance(result, dict) and "policyid" in result:
            policy_id = result["policyid"]
            return await self.get_policy(policy_id, package, adom)

        # If no policy ID in result, list policies and get the last one
        policies = await self.list_policies(package, adom)
        if policies:
            return policies[-1]

        raise ValueError("Failed to get created policy")

    async def update_policy(
        self,
        policy_id: int,
        package: str,
        adom: str = "root",
        **kwargs: Any,
    ) -> FirewallPolicy:
        """Update firewall policy.

        Args:
            policy_id: Policy ID
            package: Policy package name
            adom: ADOM name
            **kwargs: Fields to update

        Returns:
            Updated firewall policy
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy/{policy_id}"
        await self.client.set(url, data=kwargs)
        return await self.get_policy(policy_id, package, adom)

    async def delete_policy(
        self,
        policy_id: int,
        package: str,
        adom: str = "root",
    ) -> None:
        """Delete firewall policy.

        Args:
            policy_id: Policy ID
            package: Policy package name
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy/{policy_id}"
        await self.client.delete(url)

    async def move_policy(
        self,
        policy_id: int,
        package: str,
        target: int,
        option: str = "after",
        adom: str = "root",
    ) -> None:
        """Move/reorder firewall policy.

        Args:
            policy_id: Policy ID to move
            package: Policy package name
            target: Target policy ID
            option: Move option (before/after)
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy/{policy_id}"
        data = {
            "option": option,
            "target": target,
        }
        await self.client.move(url, data=data)

    async def clone_policy(
        self,
        policy_id: int,
        package: str,
        adom: str = "root",
        new_name: str | None = None,
    ) -> FirewallPolicy:
        """Clone an existing firewall policy.

        Args:
            policy_id: Policy ID to clone
            package: Policy package name
            adom: ADOM name
            new_name: Name for cloned policy (optional)

        Returns:
            Cloned firewall policy
        """
        # Get the original policy
        original = await self.get_policy(policy_id, package, adom)
        
        # Create a new policy with same settings
        policy_data = original.model_dump(exclude={"policyid"}, exclude_none=True)
        if new_name:
            policy_data["name"] = new_name
        elif original.name:
            policy_data["name"] = f"{original.name}_copy"
        
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy"
        result = await self.client.add(url, data=policy_data)
        
        # Get the new policy ID
        if isinstance(result, dict) and "policyid" in result:
            return await self.get_policy(result["policyid"], package, adom)
        
        # Fallback: get the last policy
        policies = await self.list_policies(package, adom)
        if policies:
            return policies[-1]
        
        raise ValueError("Failed to get cloned policy")

    # Central SNAT (Source NAT) Policies
    async def list_central_snat_policies(
        self,
        package: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List central SNAT policies.

        Args:
            package: Policy package name
            adom: ADOM name

        Returns:
            List of central SNAT policies
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/central-snat-map"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_central_snat_policy(
        self,
        policy_id: int,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any] | None:
        """Get central SNAT policy details.

        Args:
            policy_id: Policy ID
            package: Policy package name
            adom: ADOM name

        Returns:
            Central SNAT policy details
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/central-snat-map/{policy_id}"
        return await self.client.get(url)

    async def create_central_snat_policy(
        self,
        package: str,
        srcintf: list[str],
        dstintf: list[str],
        orig_addr: list[str],
        nat_ippool: list[str],
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create central SNAT policy.

        Args:
            package: Policy package name
            srcintf: Source interfaces
            dstintf: Destination interfaces
            orig_addr: Original source addresses
            nat_ippool: NAT IP pools
            adom: ADOM name
            **kwargs: Additional policy parameters

        Returns:
            Created policy result
        """
        data = {
            "srcintf": srcintf,
            "dstintf": dstintf,
            "orig-addr": orig_addr,
            "nat-ippool": nat_ippool,
            "nat": "enable",
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/central-snat-map"
        return await self.client.add(url, data=data)

    async def delete_central_snat_policy(
        self,
        policy_id: int,
        package: str,
        adom: str = "root",
    ) -> None:
        """Delete central SNAT policy.

        Args:
            policy_id: Policy ID
            package: Policy package name
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/central-snat-map/{policy_id}"
        await self.client.delete(url)

    # Central DNAT (Destination NAT) Policies
    async def list_central_dnat_policies(
        self,
        package: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List central DNAT policies.

        Args:
            package: Policy package name
            adom: ADOM name

        Returns:
            List of central DNAT policies
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/central-dnat-map"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_central_dnat_policy(
        self,
        policy_id: int,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any] | None:
        """Get central DNAT policy details.

        Args:
            policy_id: Policy ID
            package: Policy package name
            adom: ADOM name

        Returns:
            Central DNAT policy details
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/central-dnat-map/{policy_id}"
        return await self.client.get(url)

    async def create_central_dnat_policy(
        self,
        package: str,
        srcintf: list[str],
        dstintf: list[str],
        orig_addr: list[str],
        dst_addr: list[str],
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create central DNAT policy.

        Args:
            package: Policy package name
            srcintf: Source interfaces
            dstintf: Destination interfaces
            orig_addr: Original destination addresses
            dst_addr: Translated destination addresses
            adom: ADOM name
            **kwargs: Additional policy parameters

        Returns:
            Created policy result
        """
        data = {
            "srcintf": srcintf,
            "dstintf": dstintf,
            "orig-addr": orig_addr,
            "dst-addr": dst_addr,
            "nat": "enable",
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/central-dnat-map"
        return await self.client.add(url, data=data)

    async def delete_central_dnat_policy(
        self,
        policy_id: int,
        package: str,
        adom: str = "root",
    ) -> None:
        """Delete central DNAT policy.

        Args:
            policy_id: Policy ID
            package: Policy package name
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/central-dnat-map/{policy_id}"
        await self.client.delete(url)

    # Policy Package Folder Operations
    async def create_policy_folder(
        self,
        name: str,
        adom: str = "root",
        parent: str = "",
    ) -> dict[str, Any]:
        """Create a policy package folder.

        Args:
            name: Folder name
            adom: ADOM name
            parent: Parent folder path (empty for root level)

        Returns:
            Created folder information
        """
        data = {
            "name": name,
            "type": "folder",
        }
        
        url = f"/pm/pkg/adom/{adom}"
        if parent:
            url = f"{url}/{parent}"
        
        await self.client.add(url, data=data)
        return {"name": name, "parent": parent}

    async def move_package_to_folder(
        self,
        package: str,
        folder: str,
        adom: str = "root",
    ) -> None:
        """Move a policy package to a folder.

        Args:
            package: Package name to move
            folder: Destination folder path
            adom: ADOM name
        """
        # Get package data first
        pkg_url = f"/pm/pkg/adom/{adom}/{package}"
        pkg_data = await self.client.get(pkg_url)
        
        # Update package with new folder location
        pkg_data["folder"] = folder
        await self.client.set(pkg_url, data={"folder": folder})

    async def delete_policy_folder(
        self,
        folder: str,
        adom: str = "root",
    ) -> None:
        """Delete an empty policy package folder.

        Args:
            folder: Folder path to delete
            adom: ADOM name
        """
        url = f"/pm/pkg/adom/{adom}/{folder}"
        await self.client.delete(url)

    # Policy Block Operations
    async def list_policy_blocks(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List policy blocks in ADOM.

        Args:
            adom: ADOM name

        Returns:
            List of policy blocks
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/policy-block"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_policy_block(
        self,
        block_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get policy block details.

        Args:
            block_name: Policy block name
            adom: ADOM name

        Returns:
            Policy block details
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/policy-block/{block_name}"
        return await self.client.get(url)

    async def create_policy_block(
        self,
        name: str,
        adom: str = "root",
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create a policy block.

        Args:
            name: Block name
            adom: ADOM name
            description: Block description

        Returns:
            Created policy block
        """
        data = {"name": name}
        if description:
            data["comments"] = description
        
        url = f"/pm/config/adom/{adom}/obj/firewall/policy-block"
        await self.client.add(url, data=data)
        return await self.get_policy_block(name, adom)

    async def add_policies_to_block(
        self,
        block_name: str,
        policy_ids: list[int],
        package: str,
        adom: str = "root",
    ) -> None:
        """Add policies to a policy block.

        Args:
            block_name: Policy block name
            policy_ids: List of policy IDs to add
            package: Source policy package
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/policy-block/{block_name}/policies"
        data = {
            "pkg": package,
            "policyid": policy_ids,
        }
        await self.client.add(url, data=data)

    async def insert_policy_block(
        self,
        block_name: str,
        package: str,
        target_policy_id: int,
        position: str = "after",
        adom: str = "root",
    ) -> None:
        """Insert a policy block into a package.

        Args:
            block_name: Policy block name
            package: Target policy package
            target_policy_id: Reference policy ID
            position: Insert position (before/after)
            adom: ADOM name
        """
        url = f"/pm/pkg/adom/{adom}/{package}/firewall/policy"
        data = {
            "policyblock": block_name,
            "target": target_policy_id,
            "option": position,
        }
        await self.client.add(url, data=data)

    async def clone_policy_block(
        self,
        block_name: str,
        new_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Clone a policy block.

        Args:
            block_name: Source block name
            new_name: New block name
            adom: ADOM name

        Returns:
            Cloned policy block
        """
        # Get original block
        original = await self.get_policy_block(block_name, adom)
        
        # Create new block with same data
        clone_data = {k: v for k, v in original.items() if k != "name"}
        clone_data["name"] = new_name
        
        url = f"/pm/config/adom/{adom}/obj/firewall/policy-block"
        await self.client.add(url, data=clone_data)
        return await self.get_policy_block(new_name, adom)

    async def delete_policy_block(
        self,
        block_name: str,
        adom: str = "root",
    ) -> None:
        """Delete a policy block.

        Args:
            block_name: Block name to delete
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/obj/firewall/policy-block/{block_name}"
        await self.client.delete(url)

    # Policy Package Status & Operations
    async def get_package_status(
        self,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get policy package installation status.

        Args:
            package: Policy package name
            adom: ADOM name

        Returns:
            Package status information
        """
        url = f"/pm/pkg/adom/{adom}/{package}/status"
        return await self.client.get(url)

    async def get_package_checksum(
        self,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get policy package checksum.

        Args:
            package: Policy package name
            adom: ADOM name

        Returns:
            Package checksum information
        """
        data = {
            "adom": adom,
            "pkg": package,
        }
        return await self.client.execute("/pm/pkg/checksum", data=data)

    async def get_package_changes(
        self,
        package: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get list of changes since last installation.

        Args:
            package: Policy package name
            adom: ADOM name

        Returns:
            List of changes
        """
        url = f"/pm/pkg/adom/{adom}/{package}/changes"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_policy_hitcount(
        self,
        package: str,
        device: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get policy hit count statistics.

        Args:
            package: Policy package name
            device: Device name
            adom: ADOM name

        Returns:
            Hit count statistics
        """
        data = {
            "adom": adom,
            "pkg": package,
            "device": device,
        }
        return await self.client.execute("/pm/policy/hitcount", data=data)

    async def revert_package(
        self,
        package: str,
        revision: int,
        adom: str = "root",
    ) -> None:
        """Revert policy package to previous version.

        Args:
            package: Policy package name
            revision: Revision number to revert to
            adom: ADOM name
        """
        data = {
            "adom": adom,
            "pkg": package,
            "revision": revision,
        }
        await self.client.execute("/pm/pkg/revert", data=data)

    # Advanced Policy Operations
    async def insert_policy_at_position(
        self,
        package: str,
        position: int,
        policy_data: dict[str, Any],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Insert policy at specific position (index).

        Args:
            package: Policy package name
            position: Index position (0-based)
            policy_data: Policy configuration data
            adom: ADOM name

        Returns:
            Created policy information
        """
        policy_data["_position"] = position
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy"
        result = await self.client.add(url, data=policy_data)
        return result

    async def get_nth_policy(
        self,
        package: str,
        index: int,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get policy by index position.

        Args:
            package: Policy package name
            index: Policy index (0-based)
            adom: ADOM name

        Returns:
            Policy information
        """
        policies = await self.list_policies(package, adom)
        if index < len(policies):
            return policies[index].model_dump()
        raise IndexError(f"Policy index {index} out of range")

    async def move_policy_to_section(
        self,
        policy_id: int,
        package: str,
        section: str,
        adom: str = "root",
    ) -> None:
        """Move policy to a different section.

        Args:
            policy_id: Policy ID to move
            package: Policy package name
            section: Target section name
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy/{policy_id}"
        await self.client.set(url, data={"section": section})

    async def create_policy_section(
        self,
        package: str,
        section_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Create a policy section for organization.

        Args:
            package: Policy package name
            section_name: Section name
            adom: ADOM name

        Returns:
            Created section information
        """
        data = {
            "name": section_name,
            "type": "section",
        }
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy"
        return await self.client.add(url, data=data)

    async def import_policy_configuration(
        self,
        package: str,
        config_file_content: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Import policy configuration from file content.

        Args:
            package: Policy package name
            config_file_content: Configuration file content
            adom: ADOM name

        Returns:
            Import result
        """
        data = {
            "adom": adom,
            "pkg": package,
            "config": config_file_content,
        }
        return await self.client.execute("/pm/pkg/import", data=data)

    # =========================================================================
    # Phase 29: Complete Policy Package Management
    # =========================================================================

    async def export_policy_configuration(
        self,
        package: str,
        adom: str = "root",
    ) -> str:
        """Export policy configuration to file format.

        Args:
            package: Policy package name
            adom: ADOM name

        Returns:
            Policy configuration in FortiOS CLI format
        """
        data = {
            "adom": adom,
            "pkg": package,
        }
        result = await self.client.execute("/pm/pkg/export", data=data)
        return result.get("config", "") if isinstance(result, dict) else str(result)

    async def get_policy_usage_statistics(
        self,
        package: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get policy usage statistics showing which rules are actually used.

        Args:
            package: Policy package name
            adom: ADOM name

        Returns:
            List of policy usage statistics
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy/usage"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def consolidate_policies(
        self,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Analyze and consolidate similar policies to reduce rule count.

        Args:
            package: Policy package name
            adom: ADOM name

        Returns:
            Consolidation analysis and recommendations
        """
        data = {
            "adom": adom,
            "pkg": package,
        }
        return await self.client.execute("/pm/pkg/policy/consolidate", data=data)

    async def set_policy_global_label(
        self,
        package: str,
        policy_id: int,
        label: str,
        adom: str = "root",
    ) -> None:
        """Set a global label on a policy for categorization.

        Args:
            package: Policy package name
            policy_id: Policy ID
            label: Label text
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy/{policy_id}"
        await self.client.set(url, data={"global-label": label})

    # =========================================================================
    # Phase 44: Final Policy Operations
    # =========================================================================

    async def get_policy_by_name(
        self,
        package: str,
        policy_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get policy by name instead of ID.
        
        Args:
            package: Package name
            policy_name: Policy name
            adom: ADOM name
            
        Returns:
            Policy details
        """
        # List all policies and find by name
        policies = await self.list_firewall_policies(package=package, adom=adom)
        for policy in policies:
            if policy.get("name") == policy_name:
                return policy
        return {}

    async def duplicate_policy(
        self,
        package: str,
        policy_id: int,
        new_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Duplicate an existing policy with a new name.
        
        Args:
            package: Package name
            policy_id: Source policy ID
            new_name: Name for duplicated policy
            adom: ADOM name
            
        Returns:
            New policy details
        """
        # Get source policy
        source = await self.get_firewall_policy(package=package, policy_id=policy_id, adom=adom)
        
        # Create new policy with same settings but new name
        new_policy = source.copy()
        new_policy["name"] = new_name
        if "policyid" in new_policy:
            del new_policy["policyid"]
        
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy"
        return await self.client.add(url, data=new_policy)

    async def get_policy_references(
        self,
        package: str,
        policy_id: int,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get all objects referenced by a policy.
        
        Args:
            package: Package name
            policy_id: Policy ID
            adom: ADOM name
            
        Returns:
            Referenced objects
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/firewall/policy/{policy_id}/references"
        return await self.client.get(url)

    async def validate_policy_package(
        self,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Validate policy package for errors.
        
        Args:
            package: Package name
            adom: ADOM name
            
        Returns:
            Validation results
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/validate"
        return await self.client.execute(url, {})

    async def analyze_policy_complexity(
        self,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Analyze policy package complexity and provide optimization recommendations.
        
        Args:
            package: Package name
            adom: ADOM name
            
        Returns:
            Complexity analysis and recommendations
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/_data/analysis"
        return await self.client.get(url)

    # =========================================================================
    # Phase 49: Global Policy Packages & Install Variants
    # =========================================================================

    async def list_global_policy_packages(self) -> list[dict[str, Any]]:
        """List global policy packages.
        
        Global policy packages apply across all ADOMs and provide centralized
        policy management for common rules. Used for:
        - Organization-wide security policies
        - Centralized compliance rules
        - Common baseline policies
        - Cross-ADOM policy consistency
        
        Returns:
            List of global policy packages
            
        Note:
            Global packages are defined at the FortiManager level and can be
            inherited by individual ADOM packages.
        """
        url = "/pm/pkg/global"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_global_policy_package(
        self,
        package: str,
    ) -> dict[str, Any]:
        """Get global policy package details.
        
        Retrieves configuration and policies from a global package including:
        - Package metadata
        - Global policy rules
        - Inheritance settings
        - ADOM assignments
        
        Args:
            package: Global package name
            
        Returns:
            Global package details including policies
        """
        url = f"/pm/pkg/global/{package}"
        return await self.client.get(url)

    async def install_to_device_db_only(
        self,
        package: str,
        scope: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Install policy package to device database only (no push to devices).
        
        Installs the policy package to the FortiManager device database without
        actually pushing configuration to managed FortiGates. Useful for:
        - Staging policy changes
        - Pre-validation before production push
        - Database synchronization
        - Testing installation process
        
        The policies remain in FortiManager DB until a full install is performed.
        
        Args:
            package: Policy package name
            scope: List of target devices/VDOMs [{"name": "device", "vdom": "root"}]
            adom: ADOM name
            
        Returns:
            Installation task details
            
        Example:
            install_to_device_db_only(
                package="default",
                scope=[{"name": "FGT-01", "vdom": "root"}],
                adom="root"
            )
        """
        data = {
            "adom": adom,
            "pkg": package,
            "scope": scope,
            "flags": ["dev_rev_comments", "copy_assigned_pkg"],
        }
        return await self.client.execute("/securityconsole/install/package", data)

    async def install_offline_package(
        self,
        package: str,
        scope: list[dict[str, str]],
        adom: str = "root",
    ) -> dict[str, Any]:
        """Install policy package for offline devices.
        
        Prepares and stages policy installation for devices that are currently
        offline or unreachable. When devices reconnect, they will automatically
        receive the staged configuration. Used for:
        - Remote/branch offices with intermittent connectivity
        - Scheduled maintenance windows
        - Bulk deployments to disconnected devices
        - Disaster recovery scenarios
        
        Args:
            package: Policy package name
            scope: List of target devices/VDOMs
            adom: ADOM name
            
        Returns:
            Installation task details
            
        Note:
            The installation will be queued and applied when the device
            reconnects to FortiManager.
        """
        data = {
            "adom": adom,
            "pkg": package,
            "scope": scope,
            "flags": ["copy_assigned_pkg", "offline"],
        }
        return await self.client.execute("/securityconsole/install/package", data)

