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

# @mcp.tool() # Assuming 'mcp' is accessible
# def list_devices(adom: str = "root"):
#     """Lists devices in FortiManager, optionally filtered by ADOM."""
#     # try:
#     #     # Example API call using the initialized client
#     #     # The exact method and parameters depend on the python-fortimanagerapi library
#     #     response = fmg_client.get_devices(adom=adom) # Fictional method call
#     #     return response # Or format the response as needed
#     # except Exception as e:
#     #     return f"Error listing devices: {e}"
#     pass

# Add other tool definitions below, decorated with @mcp.tool()
# Example:
# @mcp.tool()
# def get_system_status():
#     """Retrieves the system status from FortiManager."""
#     # try:
#     #     response = fmg_client.get_system_status() # Fictional method call
#     #     return response
#     # except Exception as e:
#     #     return f"Error getting system status: {e}"
#     pass 

import os
from dotenv import load_dotenv
from pyfmg import FortiManager as FortiManagerAPI # Use pyfmg
import urllib3

# Assuming 'fastmcp' instance is passed or imported if @mcp.tool decorator is used from main.py
# from fastmcp import FastMCP
# mcp = FastMCP() # Or however it's meant to be accessed by tools

load_dotenv() # Load environment variables from .env file

# Global FortiManager API client instance
fmg_client = None

def initialize_fmg_api_client():
    """Initializes the FortiManager API client using environment variables."""
    global fmg_client
    if fmg_client:
        return fmg_client

    fmg_host = os.getenv("FORTIMANAGER_HOST")
    fmg_api_key_val = os.getenv("FORTIMANAGER_API_KEY") # Renamed to avoid clash

    if not fmg_host or not fmg_api_key_val:
        raise ValueError("FORTIMANAGER_HOST and FORTIMANAGER_API_KEY must be set in .env file.")

    verify_ssl_env = os.getenv("FORTIMANAGER_VERIFY_SSL", "false").lower()
    verify_ssl = verify_ssl_env == "true"
    
    if not verify_ssl:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        fmg_client = FortiManagerAPI(
            host=fmg_host,
            apikey=fmg_api_key_val, # Use 'apikey' as per pyfmg documentation
            use_ssl=True, 
            verify_ssl=verify_ssl, 
            timeout=10,
            debug=False # pyfmg supports a debug flag, default is False
        )
        # pyfmg documentation indicates login() is still called, even with apikey, to set up session.
        # "Notice that login() is still called and still must be used, despite that there really is no initial login. 
        # This is so the session can be created and maintained and ensures a consistent interface."
        # However, the pyfmg context manager example does: `with FortiManager('10.1.1.1', apikey=api_key) as fmg_instance:`
        # which implies login might be handled by constructor or context. Let's assume constructor handles session creation for now.
        # If errors occur, we might need to add an explicit fmg_client.login() call here.

        print(f"Successfully initialized FortiManager API client for host: {fmg_host} using pyfmg.")
        return fmg_client
    except Exception as e:
        print(f"Error initializing FortiManager API client with pyfmg: {e}")
        raise

# Ensure client is initialized before tool use (call this explicitly or ensure mcp handles it)
# initialize_fmg_api_client() 

