# Python Threading for Concurrent Connections

## Overview

When a web server uses a single thread, it can only handle one client at a time — while processing one request, all other clients must wait. The `threading` module allows the server to handle each client connection in a **separate thread**, enabling concurrent request processing.

## Why Threading?

```
Without threading:          With threading:
                            
Client A ───────►           Client A ───────►  Thread 1
     Client B waits...      Client B ───────►  Thread 2
          Client C waits... Client C ───────►  Thread 3
```

## Basic Thread Creation

```python
import threading

def worker(name):
    print(f"Thread {name} running")

# Create and start a thread
t = threading.Thread(target=worker, args=("A",))
t.start()
```

- `target`: The function to run in the new thread
- `args`: A tuple of arguments to pass to the function
- `start()`: Begins execution of the thread

## Using Threads in a Server

The pattern for a multi-threaded server:

```python
import socket
import threading

def handle_client(conn, addr):
    """Process one client connection."""
    data = conn.recv(4096)
    # ... process request and send response ...
    conn.close()

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(('', 6789))
server.listen(5)

while True:
    conn, addr = server.accept()
    # Spawn a new thread for each connection
    t = threading.Thread(target=handle_client, args=(conn, addr))
    t.daemon = True   # Thread dies when main thread exits
    t.start()
```

## Daemon Threads

```python
t.daemon = True  # Set BEFORE calling t.start()
```

A **daemon thread** runs in the background and is automatically terminated when the main program exits. This is ideal for connection handler threads — if the server shuts down (e.g., via Ctrl+C), all active handlers are cleaned up automatically.

Without daemon threads, the program would wait for all threads to finish before exiting.

## Thread Safety Considerations

For this simple web server, thread safety is rarely an issue because each thread:
- Works on its **own** connection socket
- Reads its **own** local file independently
- Has no shared mutable state with other threads

However, be aware that:
- Printing from multiple threads can cause interleaved output (cosmetic, not functional)
- If you add caching or logging to shared data structures, you would need `threading.Lock()`

## Key API Reference

| Function / Method | Description |
| :--- | :--- |
| `threading.Thread(target, args)` | Create a new thread |
| `thread.start()` | Begin execution |
| `thread.join(timeout)` | Wait for thread to finish |
| `thread.daemon` | If `True`, thread dies when main exits |
| `threading.active_count()` | Number of alive threads |
| `threading.Lock()` | Create a mutex lock |
