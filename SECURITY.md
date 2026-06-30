# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in AGENSTAB, please report it responsibly.

**Email:** security@agenstab.com

**Do NOT:**
- Open a public GitHub issue for security vulnerabilities
- Disclose the vulnerability publicly before we've had time to address it

**We will:**
- Acknowledge receipt within 24 hours
- Provide an initial assessment within 72 hours
- Work with you on a coordinated disclosure timeline

## Scope

The following are in scope for security reports:
- AGENSTAB Engine (WebSocket API, session management, action execution)
- SDK clients (Python, Node.js, Go)
- Chrome Extension
- Authentication and authorization flows

## Out of Scope
- Social engineering attacks
- Denial of service attacks
- Issues in third-party dependencies (report these upstream)

## Encryption

All audit logs are encrypted using AWS KMS AES-256-GCM envelope encryption. Session data follows a zero-retention policy — it is not persisted after session termination.
