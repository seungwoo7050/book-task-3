"""
Unreliable Channel Simulator (Provided — Do NOT Modify)

Simulates an unreliable network channel that can:
  - Lose packets (drop them entirely)
  - Corrupt packets (flip bits in the payload)
  - Delay packets (add random latency)

Usage:
    from channel import UnreliableChannel
    ch = UnreliableChannel(loss_rate=0.2, corrupt_rate=0.1)
    ch.send(packet)        # may lose or corrupt
    pkt = ch.receive()     # may return None (lost) or corrupted packet
"""

import random
import time
from typing import Optional


class UnreliableChannel:
    """Simulates an unreliable network channel.

    Attributes:
        loss_rate: Probability of packet loss (0.0 to 1.0).
        corrupt_rate: Probability of packet corruption (0.0 to 1.0).
        delay_range: Tuple (min, max) delay in seconds.
    """

    def __init__(
        self,
        loss_rate: float = 0.2,
        corrupt_rate: float = 0.1,
        delay_range: tuple[float, float] = (0.01, 0.05),
    ) -> None:
        self.loss_rate = loss_rate
        self.corrupt_rate = corrupt_rate
        self.delay_range = delay_range
        self._buffer: list[bytes] = []

    def send(self, packet: bytes) -> None:
        """Send a packet through the unreliable channel.

        The packet may be lost, corrupted, or delayed.

        Args:
            packet: The raw packet bytes to send.
        """
        # Simulate delay
        delay = random.uniform(*self.delay_range)
        time.sleep(delay)

        # Simulate loss
        if random.random() < self.loss_rate:
            print(f"  [CHANNEL] Packet LOST (simulated)")
            return

        # Simulate corruption
        if random.random() < self.corrupt_rate:
            corrupted = self._corrupt(packet)
            print(f"  [CHANNEL] Packet CORRUPTED (simulated)")
            self._buffer.append(corrupted)
            return

        # Packet delivered successfully
        self._buffer.append(packet)

    def receive(self) -> Optional[bytes]:
        """Receive a packet from the channel.

        Returns:
            The packet bytes, or None if no packet is available.
        """
        if self._buffer:
            return self._buffer.pop(0)
        return None

    def has_packet(self) -> bool:
        """Check if there is a packet waiting in the channel."""
        return len(self._buffer) > 0

    @staticmethod
    def _corrupt(data: bytes) -> bytes:
        """Flip a random bit in the data to simulate corruption."""
        if not data:
            return data
        data_arr = bytearray(data)
        idx = random.randint(0, len(data_arr) - 1)
        bit = random.randint(0, 7)
        data_arr[idx] ^= (1 << bit)
        return bytes(data_arr)
