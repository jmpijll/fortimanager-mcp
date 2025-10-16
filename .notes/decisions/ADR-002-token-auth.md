# ADR-002: Token-Based Authentication

## Status
Accepted

## Context
FortiManager supports multiple authentication methods for API access:
1. **Session-based authentication**: Username/password login that returns a session ID
2. **Token-based authentication**: Pre-generated API tokens (available since FMG 7.2.2)
3. **FortiManager Cloud OAuth**: Multi-step OAuth flow for cloud instances

We need to choose the primary authentication method for the MCP server while considering security, automation, and ease of use.

## Decision
Use **API token-based authentication** as the primary method, with **session-based authentication** as a fallback option.

## Rationale

### Token-Based Authentication (Primary)

#### Advantages
1. **Automation-Friendly**: No interactive login required, perfect for server-to-server communication
2. **Permanent Tokens**: Tokens don't expire unless manually regenerated
3. **No Session Management**: No need to track session expiration or renewal
4. **Simpler Implementation**: Just add token to HTTP header or query string
5. **Better for Stateless Design**: Aligns with stateless HTTP transport model
6. **Security**: Can be rotated without changing application code

#### Implementation
```python
# Token in HTTP Authorization header (preferred)
headers = {
    "Authorization": f"Bearer {api_token}"
}

# Or token in query string
url = f"https://{host}/jsonrpc?access_token={api_token}"
```

### Session-Based Authentication (Fallback)

#### When to Use
- FortiManager version < 7.2.2 (no API token support)
- User preference or existing infrastructure
- Testing scenarios

#### Disadvantages
- Requires explicit login/logout operations
- Session tracking and management needed
- Sessions can expire during operation
- More complex error handling (re-authentication on session expiry)

### Cloud OAuth Not Supported
We explicitly decided **not to support** FortiManager Cloud OAuth in the initial version:
- Multi-step process (get FortiCloud token → exchange for FMG session)
- Different API endpoints and payloads
- Adds complexity for a niche use case
- Can be added in future version if needed

## Configuration

Environment variables:
```bash
# Primary method
FORTIMANAGER_API_TOKEN=your-api-token-here

# Fallback method
FORTIMANAGER_USERNAME=admin
FORTIMANAGER_PASSWORD=your-password
```

Authentication priority:
1. If `FORTIMANAGER_API_TOKEN` is set → use token-based auth
2. If both `FORTIMANAGER_USERNAME` and `FORTIMANAGER_PASSWORD` are set → use session-based auth
3. Otherwise → error

## Consequences

### Positive
- Simpler codebase (token auth is straightforward)
- Better alignment with automation and DevOps practices
- Stateless design enables easy horizontal scaling
- No session expiration concerns
- Cleaner error handling

### Negative
- Requires FortiManager 7.2.2+ for token support
- Need fallback implementation for older versions
- Token rotation requires updating configuration

### Security Considerations
- Tokens stored as environment variables (not in code)
- Support for SSL/TLS verification
- Tokens should be treated as sensitive credentials
- Recommend using Docker secrets or Kubernetes secrets in production
- Log sanitization to prevent token leakage

## Implementation Notes

### Token Generation on FortiManager
```bash
# Create API user
config system admin user
    edit api_user_001
        set user_type api
        set rpc-permit read-write
    next
end

# Generate token
execute api-user generate-key api_user_001
# Output: New API key: 33fzwipq4amujunzgzn46mg1to9p8wbi
```

### Session-Based Fallback
The client will:
1. Attempt token auth first if token is configured
2. Fall back to session-based auth if username/password provided
3. Auto-logout on shutdown (for session-based only)
4. Handle session expiration gracefully with re-authentication

## Future Enhancements
- Add FortiManager Cloud OAuth support if requested
- Implement token refresh mechanism for future FMG versions
- Add support for certificate-based authentication if available

## References
- [FortiManager API Token Documentation](https://docs.fortinet.com/document/fortimanager/7.2.0/new-features/047777/fortimanager-supports-authentication-token-for-api-administrators-7-2-2)
- FortiManager-how-to-guide: `001_fmg_json_api_introduction.rst` (lines 134-198)
- Security best practices for API token management

