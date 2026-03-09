# Problem

Build a realtime backend slice that can:

- authenticate a WebSocket connection
- maintain short-lived presence state
- fan out notifications to connected clients
- expose reconnect-friendly HTTP surfaces for presence and event publication

The lab uses in-memory runtime state during tests, while the local stack still exposes Redis as the natural scaling boundary.
