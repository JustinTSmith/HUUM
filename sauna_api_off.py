"""CLI helper to stop the HUUM sauna."""
from __future__ import annotations

from huum_client import HuumClient, HuumAuthenticationError


def main() -> None:
    client = HuumClient.from_env()
    response = client.stop_sauna()
    print(response)


if __name__ == "__main__":  # pragma: no cover - CLI entry point
    try:
        main()
    except HuumAuthenticationError as exc:
        raise SystemExit(str(exc))
