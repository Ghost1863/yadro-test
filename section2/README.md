# Section 2 — Docker

## Сборка и запуск

Из корня репозитория (`yadro-test/`):

```bash
docker build -f section2/Dockerfile -t http-checker:1.0.0 .

docker run --rm --name http-checker http-checker:1.0.0
```

Аргументы (статус-коды) пробрасываются через `CMD`:

```bash
docker run --rm http-checker:1.0.0 200 301 418 503
```

## Через docker compose

```bash
cd section2
docker compose up --build
docker compose logs http-checker
docker compose down
```

## Проверка через `docker logs`

```bash
docker run -d --name http-checker http-checker:1.0.0
docker wait http-checker
docker logs http-checker
docker rm http-checker
```