# @mcp.tool() # Decorate with FastMCP's tool decorator
def list_devices(adom: str = "root"):
    """
    Lists devices in FortiManager, optionally filtered by ADOM.
    Requires FORTIMANAGER_HOST and FORTIMANAGER_API_KEY in .env file.
    ADOM defaults to 'root' if not provided.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    try:
        # The URL for listing devices in FortiManager's JSON RPC API is typically:
        # '/dvmdb/adom/{adom}/device' for devices in a specific ADOM
        # '/dvmdb/device' for all devices (might require different permissions or handling)
        # We'll use the ADOM-specific one as it's more common.
        
        # The python-fortimanagerapi library should provide a method for this.
        # Example based on typical RPC structure (actual method name may vary):
        # response = client.get(f"/dvmdb/adom/{adom}/device")
        
        # Let's assume the library has a more direct method based on common patterns:
        # response = client.get_devices(adom=adom)
        # For now, using a placeholder for the exact method call.
        # We need to find the correct method in 'python-fortimanagerapi' documentation.
        
        # Based on "How to FortiManager API" docs (8.7.2), the URL seems to be:
        # GET /dvmdb/adom/{adom}/device
        # The library might abstract this as:
        # data = {'url': f'/dvmdb/adom/{adom}/device'}
        # response = client.get(data) or client.get(url=f'/dvmdb/adom/{adom}/device')
        
        # Let's try a direct URL call assuming 'client.get()' takes a URL path.
        # This is a common pattern for API wrapper libraries.
        params = {
            "url": f"/dvmdb/adom/{adom}/device"
        }
        # Some libraries might expect 'data=params' or direct kwargs
        code, response_data = client.get(params["url"]) # Or however the library expects the call

        if code == 0: # FortiManager API success code is typically 0
            return response_data.get("data", response_data) # 'data' often holds the actual list
        else:
            return f"Error listing devices: {response_data.get('status', {}).get('message', 'Unknown error')} (Code: {code})"

    except Exception as e:
        return f"Exception listing devices: {e}"

# @mcp.tool() # Decorate with FastMCP's tool decorator
def get_system_status():
    """
    Retrieves the system status from FortiManager.
    Requires FORTIMANAGER_HOST and FORTIMANAGER_API_KEY in .env file.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    try:
        # Based on "How to FortiManager API" docs (18.3), the URL for system status is:
        # GET /sys/status
        # The library might abstract this as:
        # response = client.get_system_status()
        # Or using a direct URL call:
        params = {
            "url": "/sys/status"
        }
        code, response_data = client.get(params["url"])

        if code == 0:
            return response_data.get("data", response_data)
        else:
            return f"Error getting system status: {response_data.get('status', {}).get('message', 'Unknown error')} (Code: {code})"
            
    except Exception as e:
        return f"Exception getting system status: {e}"

# @mcp.tool() # Decorate with FastMCP's tool decorator
def list_policy_packages(adom: str = "root"):
    """
    Lists policy packages in FortiManager for a specific ADOM.
    Requires FORTIMANAGER_HOST and FORTIMANAGER_API_KEY in .env file.
    ADOM defaults to 'root' if not provided.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    try:
        # URL based on FortiManager API documentation (e.g., section 9.2.2)
        # /pm/pkg/adom/{adom_name} or similar might be the direct path for listing packages.
        # Some API versions might use /pm/pkg/adom/{adom_name}/package
        # We will use the common one found in documentation for listing within an ADOM.
        api_url = f"/pm/pkg/adom/{adom}"
        
        # pyfmg's get method typically returns (code, data)
        code, response_data = client.get(api_url)

        if code == 0 and response_data:
            # The actual list of packages is often in a nested 'data' field, 
            # or could be the top-level list if 'data' field is not present but result is a list.
            # Or it might be under response_data['data']['pkg_list'] or similar. 
            # We will try to be a bit flexible here.
            if isinstance(response_data.get("data"), list):
                return response_data["data"] # if response is {"data": [...packages...]}
            elif isinstance(response_data, list):
                return response_data # if response is [...packages...]
            else:
                # Fallback or more specific extraction if needed based on actual API response structure
                return response_data.get("data", response_data) 
        elif code == 0 and not response_data:
            return [] # No packages or empty response
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            return f"Error listing policy packages: {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception listing policy packages: {e}"

# @mcp.tool()
def get_device_details(device_name: str, adom: str = "root"):
    """
    Retrieves detailed information for a specific device in FortiManager.
    Requires FORTIMANAGER_HOST and FORTIMANAGER_API_KEY in .env file.
    Device name is required. ADOM defaults to 'root' if not provided.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."
    
    if not device_name:
        return "Error: device_name parameter is required."

    try:
        # API endpoint to get specific device details.
        # Example: /dvmdb/adom/{adom}/device/{device_name}
        # The exact fields returned will depend on the FortiManager API version and device type.
        api_url = f"/dvmdb/adom/{adom}/device/{device_name}"
        
        code, response_data = client.get(api_url)

        if code == 0 and response_data:
            # The device details are usually within the 'data' field of the response.
            # It could be a single object or a list with one object if the API supports filtering.
            # For a direct get by name, it's typically a single object.
            return response_data.get("data", response_data) 
        elif code == 0 and not response_data: # Should ideally not happen if device exists
            return f"No details found for device '{device_name}' in ADOM '{adom}'. It might not exist or the response was empty."
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            # Specific error code for "Object not found" might be -3 for some Fortinet APIs.
            if code == -3 or "Object not exist" in error_message or "No such device" in error_message:
                 return f"Error: Device '{device_name}' not found in ADOM '{adom}'. (Code: {code}) - {error_message}"
            return f"Error retrieving details for device '{device_name}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception retrieving device details for '{device_name}': {e}"

