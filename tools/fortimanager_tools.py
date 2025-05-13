# FortiManager MCP Tools will be defined here.
# Uses python-fortimanagerapi to interact with the FortiManager JSON RPC API.

# from fastmcp import FastMCP # Assuming mcp instance is defined in main.py and passed or imported
# import os
# from dotenv import load_dotenv
# from fortimanager_api import FortiManagerAPI # Import the library

# load_dotenv() # Load environment variables from .env file

# Example structure for initializing the API client:
# def initialize_fmg_api_client():
#     fmg_host = os.getenv("FORTIMANAGER_HOST")
#     fmg_api_key = os.getenv("FORTIMANAGER_API_KEY")
#
#     if not fmg_host or not fmg_api_key:
#         raise ValueError("FORTIMANAGER_HOST and FORTIMANAGER_API_KEY must be set in the environment.")
#
#     # Initialize FortiManagerAPI client using API Key (Token-based authentication)
#     # The library likely handles adding the token to requests appropriately.
#     # Refer to python-fortimanagerapi documentation for the exact initialization method.
#     # It might look something like this:
#     fmg = FortiManagerAPI(
#         host=fmg_host,
#         api_key=fmg_api_key,
#         use_ssl=True, # Recommended
#         verify_ssl=False, # Set to True in production with proper certs
#         timeout=10
#     )
#     # Or potentially using a method like: fmg.login_with_apikey(fmg_api_key)
#     # It's important to check the specific library's method.
#
#     # It is recommended to disable warnings for insecure requests if verify_ssl is False
#     # import urllib3
#     # urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
#
#     return fmg

# Placeholder for where the client would be initialized and used
# fmg_client = initialize_fmg_api_client()

import os
import requests
import urllib3
from typing import Annotated, List, Dict, Optional
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

