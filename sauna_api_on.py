"""CLI helper to start the HUUM sauna."""
from __future__ import annotations

import argparse

from huum_client import HuumClient, HuumAuthenticationError


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "temperature",
        type=int,
        help="Target temperature in Celsius",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    client = HuumClient.from_env()
    try:
        response = client.start_sauna(args.temperature)
    except ValueError as exc:
        raise SystemExit(str(exc))
    print(response)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    try:
        main()
    except HuumAuthenticationError as exc:
        raise SystemExit(str(exc))