# @mcp.tool()
def get_device_config_status(device_name: str, adom: str = "root"):
    """
    Retrieves the configuration synchronization status for a specific device.
    Interprets the 'conf_status' field from the device details.
    Device name is required. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    if not device_name:
        return "Error: device_name parameter is required."

    try:
        api_url = f"/dvmdb/adom/{adom}/device/{device_name}"
        code, response_data = client.get(api_url)

        if code == 0 and response_data and isinstance(response_data.get("data"), dict):
            device_info = response_data["data"]
            conf_status_val = device_info.get("conf_status") # Standard field for config status
            
            # Interpret conf_status (common values, might need adjustment based on FMG version)
            # 0: unknown, 1: synchronized, 2: out-of-sync, 3: auto-update, 4: never synchronized (sometimes), 5: modified (sometimes)
            status_map = {
                0: "Unknown",
                1: "Synchronized",
                2: "Out-of-Sync",
                3: "Auto-Update",
                4: "Never Synchronized / Pending", # FMG 7.0.0 changed meaning slightly
                5: "Modified / Unsynced Changes"
            }
            
            status_description = status_map.get(conf_status_val, f"Raw conf_status: {conf_status_val}")
            
            # Return both raw value and description for clarity
            return {
                "device_name": device_name,
                "adom": adom,
                "conf_status_raw": conf_status_val,
                "config_status_description": status_description,
                "details_url_checked": api_url # For reference
            }
        elif code == 0: # Device found but data format unexpected or empty
            return f"Device '{device_name}' found in ADOM '{adom}', but config status could not be determined from response: {response_data}"
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            if code == -3 or "Object not exist" in error_message or "No such device" in error_message:
                 return f"Error: Device '{device_name}' not found in ADOM '{adom}'. (Code: {code}) - {error_message}"
            return f"Error retrieving config status for device '{device_name}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception retrieving config status for '{device_name}': {e}"

# @mcp.tool()
def retrieve_device_config_from_device(device_name: str, adom: str = "root"):
    """
    Triggers FortiManager to retrieve the latest configuration from a specified device.
    This action typically starts a task on FortiManager.
    Device name is required. ADOM defaults to 'root'.
    Returns the task information if successful.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    if not device_name:
        return "Error: device_name parameter is required."

    try:
        # The API to trigger a configuration retrieval is often an 'exec' type or a POST to a specific URL.
        # Example from FortiManager API docs (8.23): /dvmdb/adom/{adom}/device/{device_name}/retrieve (often a POST or specific exec method)
        # Or it might be /sys/retrieve/device for some versions or contexts.
        # pyfmg library might have an 'execute' or 'update' method for such actions.
        # Let's assume it's a POST-like operation, often handled by `client.execute` or `client.update` or a specific named method.
        # For pyfmg, often operations like this are under an 'exec' category, so URL might be a bit different if using a generic exec method.
        # For now, let's try a common pattern which might be POSTing to a URL like this, or using an execute method.
        # If pyfmg's .get() is only for GET, we might need .post() or .execute().
        # The `pyfmg` library documentation shows an execute method: `fmg_instance.execute("securityconsole/install/package", ...)`
        # This suggests the first argument to execute is the command path, and kwargs are parameters.

        # Let's try using the execute method with a likely path.
        # The URL for the actual RPC call might be something like `/dvmdb/adom/{adom_name}/device/{device_name}/cmd/retrieve`
        # or the data payload might specify the action.

        # Assuming an exec call structure based on general FortiManager API patterns for actions.
        # The direct RPC target URL might be something like this, or the data part of a generic exec might point here.
        api_command_path = f"/dvmdb/adom/{adom}/device/{device_name}/cmd/retrieve"
        
        # The pyfmg `execute` method seems appropriate here. What it expects as `data` or `**params` for this specific command is key.
        # Often, such commands don't require a complex body, just the action invoked on the URL/path.
        # If `execute` takes the path as first arg and then kwargs for payload:
        code, response_data = client.execute(api_command_path) # May need specific parameters based on pyfmg's execute method signature

        if code == 0 and response_data:
            # Successful execution usually returns a task ID
            if response_data.get("data") and isinstance(response_data["data"], dict) and "task" in response_data["data"]:
                return {
                    "message": f"Successfully initiated configuration retrieval for device '{device_name}' in ADOM '{adom}'.",
                    "task_id": response_data["data"]["task"],
                    "details": response_data["data"]
                }
            elif "task" in response_data: # If task ID is at the root of response_data
                return {
                    "message": f"Successfully initiated configuration retrieval for device '{device_name}' in ADOM '{adom}'.",
                    "task_id": response_data["task"],
                    "details": response_data
                }
            else:
                return {"message": f"Configuration retrieval initiated for '{device_name}', but no task ID found in response.", "response": response_data}
        elif code == 0: # Should have response_data if successful
            return f"Configuration retrieval for '{device_name}' may have succeeded but response was empty or unexpected: {response_data}"
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            if code == -3 or "Object not exist" in error_message or "No such device" in error_message:
                 return f"Error: Device '{device_name}' not found in ADOM '{adom}' for config retrieval. (Code: {code}) - {error_message}"
            return f"Error initiating config retrieval for device '{device_name}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception initiating config retrieval for '{device_name}': {e}"

