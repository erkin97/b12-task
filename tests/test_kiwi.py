from datetime import date

import pytest
import responses

from flight_optimizer.kiwi import BASE_URL, City, CityNotFoundError, KiwiClient


@responses.activate
def test_resolve_city_picks_first_match():
    responses.get(
        f"{BASE_URL}/locations/query",
        json={
            "locations": [
                {
                    "code": "BER",
                    "name": "Berlin",
                    "id": "berlin_de",
                    "location": {"lat": "52.5200", "lon": "13.4050"},
                },
                {
                    "code": "BTV",
                    "name": "Burlington",
                    "id": "burlington_vt_us",
                    "location": {"lat": "44.4759", "lon": "-73.2121"},
                },
            ]
        },
    )
    client = KiwiClient(api_key="test")
    city = client.resolve_city("Berlin")
    assert city.code == "BER"
    assert city.name == "Berlin"
    assert city.lat == 52.52
    assert city.lon == 13.405


@responses.activate
def test_resolve_city_raises_when_empty():
    responses.get(f"{BASE_URL}/locations/query", json={"locations": []})
    client = KiwiClient(api_key="test")
    with pytest.raises(CityNotFoundError):
        client.resolve_city("Nowheresville")


@responses.activate
def test_cheapest_flights_parses_data():
    responses.get(
        f"{BASE_URL}/v2/search",
        json={
            "data": [
                {
                    "flyFrom": "LHR",
                    "flyTo": "CDG",
                    "cityCodeTo": "PAR",
                    "cityTo": "Paris",
                    "price": 100,
                },
                {
                    "flyFrom": "LHR",
                    "flyTo": "FRA",
                    "cityCodeTo": "FRA",
                    "cityTo": "Frankfurt",
                    "price": 250,
                },
            ]
        },
    )
    client = KiwiClient(api_key="test")
    origin = City("LON", "London", 51.5074, -0.1278)
    dests = [
        City("PAR", "Paris", 48.8566, 2.3522),
        City("FRA", "Frankfurt", 50.1109, 8.6821),
    ]
    flights = client.cheapest_flights(origin, dests, date(2026, 5, 6), date(2026, 5, 7))
    assert len(flights) == 2
    assert flights[0].city_code_to == "PAR"
    assert flights[0].city_name_to == "Paris"
    assert flights[0].price_usd == 100.0
    assert flights[0].fly_from_airport == "LHR"


@responses.activate
def test_cheapest_flights_returns_empty_when_no_destinations():
    client = KiwiClient(api_key="test")
    origin = City("LON", "London", 51.5074, -0.1278)
    assert client.cheapest_flights(origin, [], date(2026, 5, 6), date(2026, 5, 7)) == []


@responses.activate
def test_http_error_is_wrapped_in_kiwi_api_error():
    from flight_optimizer.kiwi import KiwiAPIError

    responses.get(f"{BASE_URL}/locations/query", json={"error": "rate limited"}, status=429)
    client = KiwiClient(api_key="test")
    with pytest.raises(KiwiAPIError):
        client.resolve_city("London")
