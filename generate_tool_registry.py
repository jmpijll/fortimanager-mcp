"""Generate comprehensive tool registry by scanning all tool modules."""

import importlib
import inspect
import sys
from pathlib import Path
from typing import Any

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from fortimanager_mcp.tools import (
    device_tools,
    object_tools,
    policy_tools,
    monitoring_tools,
    adom_tools,
    security_tools,
    system_tools,
    vpn_tools,
    sdwan_tools,
    script_tools,
    provisioning_tools,
    workspace_tools,
    advanced_object_tools,
    additional_object_tools,
    fortiguard_tools,
)

# Module to category mapping
MODULE_CATEGORIES = {
    "device_tools": "devices",
    "object_tools": "objects",
    "policy_tools": "policies",
    "monitoring_tools": "monitoring",
    "adom_tools": "adom",
    "security_tools": "security",
    "system_tools": "system",
    "vpn_tools": "vpn",
    "sdwan_tools": "sdwan",
    "script_tools": "scripts",
    "provisioning_tools": "provisioning",
    "workspace_tools": "workspace",
    "advanced_object_tools": "advanced_objects",
    "additional_object_tools": "additional_objects",
    "fortiguard_tools": "fortiguard",
}

MODULES_TO_SCAN = [
    device_tools,
    object_tools,
    policy_tools,
    monitoring_tools,
    adom_tools,
    security_tools,
    system_tools,
    vpn_tools,
    sdwan_tools,
    script_tools,
    provisioning_tools,
    workspace_tools,
    advanced_object_tools,
    additional_object_tools,
    fortiguard_tools,
]


def extract_tool_metadata(func: Any, module_name: str, category: str) -> dict:
    """Extract metadata from a tool function."""
    sig = inspect.signature(func)
    params = {}
    
    for param_name, param in sig.parameters.items():
        if param_name == "self":
            continue
            
        param_info = {"type": "string"}  # Default
        
        # Determine if optional
        if param.default != inspect.Parameter.empty:
            param_info["optional"] = True
            param_info["default"] = str(param.default) if param.default is not None else None
        else:
            param_info["required"] = True
        
        # Try to infer type from annotation
        if param.annotation != inspect.Parameter.empty:
            ann_str = str(param.annotation)
            if "int" in ann_str.lower():
                param_info["type"] = "integer"
            elif "bool" in ann_str.lower():
                param_info["type"] = "boolean"
            elif "dict" in ann_str.lower():
                param_info["type"] = "object"
            elif "list" in ann_str.lower():
                param_info["type"] = "array"
        
        params[param_name] = param_info
    
    # Extract description from docstring
    doc = inspect.getdoc(func) or ""
    description = doc.split("\n\n")[0].strip() if doc else f"{func.__name__} operation"
    
    # Check if requires ADOM
    requires_adom = "adom" in params or "adom" in description.lower()
    
    return {
        "name": func.__name__,
        "module": f"fortimanager_mcp.tools.{module_name}",
        "category": category,
        "description": description[:200],  # Limit length
        "parameters": params,
        "requires_adom": requires_adom,
    }


def generate_registry():
    """Generate tool registry from all modules."""
    print("Scanning tool modules...")
    registry = {}
    
    for module in MODULES_TO_SCAN:
        module_name = module.__name__.split(".")[-1]
        category = MODULE_CATEGORIES.get(module_name, "misc")
        
        print(f"\nScanning {module_name} ({category})...")
        
        # Find all async functions decorated with @mcp.tool()
        for name, obj in inspect.getmembers(module):
            if inspect.isfunction(obj) or inspect.iscoroutinefunction(obj):
                # Check if it's likely a tool (has proper name, not private)
                if not name.startswith("_") and name not in ["get_fmg_client"]:
                    try:
                        metadata = extract_tool_metadata(obj, module_name, category)
                        registry[name] = metadata
                        print(f"  ✓ {name}")
                    except Exception as e:
                        print(f"  ✗ {name}: {e}")
    
    print(f"\n{'='*60}")
    print(f"Total tools found: {len(registry)}")
    print(f"{'='*60}\n")
    
    return registry


def generate_registry_code(registry: dict) -> str:
    """Generate Python code for the registry."""
    code = []
    code.append("# Generated tool registry - DO NOT EDIT MANUALLY")
    code.append("# Run generate_tool_registry.py to update")
    code.append("")
    code.append("TOOL_REGISTRY: dict[str, ToolMetadata] = {")
    
    for tool_name, metadata in sorted(registry.items()):
        code.append(f'    "{tool_name}": ToolMetadata(')
        code.append(f'        name="{metadata["name"]}",')
        code.append(f'        module="{metadata["module"]}",')
        code.append(f'        category="{metadata["category"]}",')
        
        # Escape description
        desc = metadata["description"].replace('"', '\\"').replace("\n", " ")
        code.append(f'        description="{desc}",')
        
        # Parameters
        code.append(f'        parameters={metadata["parameters"]},')
        code.append(f'        requires_adom={metadata["requires_adom"]},')
        code.append("    ),")
    
    code.append("}")
    
    return "\n".join(code)


def main():
    """Generate and save registry."""
    registry = generate_registry()
    
    # Generate code
    registry_code = generate_registry_code(registry)
    
    # Read current tool_registry.py
    registry_file = Path(__file__).parent / "src" / "fortimanager_mcp" / "utils" / "tool_registry.py"
    current_content = registry_file.read_text()
    
    # Find where to insert (after the ToolMetadata class, before current TOOL_REGISTRY)
    before_registry = current_content.split("TOOL_REGISTRY")[0]
    after_registry = "\n\n\ndef get_tool_categories" + current_content.split("def get_tool_categories")[1]
    
    # Combine
    new_content = before_registry + registry_code + after_registry
    
    # Save
    print(f"Writing registry to {registry_file}...")
    registry_file.write_text(new_content)
    print(f"✓ Registry updated with {len(registry)} tools\n")
    
    # Print summary by category
    by_category = {}
    for tool in registry.values():
        cat = tool["category"]
        by_category[cat] = by_category.get(cat, 0) + 1
    
    print("Tools by category:")
    for cat, count in sorted(by_category.items()):
        print(f"  {cat:20s}: {count:3d} tools")


if __name__ == "__main__":
    main()

