from ninja import NinjaAPI, Schema

from flight_optimizer.kiwi import CityNotFoundError, KiwiAPIError
from flight_optimizer.optimizer import NoFlightsFoundError, find_best_destination


class BestFlightRequest(Schema):
    origin: str
    destinations: list[str]


class BestFlightResponse(Schema):
    destination_city: str
    dollars_per_km: float
    price_usd: float
    distance_km: float
    fly_from_airport: str
    fly_to_airport: str


class ErrorResponse(Schema):
    error: str


api = NinjaAPI(title="Flight Optimizer API", version="0.1.0")


@api.post(
    "/best-flight",
    response={200: BestFlightResponse, 400: ErrorResponse, 502: ErrorResponse},
)
def best_flight(request, payload: BestFlightRequest):
    try:
        best = find_best_destination(payload.origin, payload.destinations)
    except (CityNotFoundError, NoFlightsFoundError) as e:
        return 400, {"error": str(e)}
    except KiwiAPIError as e:
        return 502, {"error": f"Kiwi API: {e}"}

    return 200, BestFlightResponse(
        destination_city=best.destination_city,
        dollars_per_km=round(best.dollars_per_km, 4),
        price_usd=round(best.price_usd, 2),
        distance_km=round(best.distance_km, 1),
        fly_from_airport=best.fly_from_airport,
        fly_to_airport=best.fly_to_airport,
    )
