"""Minimal Flask application exposing HUUM sauna controls.

This server can be deployed as a lightweight bridge between the HUUM API
and an Apple Watch companion app.  By hosting it on a network accessible by
the watch (or its paired iPhone) we can issue authenticated requests to the
HUUM cloud without embedding credentials directly in the watch app.
"""
from __future__ import annotations

import os
from http import HTTPStatus
from typing import Any, Dict

from flask import Flask, jsonify, request

from huum_client import HuumAuthenticationError, HuumClient

app = Flask(__name__)


@app.route("/api/sauna/start", methods=["POST"])
def start_sauna() -> Any:
    payload: Dict[str, Any] = request.get_json(force=True, silent=True) or {}
    try:
        target_temperature = int(payload.get("targetTemperature"))
    except (TypeError, ValueError):
        return jsonify({"error": "targetTemperature must be an integer"}), HTTPStatus.BAD_REQUEST

    client = HuumClient.from_env()
    try:
        response = client.start_sauna(target_temperature)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), HTTPStatus.BAD_REQUEST
    return jsonify(response)


@app.route("/api/sauna/stop", methods=["POST"])
def stop_sauna() -> Any:
    client = HuumClient.from_env()
    response = client.stop_sauna()
    return jsonify(response)


@app.route("/api/sauna/status", methods=["GET"])
def status() -> Any:
    client = HuumClient.from_env()
    response = client.get_status()
    return jsonify(response)


@app.errorhandler(HuumAuthenticationError)
def handle_auth_error(error: HuumAuthenticationError):
    return jsonify({"error": str(error)}), HTTPStatus.UNAUTHORIZED


if __name__ == "__main__":  # pragma: no cover - manual execution helper
    port = int(os.getenv("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
