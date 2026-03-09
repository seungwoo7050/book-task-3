# A-auth-lab Docs

## Concepts

- local credential lifecycle
- verification and reset token handling
- refresh-token family rotation
- cookie + CSRF pairing

## Notes

The FastAPI app stores sent messages in an in-memory mailbox during tests, while the local Compose stack includes Mailpit for manual inspection.
