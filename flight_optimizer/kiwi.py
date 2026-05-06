from __future__ import annotations

import os
from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

import requests

BASE_URL = "https://tequila-api.kiwi.com"
_DATE_FMT = "%d/%m/%Y"  # Kiwi requires dd/mm/yyyy, not ISO


@dataclass(frozen=True)
class City:
    code: str
    name: str
    lat: float
    lon: float

    @property
    def coords(self) -> tuple[float, float]:
        return (self.lat, self.lon)


@dataclass(frozen=True)
class FlightOption:
    fly_from_airport: str
    fly_to_airport: str
    city_code_to: str
    city_name_to: str
    price_usd: float


class KiwiAPIError(RuntimeError):
    pass


class CityNotFoundError(KiwiAPIError):
    pass


class KiwiClient:
    def __init__(
        self,
        api_key: str | None = None,
        session: requests.Session | None = None,
        base_url: str = BASE_URL,
    ) -> None:
        self.api_key = api_key or os.environ.get("KIWI_API_KEY")
        if not self.api_key:
            raise KiwiAPIError("KIWI_API_KEY is not set")
        self.base_url = base_url
        self.session = session or requests.Session()
        self.session.headers.update({"apikey": self.api_key, "Content-Type": "application/json"})

    def _get(self, path: str, params: dict, timeout: float) -> dict:
        try:
            resp = self.session.get(f"{self.base_url}{path}", params=params, timeout=timeout)
            resp.raise_for_status()
            return resp.json()
        except requests.RequestException as e:
            raise KiwiAPIError(f"GET {path} failed: {e}") from e

    def resolve_city(self, name: str) -> City:
        body = self._get(
            "/locations/query",
            params={"term": name, "location_types": "city", "limit": 5},
            timeout=15,
        )
        cities = body.get("locations") or []
        if not cities:
            raise CityNotFoundError(f"No city found for: {name!r}")
        c = cities[0]
        return City(
            code=c["code"],
            name=c["name"],
            lat=float(c["location"]["lat"]),
            lon=float(c["location"]["lon"]),
        )

    def cheapest_flights(
        self,
        origin: City,
        destinations: Iterable[City],
        date_from: date,
        date_to: date,
    ) -> list[FlightOption]:
        dest_list = list(destinations)
        if not dest_list:
            return []
        body = self._get(
            "/v2/search",
            params={
                "fly_from": origin.code,
                "fly_to": ",".join(d.code for d in dest_list),
                "date_from": date_from.strftime(_DATE_FMT),
                "date_to": date_to.strftime(_DATE_FMT),
                "curr": "USD",
                "flight_type": "oneway",
                "one_for_city": 1,  # cheapest per destination city
                "adults": 1,
                "limit": 200,
            },
            timeout=30,
        )
        return [
            FlightOption(
                fly_from_airport=item["flyFrom"],
                fly_to_airport=item["flyTo"],
                city_code_to=item["cityCodeTo"],
                city_name_to=item["cityTo"],
                price_usd=float(item["price"]),
            )
            for item in body.get("data") or []
        ]
