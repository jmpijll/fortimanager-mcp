"""FortiManager Sub-Object Fetch API operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class SubFetchAPI:
    """Sub-object fetch operations.
    
    Handles fetching sub-objects and nested configurations.
    """

    def __init__(self, client: Any) -> None:
        """Initialize SubFetchAPI.
        
        Args:
            client: FortiManager API client
        """
        self.client = client

    # =========================================================================
    # Phase 34: Sub Fetch Operations
    # =========================================================================

    async def fetch_sub_objects(
        self,
        object_path: str,
        sub_object_type: str,
        adom: str = "root",
        filters: dict[str, Any] | None = None,
    ) -> list[dict[str, Any]]:
        """Fetch sub-objects from a parent object.
        
        Retrieves nested configuration objects within a parent object.
        
        Args:
            object_path: Parent object path
            sub_object_type: Type of sub-object to fetch
            adom: ADOM name
            filters: Optional filters for the query
            
        Returns:
            List of sub-objects
        """
        url = f"/pm/config/adom/{adom}/obj/{object_path}/{sub_object_type}"
        params = filters or {}
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def fetch_nested_configuration(
        self,
        config_path: str,
        depth: int = 1,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Fetch nested configuration with specified depth.
        
        Retrieves configuration including nested sub-objects up to
        the specified depth level.
        
        Args:
            config_path: Configuration path
            depth: Nesting depth to retrieve (1-5)
            adom: ADOM name
            
        Returns:
            Nested configuration data
        """
        url = f"/pm/config/adom/{adom}/obj/{config_path}"
        params = {"fetch-sub": depth}
        data = await self.client.get(url, **params)
        return data if isinstance(data, dict) else {}

    async def fetch_object_members(
        self,
        object_type: str,
        object_name: str,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """Fetch members of a group object.
        
        Retrieves member objects of address groups, service groups,
        and other group-type objects.
        
        Args:
            object_type: Object type (e.g., "firewall/addrgrp")
            object_name: Group object name
            adom: ADOM name
            
        Returns:
            List of member objects
        """
        url = f"/pm/config/adom/{adom}/obj/{object_type}/{object_name}/member"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []


