# HUUM Sauna Controller Toolkit

This repository bundles a small Python toolkit that makes it easier to
control a HUUM sauna from scripts, backend services or companion
applications such as an Apple Watch app.

## Features

* Reusable `HuumClient` class that wraps the HUUM public API
* Command line interfaces to start, stop and inspect the sauna status
* Optional Flask bridge that exposes authenticated REST endpoints your
  watch app can call without embedding HUUM credentials
* Sample watchOS SwiftUI project illustrating how to connect to the bridge

## Prerequisites

The HUUM API uses HTTP basic authentication. Store your credentials in the
following environment variables before running any of the tools:

```bash
export HUUM_USERNAME="your-huum-email"
export HUUM_PASSWORD="your-huum-password"
```

Install Python dependencies:

```bash
pip install -r requirements.txt
```

`requirements.txt` lists `requests` for the client and `flask` for the
optional API bridge.

## Command line tools

```bash
# Turn the sauna on and set the target temperature to 80°C
python sauna_api_on.py 80

# Turn the sauna off
python sauna_api_off.py

# Fetch the current status including temperature
python sauna_api_status.py
```

Each command prints the JSON payload returned by the HUUM API.

## Flask bridge for companion apps

The Apple Watch app can communicate with a small Flask service that lives on
a computer or Raspberry Pi in your local network.  The bridge translates
simple HTTP requests into authenticated HUUM API calls.

```bash
export FLASK_APP=api_server.py
flask run --host=0.0.0.0 --port=5000
```

The server exposes three endpoints:

* `POST /api/sauna/start` – Request body `{"targetTemperature": 80}`
* `POST /api/sauna/stop`
* `GET /api/sauna/status`

All responses mirror the HUUM API JSON structure, including the current
and target temperatures. Secure the server behind VPN or another auth layer
before exposing it to the Internet.

## Apple Watch sample app

The `watchos/HuumSaunaWatchApp` folder contains a minimal SwiftUI project
that calls the Flask bridge.  Update the `BridgeConfiguration.bridgeURL`
value in `SaunaViewModel.swift` with the URL where your Flask server is
hosted.
Build the project with Xcode 15 or newer and deploy to your watch.

The sample interface offers three actions:

* Toggle the sauna on or off
* Adjust the target temperature using a stepper control
* Display the live temperature reported by the HUUM API

Refer to the inline comments in the Swift files for guidance on adapting the
UI to your needs.
