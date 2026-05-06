#!/usr/bin/env python3
"""Smoke test the Kiwi.com Tequila API.

Verifies the provided API key works and that /locations/query and /v2/search
return the response shapes the brief documents.

Usage: uv run python scripts/smoke_kiwi.py
"""

from __future__ import annotations

import os
import sys
from datetime import date, timedelta

import requests

BASE_URL = "https://tequila-api.kiwi.com"


def main() -> int:
    api_key = os.environ.get("KIWI_API_KEY")
    if not api_key:
        print("[smoke] KIWI_API_KEY is not set", file=sys.stderr)
        return 1
    session = requests.Session()
    session.headers.update({"apikey": api_key, "Content-Type": "application/json"})

    print(f"[smoke] API key tail: ...{api_key[-6:]}\n")

    print("[1/2] GET /locations/query?term=London")
    try:
        resp = session.get(
            f"{BASE_URL}/locations/query",
            params={"term": "London", "location_types": "airport", "limit": 3},
            timeout=15,
        )
        resp.raise_for_status()
        airports = resp.json().get("locations", [])
        if not airports:
            print("       FAIL: no airports returned")
            return 1
        a = airports[0]
        print(f"       OK: {len(airports)} airports, top: {a['code']} ({a['name']})")
        print(f"       lat/lon: ({a['location']['lat']}, {a['location']['lon']})")
    except Exception as e:
        print(f"       FAIL: {e}")
        return 1

    today, tomorrow = date.today(), date.today() + timedelta(days=1)
    fmt = "%d/%m/%Y"  # Kiwi uses dd/mm/yyyy, not ISO

    print("\n[2/2] GET /v2/search LHR to CDG (today/tomorrow, USD)")
    try:
        resp = session.get(
            f"{BASE_URL}/v2/search",
            params={
                "fly_from": "LHR",
                "fly_to": "CDG",
                "date_from": today.strftime(fmt),
                "date_to": tomorrow.strftime(fmt),
                "curr": "USD",
                "flight_type": "oneway",
                "one_for_city": 1,
                "adults": 1,
                "limit": 1,
            },
            timeout=30,
        )
        resp.raise_for_status()
        body = resp.json()
        flights = body.get("data", [])
        if not flights:
            print("       OK: empty result (key works, no 24h availability)")
            return 0
        f = flights[0]
        print(f"       OK: {f['cityFrom']} to {f['cityTo']}")
        print(
            f"       price: ${f['price']}, "
            f"distance: {f['distance']} km, "
            f"currency: {body.get('currency')}"
        )
    except Exception as e:
        print(f"       FAIL: {e}")
        return 1

    print("\nAPI is alive.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
