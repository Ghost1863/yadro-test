# Section 1 — HTTP Checker

Python-скрипт, выполняющий запросы к [https://httpstat.us](https://httpstat.us)
и обрабатывающий ответы:

Статусы `1xx`, `2xx`, `3xx` — логируются (код + тело);

Статусы `4xx`, `5xx` — поднимают `HttpClientError`, который перехватывается
  на верхнем уровне, логируется и не прерывает дальнейшие запросы.

## Запуск

```bash
cd section1
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

python -m http_checker                       # 100 200 301 404 500 по умолчанию
python -m http_checker 200 204 301 418 503   # произвольный набор
```

## Пример вывода

```
2026-05-10 12:00:00 INFO     http_checker.client: GET https://httpstat.us/100 -> 100 | 100 Continue
2026-05-10 12:00:01 INFO     http_checker.client: GET https://httpstat.us/200 -> 200 | 200 OK
2026-05-10 12:00:01 INFO     http_checker.client: GET https://httpstat.us/301 -> 301 | 301 Moved Permanently
2026-05-10 12:00:02 ERROR    http_checker: Request for 404 failed: HTTP 404: 404 Not Found
2026-05-10 12:00:03 ERROR    http_checker: Request for 500 failed: HTTP 500: 500 Internal Server Error
2026-05-10 12:00:03 INFO     http_checker: Finished: 5 request(s), 2 failure(s)
```