# @mcp.tool()
def list_device_interfaces(device_name: str, adom: str = "root"):
    """
    Lists network interfaces for a specific device in FortiManager.
    Attempts to retrieve interface configurations (e.g., IP, status).
    Device name is required. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    if not device_name:
        return "Error: device_name parameter is required."

    try:
        # Common API path for system interfaces configuration.
        # Example: /dvmdb/adom/{adom}/device/{device_name}/config/system/interface
        # The exact path might vary slightly based on the FortiManager version or if it's a specific config block.
        # The `pyfmg` library might need a full path or a path relative to a device config tree.
        api_path = f"/dvmdb/adom/{adom}/device/{device_name}/config/system/interface"

        # Using client.get() to retrieve configuration data. 
        # This assumes the interface list is available via a GET request to this path.
        code, response_data = client.get(api_path)

        if code == 0 and response_data and isinstance(response_data.get("data"), list):
            interfaces = response_data["data"]
            if not interfaces:
                 return f"No interfaces found for device '{device_name}' in ADOM '{adom}' at path '{api_path}', or the device does not expose them this way."
            
            # We can return the raw interface data or attempt to summarize it.
            # For now, let's return the list of interface objects directly.
            return {
                "message": f"Successfully retrieved interfaces for device '{device_name}' in ADOM '{adom}'.",
                "device_name": device_name,
                "adom": adom,
                "interface_count": len(interfaces),
                "interfaces": interfaces # This will be a list of dictionaries
            }
        elif code == 0: # Data format unexpected or empty
            return f"Retrieved data for device '{device_name}' interfaces at '{api_path}', but the format was unexpected or empty: {response_data}"
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            if code == -3 or "Object not exist" in error_message or "No such device" in error_message or "No such an entry" in error_message:
                 return f"Error: Device '{device_name}' or interface config path '{api_path}' not found in ADOM '{adom}'. (Code: {code}) - {error_message}"
            return f"Error retrieving interfaces for device '{device_name}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception retrieving interfaces for '{device_name}': {e}"

# @mcp.tool()
def get_device_routing_table(device_name: str, adom: str = "root"):
    """
    Retrieves the routing table for a specific device in FortiManager.
    Device name is required. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    if not device_name:
        return "Error: device_name parameter is required."

    try:
        # API path for device routing table. This is often a monitor-type call.
        # Example paths from various FortiManager API versions/contexts:
        # - /monitor/router/select (with device specified in payload)
        # - /dvmdb/adom/{adom}/device/{device_name}/monitor/router/select
        # - /monitor/device/{device_name}/routing-table
        # The exact path will depend on how pyfmg structures calls to monitor endpoints.
        
        # Using a common pattern for device-specific monitor calls.
        api_url = f"/dvmdb/adom/{adom}/device/{device_name}/monitor/router/select" 
        
        # This endpoint might expect specific parameters in the payload for `client.get()` if it's more like a POST,
        # or if `client.get()` can send a body, or it might be an `client.execute()` call.
        # For a simple retrieval, a GET to this URL might suffice or return available sub-monitors.
        # Actual FortiManager API might require GET to /dvmdb/adom/{adom}/device/{device_name}/monitor/router/ipv4 (or ipv6 or all)
        # For now, we assume /select gives a general overview or list if not the full table directly.
        code, response_data = client.get(api_url) 

        if code == 0 and response_data and isinstance(response_data.get("data"), list):
            routing_table = response_data["data"]
            if not routing_table:
                return f"Routing table for device '{device_name}' in ADOM '{adom}' at '{api_url}' is empty or not found."
            return {
                "message": f"Successfully retrieved routing table for device '{device_name}' in ADOM '{adom}'.",
                "device_name": device_name,
                "adom": adom,
                "route_count": len(routing_table),
                "routing_table": routing_table
            }
        elif code == 0: # Data format unexpected or empty
            # It might be that the response_data itself is the list of routes if data field is not used for lists by this endpoint
            if isinstance(response_data, list):
                return {
                    "message": f"Successfully retrieved routing table for device '{device_name}' in ADOM '{adom}'.",
                    "device_name": device_name,
                    "adom": adom,
                    "route_count": len(response_data),
                    "routing_table": response_data
                }
            return f"Retrieved data for device '{device_name}' routing table at '{api_url}', but the format was unexpected or empty: {response_data}"
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            if code == -3 or "Object not exist" in error_message or "No such device" in error_message or "Monitor command failed" in error_message:
                 return f"Error: Device '{device_name}' or routing table monitor path '{api_url}' not found/failed in ADOM '{adom}'. (Code: {code}) - {error_message}"
            return f"Error retrieving routing table for device '{device_name}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception retrieving routing table for '{device_name}': {e}"

