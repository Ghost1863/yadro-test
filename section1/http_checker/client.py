from __future__ import annotations

import logging
from dataclasses import dataclass

import requests

from .exceptions import HttpClientError

BASE_URL = "https://httpstat.us"
REQUEST_TIMEOUT = 10.0
ERROR_RANGE = range(400, 600)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class HttpResponse:
    status_code: int
    body: str


def fetch(
    status_code: int,
    *,
    base_url: str = BASE_URL,
    timeout: float = REQUEST_TIMEOUT,
) -> HttpResponse:
    url = f"{base_url}/{status_code}"
    response = requests.get(url, headers={"Accept": "text/plain"}, timeout=timeout)
    result = HttpResponse(status_code=response.status_code, body=response.text.strip())

    if result.status_code in ERROR_RANGE:
        raise HttpClientError(result.status_code, result.body)

    logger.info("GET %s -> %s | %s", url, result.status_code, result.body)
    return result
