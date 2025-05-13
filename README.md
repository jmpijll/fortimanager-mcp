# 🧠 FortiManager MCP Server 🎉

Welcome to the FortiManager MCP Server project! This server leverages the power of the [FastMCP library](https://github.com/context-labs/fastmcp) to bridge the gap between Large Language Models (LLMs) and your FortiManager instance. Imagine effortlessly querying device statuses, listing policy packages, and eventually automating complex network tasks, all through a conversational AI or other MCP-compatible clients! 🚀

## 🎯 Project Goal

To expose FortiManager API functionalities as a suite of intuitive MCP tools. This enables seamless integration with AI assistants and automation scripts, paving the way for:

*   Automated network management tasks.
*   Intelligent information retrieval from FortiManager.
*   Configuration changes driven by natural language or programmatic MCP calls.
*   Enhanced operational efficiency and responsiveness.

## ✨ Key Libraries

*   **Python**: 3.10+ (as recommended for FastMCP)
*   **FastMCP**: The core library for building and running the MCP server.
*   **pyfmg**: The Python library used to interact with the FortiManager JSON RPC API.
*   **python-dotenv**: For managing environment variables and keeping your credentials secure.

## 📂 Directory Structure

A quick overview of how the project is organized:

```
.
├── .git/                # Git repository data
├── .gitignore           # Specifies intentionally untracked files that Git should ignore
├── README.md            # This amazing file you're reading!
├── example.env          # Example environment variables file
├── main.py              # Main MCP server application (starts FastMCP)
├── requirements.txt     # Python package dependencies
└── tools/
    ├── __init__.py      # Makes 'tools' a Python package
    └── fortimanager_tools.py # Module for all FortiManager-related MCP tools
```

## 🚀 Getting Started

Ready to unleash the power? Here's how to get up and running:

### 1. Prerequisites

*   **Python 3.10 or higher**: Download from [python.org](https://www.python.org/) if you haven't already.
*   **Git**: For cloning and managing versions.
*   **Access to a FortiManager instance**: You'll need its IP address/hostname and an API key.
    *   Ensure the API key has the necessary permissions for the tools you intend to use (e.g., read access to devices, system status, etc.).

### 2. Clone the Repository (if you haven't)

If you're setting this up from scratch on a new machine:
```bash
git clone <your-repository-url>
cd <repository-directory-name>
```

### 3. Set up a Python Virtual Environment (Recommended)

This keeps your project dependencies isolated.
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 4. Install Dependencies

Install all the necessary Python packages:
```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Sensitive information like API keys and hostnames should be stored in environment variables.

1.  **Create a `.env` file**: Copy the example file:
    ```bash
    cp example.env .env
    ```
2.  **Edit `.env`**: Open the newly created `.env` file and fill in your FortiManager details:
    ```
    FORTIMANAGER_HOST="your_fortimanager_ip_or_hostname"
    FORTIMANAGER_API_KEY="your_fortimanager_api_key"
    # FORTIMANAGER_ADOM="root" # Default is 'root', uncomment and change if needed for specific tools
    # FORTIMANAGER_VERIFY_SSL="false" # Set to "true" in production with proper certs. Defaults to "false".
    ```
    *   **`FORTIMANAGER_HOST`**: The IP address or fully qualified domain name (FQDN) of your FortiManager.
    *   **`FORTIMANAGER_API_KEY`**: The API key generated from your FortiManager for an admin user with appropriate permissions.
    *   **`FORTIMANAGER_VERIFY_SSL`**: (Optional) Set to `"true"` if your FortiManager has a valid SSL certificate from a trusted CA. Defaults to `"false"` (which will disable SSL warnings for self-signed certificates). **For production, always use valid certificates and set this to `"true"`**.

    🔒 **Important**: The `.env` file is included in `.gitignore` by default to prevent accidental commitment of your credentials.

## 🛠️ Running the Server

Once configured, you can start the MCP server. The `main.py` script is set up to run using FastMCP.

*   **For development (with auto-reload and a web interface for testing):**
    ```bash
    fastmcp dev main.py
    ```
    This will typically start a web server (e.g., on `http://localhost:8000`) where you can see the MCP server's capabilities and test tools.

*   **To run normally (e.g., for client connections):**
    ```bash
    python main.py
    ```
    This will start the server, usually using the stdio transport by default, unless configured otherwise in `main.py`. The server will print its name and available tools upon startup.

## 🤖 Using with MCP Clients

This server exposes its tools via the Model Context Protocol. You can connect to it using various MCP-compatible clients:

*   **AI Assistants / Chatbots**: Some advanced AI assistants can be configured to use MCP servers as tool providers. You would typically point the assistant to the running server's address (e.g., `http://localhost:8000` if running with HTTP transport, or via its installed name if using `fastmcp install`).
*   **Automation Scripts**: Custom Python scripts can use the `fastmcp.client` module to interact with the server programmatically.
*   **Other MCP-Compliant Applications**: Any application that speaks MCP can potentially use the tools provided by this server.

**General Steps for Client Connection (will vary by client):**

1.  Ensure the FortiManager MCP Server is running.
2.  Configure your MCP client with the server's address and port if it's running with a network transport (like HTTP).
3.  If you used `fastmcp install main.py`, the client might discover it by its registered name (`FortiManagerMCPServer`).
4.  The client should then be able to list and execute the available tools.

## ✨ Available Tools

Here are the tools currently implemented and ready for use:

1.  **`list_fortimanager_devices`**
    *   **Description**: Lists devices in FortiManager, optionally filtered by ADOM. Requires FORTIMANAGER_HOST and FORTIMANAGER_API_KEY in .env file. ADOM defaults to 'root' if not provided.
    *   **Parameters**: `adom` (string, optional, default: "root") - The Administrative Domain to query.
    *   **Returns**: A list of device details or an error message.

2.  **`get_fortimanager_system_status`**
    *   **Description**: Retrieves the system status from FortiManager. Requires FORTIMANAGER_HOST and FORTIMANAGER_API_KEY in .env file.
    *   **Parameters**: None.
    *   **Returns**: System status information or an error message.

3.  **`list_fortimanager_policy_packages`**
    *   **Description**: Lists policy packages in FortiManager for a specific ADOM. Requires FORTIMANAGER_HOST and FORTIMANAGER_API_KEY in .env file. ADOM defaults to 'root' if not provided.
    *   **Parameters**: `adom` (string, optional, default: "root") - The Administrative Domain to query.
    *   **Returns**: A list of policy package details or an error message.

*(More tools to come!)*

## 🔮 Future Enhancements

This project is just getting started! Here are some ideas for future development:

*   **More Tools!**
    *   Get detailed device information (config, interfaces, etc.).
    *   List and inspect policy packages and firewall policies.
    *   Retrieve script execution status.
    *   Manage ADOMs.
    *   Install policy packages or device settings.
    *   Retrieve FortiGuard status and package versions.
*   **Advanced Error Handling**: More specific error codes and messages from API interactions.
*   **Tool Input Validation**: Stricter validation for tool parameters.
*   **Configuration for Different ADOMs**: Easier way to specify ADOMs for tools.
*   **Write Operations**: Carefully implement tools that make changes to FortiManager (e.g., adding objects, modifying policies) with appropriate safeguards.

## 🤝 Contributing

Contributions are welcome! If you have ideas for new tools, improvements, or bug fixes, please feel free to:

1.  Fork the repository.
2.  Create a new branch for your feature (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add some amazing feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Open a Pull Request.

## ❓ Troubleshooting Tips

Encountering issues? Here are a few common things to check:

*   **`.env` File**:
    *   Ensure your `.env` file exists in the project root and is correctly named.
    *   Verify that `FORTIMANAGER_HOST` and `FORTIMANAGER_API_KEY` are correctly set and have no typos.
    *   Make sure there are no extra spaces or quotes around the values unless they are part of the actual credentials.
*   **FortiManager Connectivity**:
    *   Can the machine running the MCP server reach the `FORTIMANAGER_HOST`? Try a simple `ping` or `curl` to the FortiManager IP/hostname.
    *   Check for any firewalls blocking communication between the server and FortiManager.
*   **API Key Permissions**:
    *   Does the API key used have sufficient permissions on FortiManager to perform the actions required by the tools? (e.g., read access for devices, system status).
    *   Is the API key enabled and valid?
*   **Python Dependencies**:
    *   Did `pip install -r requirements.txt` complete without errors?
    *   Are you in the correct Python virtual environment?
*   **`pyfmg` Library**:
    *   The server relies on `pyfmg`. If you suspect issues with it, ensure it's installed correctly. The error messages from `tools/fortimanager_tools.py` might give clues.
*   **SSL Verification (`FORTIMANAGER_VERIFY_SSL`)**:
    *   If `FORTIMANAGER_VERIFY_SSL="true"`, ensure your FortiManager has a valid SSL certificate trusted by the machine running the server.
    *   If using a self-signed certificate, set `FORTIMANAGER_VERIFY_SSL="false"` for testing/development, but be aware of the security implications.
*   **FastMCP Server Logs**:
    *   When you run `fastmcp dev main.py` or `python main.py`, check the terminal output for any error messages from FastMCP or the tools themselves.
*   **Tool Errors**:
    *   If a specific tool returns an error, the error message might indicate whether the problem is with the API call, missing parameters, or FortiManager itself. The `list_...` and `get_...` tools usually return a string with an error message if something goes wrong.

---

Let's make FortiManager management smarter and more accessible! ✨ 