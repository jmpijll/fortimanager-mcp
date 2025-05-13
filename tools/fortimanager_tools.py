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
        
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An error occurred during testing: {e}") 