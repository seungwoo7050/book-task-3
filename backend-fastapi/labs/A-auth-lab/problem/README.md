# Problem

Build a backend-only authentication service that focuses on local credentials rather than OAuth.

The lab should make these concerns explicit:

- password hashing and credential verification
- email verification before privileged login
- reset-token issuance and consumption
- session issuance using short-lived access tokens and rotating refresh tokens
- CSRF protection for state-changing cookie-authenticated requests
- predictable local developer experience for email testing

This lab intentionally excludes external identity providers and two-factor authentication. Those move to `B-federation-security-lab`.