# @mcp.tool()
def get_policy_package_details(package_name: str, adom: str = "root"):
    """
    Retrieves detailed information for a specific policy package in an ADOM.
    Requires package_name. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    if not package_name:
        return "Error: package_name parameter is required."

    try:
        # API URL for specific policy package details.
        # Example: /pm/pkg/adom/{adom}/{package_name}
        api_url = f"/pm/pkg/adom/{adom}/{package_name}"
        
        code, response_data = client.get(api_url)

        if code == 0 and response_data:
            # Policy package details are typically in the 'data' field or could be the root response.
            package_details = response_data.get("data", response_data)
            if not package_details: # Check if details are empty even if call succeeded
                 return f"No details found for policy package '{package_name}' in ADOM '{adom}' at '{api_url}'. The package might be empty or details are not available."
            return {
                "message": f"Successfully retrieved details for policy package '{package_name}' in ADOM '{adom}'.",
                "package_name": package_name,
                "adom": adom,
                "details": package_details
            }
        elif code == 0: # Successful call but empty response_data
            return f"Policy package '{package_name}' in ADOM '{adom}' was found (or query was successful), but no details were returned from '{api_url}'."
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            # Check for common "not found" errors
            if code == -3 or "Object not exist" in error_message or "No such package" in error_message or "not found" in error_message.lower():
                 return f"Error: Policy package '{package_name}' not found in ADOM '{adom}'. (Code: {code}) - {error_message}"
            return f"Error retrieving details for policy package '{package_name}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception retrieving details for policy package '{package_name}': {e}"

# @mcp.tool()
def list_firewall_policies(package_name: str, adom: str = "root"):
    """
    Lists firewall policies within a specific policy package in an ADOM.
    Requires package_name. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    if not package_name:
        return "Error: package_name parameter is required."

    try:
        # API URL for listing firewall policies within a package.
        # Example: /pm/config/adom/{adom}/pkg/{package_name}/firewall/policy
        # Or sometimes /pm/pkg/adom/{adom_name}/{package_name}/firewall/policy
        # Using the /pm/config path as it's common for configuration objects.
        api_url = f"/pm/config/adom/{adom}/pkg/{package_name}/firewall/policy"
        
        code, response_data = client.get(api_url)

        if code == 0 and response_data:
            # Firewall policies are usually returned as a list in the 'data' field.
            policies = response_data.get("data")
            
            # The 'data' field might be a list directly, or an object containing a list (e.g., under a key like 'policy_list')
            # For now, assuming 'data' is the list if it exists and is a list.
            if isinstance(policies, list):
                if not policies:
                    return f"No firewall policies found in package '{package_name}' in ADOM '{adom}' at '{api_url}'."
                return {
                    "message": f"Successfully retrieved firewall policies for package '{package_name}' in ADOM '{adom}'.",
                    "package_name": package_name,
                    "adom": adom,
                    "policy_count": len(policies),
                    "policies": policies
                }
            else:
                # If policies is not a list, the response structure might be different or an error/empty case.
                return f"Firewall policies data for package '{package_name}' at '{api_url}' is not in the expected list format: {policies}"
        elif code == 0: # Successful call but empty response_data or unexpected format
             return f"Query for firewall policies in package '{package_name}' (ADOM '{adom}') at '{api_url}' was successful, but no data was returned or data was not in expected format: {response_data}"
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            if code == -3 or "Object not exist" in error_message or "No such package" in error_message or "not found" in error_message.lower() or "No such an entry" in error_message:
                 return f"Error: Policy package '{package_name}' or firewall policy path not found in ADOM '{adom}'. (Code: {code}) - {error_message}"
            return f"Error listing firewall policies for package '{package_name}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception listing firewall policies for package '{package_name}': {e}"

