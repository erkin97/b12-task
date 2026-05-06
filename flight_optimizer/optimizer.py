from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from flight_optimizer.distance import km_between
from flight_optimizer.kiwi import City, KiwiClient


@dataclass(frozen=True)
class BestFlight:
    destination_city: str
    fly_from_airport: str
    fly_to_airport: str
    price_usd: float
    distance_km: float

    @property
    def dollars_per_km(self) -> float:
        return self.price_usd / self.distance_km


class NoFlightsFoundError(RuntimeError):
    pass


def find_best_destination(
    origin_city: str,
    destination_cities: list[str],
    client: KiwiClient | None = None,
    today: date | None = None,
) -> BestFlight:
    client = client or KiwiClient()
    today = today or date.today()
    tomorrow = today + timedelta(days=1)

    origin = client.resolve_city(origin_city)
    destinations = [client.resolve_city(c) for c in destination_cities]
    by_code: dict[str, City] = {c.code: c for c in destinations}

    flights = client.cheapest_flights(origin, destinations, today, tomorrow)
    if not flights:
        raise NoFlightsFoundError(f"No flights from {origin_city} to any of: {destination_cities}")

    candidates = []
    for flight in flights:
        dest = by_code.get(flight.city_code_to)
        if dest is None:
            continue  # API may return a city we did not request; ignore
        distance_km = km_between(origin.coords, dest.coords)
        candidates.append((distance_km, flight, dest))

    if not candidates:
        raise NoFlightsFoundError("No flights matched a requested destination city")

    distance_km, flight, _ = min(candidates, key=lambda t: t[1].price_usd / t[0])
    return BestFlight(
        destination_city=flight.city_name_to,
        fly_from_airport=flight.fly_from_airport,
        fly_to_airport=flight.fly_to_airport,
        price_usd=flight.price_usd,
        distance_km=distance_km,
    )
