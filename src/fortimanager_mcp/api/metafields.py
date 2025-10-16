"""FortiManager Meta Fields API operations."""

import logging
from typing import Any

logger = logging.getLogger(__name__)


class MetaFieldsAPI:
    """Meta fields management operations.
    
    Handles custom metadata fields for objects, devices, and policies.
    """

    def __init__(self, client: Any) -> None:
        """Initialize MetaFieldsAPI.
        
        Args:
            client: FortiManager API client
        """
        self.client = client

    # =========================================================================
    # Phase 32: Meta Fields
    # =========================================================================

    async def list_meta_fields(
        self,
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List all meta field definitions.
        
        Meta fields are custom key-value pairs for categorizing and tagging
        objects, policies, and devices.
        
        Args:
            adom: ADOM name
            
        Returns:
            List of meta field definitions
        """
        url = f"/pm/config/adom/{adom}/obj/system/meta"
        data = await self.client.get(url)
        return data if isinstance(data, list) else [data] if data else []

    async def get_meta_field(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get meta field definition.
        
        Args:
            name: Meta field name
            adom: ADOM name
            
        Returns:
            Meta field definition
        """
        url = f"/pm/config/adom/{adom}/obj/system/meta/{name}"
        data = await self.client.get(url)
        return data if isinstance(data, dict) else {}

    async def create_meta_field(
        self,
        name: str,
        field_type: str = "string",
        adom: str = "root",
        **kwargs: Any,
    ) -> dict[str, Any]:
        """Create a meta field definition.
        
        Args:
            name: Meta field name
            field_type: Field type (string, integer, boolean)
            adom: ADOM name
            **kwargs: Additional field properties
            
        Returns:
            Created meta field
        """
        data = {
            "name": name,
            "type": field_type,
            **kwargs,
        }
        url = f"/pm/config/adom/{adom}/obj/system/meta"
        return await self.client.add(url, data=data)

    async def delete_meta_field(
        self,
        name: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Delete a meta field definition.
        
        Args:
            name: Meta field name
            adom: ADOM name
            
        Returns:
            Deletion result
        """
        url = f"/pm/config/adom/{adom}/obj/system/meta/{name}"
        return await self.client.delete(url)

    async def list_objects_with_meta_field(
        self,
        field_name: str,
        field_value: str,
        object_type: str = "firewall/address",
        adom: str = "root",
    ) -> list[dict[str, Any]]:
        """List objects with specific meta field value.
        
        Args:
            field_name: Meta field name
            field_value: Meta field value to search for
            object_type: Object type (firewall/address, firewall/policy, etc.)
            adom: ADOM name
            
        Returns:
            List of objects with matching meta field
        """
        url = f"/pm/config/adom/{adom}/obj/{object_type}"
        params = {
            "filter": f"{field_name}=={field_value}",
        }
        data = await self.client.get(url, **params)
        return data if isinstance(data, list) else [data] if data else []

    async def set_object_meta_field(
        self,
        object_name: str,
        object_type: str,
        field_name: str,
        field_value: Any,
        adom: str = "root",
    ) -> None:
        """Set meta field value on an object.
        
        Args:
            object_name: Object name
            object_type: Object type (firewall/address, firewall/policy, etc.)
            field_name: Meta field name
            field_value: Meta field value
            adom: ADOM name
        """
        url = f"/pm/config/adom/{adom}/obj/{object_type}/{object_name}"
        data = {
            "meta-fields": {
                field_name: field_value,
            },
        }
        await self.client.set(url, data=data)

    async def get_object_meta_fields(
        self,
        object_name: str,
        object_type: str,
        adom: str = "root",
    ) -> dict[str, Any]:
        """Get all meta fields for an object.
        
        Args:
            object_name: Object name
            object_type: Object type (firewall/address, firewall/policy, etc.)
            adom: ADOM name
            
        Returns:
            Object's meta fields
        """
        url = f"/pm/config/adom/{adom}/obj/{object_type}/{object_name}"
        data = await self.client.get(url)
        if isinstance(data, dict):
            return data.get("meta-fields", {})
        return {}

