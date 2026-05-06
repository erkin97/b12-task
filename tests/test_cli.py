from unittest.mock import patch

import pytest

import flight_optimizer.cli as cli_mod
from flight_optimizer.cli import build_parser


def test_parser_requires_from():
    parser = build_parser()
    with pytest.raises(SystemExit):
        parser.parse_args(["--to", "Paris"])


def test_parser_accepts_multiple_destinations():
    parser = build_parser()
    args = parser.parse_args(["--from", "London", "--to", "Paris", "Berlin", "Rome"])
    assert args.origin == "London"
    assert args.destinations == ["Paris", "Berlin", "Rome"]


def test_main_prints_destination_and_dollars_per_km(capsys):
    fake = type(
        "Best",
        (),
        {"destination_city": "Berlin", "dollars_per_km": 0.107},
    )()
    with patch.object(cli_mod, "find_best_destination", return_value=fake):
        rc = cli_mod.main(["--from", "London", "--to", "Berlin"])
    assert rc == 0
    out = capsys.readouterr().out.strip().split("\n")
    assert out == ["Berlin", "$0.11/km"]
