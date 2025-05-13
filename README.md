# FortiManager MCP Server

This project aims to create an MCP (Model Context Protocol) server for interacting with a FortiManager instance using the FastMCP library. This will allow LLMs to leverage FortiManager's capabilities through a standardized interface.

## Project Goal

To expose FortiManager API functionalities as MCP tools, enabling automated network management tasks, information retrieval, and configuration changes through conversational AI or other MCP clients.

## Initial Setup

- Python version: 3.10+ (as required by FastMCP)
- Key library: `fastmcp`
- FortiManager interaction: `python-fortimanagerapi` (or similar, to be confirmed)

## Directory Structure

```
.gitignore
README.md
requirements.txt
main.py               # Main MCP server application
tools/
  __init__.py
  fortimanager_tools.py # Module for FortiManager related MCP tools
```

## Planning: Initial MCP Tools

The following are suggestions for initial simple tools to implement for testing and basic functionality. These will help establish the connection to FortiManager and the basic structure for adding more complex tools later.

1.  **List Devices (`list_devices`)**
    *   **Description**: Retrieves a list of all devices managed by FortiManager.
    *   **FortiManager API Interaction**: Likely uses an API endpoint to get all managed devices (e.g., `/dvmdb/device`).
    *   **Parameters**: None (or optional: ADOM name).
    *   **Returns**: A list of device names or a list of objects with device details (name, IP, model, status).

2.  **Get Device Status (`get_device_status`)**
    *   **Description**: Fetches the current operational status of a specific device.
    *   **FortiManager API Interaction**: API endpoint to get specific device details or status (e.g., `/dvmdb/device/{device_name}/status` - specific endpoint needs verification).
    *   **Parameters**: `device_name` (string) or `device_id` (string/int).
    *   **Returns**: String indicating status (e.g., "Up", "Down", "Unknown") or a more detailed status object.

3.  **List Policy Packages (`list_policy_packages`)**
    *   **Description**: Retrieves a list of policy packages within a specific ADOM (Administrative Domain).
    *   **FortiManager API Interaction**: API endpoint to list policy packages (e.g., `/pm/pkg/{adom_name}`).
    *   **Parameters**: `adom_name` (string).
    *   **Returns**: A list of policy package names or objects with package details.

## Future Expansion Ideas

*   Tool for retrieving device configuration.
*   Tool for checking firewall policy by source/destination/service.
*   Tool for installing policy packages to devices.
*   Tool for retrieving FortiGuard status.
*   Resource for ADOM list.

## Development Notes

*   Ensure FortiManager API credentials and address are configurable (e.g., via environment variables or a config file not committed to git).
*   Implement robust error handling for API interactions.
*   Follow FastMCP best practices for defining tools and resources. 