# A-auth-lab Notes

## Implemented now

- local account register, login, refresh, logout, and `me` endpoints
- refresh rotation and CSRF mismatch example flow
- Mailpit-ready Compose stack for local email-oriented exercises

## Important simplifications

- password hashing is modeled in memory rather than persisted through a real user table
- cookie handling is represented at API shape level instead of full browser integration
- verification and reset links are not backed by a full mail-delivery lifecycle yet

## Next improvements

- persist users, verification tokens, and refresh token families
- move cookie behavior from JSON response modeling to actual response cookies
- add reset and verify endpoints instead of documenting them only
