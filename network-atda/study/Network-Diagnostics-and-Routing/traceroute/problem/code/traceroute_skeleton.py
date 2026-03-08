"""
Traceroute — Skeleton Code

Usage:
    sudo python3 traceroute_skeleton.py <host>
"""

import argparse


def trace_route(host: str, max_hops: int = 30, probes_per_hop: int = 3) -> None:
    """Send UDP probes with increasing TTL values and report each hop.

    TODO:
      1. Resolve the destination host
      2. Send UDP probes with a different destination port per probe
      3. Listen for ICMP replies on a raw socket
      4. Match the embedded UDP destination port back to the probe
      5. Stop once the destination sends Port Unreachable
    """
    raise NotImplementedError


def main() -> None:
    parser = argparse.ArgumentParser(description="Traceroute skeleton")
    parser.add_argument("host", help="Target hostname or IP address")
    parser.add_argument("--max-hops", type=int, default=30)
    parser.add_argument("--probes", type=int, default=3)
    args = parser.parse_args()
    trace_route(args.host, args.max_hops, args.probes)


if __name__ == "__main__":
    main()
