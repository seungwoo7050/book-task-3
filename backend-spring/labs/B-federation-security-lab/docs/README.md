# B-federation-security-lab Notes

## Implemented now

- Google authorize URL generation and callback-shaped linking flow
- TOTP setup and verify example flow
- in-memory audit event recording

## Important simplifications

- Google integration is mocked at contract level only
- TOTP codes are generated for readability, not security hardness
- throttling is still a documented concern rather than a hard enforcement layer

## Next improvements

- use Spring Security OAuth2 client with real provider configuration
- store provider subject and audit events in PostgreSQL
- add rate-limit middleware backed by Redis
