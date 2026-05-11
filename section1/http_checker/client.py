from __future__ import annotations

import logging
from dataclasses import dataclass

import requests

from .exceptions import HttpClientError

BASE_URL = "https://tools-httpstatus.pickup-services.com"
REQUEST_TIMEOUT = 10.0
ERROR_RANGE = range(400, 600)
VALID_RANGE = range(100, 600)
MAX_BODY_LOG_CHARS = 200

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
    if status_code not in VALID_RANGE:
        raise ValueError(
            f"Status code {status_code} is outside the valid HTTP range "
            f"[{VALID_RANGE.start}, {VALID_RANGE.stop})."
        )

    url = f"{base_url.rstrip('/')}/{status_code}"
    response = requests.get(url, headers={"Accept": "text/plain"}, timeout=timeout)
    body = _shorten(response.text.strip())
    result = HttpResponse(status_code=response.status_code, body=body)

    if result.status_code in ERROR_RANGE:
        raise HttpClientError(result.status_code, result.body)

    logger.info("GET %s -> %s | %s", url, result.status_code, result.body)
    return result


def _shorten(text: str, limit: int = MAX_BODY_LOG_CHARS) -> str:
    if len(text) <= limit:
        return text
    return text[:limit] + f"... [+{len(text) - limit} chars truncated]"
