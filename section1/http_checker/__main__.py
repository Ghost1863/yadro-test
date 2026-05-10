from __future__ import annotations

import argparse
import logging
import sys
from collections.abc import Sequence

import requests

from .client import fetch
from .exceptions import HttpClientError

DEFAULT_STATUS_CODES: tuple[int, ...] = (100, 200, 301, 404, 500)

logger = logging.getLogger("http_checker")


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="http_checker",
        description="Probe https://httpstat.us with the given status codes.",
    )
    parser.add_argument(
        "status_codes",
        nargs="*",
        type=int,
        default=list(DEFAULT_STATUS_CODES),
        metavar="CODE",
        help="HTTP status codes to request (default: %(default)s).",
    )
    return parser.parse_args(argv)


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-8s %(name)s: %(message)s",
        stream=sys.stdout,
    )


def main(argv: Sequence[str] | None = None) -> int:
    configure_logging()
    args = parse_args(argv)

    failures = 0
    for code in args.status_codes:
        try:
            fetch(code)
        except HttpClientError as exc:
            failures += 1
            logger.error("Request for %s failed: %s", code, exc)
        except requests.RequestException as exc:
            failures += 1
            logger.error("Network error while requesting %s: %s", code, exc)

    logger.info(
        "Finished: %d request(s), %d failure(s)",
        len(args.status_codes),
        failures,
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
