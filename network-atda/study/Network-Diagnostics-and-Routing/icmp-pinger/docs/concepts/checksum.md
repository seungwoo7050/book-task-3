# Internet Checksum Algorithm (RFC 1071)

## Purpose

The **Internet checksum** is used by ICMP, IP, TCP, and UDP to detect errors in transmitted data. It operates on 16-bit words and uses **one's complement arithmetic**.

## Algorithm

1. Divide the data into **16-bit (2-byte) words**
2. If the data has an odd number of bytes, pad with a zero byte
3. **Sum** all the 16-bit words using one's complement addition
4. **Fold** any carry bits back into the 16-bit sum
5. Take the **one's complement** (bitwise NOT) of the result

## Step-by-Step Example

Given data bytes: `45 00 00 3c 1c 46 40 00 40 06`

```
Step 1: Group into 16-bit words
  4500  003c  1c46  4000  4006

Step 2: Sum all words
  4500 + 003c + 1c46 + 4000 + 4006 = 0x0_F888

Step 3: Fold carries (upper 16 bits into lower 16)
  F888 + 0 = F888  (no carry in this example)

Step 4: One's complement
  ~F888 = 0777

Checksum = 0x0777
```

## Python Implementation

```python
def internet_checksum(data: bytes) -> int:
    """Compute the Internet checksum per RFC 1071.

    Args:
        data: The bytes to checksum.

    Returns:
        A 16-bit checksum value.
    """
    # Pad with a zero byte if odd length
    if len(data) % 2 != 0:
        data += b'\x00'

    # Sum all 16-bit words
    total = 0
    for i in range(0, len(data), 2):
        word = (data[i] << 8) + data[i + 1]
        total += word

    # Fold 32-bit sum to 16 bits (add carry)
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)

    # One's complement
    checksum = ~total & 0xFFFF
    return checksum
```

## Alternative Using `struct`

```python
import struct

def internet_checksum(data: bytes) -> int:
    if len(data) % 2 != 0:
        data += b'\x00'

    # Unpack all 16-bit words at once
    words = struct.unpack(f"!{len(data) // 2}H", data)
    total = sum(words)

    # Fold carries
    while total >> 16:
        total = (total & 0xFFFF) + (total >> 16)

    return ~total & 0xFFFF
```

## Verification

The checksum has a useful property: if you include the checksum in the data and recompute, the result should be **0** (or `0xFFFF` before complement):

```python
# Sender: compute checksum
header_no_checksum = struct.pack("!BBHHH", 8, 0, 0, id, seq)
cs = internet_checksum(header_no_checksum + payload)

# Receiver: verify
header_with_checksum = struct.pack("!BBHHH", 8, 0, cs, id, seq)
result = internet_checksum(header_with_checksum + payload)
assert result == 0  # Valid!
```

## Key Points

- The checksum is computed with the checksum field set to **0**
- Carry bits must be folded back into the 16-bit sum
- The final result is the **one's complement** (bitwise NOT)
- A valid packet's checksum verification yields **0**
- Byte order matters: use network byte order (big-endian)