# Disable SSL warnings if needed
verify_ssl_env = os.getenv("FORTIMANAGER_VERIFY_SSL", "false").lower()
VERIFY_SSL = verify_ssl_env == "true"
if not VERIFY_SSL:
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class FortiManagerJsonRpcClient:
    def __init__(self, host: str, api_key: str, verify_ssl: bool = False, timeout: int = 10):
        self.host = host.rstrip("/")
        self.api_key = api_key
        self.verify_ssl = verify_ssl
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        })
        self.id_counter = 1

    def call(self, method: str, url: str, params: Optional[dict] = None):
        # FortiManager JSON-RPC expects POST to /jsonrpc
        endpoint = f"{self.host}/jsonrpc"
        payload = {
            "method": method,
            "params": [params or {}],
            "id": self.id_counter,
            "session": None,  # Not needed for token auth
            "url": url
        }
        self.id_counter += 1
        resp = self.session.post(endpoint, json=payload, verify=self.verify_ssl, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        if "error" in data:
            raise RuntimeError(f"FortiManager API error: {data['error']}")
        return data.get("result", [{}])[0]

# Singleton client
_fmg_client = None

def initialize_fmg_api_client():
    global _fmg_client
    if _fmg_client:
        return _fmg_client
    fmg_host = os.getenv("FORTIMANAGER_HOST")
    fmg_api_key = os.getenv("FORTIMANAGER_API_KEY")
    if not fmg_host or not fmg_api_key:
        raise ValueError("FORTIMANAGER_HOST and FORTIMANAGER_API_KEY must be set in .env file.")
    _fmg_client = FortiManagerJsonRpcClient(fmg_host, fmg_api_key, verify_ssl=VERIFY_SSL)
    return _fmg_client

@mcp.tool() # Decorate with FastMCP's tool decorator
def list_devices(
    adom: Annotated[str, Field(description="The Administrative Domain to query")] = "root"
) -> list[dict]:
    """
    Lists devices in FortiManager, optionally filtered by ADOM.
    Returns a list of device details.
    """
    client = initialize_fmg_api_client()
    url = f"/dvmdb/adom/{adom}/device"
    result = client.call("get", url)
    return result.get("data", result)

@mcp.tool()
def get_system_status() -> dict:
    """
    Retrieves the system status from FortiManager.
    Returns system status information as a dict.
    """
    client = initialize_fmg_api_client()
    url = "/sys/status"
    result = client.call("get", url)
    return result.get("data", result)

@mcp.tool()
def get_fortimanager_fortiguard_status(adom: str = "root"):
    """
    Retrieves the FortiGuard service status from FortiManager.
    This includes AV/IPS DB versions, license information, and service availability.
    ADOM parameter is typically not required for global FortiGuard status but included for consistency.
    """
    client = initialize_fmg_api_client()
    api_url = "/pm/config/global/fgd/status"
    result = client.call("get", api_url)
    return {
        "message": "Successfully retrieved FortiManager FortiGuard status.",
        "fortiguard_status": result.get("data", result),
        "response_code": result.get("code", 0),
        "raw_response": result
    }

@mcp.tool() # Decorate with FastMCP's tool decorator
def list_policy_packages(
    adom: Annotated[str, Field(description="The Administrative Domain to query")] = "root"
) -> list[dict]:
    """
    Lists policy packages in FortiManager for a specific ADOM.
    Returns a list of policy package details.
    """
    client = initialize_fmg_api_client()
    api_url = f"/pm/pkg/adom/{adom}"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def get_device_details(
    device_name: Annotated[str, Field(description="Name of the device")],
    adom: Annotated[str, Field(description="Administrative Domain")] = "root"
) -> dict:
    """
    Retrieves detailed information for a specific device in FortiManager.
    Device name is required. ADOM defaults to 'root' if not provided.
    Returns device details as a dict.
    """
    client = initialize_fmg_api_client()
    api_url = f"/dvmdb/adom/{adom}/device/{device_name}"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def get_device_config_status(
    device_name: Annotated[str, Field(description="Name of the device")],
    adom: Annotated[str, Field(description="Administrative Domain")] = "root"
) -> dict:
    """
    Retrieves the configuration synchronization status for a specific device.
    Interprets the 'conf_status' field from the device details.
    Device name is required. ADOM defaults to 'root'.
    Returns a dict with raw and interpreted config status.
    """
    client = initialize_fmg_api_client()
    api_url = f"/dvmdb/adom/{adom}/device/{device_name}"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def retrieve_device_config_from_device(
    device_name: Annotated[str, Field(description="Name of the device")],
    adom: Annotated[str, Field(description="Administrative Domain")] = "root"
) -> dict:
    """
    Triggers FortiManager to retrieve the latest configuration from a specified device.
    This action typically starts a task on FortiManager.
    Device name is required. ADOM defaults to 'root'.
    Returns information about the initiated task.
    """
    client = initialize_fmg_api_client()
    api_command_path = f"/dvmdb/adom/{adom}/device/{device_name}/cmd/retrieve"
    result = client.call("execute", api_command_path)
    return result.get("data", result)

@mcp.tool()
def list_device_interfaces(device_name: str, adom: str = "root"):
    """
    Lists network interfaces for a specific device in FortiManager.
    Attempts to retrieve interface configurations (e.g., IP, status).
    Device name is required. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    api_path = f"/dvmdb/adom/{adom}/device/{device_name}/config/system/interface"
    result = client.call("get", api_path)
    return result.get("data", result)

@mcp.tool()
def get_device_routing_table(device_name: str, adom: str = "root"):
    """
    Retrieves the routing table for a specific device in FortiManager.
    Device name is required. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    api_url = f"/dvmdb/adom/{adom}/device/{device_name}/monitor/router/select"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def get_policy_package_details(package_name: str, adom: str = "root"):
    """
    Retrieves detailed information for a specific policy package in an ADOM.
    Requires package_name. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    api_url = f"/pm/pkg/adom/{adom}/{package_name}"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def list_firewall_policies(package_name: str, adom: str = "root"):
    """
    Lists firewall policies within a specific policy package in an ADOM.
    Requires package_name. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    api_url = f"/pm/config/adom/{adom}/pkg/{package_name}/firewall/policy"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def get_firewall_policy_details(policy_id: str, package_name: str, adom: str = "root"):
    """
    Retrieves detailed configuration for a specific firewall policy by its ID.
    Requires policy_id, package_name. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    api_url = f"/pm/config/adom/{adom}/pkg/{package_name}/firewall/policy/{policy_id}"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def list_firewall_objects(object_type: str, adom: str = "root"):
    """
    Lists firewall objects of a specified type within an ADOM.
    Requires object_type (e.g., 'firewall/address', 'firewall/service/custom', 'firewall/addrgrp').
    ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    api_url = f"/pm/config/adom/{adom}/obj/{object_type.strip()}"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def get_firewall_object_details(object_name: str, object_type: str, adom: str = "root"):
    """
    Retrieves details for a specific firewall object by its name and type.
    Requires object_name and object_type (e.g., 'firewall/address', 'firewall/service/custom').
    ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    api_url = f"/pm/config/adom/{adom}/obj/{object_type.strip()}/{object_name.strip()}"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def query_firewall_policies(
    package_name: str,
    adom: str = "root", 
    source_address: str = None, 
    destination_address: str = None, 
    service: str = None, 
    action: str = None,
    status: str = None,
    policy_name_contains: str = None # For simple name filtering
):
    """
    Queries firewall policies within a specific policy package based on filter criteria.
    Requires package_name. ADOM defaults to 'root'.
    All filter parameters are optional. If none are provided, it may list all policies (or a default limit).
    Note: Field names for filtering (e.g., 'srcaddr', 'dstaddr', 'service', 'action', 'status', 'name') must match FortiManager API schema.
    This tool constructs a basic filter. For more complex queries, direct API interaction might be needed.
    """
    client = initialize_fmg_api_client()
    filters = []
    if source_address:
        filters.append(["srcaddr", "==", source_address])
    if destination_address:
        filters.append(["dstaddr", "==", destination_address])
    if service:
        filters.append(["service", "==", service])
    if action:
        filters.append(["action", "==", action.lower()])
    if status:
        filters.append(["status", "==", status.lower()])
    if policy_name_contains:
        filters.append(["name", "like", f"%{policy_name_contains}%"])

    api_url = f"/pm/config/adom/{adom}/pkg/{package_name}/firewall/policy"
    payload = {"filter": filters}
    result = client.call("get", api_url, payload)
    return result.get("data", result)

@mcp.tool()
def list_cli_scripts(adom: str = "root"):
    """
    Lists available CLI scripts in FortiManager for a specific ADOM.
    ADOM defaults to 'root' if not provided.
    """
    client = initialize_fmg_api_client()
    api_url = f"/pm/config/adom/{adom}/script/script"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def get_cli_script_content(script_name: str, adom: str = "root"):
    """
    Retrieves the content of a specific CLI script from FortiManager.
    Requires script_name. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    api_url = f"/pm/config/adom/{adom}/script/script/{script_name.strip()}"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def run_cli_script_on_device(script_name: str, device_name: str, adom: str = "root", vdom: str = "root"):
    """
    Executes a pre-defined CLI script on a target device/VDOM via FortiManager.
    Requires script_name and device_name. ADOM and VDOM default to 'root'.
    """
    client = initialize_fmg_api_client()
    api_url = f"/dvmdb/adom/{adom}/script/execute"
    payload = {
        "adom": adom,
        "script": script_name.strip(),
        "scope": [
            {
                "name": device_name.strip(),
                "vdom": vdom.strip()
            }
        ]
    }
    result = client.call("execute", api_url, payload)
    return result.get("data", result)

@mcp.tool()
def list_adoms():
    """
    Lists all Administrative Domains (ADOMs) in FortiManager.
    """
    client = initialize_fmg_api_client()
    api_url = "/dvmdb/adom/"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def get_adom_details(adom_name: str):
    """
    Retrieves specific details for a given Administrative Domain (ADOM) in FortiManager.
    Requires adom_name.
    """
    client = initialize_fmg_api_client()
    api_url = f"/dvmdb/adom/{adom_name.strip()}"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def list_vdoms_on_device(device_name: str, adom: str = "root"):
    """
    Lists Virtual Domains (VDOMs) for a specified device in FortiManager.
    Requires device_name. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    api_url = f"/dvmdb/adom/{adom}/device/{device_name.strip()}/vdom"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool() # Ensure this decorator is active
def get_device_ha_status(device_name: str, adom: str = "root"):
    """
    Retrieves the High Availability (HA) status for a specific device from FortiManager.
    Requires device_name. ADOM defaults to 'root'.
    The HA status might be part of a general device status endpoint.
    """
    client = initialize_fmg_api_client()
    api_url = f"/dvmdb/adom/{adom}/device/{device_name.strip()}/status"
    result = client.call("get", api_url)
    return {
        "message": f"HA status information for device '{device_name}' in ADOM '{adom}'.",
        "device_name": device_name,
        "adom": adom,
        "ha_details": result.get("data", result),
        "response_code": result.get("code", 0),
        "raw_response": result
    }

@mcp.tool()
def list_available_firmware_versions(
    device_model: Annotated[str, Field(description="Device model to list available firmware versions for")]
) -> list[dict]:
    """
    Lists firmware versions available on FortiManager for a given device model.
    Returns a list of firmware version details.
    """
    client = initialize_fmg_api_client()
    api_url = f"/dvmdb/firmware/{device_model}"
    result = client.call("get", api_url)
    return result.get("data", result)

@mcp.tool()
def get_fortimanager_api_version() -> dict:
    """
    Gets the FortiManager API version and build number.
    Returns a dict with version and build information.
    """
    api_url = "/sys/status"
    result = client.call("get", api_url)
    return {
        "version": result.get("data", result).get("version"),
        "build": result.get("data", result).get("build"),
        "full_status": result.get("data", result)
    }

@mcp.tool()
def install_policy_package(
    package_name: Annotated[str, Field(description="Name of the policy package to install")],
    scope: Annotated[List[Dict[str, str]], Field(description="List of targets, each with 'name' (device) and 'vdom'")],
    adom: Annotated[str, Field(description="Administrative Domain")] = "root"
) -> dict:
    """
    Installs a policy package to its targets.
    Uses the /securityconsole/install/package endpoint (FortiManager JSON API @Web).
    Parameters:
      - package_name: Name of the policy package to install.
      - scope: List of dicts, each with 'name' (device) and 'vdom'.
      - adom: Administrative Domain (default: 'root').
    Returns a dict with task ID and status, or raises on error.
    """
    client = initialize_fmg_api_client()
    api_url = "/securityconsole/install/package"
    payload = {
        "adom": adom,
        "pkg": package_name,
        "scope": scope
    }
    result = client.call("execute", api_url, payload)
    return result.get("data", result)

@mcp.tool()
def install_device_config(
    scope: Annotated[List[Dict[str, str]], Field(description="List of targets, each with 'name' (device) and 'vdom'")],
    adom: Annotated[str, Field(description="Administrative Domain")] = "root"
) -> dict:
    """
    Installs device-level settings to a device.
    Uses the /securityconsole/install/device endpoint (FortiManager 7.4 API @Web).
    Parameters:
      - scope: List of dicts, each with 'name' (device) and 'vdom'.
      - adom: Administrative Domain (default: 'root').
    Returns a dict with task ID and status, or raises on error.
    """
    client = initialize_fmg_api_client()
    api_url = "/securityconsole/install/device"
    payload = {
        "adom": adom,
        "scope": scope
    }
    result = client.call("execute", api_url, payload)
    return result.get("data", result)

@mcp.tool()
def get_task_status(
    task_id: Annotated[str, Field(description="The task ID to check status for")]
) -> dict:
    """
    Checks the status of a background FortiManager task by its ID.
    Uses the /task/task/{task_id} endpoint (FortiManager 7.4 API @Web).
    Parameters:
      - task_id: The task ID to check status for.
    Returns a dict with task status details, or raises on error.
    """
    client = initialize_fmg_api_client()
    api_url = f"/task/task/{task_id}"
    result = client.call("get", api_url)
    return result.get("data", result)

# Example usage (for testing locally, not part of MCP normally)
if __name__ == '__main__':
    try:
        print("Attempting to initialize client and fetch data using pyfmg...")
        # Ensure .env file has FORTIMANAGER_HOST and FORTIMANAGER_API_KEY
        
        # Test list_devices
        print("\n--- List Devices (ADOM: root) ---")
        devices = list_devices(adom="root")
        print(devices)

        # Test get_system_status
        print("\n--- Get System Status ---")
        status = get_system_status()
        print(status)

        # Test list_policy_packages
        print("\n--- List Policy Packages (ADOM: root) ---")
        packages = list_policy_packages(adom="root")
        print(packages)

        # Test get_device_details - replace 'YOUR_DEVICE_NAME' with an actual device name
        # print("\n--- Get Device Details (ADOM: root, Device: YOUR_DEVICE_NAME) ---")
        # if isinstance(devices, list) and len(devices) > 0 and isinstance(devices[0], dict) and 'name' in devices[0]:
        #     test_device_name = devices[0]['name'] # Use the first device found for testing
        #     print(f"Testing with device: {test_device_name}")
        #     details = get_device_details(device_name=test_device_name, adom="root")
        #     print(details)
        # else:
        #     print("Skipping get_device_details test as no device name could be determined automatically.")
        #     print("Please manually provide a device_name to test get_device_details.")
        
        # Test get_device_config_status - uses the same test_device_name from above
        # print("\n--- Get Device Config Status ---")
        # if 'test_device_name' in locals() and test_device_name:
        #     print(f"Testing config status for device: {test_device_name}")
        #     config_status = get_device_config_status(device_name=test_device_name, adom="root")
        #     print(config_status)
        # else:
        #     print("Skipping get_device_config_status test as no device name was determined from list_devices.")
        
        # Test retrieve_device_config_from_device
        # print("\n--- Retrieve Device Config ---")
        # if 'test_device_name' in locals() and test_device_name:
        #     print(f"Attempting to retrieve config for device: {test_device_name}")
        #     retrieval_result = retrieve_device_config_from_device(device_name=test_device_name, adom="root")
        #     print(retrieval_result)
        # else:
        #     print("Skipping retrieve_device_config test as no device name was determined.")
        
        # Test list_device_interfaces
        # print("\n--- List Device Interfaces ---")
        # if 'test_device_name' in locals() and test_device_name:
        #     print(f"Listing interfaces for device: {test_device_name}")
        #     interfaces_result = list_device_interfaces(device_name=test_device_name, adom="root")
        #     if isinstance(interfaces_result, dict) and "interfaces" in interfaces_result:
        #         print(f"Found {interfaces_result['interface_count']} interfaces.")
        #         for iface in interfaces_result["interfaces"][:3]: # Print first 3 interfaces for brevity
        #             print(f"  - Name: {iface.get('name', 'N/A')}, IP: {iface.get('ip', 'N/A')}, Status: {iface.get('status', 'N/A')}")
        #         if interfaces_result['interface_count'] > 3:
        #             print(f"  ... and {interfaces_result['interface_count'] - 3} more.")
        #     else:
        #         print(interfaces_result) # Print error or other message
        # else:
        #     print("Skipping list_device_interfaces test as no device name was determined.")
        
        # Test get_device_routing_table
        # print("\n--- Get Device Routing Table ---")
        # if 'test_device_name' in locals() and test_device_name:
        #     print(f"Getting routing table for device: {test_device_name}")
        #     routing_table_result = get_device_routing_table(device_name=test_device_name, adom="root")
        #     if isinstance(routing_table_result, dict) and "routing_table" in routing_table_result:
        #         print(f"Found {routing_table_result.get('route_count', 0)} routes.")
        #         for route in routing_table_result["routing_table"][:5]: # Print first 5 routes
        #             print(f"  - Dest: {route.get('destination', 'N/A')}, Gateway: {route.get('gateway', 'N/A')}, Interface: {route.get('interface', 'N/A')}")
        #         if routing_table_result.get('route_count', 0) > 5:
        #             print(f"  ... and {routing_table_result['route_count'] - 5} more routes.")
        #     else:
        #         print(routing_table_result)
        # else:
        #     print("Skipping get_device_routing_table test as no device name was determined.")

        # Test get_policy_package_details
        # print("\n--- Get Policy Package Details ---")
        # if isinstance(packages, list) and len(packages) > 0 and isinstance(packages[0], dict) and 'name' in packages[0]:
        #     test_package_name = packages[0]['name'] # Use the first package from list_policy_packages for testing
        #     print(f"Getting details for policy package: {test_package_name}")
        #     package_details_result = get_policy_package_details(package_name=test_package_name, adom="root")
        #     print(package_details_result)
        # else:
        #     print("Skipping get_policy_package_details test as no package name could be determined automatically from list_policy_packages.")

        # Test list_firewall_policies
        # print("\n--- List Firewall Policies ---")
        # if 'test_package_name' in locals() and test_package_name: # Use package from previous test
        #     print(f"Listing firewall policies for package: {test_package_name}")
        #     firewall_policies_result = list_firewall_policies(package_name=test_package_name, adom="root")
        #     if isinstance(firewall_policies_result, dict) and "policies" in firewall_policies_result:
        #         print(f"Found {firewall_policies_result.get('policy_count', 0)} firewall policies.")
        #         test_policy_id = None
        #         for policy in firewall_policies_result["policies"][:3]: # Print first 3 policies
        #             print(f"  - Policy ID: {policy.get('policyid', 'N/A')}, Name: {policy.get('name', 'N/A')}, Action: {policy.get('action','N/A')}")
        #             if policy.get('policyid') is not None:
        #                 test_policy_id = policy.get('policyid') # Grab a policy ID for the next test
        #         if firewall_policies_result.get('policy_count', 0) > 3:
        #             print(f"  ... and {firewall_policies_result['policy_count'] - 3} more policies.")
        #
        #         # Test get_firewall_policy_details (uses test_policy_id from above)
        #         print("\n--- Get Firewall Policy Details ---")
        #         if test_policy_id is not None and 'test_package_name' in locals() and test_package_name:
        #             print(f"Getting details for policy ID: {test_policy_id} in package {test_package_name}")
        #             policy_detail_result = get_firewall_policy_details(policy_id=str(test_policy_id), package_name=test_package_name, adom="root")
        #             print(policy_detail_result)
        #         else:
        #             print("Skipping get_firewall_policy_details test as no policy_id or package_name was available.")
        #     else:
        #         print(firewall_policies_result)
        # else:
        #     print("Skipping list_firewall_policies test as no package_name was available.")

        # Test list_firewall_objects
        # print("\n--- List Firewall Objects (firewall/address) ---")
        # firewall_objects_result = list_firewall_objects(object_type="firewall/address", adom="root")
        # if isinstance(firewall_objects_result, dict) and "objects" in firewall_objects_result:
        #     print(f"Found {firewall_objects_result.get('object_count', 0)} firewall/address objects.")
        #     for obj in firewall_objects_result["objects"][:3]: # Print first 3 objects
        #         print(f"  - Name: {obj.get('name', 'N/A')}, Subnet: {obj.get('subnet', 'N/A')}, Type: {obj.get('type','N/A')}")
        #     if firewall_objects_result.get('object_count', 0) > 3:
        #         print(f"  ... and {firewall_objects_result['object_count'] - 3} more objects.")
        # else:
        #     print(firewall_objects_result)

        # print("\n--- List Firewall Objects (firewall/service/custom) ---")
        # custom_services_result = list_firewall_objects(object_type="firewall/service/custom", adom="root")
        # if isinstance(custom_services_result, dict) and "objects" in custom_services_result:
        #     print(f"Found {custom_services_result.get('object_count', 0)} firewall/service/custom objects.")
        #     for srv in custom_services_result["objects"][:3]: # Print first 3 objects
        #         print(f"  - Name: {srv.get('name', 'N/A')}, Protocol: {srv.get('protocol', 'N/A')}, TCP Portrange: {srv.get('tcp-portrange','N/A')}")
        #     if custom_services_result.get('object_count', 0) > 3:
        #         print(f"  ... and {custom_services_result['object_count'] - 3} more objects.")
        # else:
        #     print(custom_services_result)

        # Test get_firewall_object_details
        # print("\n--- Get Firewall Object Details (example: an address object) ---")
        # if isinstance(firewall_objects_result, dict) and \
        #    firewall_objects_result.get("objects") and \
        #    len(firewall_objects_result["objects"]) > 0 and \
        #    isinstance(firewall_objects_result["objects"][0], dict) and \
        #    'name' in firewall_objects_result["objects"][0]:
        #     test_object_name = firewall_objects_result["objects"][0]['name']
        #     test_object_type = "firewall/address" # Assuming the first list was for this type
        #     print(f"Getting details for object: {test_object_name}, type: {test_object_type}")
        #     object_detail_result = get_firewall_object_details(object_name=test_object_name, object_type=test_object_type, adom="root")
        #     print(object_detail_result)
        # else:
        #     print("Skipping get_firewall_object_details test as no object name/type could be determined from previous tests.")

        # Test query_firewall_policies
        # print("\n--- Query Firewall Policies (example: action=accept) ---")
        # if 'test_package_name' in locals() and test_package_name:
        #     print(f"Querying policies in package: {test_package_name} with action='accept'")
        #     query_result = query_firewall_policies(package_name=test_package_name, adom="root", action="accept")
        #     if isinstance(query_result, dict) and "policies" in query_result:
        #         print(f"Found {query_result.get('policy_count', 0)} policies matching criteria.")
        #         for policy in query_result["policies"][:3]: # Print first 3
        #             print(f"  - ID: {policy.get('policyid')}, Name: {policy.get('name')}, Action: {policy.get('action')}, Status: {policy.get('status')}")
        #     else:
        #         print(query_result)
        # else:
        #     print("Skipping query_firewall_policies test as no package_name was available.")

        # Test list_cli_scripts
        # print("\n--- List CLI Scripts (ADOM: root) ---")
        # cli_scripts_result = list_cli_scripts(adom="root")
        # if isinstance(cli_scripts_result, dict) and "scripts" in cli_scripts_result:
        #     print(f"Found {cli_scripts_result.get('script_count', 0)} CLI scripts.")
        #     for script in cli_scripts_result["scripts"][:3]: # Print first 3
        #         print(f"  - Name: {script.get('name')}, Description: {script.get('desc')}")
        # else:
        #     print(cli_scripts_result)

    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An error occurred during testing: {e}") 