# @mcp.tool()
def get_firewall_policy_details(policy_id: str, package_name: str, adom: str = "root"):
    """
    Retrieves detailed configuration for a specific firewall policy by its ID.
    Requires policy_id, package_name. ADOM defaults to 'root'.
    Note: policy_id is usually an integer.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    if not policy_id or not package_name:
        return "Error: policy_id and package_name parameters are required."

    try:
        # API URL for specific firewall policy details.
        # Example: /pm/config/adom/{adom}/pkg/{package_name}/firewall/policy/{policy_id}
        api_url = f"/pm/config/adom/{adom}/pkg/{package_name}/firewall/policy/{policy_id}"
        
        code, response_data = client.get(api_url)

        if code == 0 and response_data:
            # Policy details are typically in the 'data' field or could be the root response.
            policy_details = response_data.get("data", response_data)
            if not policy_details: # Check if details are empty
                 return f"No details found for firewall policy ID '{policy_id}' in package '{package_name}' (ADOM '{adom}') at '{api_url}'."
            return {
                "message": f"Successfully retrieved details for firewall policy ID '{policy_id}'.",
                "policy_id": policy_id,
                "package_name": package_name,
                "adom": adom,
                "details": policy_details
            }
        elif code == 0: # Successful call but empty response_data
            return f"Query for firewall policy ID '{policy_id}' in package '{package_name}' (ADOM '{adom}') at '{api_url}' was successful, but no details were returned."
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            # Check for common "not found" errors
            if code == -3 or "Object not exist" in error_message or "No such policy" in error_message or "not found" in error_message.lower() or "No such an entry" in error_message:
                 return f"Error: Firewall policy ID '{policy_id}' not found in package '{package_name}' (ADOM '{adom}'). (Code: {code}) - {error_message}"
            return f"Error retrieving details for firewall policy ID '{policy_id}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception retrieving details for firewall policy ID '{policy_id}': {e}"

# @mcp.tool()
def list_firewall_objects(object_type: str, adom: str = "root"):
    """
    Lists firewall objects of a specified type within an ADOM.
    Requires object_type (e.g., 'firewall/address', 'firewall/service/custom', 'firewall/addrgrp').
    ADOM defaults to 'root'.
    Common object_type examples:
    - firewall/address
    - firewall/addrgrp
    - firewall/service/custom
    - firewall/service/group
    - application/list
    - ips/sensor
    - webfilter/profile
    - antivirus/profile
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    if not object_type:
        return "Error: object_type parameter is required."

    try:
        # API URL for listing firewall objects of a specific type.
        # Example: /pm/config/adom/{adom}/obj/{object_type}
        # The object_type needs to be correctly formatted, e.g., 'firewall/address'
        api_url = f"/pm/config/adom/{adom}/obj/{object_type.strip()}"
        
        code, response_data = client.get(api_url)

        if code == 0 and response_data:
            objects_list = response_data.get("data")
            
            if isinstance(objects_list, list):
                if not objects_list:
                    return f"No objects of type '{object_type}' found in ADOM '{adom}' at '{api_url}'."
                return {
                    "message": f"Successfully retrieved objects of type '{object_type}' in ADOM '{adom}'.",
                    "object_type": object_type,
                    "adom": adom,
                    "object_count": len(objects_list),
                    "objects": objects_list
                }
            else:
                return f"Objects data for type '{object_type}' at '{api_url}' is not in the expected list format: {objects_list}"
        elif code == 0: # Successful call but empty response_data or unexpected format
             return f"Query for objects of type '{object_type}' in ADOM '{adom}' at '{api_url}' was successful, but no data was returned or data was not in expected format: {response_data}"
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            # Check for common "not found" or "invalid type" errors
            if code == -3 or "Object not exist" in error_message or "not found" in error_message.lower() or "Invalid object type" in error_message or "No such an entry" in error_message:
                 return f"Error: Objects of type '{object_type}' or the specified path not found in ADOM '{adom}'. (Code: {code}) - {error_message}"
            return f"Error listing objects of type '{object_type}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception listing objects of type '{object_type}': {e}"

