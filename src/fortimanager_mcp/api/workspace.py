"""Workspace and FortiManager operations API client."""

from typing import Any

from fortimanager_mcp.api.client import FortiManagerClient


class WorkspaceAPI:
    """API client for workspace locking, committing, and FortiManager operations."""

    def __init__(self, client: FortiManagerClient):
        """Initialize Workspace API client."""
        self.client = client

    # ============================================================================
    # ADOM Workspace Operations
    # ============================================================================

    async def lock_adom(self, adom: str = "root") -> dict[str, Any]:
        """Lock an ADOM workspace for editing.
        
        Locking prevents other administrators from making changes while you work.
        Always unlock or commit when done to release the lock.
        
        Args:
            adom: ADOM name
            
        Returns:
            Result of lock operation
        """
        url = f"/dvmdb/adom/{adom}/workspace/lock"
        return await self.client.exec(url)

    async def unlock_adom(self, adom: str = "root") -> dict[str, Any]:
        """Unlock an ADOM workspace.
        
        WARNING: Unlocking without committing will lose all unsaved changes!
        
        Args:
            adom: ADOM name
            
        Returns:
            Result of unlock operation
        """
        url = f"/dvmdb/adom/{adom}/workspace/unlock"
        return await self.client.exec(url)

    async def commit_adom(self, adom: str = "root") -> dict[str, Any]:
        """Commit changes to an ADOM workspace.
        
        Saves all pending changes made while the ADOM was locked.
        Creates a new ADOM revision.
        
        Args:
            adom: ADOM name
            
        Returns:
            Result of commit operation
        """
        url = f"/dvmdb/adom/{adom}/workspace/commit"
        return await self.client.exec(url)

    async def get_lock_info(self, adom: str = "root") -> dict[str, Any]:
        """Get workspace lock information for an ADOM.
        
        Shows who has locked the ADOM, when, and what changes are pending.
        
        Args:
            adom: ADOM name
            
        Returns:
            Lock information including user, timestamp, and dirty flags
        """
        url = f"/dvmdb/adom/{adom}/workspace/lockinfo"
        return await self.client.get(url)

    # ============================================================================
    # Policy Package Workspace Operations
    # ============================================================================

    async def lock_package(
        self,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Lock a policy package for editing.
        
        Args:
            package: Policy package name
            adom: ADOM name
            
        Returns:
            Result of lock operation
        """
        url = f"/dvmdb/adom/{adom}/workspace/lock/pkg/{package}"
        return await self.client.exec(url)

    async def unlock_package(
        self,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Unlock a policy package.
        
        WARNING: Unlocking without committing will lose all unsaved changes!
        
        Args:
            package: Policy package name
            adom: ADOM name
            
        Returns:
            Result of unlock operation
        """
        url = f"/dvmdb/adom/{adom}/workspace/unlock/pkg/{package}"
        return await self.client.exec(url)

    async def commit_package(
        self,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Commit changes to a policy package.
        
        Args:
            package: Policy package name
            adom: ADOM name
            
        Returns:
            Result of commit operation
        """
        url = f"/dvmdb/adom/{adom}/workspace/commit/pkg/{package}"
        return await self.client.exec(url)

    async def get_package_lock_info(
        self,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get lock information for a policy package.
        
        Args:
            package: Policy package name
            adom: ADOM name
            
        Returns:
            Lock information for the package
        """
        url = f"/dvmdb/adom/{adom}/workspace/lockinfo/pkg/{package}"
        return await self.client.get(url)

    # ============================================================================
    # Device Workspace Operations
    # ============================================================================

    async def lock_device(
        self,
        device: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Lock a device for editing.
        
        Args:
            device: Device name
            adom: ADOM name
            
        Returns:
            Result of lock operation
        """
        url = f"/dvmdb/adom/{adom}/workspace/lock/dev/{device}"
        return await self.client.exec(url)

    async def unlock_device(
        self,
        device: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Unlock a device.
        
        WARNING: Unlocking without committing will lose all unsaved changes!
        
        Args:
            device: Device name
            adom: ADOM name
            
        Returns:
            Result of unlock operation
        """
        url = f"/dvmdb/adom/{adom}/workspace/unlock/dev/{device}"
        return await self.client.exec(url)

    async def commit_device(
        self,
        device: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Commit changes to a device.
        
        Args:
            device: Device name
            adom: ADOM name
            
        Returns:
            Result of commit operation
        """
        url = f"/dvmdb/adom/{adom}/workspace/commit/dev/{device}"
        return await self.client.exec(url)

    # ============================================================================
    # ADOM Revision Operations
    # ============================================================================

    async def revert_adom_revision(
        self,
        version: int,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Revert an ADOM to a previous revision.
        
        WARNING: This will discard all changes made after the specified revision!
        
        Args:
            version: Revision version number to revert to
            adom: ADOM name
            
        Returns:
            Result of revert operation
        """
        url = f"/dvmdb/adom/{adom}/revision/revert"
        data = {"version": version}
        return await self.client.set(url, data=data)

    # =========================================================================
    # Phase 44: Additional Workspace Operations
    # =========================================================================

    async def get_workspace_lock_info(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get detailed information about current workspace locks.
        
        Args:
            adom: ADOM name
            
        Returns:
            Lock information including lock holder and timestamp
        """
        url = f"/dvmdb/adom/{adom}/workspace/lockinfo"
        return await self.client.get(url)

    async def get_package_lock_info(
        self,
        package: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get lock information for a specific policy package.
        
        Args:
            package: Policy package name
            adom: ADOM name
            
        Returns:
            Package lock details
        """
        url = f"/pm/config/adom/{adom}/pkg/{package}/lockinfo"
        return await self.client.get(url)

    async def discard_adom_changes(
        self,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Discard all uncommitted changes in an ADOM workspace.
        
        Args:
            adom: ADOM name
            
        Returns:
            Result of discard operation
        """
        url = f"/dvmdb/adom/{adom}/workspace/discard"
        return await self.client.exec(url)

    async def get_revision_diff(
        self,
        version1: int,
        version2: int,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get differences between two ADOM revisions.
        
        Args:
            version1: First revision version
            version2: Second revision version
            adom: ADOM name
            
        Returns:
            Difference details between revisions
        """
        url = f"/dvmdb/adom/{adom}/revision/diff"
        data = {"version1": version1, "version2": version2}
        return await self.client.exec(url, data=data)

