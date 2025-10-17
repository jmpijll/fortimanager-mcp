# Security Policy

## Supported Versions

This project is currently in beta.

- Current supported version: `v0.1.0-beta`
- Security fixes are applied to the latest beta release only

## Reporting a Vulnerability

We take security seriously. If you believe you have found a security vulnerability:

1. Please do not create a public issue.
2. Report privately using GitHub Security Advisories (preferred) or contact the repository owner (`jmpijll`) via their GitHub profile email.
3. Include detailed steps to reproduce, affected versions, and any relevant logs.

## Response Timeline

- Acknowledgement: within 3 business days
- Initial assessment: within 7 business days
- Targeted fix or mitigation plan: within 14 business days

These timelines may vary depending on severity and complexity.

## Disclosure Policy

- We follow responsible disclosure practices.
- We will work with you to validate and remediate the issue.
- Public disclosure will occur after a fix or mitigation is available, or as mutually agreed.

## Security Best Practices for Users

- Prefer token-based authentication over username/password when possible
- Restrict FortiManager API access to trusted networks
- Use least-privilege credentials for testing
- Store secrets in environment variables; never commit credentials
- Keep Docker images up to date and rebuild regularly

## Cryptography and Dependencies

- Dependencies are pinned by major versions in `pyproject.toml`
- We prefer standard library and security-focused packages
- Docker images are built via CI with reproducible steps