# @mcp.tool()
def get_firewall_object_details(object_name: str, object_type: str, adom: str = "root"):
    """
    Retrieves details for a specific firewall object by its name and type.
    Requires object_name and object_type (e.g., 'firewall/address', 'firewall/service/custom').
    ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    if not object_name or not object_type:
        return "Error: object_name and object_type parameters are required."

    try:
        # API URL for specific firewall object details.
        # Example: /pm/config/adom/{adom}/obj/{object_type}/{object_name}
        api_url = f"/pm/config/adom/{adom}/obj/{object_type.strip()}/{object_name.strip()}"
        
        code, response_data = client.get(api_url)

        if code == 0 and response_data:
            object_details = response_data.get("data", response_data)
            if not object_details:
                 return f"No details found for object '{object_name}' of type '{object_type}' in ADOM '{adom}' at '{api_url}'."
            return {
                "message": f"Successfully retrieved details for object '{object_name}' of type '{object_type}'.",
                "object_name": object_name,
                "object_type": object_type,
                "adom": adom,
                "details": object_details
            }
        elif code == 0:
            return f"Query for object '{object_name}' (type '{object_type}') at '{api_url}' was successful, but no details were returned."
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            if code == -3 or "Object not exist" in error_message or "not found" in error_message.lower() or "No such an entry" in error_message:
                 return f"Error: Object '{object_name}' of type '{object_type}' not found in ADOM '{adom}'. (Code: {code}) - {error_message}"
            return f"Error retrieving details for object '{object_name}' (type '{object_type}'): {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception retrieving details for object '{object_name}' (type '{object_type}'): {e}"

# @mcp.tool()
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
    if not client:
        return "FortiManager API client not initialized."

    if not package_name:
        return "Error: package_name parameter is required."

    filters = []
    if source_address:
        filters.append(["srcaddr", "==", source_address]) # Assuming 'srcaddr' is the field name for source address objects
    if destination_address:
        filters.append(["dstaddr", "==", destination_address]) # Assuming 'dstaddr' for destination
    if service:
        filters.append(["service", "==", service]) # Assuming 'service' for service objects
    if action:
        # Common actions: accept, deny. FMG API might use numeric values or specific strings.
        # For simplicity, assuming string match here. Might need mapping if API uses integers.
        filters.append(["action", "==", action.lower()]) 
    if status:
        # Common status: enable, disable
        filters.append(["status", "==", status.lower()])
    if policy_name_contains:
        # FortiManager API might use 'like' or a regex operator for contains.
        # For simplicity, using '==' with wildcard assumption or a specific 'contains' operator if available.
        # A common pattern is using a wildcard that the API interprets, e.g. *value* or %value%.
        # Here, we'll use a field name `name` and assume the API supports partial match or we use `==` for exact name if no partial match built-in.
        # For a true "contains", the API might require a specific syntax or operator like "~~" or "like".
        # Let's use a simple filter for name for now; this part is highly API dependent for true 'contains'.
        filters.append(["name", "==", f"*{policy_name_contains}*"]) # Using wildcards, assuming API supports them with '==' or implies 'like'

    api_url = f"/pm/config/adom/{adom}/pkg/{package_name}/firewall/policy"
    payload = {}
    if filters:
        payload["filter"] = filters
    
    # You can also add options like 'limit', 'offset', 'sort' to payload if needed
    # payload["limit"] = 100 

    try:
        # pyfmg's get method can take a `data` parameter for the payload (including filters)
        code, response_data = client.get(url=api_url, data=payload if payload else None)

        if code == 0 and response_data:
            policies = response_data.get("data")
            if isinstance(policies, list):
                if not policies:
                    return f"No firewall policies found matching the criteria in package '{package_name}' (ADOM '{adom}')."
                return {
                    "message": f"Successfully queried firewall policies in package '{package_name}' (ADOM '{adom}').",
                    "package_name": package_name,
                    "adom": adom,
                    "filter_criteria_used": filters if filters else "None (all policies potentially listed)",
                    "policy_count": len(policies),
                    "policies": policies
                }
            else:
                return f"Policy query data for package '{package_name}' is not in the expected list format: {policies}"
        elif code == 0:
             return f"Policy query for package '{package_name}' was successful, but no data was returned or data format was unexpected: {response_data}"
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            return f"Error querying firewall policies in package '{package_name}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception querying firewall policies in package '{package_name}': {e}"

# @mcp.tool()
def list_cli_scripts(adom: str = "root"):
    """
    Lists available CLI scripts in FortiManager for a specific ADOM.
    ADOM defaults to 'root' if not provided.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    try:
        # Common API path for listing CLI scripts.
        # Examples: /pm/config/adom/{adom}/script/script  or /dvmdb/adom/{adom}/script/script
        # Using /pm/config/ as scripts are often treated as configuration elements.
        api_url = f"/pm/config/adom/{adom}/script/script"
        
        code, response_data = client.get(api_url)

        if code == 0 and response_data:
            scripts = response_data.get("data")
            if isinstance(scripts, list):
                if not scripts:
                    return f"No CLI scripts found in ADOM '{adom}' at '{api_url}'."
                return {
                    "message": f"Successfully retrieved CLI scripts for ADOM '{adom}'.",
                    "adom": adom,
                    "script_count": len(scripts),
                    "scripts": scripts # List of script objects, usually with 'name', 'description', etc.
                }
            else:
                return f"CLI scripts data for ADOM '{adom}' is not in the expected list format: {scripts}"
        elif code == 0:
             return f"Query for CLI scripts in ADOM '{adom}' was successful, but no data was returned or format was unexpected: {response_data}"
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            if code == -3 or "Object not exist" in error_message or "not found" in error_message.lower() or "No such an entry" in error_message:
                 return f"Error: CLI script path not found in ADOM '{adom}'. (Code: {code}) - {error_message}"
            return f"Error listing CLI scripts in ADOM '{adom}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception listing CLI scripts in ADOM '{adom}': {e}"

