from dataclasses import dataclass

import pytest

from flight_optimizer.kiwi import City, FlightOption
from flight_optimizer.optimizer import NoFlightsFoundError, find_best_destination


@dataclass
class FakeKiwiClient:
    cities: dict[str, City]
    flights: list[FlightOption]

    def resolve_city(self, name: str) -> City:
        return self.cities[name]

    def cheapest_flights(self, origin, destinations, date_from, date_to):
        return self.flights


def _cities() -> dict[str, City]:
    return {
        "London": City("LON", "London", 51.5074, -0.1278),
        "Paris": City("PAR", "Paris", 48.8566, 2.3522),
        "Berlin": City("BER", "Berlin", 52.5200, 13.4050),
    }


def test_picks_lowest_dollars_per_km():
    flights = [
        FlightOption("LHR", "CDG", "PAR", "Paris", price_usd=200),
        FlightOption("LHR", "BER", "BER", "Berlin", price_usd=100),
    ]
    client = FakeKiwiClient(cities=_cities(), flights=flights)
    best = find_best_destination("London", ["Paris", "Berlin"], client=client)
    assert best.destination_city == "Berlin"
    assert best.fly_to_airport == "BER"


def test_higher_price_can_win_when_distance_is_better():
    cities = {
        "Origin": City("ORG", "Origin", 0.0, 0.0),
        "Far": City("FAR", "Far", 0.0, 26.95),
        "Near": City("NER", "Near", 0.0, 3.6),
    }
    flights = [
        FlightOption("ORG", "FAR", "FAR", "Far", price_usd=1000),
        FlightOption("ORG", "NER", "NER", "Near", price_usd=200),
    ]
    client = FakeKiwiClient(cities=cities, flights=flights)
    best = find_best_destination("Origin", ["Far", "Near"], client=client)
    assert best.destination_city == "Far"


def test_raises_when_no_flights():
    client = FakeKiwiClient(cities=_cities(), flights=[])
    with pytest.raises(NoFlightsFoundError):
        find_best_destination("London", ["Paris"], client=client)


def test_ignores_unrequested_destination_city():
    flights = [
        FlightOption("LHR", "JFK", "NYC", "New York", price_usd=50),
        FlightOption("LHR", "CDG", "PAR", "Paris", price_usd=200),
    ]
    client = FakeKiwiClient(cities=_cities(), flights=flights)
    best = find_best_destination("London", ["Paris", "Berlin"], client=client)
    assert best.destination_city == "Paris"
