from haversine import Unit, haversine


def km_between(origin: tuple[float, float], destination: tuple[float, float]) -> float:
    return haversine(origin, destination, unit=Unit.KILOMETERS)
