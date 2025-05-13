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
from fortimanager_api import FortiManagerAPI  # Official library name to be confirmed
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
    fmg_api_key = os.getenv("FORTIMANAGER_API_KEY")

    if not fmg_host or not fmg_api_key:
        raise ValueError("FORTIMANAGER_HOST and FORTIMANAGER_API_KEY must be set in .env file.")

    # Disable InsecureRequestWarning if SSL verification is off
    # This is common for lab/dev environments. In production, use proper SSL certs.
    verify_ssl_env = os.getenv("FORTIMANAGER_VERIFY_SSL", "false").lower()
    verify_ssl = verify_ssl_env == "true"
    
    if not verify_ssl:
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    try:
        # Assuming the library uses 'api_key' for token authentication
        # and has parameters like 'use_ssl' and 'verify_ssl'.
        # These are common but need to be confirmed with python-fortimanagerapi docs.
        fmg_client = FortiManagerAPI(
            host=fmg_host,
            api_key=fmg_api_key,
            use_ssl=True, # Assuming HTTPS is preferred
            verify_ssl=verify_ssl, # Set to True in production with proper certs
            timeout=10 # Default timeout
        )
        # Some libraries might require an explicit login call even with an API key
        # e.g., fmg_client.login() or fmg_client.login_with_apikey(fmg_api_key)
        # For now, assuming constructor handles it or it's not needed for API key auth.
        print(f"Successfully initialized FortiManager API client for host: {fmg_host}")
        return fmg_client
    except Exception as e:
        print(f"Error initializing FortiManager API client: {e}")
        # Potentially re-raise or handle more gracefully
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

# Example usage (for testing locally, not part of MCP normally)
if __name__ == '__main__':
    try:
        print("Attempting to initialize client and fetch data...")
        # Ensure .env file has FORTIMANAGER_HOST and FORTIMANAGER_API_KEY
        
        # Test list_devices
        print("\n--- List Devices (ADOM: root) ---")
        devices = list_devices(adom="root")
        print(devices)

        # Test get_system_status
        print("\n--- Get System Status ---")
        status = get_system_status()
        print(status)
        
    except ValueError as ve:
        print(f"Configuration Error: {ve}")
    except Exception as e:
        print(f"An error occurred during testing: {e}") 