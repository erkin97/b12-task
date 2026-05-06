from __future__ import annotations

import argparse
import sys

from flight_optimizer.kiwi import CityNotFoundError, KiwiAPIError
from flight_optimizer.optimizer import NoFlightsFoundError, find_best_destination


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="flight-optimizer",
        description="Find the destination with the cheapest dollars-per-kilometer flight.",
    )
    parser.add_argument("--from", dest="origin", required=True, metavar="CITY")
    parser.add_argument(
        "--to",
        dest="destinations",
        nargs="+",
        required=True,
        metavar="CITY",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        best = find_best_destination(args.origin, args.destinations)
    except CityNotFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    except NoFlightsFoundError as e:
        print(f"error: {e}", file=sys.stderr)
        return 3
    except KiwiAPIError as e:
        print(f"error: kiwi api: {e}", file=sys.stderr)
        return 4

    print(best.destination_city)
    print(f"${best.dollars_per_km:.2f}/km")
    return 0


if __name__ == "__main__":
    sys.exit(main())
