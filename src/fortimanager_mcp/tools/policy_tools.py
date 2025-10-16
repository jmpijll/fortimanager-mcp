"""MCP tools for policy management operations."""

import logging
from typing import Any

from fortimanager_mcp.api.installation import InstallationAPI
from fortimanager_mcp.api.policies import PolicyAPI
from fortimanager_mcp.server import get_fmg_client, mcp

logger = logging.getLogger(__name__)


def _get_policy_api() -> PolicyAPI:
    """Get PolicyAPI instance."""
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return PolicyAPI(client)


def _get_installation_api() -> InstallationAPI:
    """Get InstallationAPI instance."""
    client = get_fmg_client()
    if not client:
        raise RuntimeError("FortiManager client not initialized")
    return InstallationAPI(client)


@mcp.tool()
async def list_policy_packages(adom: str = "root") -> dict[str, Any]:
    """List all policy packages in an ADOM.

    Policy packages contain firewall policies and are assigned to devices.
    Each device typically has one policy package assigned.

    Args:
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of policy packages

    Example:
        result = list_policy_packages(adom="root")
    """
    try:
        api = _get_policy_api()
        packages = await api.list_packages(adom=adom)

        return {
            "status": "success",
            "count": len(packages),
            "packages": [
                {
                    "name": pkg.name,
                    "type": pkg.type,
                    "assigned_devices": pkg.scope_member,
                }
                for pkg in packages
            ],
        }
    except Exception as e:
        logger.error(f"Error listing policy packages in ADOM {adom}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_firewall_policies(
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """List firewall policies in a policy package.

    Retrieves all firewall policy rules from a specified policy package.
    Policies define traffic flow rules between interfaces and addresses.

    Args:
        package: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of firewall policies

    Example:
        result = list_firewall_policies(package="default", adom="root")
    """
    try:
        api = _get_policy_api()
        policies = await api.list_policies(package=package, adom=adom)

        return {
            "status": "success",
            "count": len(policies),
            "policies": [
                {
                    "policy_id": pol.policyid,
                    "name": pol.name,
                    "source_interfaces": pol.srcintf,
                    "destination_interfaces": pol.dstintf,
                    "source_addresses": pol.srcaddr,
                    "destination_addresses": pol.dstaddr,
                    "services": pol.service,
                    "action": pol.action,
                    "status": pol.status,
                    "comments": pol.comments,
                }
                for pol in policies
            ],
        }
    except Exception as e:
        logger.error(f"Error listing policies in package {package}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_firewall_policy(
    policy_id: int,
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get detailed information about a specific firewall policy.

    Retrieves complete details of a single firewall policy rule.

    Args:
        policy_id: Policy ID
        package: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with policy details

    Example:
        result = get_firewall_policy(policy_id=1, package="default", adom="root")
    """
    try:
        api = _get_policy_api()
        policy = await api.get_policy(policy_id=policy_id, package=package, adom=adom)

        return {
            "status": "success",
            "policy": {
                "policy_id": policy.policyid,
                "name": policy.name,
                "source_interfaces": policy.srcintf,
                "destination_interfaces": policy.dstintf,
                "source_addresses": policy.srcaddr,
                "destination_addresses": policy.dstaddr,
                "services": policy.service,
                "action": policy.action,
                "status": policy.status,
                "schedule": policy.schedule,
                "comments": policy.comments,
                "nat": policy.nat,
                "log_traffic": policy.logtraffic,
            },
        }
    except Exception as e:
        logger.error(f"Error getting policy {policy_id}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_firewall_policy(
    package: str,
    source_interfaces: list[str],
    destination_interfaces: list[str],
    source_addresses: list[str],
    destination_addresses: list[str],
    services: list[str],
    action: str = "accept",
    adom: str = "root",
    name: str | None = None,
    comments: str | None = None,
) -> dict[str, Any]:
    """Create a new firewall policy rule.

    Creates a new policy rule in the specified policy package.
    The policy controls traffic flow based on interfaces, addresses, and services.

    Args:
        package: Policy package name
        source_interfaces: List of source interface names (e.g., ["port1", "port2"])
        destination_interfaces: List of destination interface names
        source_addresses: List of source address object names (e.g., ["internal_net"])
        destination_addresses: List of destination address object names
        services: List of service object names (e.g., ["HTTP", "HTTPS"])
        action: Policy action - "accept" or "deny" (default: "accept")
        adom: ADOM name (default: "root")
        name: Optional policy name
        comments: Optional policy description

    Returns:
        Dictionary with created policy details

    Example:
        result = create_firewall_policy(
            package="default",
            source_interfaces=["port1"],
            destination_interfaces=["port2"],
            source_addresses=["internal_network"],
            destination_addresses=["all"],
            services=["HTTP", "HTTPS"],
            action="accept",
            adom="root",
            name="Allow_Web_Traffic",
            comments="Allow HTTP/HTTPS from internal to internet"
        )
    """
    try:
        api = _get_policy_api()
        policy = await api.create_policy(
            package=package,
            srcintf=source_interfaces,
            dstintf=destination_interfaces,
            srcaddr=source_addresses,
            dstaddr=destination_addresses,
            service=services,
            action=action,
            adom=adom,
            name=name,
            comments=comments,
        )

        return {
            "status": "success",
            "message": "Policy created successfully",
            "policy": {
                "policy_id": policy.policyid,
                "name": policy.name,
                "action": policy.action,
                "status": policy.status,
            },
        }
    except Exception as e:
        logger.error(f"Error creating policy: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_firewall_policy(
    policy_id: int,
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a firewall policy rule.

    Removes a policy from the specified policy package.

    Args:
        policy_id: Policy ID to delete
        package: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with deletion status

    Example:
        result = delete_firewall_policy(policy_id=10, package="default", adom="root")
    """
    try:
        api = _get_policy_api()
        await api.delete_policy(policy_id=policy_id, package=package, adom=adom)

        return {
            "status": "success",
            "message": f"Policy {policy_id} deleted successfully",
        }
    except Exception as e:
        logger.error(f"Error deleting policy {policy_id}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def install_policy_package(
    package: str,
    device: str,
    adom: str = "root",
    vdom: str = "root",
) -> dict[str, Any]:
    """Install policy package to a device.

    Pushes both pending device settings AND pending security settings
    (objects and policies) to the specified device.
    Returns a task ID for monitoring the installation progress.

    Args:
        package: Policy package name
        device: Device name to install to
        adom: ADOM name (default: "root")
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with installation task information

    Example:
        result = install_policy_package(
            package="default",
            device="FGT-Branch-01",
            adom="root",
            vdom="root"
        )
    """
    try:
        api = _get_installation_api()
        result = await api.install_policy_package(
            package=package,
            device=device,
            adom=adom,
            vdom=vdom,
        )

        task_id = result.get("task")
        return {
            "status": "success",
            "message": f"Policy package installation initiated for {device}",
            "task_id": task_id,
            "note": "Use get_task_status tool to monitor installation progress",
        }
    except Exception as e:
        logger.error(f"Error installing package {package} to {device}: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Advanced Policy Features
# ============================================================================

@mcp.tool()
async def move_firewall_policy(
    policy_id: int,
    target_policy_id: int,
    package: str,
    position: str = "after",
    adom: str = "root",
) -> dict[str, Any]:
    """Move/reorder a firewall policy relative to another policy.

    Changes the order of policies in a policy package. Policies are evaluated
    top-to-bottom, so order is critical for traffic matching.

    Args:
        policy_id: ID of the policy to move
        target_policy_id: ID of the reference policy
        package: Policy package name
        position: Position relative to target ("before" or "after")
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with move operation result

    Example:
        # Move policy 42 to after policy 10
        result = move_firewall_policy(
            policy_id=42,
            target_policy_id=10,
            package="default",
            position="after"
        )
    """
    try:
        api = _get_policy_api()
        await api.move_policy(
            policy_id=policy_id,
            package=package,
            target=target_policy_id,
            option=position,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Policy {policy_id} moved {position} policy {target_policy_id}",
        }
    except Exception as e:
        logger.error(f"Error moving policy {policy_id}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def clone_firewall_policy(
    policy_id: int,
    package: str,
    new_name: str | None = None,
    adom: str = "root",
) -> dict[str, Any]:
    """Clone an existing firewall policy.

    Creates a copy of an existing policy with all its settings. Useful for
    creating similar policies without manual re-entry.

    Args:
        policy_id: ID of the policy to clone
        package: Policy package name
        new_name: Name for the cloned policy (optional, defaults to "original_copy")
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with cloned policy details

    Example:
        result = clone_firewall_policy(
            policy_id=42,
            package="default",
            new_name="Production_to_DMZ_v2"
        )
    """
    try:
        api = _get_policy_api()
        cloned = await api.clone_policy(
            policy_id=policy_id,
            package=package,
            adom=adom,
            new_name=new_name,
        )
        return {
            "status": "success",
            "message": f"Policy cloned successfully",
            "cloned_policy": {
                "policy_id": cloned.policyid,
                "name": cloned.name,
                "source_interfaces": cloned.srcintf,
                "destination_interfaces": cloned.dstintf,
                "action": cloned.action,
            },
        }
    except Exception as e:
        logger.error(f"Error cloning policy {policy_id}: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Central NAT Policies
# ============================================================================

@mcp.tool()
async def list_central_snat_policies(
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """List central source NAT (SNAT) policies.

    Central SNAT policies translate source IP addresses for outbound traffic.
    Commonly used for internet access from private networks.

    Args:
        package: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of central SNAT policies

    Example:
        result = list_central_snat_policies(package="default")
    """
    try:
        api = _get_policy_api()
        policies = await api.list_central_snat_policies(package=package, adom=adom)
        return {
            "status": "success",
            "count": len(policies),
            "snat_policies": policies,
        }
    except Exception as e:
        logger.error(f"Error listing central SNAT policies: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_central_snat_policy(
    policy_id: int,
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get central SNAT policy details.

    Args:
        policy_id: Policy ID
        package: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with SNAT policy details
    """
    try:
        api = _get_policy_api()
        policy = await api.get_central_snat_policy(
            policy_id=policy_id,
            package=package,
            adom=adom,
        )
        return {"status": "success", "snat_policy": policy}
    except Exception as e:
        logger.error(f"Error getting central SNAT policy {policy_id}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_central_snat_policy(
    package: str,
    source_interfaces: list[str],
    destination_interfaces: list[str],
    original_addresses: list[str],
    nat_ip_pools: list[str],
    adom: str = "root",
) -> dict[str, Any]:
    """Create a central source NAT policy.

    Creates a policy to translate source IP addresses using NAT IP pools.

    Args:
        package: Policy package name
        source_interfaces: Source interface names
        destination_interfaces: Destination interface names
        original_addresses: Original source address objects
        nat_ip_pools: NAT IP pool objects for translation
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with creation result

    Example:
        result = create_central_snat_policy(
            package="default",
            source_interfaces=["internal"],
            destination_interfaces=["wan1"],
            original_addresses=["LAN_Subnet"],
            nat_ip_pools=["NAT_Pool_1"]
        )
    """
    try:
        api = _get_policy_api()
        result = await api.create_central_snat_policy(
            package=package,
            srcintf=source_interfaces,
            dstintf=destination_interfaces,
            orig_addr=original_addresses,
            nat_ippool=nat_ip_pools,
            adom=adom,
        )
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error creating central SNAT policy: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_central_snat_policy(
    policy_id: int,
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a central SNAT policy.

    Args:
        policy_id: Policy ID
        package: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_policy_api()
        await api.delete_central_snat_policy(
            policy_id=policy_id,
            package=package,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Central SNAT policy {policy_id} deleted",
        }
    except Exception as e:
        logger.error(f"Error deleting central SNAT policy {policy_id}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_central_dnat_policies(
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """List central destination NAT (DNAT) policies.

    Central DNAT policies translate destination IP addresses for inbound traffic.
    Commonly used for port forwarding and publishing internal servers.

    Args:
        package: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of central DNAT policies

    Example:
        result = list_central_dnat_policies(package="default")
    """
    try:
        api = _get_policy_api()
        policies = await api.list_central_dnat_policies(package=package, adom=adom)
        return {
            "status": "success",
            "count": len(policies),
            "dnat_policies": policies,
        }
    except Exception as e:
        logger.error(f"Error listing central DNAT policies: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_central_dnat_policy(
    policy_id: int,
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get central DNAT policy details.

    Args:
        policy_id: Policy ID
        package: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with DNAT policy details
    """
    try:
        api = _get_policy_api()
        policy = await api.get_central_dnat_policy(
            policy_id=policy_id,
            package=package,
            adom=adom,
        )
        return {"status": "success", "dnat_policy": policy}
    except Exception as e:
        logger.error(f"Error getting central DNAT policy {policy_id}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_central_dnat_policy(
    package: str,
    source_interfaces: list[str],
    destination_interfaces: list[str],
    original_addresses: list[str],
    translated_addresses: list[str],
    adom: str = "root",
) -> dict[str, Any]:
    """Create a central destination NAT policy.

    Creates a policy to translate destination IP addresses.

    Args:
        package: Policy package name
        source_interfaces: Source interface names
        destination_interfaces: Destination interface names
        original_addresses: Original destination address objects
        translated_addresses: Translated destination address objects
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with creation result

    Example:
        result = create_central_dnat_policy(
            package="default",
            source_interfaces=["wan1"],
            destination_interfaces=["dmz"],
            original_addresses=["Public_IP"],
            translated_addresses=["Web_Server"]
        )
    """
    try:
        api = _get_policy_api()
        result = await api.create_central_dnat_policy(
            package=package,
            srcintf=source_interfaces,
            dstintf=destination_interfaces,
            orig_addr=original_addresses,
            dst_addr=translated_addresses,
            adom=adom,
        )
        return {"status": "success", "result": result}
    except Exception as e:
        logger.error(f"Error creating central DNAT policy: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_central_dnat_policy(
    policy_id: int,
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a central DNAT policy.

    Args:
        policy_id: Policy ID
        package: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with deletion result
    """
    try:
        api = _get_policy_api()
        await api.delete_central_dnat_policy(
            policy_id=policy_id,
            package=package,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Central DNAT policy {policy_id} deleted",
        }
    except Exception as e:
        logger.error(f"Error deleting central DNAT policy {policy_id}: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Policy Package Folder Management
# ============================================================================

@mcp.tool()
async def create_policy_folder(
    folder_name: str,
    adom: str = "root",
    parent_folder: str = "",
) -> dict[str, Any]:
    """Create a folder to organize policy packages.

    Policy package folders help organize packages hierarchically.
    Folders can be nested for better organization.

    Args:
        folder_name: Name for the new folder
        adom: ADOM name (default: "root")
        parent_folder: Parent folder path (empty for root level)

    Returns:
        Dictionary with folder creation result

    Example:
        # Create root-level folder
        result = create_policy_folder(
            folder_name="Branch_Offices",
            adom="root"
        )

        # Create nested folder
        result = create_policy_folder(
            folder_name="US_West",
            parent_folder="Branch_Offices",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        folder = await api.create_policy_folder(
            name=folder_name,
            adom=adom,
            parent=parent_folder,
        )
        return {
            "status": "success",
            "message": f"Policy folder '{folder_name}' created",
            "folder": folder,
        }
    except Exception as e:
        logger.error(f"Error creating policy folder {folder_name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def move_policy_package_to_folder(
    package_name: str,
    folder_path: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Move a policy package into a folder.

    Organizes policy packages by moving them into folder hierarchies.

    Args:
        package_name: Policy package name to move
        folder_path: Destination folder path
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with move operation result

    Example:
        result = move_policy_package_to_folder(
            package_name="Branch_01_Policy",
            folder_path="Branch_Offices/US_West",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        await api.move_package_to_folder(
            package=package_name,
            folder=folder_path,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Package '{package_name}' moved to folder '{folder_path}'",
        }
    except Exception as e:
        logger.error(f"Error moving package {package_name} to folder {folder_path}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_policy_folder(
    folder_path: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete an empty policy package folder.

    Removes a folder from the policy package hierarchy.
    The folder must be empty (no packages or subfolders).

    Args:
        folder_path: Folder path to delete
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with deletion result

    Example:
        result = delete_policy_folder(
            folder_path="Branch_Offices/Unused",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        await api.delete_policy_folder(
            folder=folder_path,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Policy folder '{folder_path}' deleted",
        }
    except Exception as e:
        logger.error(f"Error deleting policy folder {folder_path}: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Policy Blocks
# ============================================================================

@mcp.tool()
async def list_policy_blocks(
    adom: str = "root",
) -> dict[str, Any]:
    """List all policy blocks in an ADOM.

    Policy blocks are reusable groups of policies that can be inserted
    into multiple policy packages.

    Args:
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of policy blocks

    Example:
        result = list_policy_blocks(adom="root")
    """
    try:
        api = _get_policy_api()
        blocks = await api.list_policy_blocks(adom=adom)
        return {
            "status": "success",
            "count": len(blocks),
            "policy_blocks": blocks,
        }
    except Exception as e:
        logger.error(f"Error listing policy blocks: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_policy_block(
    block_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get details of a specific policy block.

    Args:
        block_name: Policy block name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with policy block details

    Example:
        result = get_policy_block(
            block_name="Common_Security_Rules",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        block = await api.get_policy_block(
            block_name=block_name,
            adom=adom,
        )
        return {
            "status": "success",
            "policy_block": block,
        }
    except Exception as e:
        logger.error(f"Error getting policy block {block_name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_policy_block(
    block_name: str,
    adom: str = "root",
    description: str | None = None,
) -> dict[str, Any]:
    """Create a new policy block.

    Policy blocks are reusable containers for policies that can be
    inserted into multiple policy packages, ensuring consistency.

    Args:
        block_name: Name for the new policy block
        adom: ADOM name (default: "root")
        description: Optional description of the policy block

    Returns:
        Dictionary with created policy block details

    Example:
        result = create_policy_block(
            block_name="Common_Security_Rules",
            description="Standard security policies for all branches",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        block = await api.create_policy_block(
            name=block_name,
            adom=adom,
            description=description,
        )
        return {
            "status": "success",
            "message": f"Policy block '{block_name}' created",
            "policy_block": block,
        }
    except Exception as e:
        logger.error(f"Error creating policy block {block_name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def add_policies_to_block(
    block_name: str,
    policy_ids: list[int],
    source_package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Add policies to a policy block.

    Copies policies from a package into a policy block for reuse.

    Args:
        block_name: Policy block name
        policy_ids: List of policy IDs to add to the block
        source_package: Source policy package containing the policies
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with operation result

    Example:
        result = add_policies_to_block(
            block_name="Common_Security_Rules",
            policy_ids=[1, 2, 3, 5],
            source_package="default",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        await api.add_policies_to_block(
            block_name=block_name,
            policy_ids=policy_ids,
            package=source_package,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Added {len(policy_ids)} policies to block '{block_name}'",
        }
    except Exception as e:
        logger.error(f"Error adding policies to block {block_name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def insert_policy_block(
    block_name: str,
    target_package: str,
    reference_policy_id: int,
    position: str = "after",
    adom: str = "root",
) -> dict[str, Any]:
    """Insert a policy block into a policy package.

    Inserts all policies from a block into a package at a specific position.
    This allows reusing common policy sets across multiple packages.

    Args:
        block_name: Policy block name to insert
        target_package: Target policy package
        reference_policy_id: Reference policy ID for insertion point
        position: Insert position relative to reference ("before" or "after")
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with insertion result

    Example:
        result = insert_policy_block(
            block_name="Common_Security_Rules",
            target_package="Branch_01_Policy",
            reference_policy_id=10,
            position="after",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        await api.insert_policy_block(
            block_name=block_name,
            package=target_package,
            target_policy_id=reference_policy_id,
            position=position,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Policy block '{block_name}' inserted into package '{target_package}'",
        }
    except Exception as e:
        logger.error(f"Error inserting policy block {block_name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def clone_policy_block(
    source_block_name: str,
    new_block_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Clone an existing policy block.

    Creates a copy of a policy block with all its policies.

    Args:
        source_block_name: Name of the block to clone
        new_block_name: Name for the cloned block
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with cloned policy block details

    Example:
        result = clone_policy_block(
            source_block_name="Common_Security_Rules",
            new_block_name="Common_Security_Rules_v2",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        cloned = await api.clone_policy_block(
            block_name=source_block_name,
            new_name=new_block_name,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Policy block cloned as '{new_block_name}'",
            "policy_block": cloned,
        }
    except Exception as e:
        logger.error(f"Error cloning policy block {source_block_name}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def delete_policy_block(
    block_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Delete a policy block.

    Removes a policy block from the ADOM.
    The block must not be in use by any policy packages.

    Args:
        block_name: Policy block name to delete
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with deletion result

    Example:
        result = delete_policy_block(
            block_name="Obsolete_Rules",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        await api.delete_policy_block(
            block_name=block_name,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Policy block '{block_name}' deleted",
        }
    except Exception as e:
        logger.error(f"Error deleting policy block {block_name}: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Scheduled Policy Installations
# ============================================================================

@mcp.tool()
async def schedule_policy_install(
    package_name: str,
    device_name: str,
    schedule_time: str,
    adom: str = "root",
    vdom: str = "root",
) -> dict[str, Any]:
    """Schedule a policy package installation for a future time.

    Allows scheduling policy installations during maintenance windows
    or off-peak hours.

    Args:
        package_name: Policy package name
        device_name: Device name
        schedule_time: Scheduled time (format: "YYYY-MM-DD HH:MM:SS")
        adom: ADOM name (default: "root")
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with scheduled installation information

    Example:
        result = schedule_policy_install(
            package_name="default",
            device_name="FGT-Branch-01",
            schedule_time="2025-10-17 02:00:00",
            adom="root"
        )
    """
    try:
        api = _get_installation_api()
        result = await api.schedule_policy_install(
            package=package_name,
            device=device_name,
            schedule_time=schedule_time,
            adom=adom,
            vdom=vdom,
        )
        return {
            "status": "success",
            "message": f"Policy install scheduled for {schedule_time}",
            "schedule_info": result,
        }
    except Exception as e:
        logger.error(f"Error scheduling policy install: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def list_scheduled_installs(
    adom: str = "root",
) -> dict[str, Any]:
    """List all scheduled policy package installations.

    Shows pending scheduled installations across the ADOM.

    Args:
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of scheduled installations

    Example:
        result = list_scheduled_installs(adom="root")
    """
    try:
        api = _get_installation_api()
        schedules = await api.list_scheduled_installs(adom=adom)
        return {
            "status": "success",
            "count": len(schedules),
            "scheduled_installs": schedules,
        }
    except Exception as e:
        logger.error(f"Error listing scheduled installs: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def cancel_scheduled_install(
    schedule_id: int,
    adom: str = "root",
) -> dict[str, Any]:
    """Cancel a scheduled policy package installation.

    Removes a pending scheduled installation.

    Args:
        schedule_id: Scheduled installation ID
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with cancellation result

    Example:
        result = cancel_scheduled_install(
            schedule_id=12345,
            adom="root"
        )
    """
    try:
        api = _get_installation_api()
        await api.cancel_scheduled_install(
            schedule_id=schedule_id,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Scheduled install {schedule_id} cancelled",
        }
    except Exception as e:
        logger.error(f"Error cancelling scheduled install {schedule_id}: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Install Preview Operations
# ============================================================================

@mcp.tool()
async def preview_policy_install_single(
    package_name: str,
    device_name: str,
    adom: str = "root",
    vdom: str = "root",
) -> dict[str, Any]:
    """Preview policy package installation for a single device (dry run).

    Shows what changes would be made without actually installing.
    Useful for verifying changes before deployment.

    Args:
        package_name: Policy package name
        device_name: Device name
        adom: ADOM name (default: "root")
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with preview information

    Example:
        result = preview_policy_install_single(
            package_name="default",
            device_name="FGT-Branch-01",
            adom="root"
        )
    """
    try:
        api = _get_installation_api()
        preview = await api.check_install_preview(
            package=package_name,
            device=device_name,
            adom=adom,
            vdom=vdom,
        )
        return {
            "status": "success",
            "preview": preview,
        }
    except Exception as e:
        logger.error(f"Error previewing install: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def preview_policy_install_multiple(
    package_name: str,
    devices: list[dict[str, str]],
    adom: str = "root",
) -> dict[str, Any]:
    """Preview policy package installation for multiple devices.

    Shows what changes would be made across multiple devices.

    Args:
        package_name: Policy package name
        devices: List of devices [{"name": "dev1", "vdom": "root"}, ...]
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with preview information for all devices

    Example:
        result = preview_policy_install_multiple(
            package_name="default",
            devices=[
                {"name": "FGT-Branch-01", "vdom": "root"},
                {"name": "FGT-Branch-02", "vdom": "root"}
            ],
            adom="root"
        )
    """
    try:
        api = _get_installation_api()
        preview = await api.preview_install_multiple_devices(
            package=package_name,
            devices=devices,
            adom=adom,
        )
        return {
            "status": "success",
            "preview": preview,
        }
    except Exception as e:
        logger.error(f"Error previewing multi-device install: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def preview_partial_install(
    package_name: str,
    device_name: str,
    policy_ids: list[int],
    adom: str = "root",
    vdom: str = "root",
) -> dict[str, Any]:
    """Preview partial policy installation (specific policies only).

    Shows what changes would be made when installing only specific policies.

    Args:
        package_name: Policy package name
        device_name: Device name
        policy_ids: List of policy IDs to preview
        adom: ADOM name (default: "root")
        vdom: VDOM name (default: "root")

    Returns:
        Dictionary with preview information

    Example:
        result = preview_partial_install(
            package_name="default",
            device_name="FGT-Branch-01",
            policy_ids=[1, 2, 5, 10],
            adom="root"
        )
    """
    try:
        api = _get_installation_api()
        preview = await api.preview_partial_install(
            package=package_name,
            device=device_name,
            policy_ids=policy_ids,
            adom=adom,
            vdom=vdom,
        )
        return {
            "status": "success",
            "preview": preview,
        }
    except Exception as e:
        logger.error(f"Error previewing partial install: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Policy Package Status & Operations
# ============================================================================

@mcp.tool()
async def get_policy_package_status(
    package_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get policy package installation and sync status.

    Shows the current status of a policy package including
    which devices it's installed on and sync state.

    Args:
        package_name: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with package status information

    Example:
        result = get_policy_package_status(
            package_name="default",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        status = await api.get_package_status(
            package=package_name,
            adom=adom,
        )
        return {
            "status": "success",
            "package_status": status,
        }
    except Exception as e:
        logger.error(f"Error getting package status: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_policy_package_checksum(
    package_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get policy package checksum for verification.

    Returns a checksum that can be used to verify package integrity
    and detect changes.

    Args:
        package_name: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with package checksum

    Example:
        result = get_policy_package_checksum(
            package_name="default",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        checksum = await api.get_package_checksum(
            package=package_name,
            adom=adom,
        )
        return {
            "status": "success",
            "checksum": checksum,
        }
    except Exception as e:
        logger.error(f"Error getting package checksum: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_policy_package_changes(
    package_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get list of changes since last installation.

    Shows pending changes that haven't been installed yet.

    Args:
        package_name: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with list of changes

    Example:
        result = get_policy_package_changes(
            package_name="default",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        changes = await api.get_package_changes(
            package=package_name,
            adom=adom,
        )
        return {
            "status": "success",
            "count": len(changes),
            "changes": changes,
        }
    except Exception as e:
        logger.error(f"Error getting package changes: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_policy_hitcount(
    package_name: str,
    device_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get policy hit count statistics from a device.

    Shows how many times each policy has been matched/hit.
    Useful for optimizing policy order and identifying unused policies.

    Args:
        package_name: Policy package name
        device_name: Device name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with hit count statistics

    Example:
        result = get_policy_hitcount(
            package_name="default",
            device_name="FGT-Branch-01",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        hitcount = await api.get_policy_hitcount(
            package=package_name,
            device=device_name,
            adom=adom,
        )
        return {
            "status": "success",
            "hitcount": hitcount,
        }
    except Exception as e:
        logger.error(f"Error getting policy hitcount: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def revert_policy_package(
    package_name: str,
    revision_number: int,
    adom: str = "root",
) -> dict[str, Any]:
    """Revert policy package to a previous version.

    Rolls back a policy package to a specific revision.
    Use list_package_revisions to find available revisions.

    Args:
        package_name: Policy package name
        revision_number: Revision number to revert to
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with revert result

    Example:
        result = revert_policy_package(
            package_name="default",
            revision_number=42,
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        await api.revert_package(
            package=package_name,
            revision=revision_number,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Package '{package_name}' reverted to revision {revision_number}",
        }
    except Exception as e:
        logger.error(f"Error reverting package: {e}")
        return {"status": "error", "message": str(e)}


# ============================================================================
# Advanced Policy Operations
# ============================================================================

@mcp.tool()
async def insert_policy_at_position(
    package_name: str,
    position: int,
    source_interfaces: list[str],
    destination_interfaces: list[str],
    source_addresses: list[str],
    destination_addresses: list[str],
    services: list[str],
    action: str = "accept",
    adom: str = "root",
    policy_name: str | None = None,
) -> dict[str, Any]:
    """Insert a firewall policy at a specific position (index).

    Creates a policy at an exact position in the policy list,
    pushing existing policies down.

    Args:
        package_name: Policy package name
        position: Index position (0-based)
        source_interfaces: Source interface names
        destination_interfaces: Destination interface names
        source_addresses: Source address object names
        destination_addresses: Destination address object names
        services: Service object names
        action: Policy action ("accept" or "deny")
        adom: ADOM name (default: "root")
        policy_name: Optional policy name

    Returns:
        Dictionary with created policy information

    Example:
        result = insert_policy_at_position(
            package_name="default",
            position=0,  # Insert at top
            source_interfaces=["port1"],
            destination_interfaces=["port2"],
            source_addresses=["internal_net"],
            destination_addresses=["all"],
            services=["HTTP", "HTTPS"],
            action="accept",
            policy_name="Web_Access_Priority"
        )
    """
    try:
        api = _get_policy_api()
        policy_data = {
            "name": policy_name,
            "srcintf": source_interfaces,
            "dstintf": destination_interfaces,
            "srcaddr": source_addresses,
            "dstaddr": destination_addresses,
            "service": services,
            "action": action,
            "status": "enable",
        }
        
        result = await api.insert_policy_at_position(
            package=package_name,
            position=position,
            policy_data=policy_data,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Policy inserted at position {position}",
            "policy": result,
        }
    except Exception as e:
        logger.error(f"Error inserting policy at position {position}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_nth_policy(
    package_name: str,
    index: int,
    adom: str = "root",
) -> dict[str, Any]:
    """Get firewall policy by index position.

    Retrieves the policy at a specific position in the policy list.

    Args:
        package_name: Policy package name
        index: Policy index (0-based)
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with policy information

    Example:
        # Get the first policy (top of list)
        result = get_nth_policy(
            package_name="default",
            index=0,
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        policy = await api.get_nth_policy(
            package=package_name,
            index=index,
            adom=adom,
        )
        return {
            "status": "success",
            "policy": policy,
        }
    except IndexError as e:
        logger.error(f"Policy index {index} out of range: {e}")
        return {"status": "error", "message": str(e)}
    except Exception as e:
        logger.error(f"Error getting policy at index {index}: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def move_policy_to_section(
    policy_id: int,
    package_name: str,
    section_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Move a policy to a different section.

    Organizes policies by moving them between named sections.

    Args:
        policy_id: Policy ID to move
        package_name: Policy package name
        section_name: Target section name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with move result

    Example:
        result = move_policy_to_section(
            policy_id=42,
            package_name="default",
            section_name="DMZ_Rules",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        await api.move_policy_to_section(
            policy_id=policy_id,
            package=package_name,
            section=section_name,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Policy {policy_id} moved to section '{section_name}'",
        }
    except Exception as e:
        logger.error(f"Error moving policy to section: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def create_policy_section(
    package_name: str,
    section_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Create a named section for organizing policies.

    Sections help organize policies into logical groups
    for better management and readability.

    Args:
        package_name: Policy package name
        section_name: Name for the new section
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with created section information

    Example:
        result = create_policy_section(
            package_name="default",
            section_name="DMZ_Rules",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        section = await api.create_policy_section(
            package=package_name,
            section_name=section_name,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Policy section '{section_name}' created",
            "section": section,
        }
    except Exception as e:
        logger.error(f"Error creating policy section: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def import_policy_configuration(
    package_name: str,
    config_content: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Import policy configuration from file content.

    Imports policies from a FortiGate configuration file.
    Useful for migrating policies or bulk imports.

    Args:
        package_name: Policy package name
        config_content: Configuration file content (FortiGate format)
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with import result

    Example:
        config = '''
        config firewall policy
            edit 1
                set name "Allow_HTTP"
                set srcintf "port1"
                set dstintf "port2"
                ...
            next
        end
        '''
        result = import_policy_configuration(
            package_name="default",
            config_content=config,
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        result = await api.import_policy_configuration(
            package=package_name,
            config_file_content=config_content,
            adom=adom,
        )
        return {
            "status": "success",
            "message": "Policy configuration imported",
            "import_result": result,
        }
    except Exception as e:
        logger.error(f"Error importing policy configuration: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 29: Complete Policy Package Management
# =============================================================================


@mcp.tool()
async def export_policy_configuration(
    package_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Export policy configuration to FortiGate CLI format.

    Exports all policies from a package in FortiGate CLI format.
    Useful for:
    - Backup and version control
    - Migration to other FortiManager instances
    - Documentation
    - Offline review

    Args:
        package_name: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with exported configuration

    Example:
        result = export_policy_configuration(
            package_name="default",
            adom="root"
        )
        # Save result['configuration'] to file
    """
    try:
        api = _get_policy_api()
        config = await api.export_policy_configuration(
            package=package_name,
            adom=adom,
        )
        return {
            "status": "success",
            "package": package_name,
            "configuration": config,
        }
    except Exception as e:
        logger.error(f"Error exporting policy configuration: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_policy_usage_stats(
    package_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Get usage statistics for policies showing which rules are active.

    Analyzes policy hit counts and usage patterns to identify:
    - Unused policies (candidates for removal)
    - Frequently hit policies
    - Policy effectiveness
    - Rule optimization opportunities

    Args:
        package_name: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with policy usage statistics

    Example:
        result = get_policy_usage_stats(
            package_name="default",
            adom="root"
        )
        # Identify unused policies for cleanup
    """
    try:
        api = _get_policy_api()
        stats = await api.get_policy_usage_statistics(
            package=package_name,
            adom=adom,
        )
        return {
            "status": "success",
            "package": package_name,
            "statistics": stats,
        }
    except Exception as e:
        logger.error(f"Error getting policy usage statistics: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def consolidate_similar_policies(
    package_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Analyze and consolidate similar policies to reduce rule count.

    Identifies policies that can be merged or consolidated:
    - Overlapping address ranges
    - Similar service sets
    - Redundant rules
    - Consolidation opportunities

    This helps optimize firewall performance and simplify management.

    Args:
        package_name: Policy package name
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with consolidation analysis and recommendations

    Example:
        result = consolidate_similar_policies(
            package_name="default",
            adom="root"
        )
        # Review recommendations for policy optimization
    """
    try:
        api = _get_policy_api()
        analysis = await api.consolidate_policies(
            package=package_name,
            adom=adom,
        )
        return {
            "status": "success",
            "package": package_name,
            "analysis": analysis,
        }
    except Exception as e:
        logger.error(f"Error consolidating policies: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def set_policy_label(
    policy_id: int,
    package_name: str,
    label: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Set a global label on a policy for categorization.

    Labels help organize and categorize policies:
    - "Production", "Testing", "Temporary"
    - "Web_Services", "Database_Access"
    - "High_Priority", "Review_Required"

    Args:
        policy_id: Policy ID
        package_name: Policy package name
        label: Label text
        adom: ADOM name (default: "root")

    Returns:
        Dictionary with operation status

    Example:
        result = set_policy_label(
            policy_id=42,
            package_name="default",
            label="Production_Critical",
            adom="root"
        )
    """
    try:
        api = _get_policy_api()
        await api.set_policy_global_label(
            package=package_name,
            policy_id=policy_id,
            label=label,
            adom=adom,
        )
        return {
            "status": "success",
            "message": f"Policy {policy_id} labeled as '{label}'",
        }
    except Exception as e:
        logger.error(f"Error setting policy label: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 38: Advanced Installation Operations
# =============================================================================


@mcp.tool()
async def abort_policy_install(task_id: int) -> dict[str, Any]:
    """Abort an ongoing policy installation task.
    
    Args:
        task_id: Installation task ID
    
    Returns:
        Dictionary with abort status
    """
    try:
        api = _get_installation_api()
        result = await api.abort_install(task_id=task_id)
        return {"status": "success", "message": "Installation aborted", "result": result}
    except Exception as e:
        logger.error(f"Error aborting install: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_device_install_history(
    device: str,
    adom: str = "root",
    limit: int = 50,
) -> dict[str, Any]:
    """Get installation history for a specific device."""
    try:
        api = _get_installation_api()
        history = await api.get_install_history(device=device, adom=adom, limit=limit)
        return {"status": "success", "count": len(history), "history": history}
    except Exception as e:
        logger.error(f"Error getting install history: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def validate_policy_package(
    package: str,
    adom: str = "root",
    devices: list[str] | None = None,
) -> dict[str, Any]:
    """Validate policy package before installation to check for errors."""
    try:
        api = _get_installation_api()
        validation = await api.validate_install_package(package=package, adom=adom, devices=devices)
        return {"status": "success", "validation": validation}
    except Exception as e:
        logger.error(f"Error validating package: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_install_progress_detailed(task_id: int) -> dict[str, Any]:
    """Get real-time detailed installation progress with line-by-line output."""
    try:
        api = _get_installation_api()
        progress = await api.get_install_progress(task_id=task_id)
        return {"status": "success", "progress": progress}
    except Exception as e:
        logger.error(f"Error getting install progress: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def schedule_package_install(
    package: str,
    devices: list[str],
    adom: str = "root",
    schedule_time: str | None = None,
) -> dict[str, Any]:
    """Schedule a policy package installation for future time."""
    try:
        api = _get_installation_api()
        result = await api.schedule_install(
            package=package, devices=devices, adom=adom, schedule_time=schedule_time
        )
        return {"status": "success", "schedule": result}
    except Exception as e:
        logger.error(f"Error scheduling install: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_install_targets(adom: str = "root") -> dict[str, Any]:
    """Get list of devices available for policy installation."""
    try:
        api = _get_installation_api()
        targets = await api.get_device_install_targets(adom=adom)
        return {"status": "success", "count": len(targets), "devices": targets}
    except Exception as e:
        logger.error(f"Error getting install targets: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def verify_package_installation(
    device: str,
    package: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Verify that a package was successfully installed on a device."""
    try:
        api = _get_installation_api()
        verification = await api.verify_installed_package(device=device, package=package, adom=adom)
        return {"status": "success", "verification": verification}
    except Exception as e:
        logger.error(f"Error verifying installation: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_package_dependencies(package: str, adom: str = "root") -> dict[str, Any]:
    """Get installation dependencies for a policy package."""
    try:
        api = _get_installation_api()
        deps = await api.get_install_dependencies(package=package, adom=adom)
        return {"status": "success", "dependencies": deps}
    except Exception as e:
        logger.error(f"Error getting dependencies: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def rollback_device_install(
    device: str,
    adom: str = "root",
    revision: int | None = None,
) -> dict[str, Any]:
    """Rollback a device to previous installation state."""
    try:
        api = _get_installation_api()
        result = await api.rollback_install(device=device, adom=adom, revision=revision)
        return {"status": "success", "message": "Rollback initiated", "result": result}
    except Exception as e:
        logger.error(f"Error rolling back install: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 44: Additional Policy Operations
# =============================================================================


@mcp.tool()
async def find_policy_by_name(
    package_name: str,
    policy_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Find firewall policy by name instead of ID.
    
    Args:
        package_name: Policy package name
        policy_name: Name of the policy to find
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with policy details
    """
    try:
        api = _get_policy_api()
        policy = await api.get_policy_by_name(package=package_name, policy_name=policy_name, adom=adom)
        if not policy:
            return {"status": "not_found", "message": f"Policy '{policy_name}' not found"}
        return {"status": "success", "policy": policy}
    except Exception as e:
        logger.error(f"Error finding policy: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def duplicate_firewall_policy(
    package_name: str,
    policy_id: int,
    new_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Duplicate an existing firewall policy with a new name.
    
    Args:
        package_name: Policy package name
        policy_id: Source policy ID to duplicate
        new_name: Name for the new duplicated policy
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with new policy details
    """
    try:
        api = _get_policy_api()
        result = await api.duplicate_policy(package=package_name, policy_id=policy_id, new_name=new_name, adom=adom)
        return {"status": "success", "message": f"Policy duplicated as '{new_name}'", "policy": result}
    except Exception as e:
        logger.error(f"Error duplicating policy: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_policy_references_list(
    package_name: str,
    policy_id: int,
    adom: str = "root",
) -> dict[str, Any]:
    """Get all objects referenced by a specific policy.
    
    Args:
        package_name: Policy package name
        policy_id: Policy ID to check
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with all referenced objects
    """
    try:
        api = _get_policy_api()
        references = await api.get_policy_references(package=package_name, policy_id=policy_id, adom=adom)
        return {"status": "success", "references": references}
    except Exception as e:
        logger.error(f"Error getting policy references: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def validate_policy_package_errors(
    package_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Validate policy package configuration for errors.
    
    Args:
        package_name: Policy package name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with validation results
    """
    try:
        api = _get_policy_api()
        result = await api.validate_policy_package(package=package_name, adom=adom)
        return {"status": "success", "validation": result}
    except Exception as e:
        logger.error(f"Error validating package: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def analyze_policy_package_complexity(
    package_name: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Analyze policy package complexity and get optimization recommendations.
    
    Provides insights into policy organization, complexity metrics, and
    recommendations for optimization.
    
    Args:
        package_name: Policy package name
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with complexity analysis
    """
    try:
        api = _get_policy_api()
        analysis = await api.analyze_policy_complexity(package=package_name, adom=adom)
        return {"status": "success", "package": package_name, "analysis": analysis}
    except Exception as e:
        logger.error(f"Error analyzing policy complexity: {e}")
        return {"status": "error", "message": str(e)}


# =============================================================================
# Phase 49: Global Policy Packages & Install Variants
# =============================================================================


@mcp.tool()
async def list_global_policy_packages() -> dict[str, Any]:
    """List global policy packages that apply across all ADOMs.
    
    Global policy packages provide centralized policy management for rules
    that should apply organization-wide. These packages:
    - Apply across all ADOMs
    - Provide centralized compliance rules
    - Ensure consistent baseline security
    - Can be inherited by ADOM-specific packages
    
    Use cases:
    - Organization-wide security policies
    - Compliance requirements (PCI-DSS, HIPAA)
    - Common baseline rules
    - Corporate security standards
    
    Returns:
        Dictionary with list of global policy packages
    
    Example:
        result = list_global_policy_packages()
        # Returns global packages like "corporate-baseline", "compliance-rules"
    """
    try:
        api = _get_policy_api()
        packages = await api.list_global_policy_packages()
        return {
            "status": "success",
            "count": len(packages),
            "packages": packages,
        }
    except Exception as e:
        logger.error(f"Error listing global policy packages: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def get_global_policy_package_details(package_name: str) -> dict[str, Any]:
    """Get details of a specific global policy package.
    
    Retrieves complete information about a global package including:
    - Package metadata and settings
    - Global policy rules
    - Inheritance configuration
    - ADOM assignments
    - Policy statistics
    
    Args:
        package_name: Global policy package name
    
    Returns:
        Dictionary with global package details
    
    Example:
        result = get_global_policy_package_details(
            package_name="corporate-baseline"
        )
    """
    try:
        api = _get_policy_api()
        package = await api.get_global_policy_package(package=package_name)
        return {
            "status": "success",
            "package": package,
        }
    except Exception as e:
        logger.error(f"Error getting global policy package: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def install_package_to_device_db(
    package_name: str,
    target_devices: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Install policy package to FortiManager device database only (no push to devices).
    
    Installs policies to the FortiManager device database without actually
    pushing the configuration to managed FortiGates. This is useful for:
    - Staging policy changes for review
    - Pre-validation before production push
    - Database synchronization
    - Testing installation process
    - Two-stage deployment workflow
    
    The policies remain staged in FortiManager until a full install is performed.
    
    Args:
        package_name: Policy package name to install
        target_devices: Comma-separated list of "device:vdom" (e.g., "FGT-01:root,FGT-02:root")
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with installation task details
    
    Example:
        result = install_package_to_device_db(
            package_name="default",
            target_devices="FGT-BRANCH-01:root,FGT-BRANCH-02:root",
            adom="root"
        )
        # Policies staged in DB, use regular install to push to devices
    """
    try:
        api = _get_policy_api()
        
        # Parse target devices
        scope = []
        for device in target_devices.split(","):
            parts = device.strip().split(":")
            if len(parts) == 2:
                scope.append({"name": parts[0], "vdom": parts[1]})
            else:
                scope.append({"name": parts[0], "vdom": "root"})
        
        result = await api.install_to_device_db_only(
            package=package_name,
            scope=scope,
            adom=adom,
        )
        
        return {
            "status": "success",
            "message": f"Package '{package_name}' staged to device DB",
            "devices": len(scope),
            "task": result,
        }
    except Exception as e:
        logger.error(f"Error installing to device DB: {e}")
        return {"status": "error", "message": str(e)}


@mcp.tool()
async def install_package_offline(
    package_name: str,
    target_devices: str,
    adom: str = "root",
) -> dict[str, Any]:
    """Stage policy package installation for offline/disconnected devices.
    
    Prepares and queues policy installation for devices that are currently
    offline or unreachable. When devices reconnect to FortiManager, they
    will automatically receive the staged configuration.
    
    Perfect for:
    - Remote/branch offices with intermittent connectivity
    - Scheduled maintenance windows
    - Bulk deployments to disconnected sites
    - Disaster recovery scenarios
    - Pre-staging updates before device connection
    
    Args:
        package_name: Policy package name to install
        target_devices: Comma-separated list of "device:vdom"
        adom: ADOM name (default: root)
    
    Returns:
        Dictionary with installation task details
    
    Example:
        result = install_package_offline(
            package_name="branch-policies",
            target_devices="FGT-REMOTE-01:root,FGT-REMOTE-02:root",
            adom="branches"
        )
        # Policies queued, will apply when devices reconnect
    """
    try:
        api = _get_policy_api()
        
        # Parse target devices
        scope = []
        for device in target_devices.split(","):
            parts = device.strip().split(":")
            if len(parts) == 2:
                scope.append({"name": parts[0], "vdom": parts[1]})
            else:
                scope.append({"name": parts[0], "vdom": "root"})
        
        result = await api.install_offline_package(
            package=package_name,
            scope=scope,
            adom=adom,
        )
        
        return {
            "status": "success",
            "message": f"Package '{package_name}' queued for offline installation",
            "devices": len(scope),
            "task": result,
        }
    except Exception as e:
        logger.error(f"Error installing offline package: {e}")
        return {"status": "error", "message": str(e)}

