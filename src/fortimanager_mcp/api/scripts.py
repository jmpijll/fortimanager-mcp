"""FortiManager CLI Script API operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class ScriptAPI:
    """CLI Script management operations.
    
    Handles CLI script creation, execution, and management.
    """

    def __init__(self, client: Any) -> None:
        """Initialize ScriptAPI.
        
        Args:
            client: FortiManager API client
        """
        self.client = client

    async def list_scripts(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List CLI scripts in an ADOM.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of CLI scripts with their details
        """
        url = f"/dvmdb/adom/{adom}/script"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_script(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get CLI script details.
        
        Args:
            name: Script name
            adom: ADOM name
            
        Returns:
            Script details
        """
        url = f"/dvmdb/adom/{adom}/script/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_script(
        self,
        name: str,
        content: str,
        target: str,
        adom: str = "root",
        script_type: str = "cli",
        description: str | None = None,
    ) -> dict[str, Any]:
        """Create a CLI script.
        
        Args:
            name: Script name
            content: Script content (CLI commands or Jinja template)
            target: Script target - "adom_database", "device_database", or "remote_device"
            adom: ADOM name
            script_type: Script type - "cli" or "jinja" (default: "cli")
            description: Optional script description
            
        Returns:
            Created script details
        """
        url = f"/dvmdb/adom/{adom}/script"
        
        data = {
            "name": name,
            "content": content,
            "target": target,
            "type": script_type,
        }
        
        if description:
            data["desc"] = description
        
        result = await self.client.add(url, data)
        return result if isinstance(result, dict) else {}

    async def update_script(
        self,
        name: str,
        adom: str = "root",
        content: str | None = None,
        description: str | None = None,
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Update a CLI script.
        
        Args:
            name: Script name
            adom: ADOM name
            content: Updated script content
            description: Updated description
            **kwargs: Additional fields to update
            
        Returns:
            Updated script details
        """
        url = f"/dvmdb/adom/{adom}/script/{name}"
        
        data = {}
        if content is not None:
            data["content"] = content
        if description is not None:
            data["desc"] = description
        data.update(kwargs)
        
        result = await self.client.update(url, data)
        return result if isinstance(result, dict) else {}

    async def delete_script(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a CLI script.
        
        Args:
            name: Script name
            adom: ADOM name
            
        Returns:
            Deletion status
        """
        url = f"/dvmdb/adom/{adom}/script/{name}"
        result = await self.client.delete(url)
        return result

    async def execute_script(
        self,
        script: str,
        adom: str = "root",
        package: str | None = None,
        scope: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        """Execute a CLI script.
        
        Args:
            script: Script name
            adom: ADOM name
            package: Policy package name (for adom_database target)
            scope: Device scope list with {"name": "device", "vdom": "global"}
                  (for remote_device target)
            
        Returns:
            Execution result with task ID
            
        Notes:
            - For ADOM database: No package or scope needed
            - For policy package: Specify package name
            - For device: Specify scope with device name and vdom="global"
        """
        url = f"/dvmdb/adom/{adom}/script/execute"
        
        data: dict[str, Any] = {
            "adom": adom,
            "script": script,
        }
        
        if package:
            data["package"] = package
        
        if scope:
            data["scope"] = scope
        
        result = await self.client.exec(url, data)
        return result if isinstance(result, dict) else {}

    async def get_script_log(
        self,
        log_id: int,
    ) -> dict[str, Any]:
        """Get CLI script execution log.
        
        Args:
            log_id: Log ID (generated from task_id)
                   - For ADOM/Package DB: log_id = task_id + "1"
                   - For device: log_id = task_id + "0"
            
        Returns:
            Script execution log
        """
        url = f"/logview/adom/script_log/{log_id}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    # =========================================================================
    # Phase 24: Complete CLI Script Management
    # =========================================================================

    async def clone_script(
        self,
        source_name: str,
        new_name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Clone an existing CLI script.
        
        Args:
            source_name: Source script name
            new_name: New script name
            adom: ADOM name
            
        Returns:
            Cloned script details
        """
        url = f"/dvmdb/adom/{adom}/script/{source_name}"
        data = {"name": new_name}
        result = await self.client.clone(url, data)
        return result if isinstance(result, dict) else {}

    async def list_script_history(
        self,
        adom: str = "root",
        limit: int = 100,
    ) -> list[dict[str, Any]]:
        """List CLI script execution history.
        
        Args:
            adom: ADOM name
            limit: Maximum number of history records to return
            
        Returns:
            List of script execution history records
        """
        url = f"/dvmdb/adom/{adom}/script/log/list"
        params = {"limit": limit}
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def get_script_history(
        self,
        script_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Get execution history for a specific script.
        
        Args:
            script_name: Script name
            adom: ADOM name
            
        Returns:
            List of execution records for the script
        """
        url = f"/dvmdb/adom/{adom}/script/{script_name}/log"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def validate_script(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Validate CLI script syntax.
        
        Args:
            name: Script name
            adom: ADOM name
            
        Returns:
            Validation result with syntax check status
        """
        url = f"/dvmdb/adom/{adom}/script/{name}/validate"
        result = await self.client.exec(url, data={})
        return result if isinstance(result, dict) else {}

    async def schedule_script_execution(
        self,
        script: str,
        schedule_time: str,
        adom: str = "root",
        package: str | None = None,
        scope: list[dict[str, str]] | None = None,
    ) -> dict[str, Any]:
        """Schedule a CLI script for future execution.
        
        Args:
            script: Script name
            schedule_time: Schedule time in format "YYYY-MM-DD HH:MM:SS"
            adom: ADOM name
            package: Policy package name (for adom_database target)
            scope: Device scope list
            
        Returns:
            Scheduled task information
        """
        url = f"/dvmdb/adom/{adom}/script/schedule"
        
        data: dict[str, Any] = {
            "adom": adom,
            "script": script,
            "schedule": schedule_time,
        }
        
        if package:
            data["package"] = package
        
        if scope:
            data["scope"] = scope
        
        result = await self.client.exec(url, data)
        return result if isinstance(result, dict) else {}

