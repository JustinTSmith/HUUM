"""Client utilities for interacting with the HUUM sauna HTTP API.

This module consolidates the previous ad-hoc scripts into a reusable
client that exposes higher level methods for powering the sauna on or off
as well as querying its current status.  The client is designed to be used
from command line tools, web backends or other services (such as an Apple
Watch companion app).
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests
from requests import Response


class HuumAuthenticationError(RuntimeError):
    """Raised when authentication credentials are missing or invalid."""


class HuumApiError(RuntimeError):
    """Raised when the HUUM API returns a non-successful response."""


@dataclass
class HuumClient:
    """Light-weight wrapper around the HUUM REST API."""

    username: str
    password: str
    base_url: str = "https://api.huum.eu"
    timeout: Optional[float] = 10

    @classmethod
    def from_env(cls) -> "HuumClient":
        """Instantiate the client using the ``HUUM_USERNAME`` and
        ``HUUM_PASSWORD`` environment variables.

        Raises
        ------
        HuumAuthenticationError
            If either credential is missing.
        """

        username = os.getenv("HUUM_USERNAME")
        password = os.getenv("HUUM_PASSWORD")
        if not username or not password:
            raise HuumAuthenticationError(
                "HUUM_USERNAME and HUUM_PASSWORD environment variables must be set"
            )
        return cls(username=username, password=password)

    def _request(self, method: str, path: str, **kwargs: Any) -> Dict[str, Any]:
        url = f"{self.base_url}{path}"
        response = requests.request(
            method,
            url,
            auth=(self.username, self.password),
            timeout=self.timeout,
            **kwargs,
        )
        self._raise_for_status(response)
        try:
            return response.json()
        except ValueError as exc:  # pragma: no cover - defensive
            raise HuumApiError("HUUM API returned a non-JSON response") from exc

    def _raise_for_status(self, response: Response) -> None:
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:  # pragma: no cover - defensive
            try:
                payload = response.json()
            except ValueError:
                payload = response.text
            raise HuumApiError(
                f"HUUM API request failed with status {response.status_code}: {payload}"
            ) from exc

    def start_sauna(self, target_temperature: int) -> Dict[str, Any]:
        """Start the sauna and set a target temperature.

        The HUUM API accepts temperatures between 40°C and 110°C.
        """

        if not 40 <= target_temperature <= 110:
            raise ValueError("target_temperature must be between 40 and 110 Celsius")

        payload = {"targetTemperature": target_temperature}
        return self._request("POST", "/action/home/start", data=payload)

    def stop_sauna(self) -> Dict[str, Any]:
        """Turn the sauna off."""

        return self._request("POST", "/action/home/stop")

    def get_status(self) -> Dict[str, Any]:
        """Fetch the sauna's current status information."""

        return self._request("GET", "/action/home/status")