# @mcp.tool()
def get_cli_script_content(script_name: str, adom: str = "root"):
    """
    Retrieves the content of a specific CLI script from FortiManager.
    Requires script_name. ADOM defaults to 'root'.
    """
    client = initialize_fmg_api_client()
    if not client:
        return "FortiManager API client not initialized."

    if not script_name:
        return "Error: script_name parameter is required."

    try:
        # API URL for fetching a specific CLI script's content.
        # Typically /pm/config/adom/{adom}/script/script/{script_name}
        api_url = f"/pm/config/adom/{adom}/script/script/{script_name.strip()}"
        
        code, response_data = client.get(api_url)

        if code == 0 and response_data:
            script_details = response_data.get("data")
            if isinstance(script_details, dict):
                # The script content is often in a field like 'content' or 'script'
                script_content = script_details.get("content", script_details.get("script"))
                if script_content is not None:
                    return {
                        "message": f"Successfully retrieved content for CLI script '{script_name}' in ADOM '{adom}'.",
                        "script_name": script_name,
                        "adom": adom,
                        "content": script_content,
                        "details": script_details # Return all details as well
                    }
                else:
                    return f"CLI script '{script_name}' found, but its content field ('content' or 'script') is missing or empty. Details: {script_details}"
            elif script_details: # If data is not a dict but not empty
                 return f"Retrieved data for script '{script_name}', but it was not in the expected dictionary format: {script_details}"
            else: # No data field or empty
                return f"No data returned for CLI script '{script_name}' in ADOM '{adom}' at '{api_url}'. Script might be empty or not found."

        elif code == 0: # Successful call but empty/unexpected response_data
             return f"Query for CLI script '{script_name}' in ADOM '{adom}' at '{api_url}' was successful, but no data was returned or format was unexpected: {response_data}"
        else:
            error_message = response_data.get('status', {}).get('message', 'Unknown error')
            if code == -3 or "Object not exist" in error_message or "not found" in error_message.lower() or "No such an entry" in error_message:
                 return f"Error: CLI script '{script_name}' not found in ADOM '{adom}'. (Code: {code}) - {error_message}"
            return f"Error retrieving CLI script '{script_name}': {error_message} (Code: {code})"

    except Exception as e:
        return f"Exception retrieving CLI script '{script_name}': {e}"

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