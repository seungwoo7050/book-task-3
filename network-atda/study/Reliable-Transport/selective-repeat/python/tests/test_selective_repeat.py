"""Selective Repeat unit tests."""

from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT / "python" / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "problem" / "code"))

from channel import UnreliableChannel
from selective_repeat import load_messages, selective_repeat_send_receive


def test_selective_repeat_delivers_all_messages_without_loss():
    messages = ["A", "B", "C", "D"]
    delivered = selective_repeat_send_receive(
        UnreliableChannel(loss_rate=0.0, corrupt_rate=0.0),
        UnreliableChannel(loss_rate=0.0, corrupt_rate=0.0),
        messages,
        window_size=3,
    )
    assert delivered == messages


def test_message_fixture_is_available():
    messages = load_messages()
    assert messages
    assert all(messages)
