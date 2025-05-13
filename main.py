from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file at the very start

from fastmcp import FastMCP
import tools.fortimanager_tools as fmg_tools # Import your tools module

# Initialize the FastMCP server
# You might want to load the server name from config or environment variables
mcp = FastMCP(name="FortiManagerMCPServer")

# Register tools from the fortimanager_tools module
# This requires functions in fortimanager_tools.py to be decorated with @mcp.tool()
# For now, we are manually wrapping them or will decorate them later.

# Initialize the FortiManager client once
# This should ideally be called before any tool that needs it runs for the first time.
# FastMCP might have hooks for this, or tools can call it if not initialized.
fmg_tools.initialize_fmg_api_client() # Initialize client on startup

# Manually define and register tools if not using @mcp.tool() decorator in the module
# Or, if tools are decorated, FastMCP might auto-discover them if the module is processed.

# Assuming the tools in fmg_tools are (or will be) decorated with @mcp.tool(),
# they might be auto-registered by FastMCP if it scans the module, 
# or we might need a registration function.

# For demonstration, let's assume FastMCP requires explicit registration 
# or that we will add the @mcp.tool decorator directly in fortimanager_tools.py.

# If tools are decorated in fmg_tools.py with an mcp instance defined THERE,
# this is simpler. If the mcp instance is only here, they need access to it.

# Let's add the @mcp.tool decorator to the functions in fortimanager_tools.py
# For now, we will assume that FastMCP can discover them if the module is imported
# and the functions are decorated correctly.

# To make them available, we can explicitly add them if they are not auto-discovered
# or if we want to control their exposed names.

@mcp.tool(name="list_fortimanager_devices", description=fmg_tools.list_devices.__doc__)
def list_devices_wrapper(adom: str = "root"):
    return fmg_tools.list_devices(adom=adom)

@mcp.tool(name="get_fortimanager_system_status", description=fmg_tools.get_system_status.__doc__)
def get_system_status_wrapper():
    return fmg_tools.get_system_status()

@mcp.tool(name="list_fortimanager_policy_packages", description=fmg_tools.list_policy_packages.__doc__)
def list_policy_packages_wrapper(adom: str = "root"):
    return fmg_tools.list_policy_packages(adom=adom)

@mcp.tool(name="get_fortimanager_device_details", description=fmg_tools.get_device_details.__doc__)
def get_device_details_wrapper(device_name: str, adom: str = "root"):
    return fmg_tools.get_device_details(device_name=device_name, adom=adom)

@mcp.tool(name="get_fortimanager_device_config_status", description=fmg_tools.get_device_config_status.__doc__)
def get_device_config_status_wrapper(device_name: str, adom: str = "root"):
    return fmg_tools.get_device_config_status(device_name=device_name, adom=adom)

@mcp.tool(name="retrieve_fortimanager_device_config", description=fmg_tools.retrieve_device_config_from_device.__doc__)
def retrieve_device_config_from_device_wrapper(device_name: str, adom: str = "root"):
    return fmg_tools.retrieve_device_config_from_device(device_name=device_name, adom=adom)

@mcp.tool(name="list_fortimanager_device_interfaces", description=fmg_tools.list_device_interfaces.__doc__)
def list_device_interfaces_wrapper(device_name: str, adom: str = "root"):
    return fmg_tools.list_device_interfaces(device_name=device_name, adom=adom)

@mcp.tool(name="get_fortimanager_device_routing_table", description=fmg_tools.get_device_routing_table.__doc__)
def get_device_routing_table_wrapper(device_name: str, adom: str = "root"):
    return fmg_tools.get_device_routing_table(device_name=device_name, adom=adom)

@mcp.tool(name="get_fortimanager_policy_package_details", description=fmg_tools.get_policy_package_details.__doc__)
def get_policy_package_details_wrapper(package_name: str, adom: str = "root"):
    return fmg_tools.get_policy_package_details(package_name=package_name, adom=adom)

@mcp.tool(name="list_fortimanager_firewall_policies", description=fmg_tools.list_firewall_policies.__doc__)
def list_firewall_policies_wrapper(package_name: str, adom: str = "root"):
    return fmg_tools.list_firewall_policies(package_name=package_name, adom=adom)

@mcp.tool(name="get_fortimanager_firewall_policy_details", description=fmg_tools.get_firewall_policy_details.__doc__)
def get_firewall_policy_details_wrapper(policy_id: str, package_name: str, adom: str = "root"):
    return fmg_tools.get_firewall_policy_details(policy_id=policy_id, package_name=package_name, adom=adom)

if __name__ == "__main__":
    # You can configure host, port, and transport as needed.
    # Default is stdio transport.
    # For web-based access, you might use 'streamable-http' or 'sse'.
    # mcp.run(transport="streamable-http", host="0.0.0.0", port=8000)
    print("Starting FortiManager MCP Server...")
    print(f"MCP Server Name: {mcp.name}")
    print("Available tools will be listed by FastMCP when it starts.")
    print("To run with web interface for testing: fastmcp dev main.py")
    print("To make available to clients (e.g. Claude Desktop): fastmcp install main.py")
    print(f"FortiManager MCP Server '{mcp.name}' initialized.")
    print("Registered tools:")
    for tool_name, tool_func in mcp.tools.items():
        print(f"- {tool_name}: {tool_func.description}")
    
    print("\nTo run the server (example, replace with actual FastMCP run command):")
    print("# from fastmcp.server import run_server")
    print("# run_server(mcp, host=\"0.0.0.0\", port=8000)")
    print("\nPlease consult FastMCP documentation for the correct way to run the server.")

    # Example of calling a tool directly (for testing, not how an MCP client would do it)
    # print("\nTesting list_devices via MCP wrapper...")
    # print(list_devices_wrapper(adom="root"))
    # print("\nTesting get_system_status via MCP wrapper...")
    # print(get_system_status_wrapper())
    mcp.run() 