# yadro-test

Тестовое задание из трёх частей: Python-скрипт, Docker-образ для него и
Ansible-автоматизация развёртывания на целевой хост.

## Section 1. HTTP-чекер на Python

В `section1/` лежит пакет `http_checker`, который отправляет запросы на сервис-зеркало
`tools-httpstatus.pickup-services.com` заданным набором статус-кодов
(оригинальный `httpstat.us` из ТЗ недоступен из РФ, поведение зеркала
эквивалентное). Ответы 1xx, 2xx и 3xx логируются в stdout (код и тело),
4xx и 5xx поднимают доменное исключение `HttpClientError`. На верхнем
уровне исключение ловится, пишется в лог и не прерывает остальные запросы,
поэтому все запросы из переданного списка всегда выполняются. Тело ответа
в логах ограничено 200 символами.

Зависимости закреплены в `section1/requirements.txt`.
Дефолтный набор кодов 100, 200, 301, 404, 500, по одному из каждой
категории. Любой список передаётся через CLI.

```bash
cd section1
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python3 -m http_checker
python3 -m http_checker 200 418 503
```

## Section 2. Docker

В `section2/` собран multi-stage Dockerfile на базе `ubuntu:22.04`.
Builder ставит python3, venv и pip-зависимости,
runtime копирует только venv и сам пакет, поэтому в финальном образе нет
pip и build-инструментов. В качестве PID 1 используется `tini`. Процесс
запускается от непривилегированного UID и GID 10001. Логи идут в stdout
без буферизации и доступны через `docker logs`.

Образ опубликован как `imm174/http-checker:1.0.0` на Docker Hub и
используется ролью `http_checker` из `section3` в режиме pull. На каждый
push в `master` GitHub Actions запускает воркфлоу
`.github/workflows/build-and-push.yml` из трёх джобов: `lint` (ruff,
yamllint, ansible-lint, hadolint), `security` (bandit + trivy, фейлится
только на CRITICAL), и `build-and-push`, который собирает образ и
публикует его в Docker Hub через `secrets.DOCKERHUB_TOKEN`. Конфиги
линтеров лежат в корне (`.yamllint`, `.hadolint.yaml`,
`section3/.ansible-lint`), версии — в `.github/requirements/`.

Сборка из корня репозитория:

```bash
docker build -f section2/Dockerfile -t http-checker:1.0.0 .
docker run --rm http-checker:1.0.0
docker run --rm http-checker:1.0.0 200 301 418 503
```

`section2/docker-compose.yml` запускает контейнер с hardened-настройками:
`read_only`, `tmpfs /tmp` с `noexec`, `nosuid`, `no-new-privileges`,
`cap_drop: ALL`, ограничения на cpu, mem, pids и ротация json-логов.

## Section 3. Ansible

В `section3/` две роли и плейбук `site.yml`, который ставит Docker на
целевом хосте, тянет образ из реестра, запускает контейнер и проверяет
результат.

Роль `docker` ставит Docker Engine, плагины `buildx` и `compose`,
`python3-docker` (с зависимостью `requests`) для модулей
`community.docker.*`, добавляет указанных пользователей в группу `docker`,
поднимает и включает `docker.service`. После установки печатается результат
`docker --version`. Подробное описание переменных лежит в
[roles/docker/README.md](section3/roles/docker/README.md).

Роль `http_checker` подтягивает образ `imm174/http-checker:1.0.0` из реестра
и запускает контейнер. После запуска роль дожидается завершения работы
скрипта (через модуль `community.docker.docker_container_info`), читает его
stdout командой `docker logs`, выводит результат в плейбук и проверяет, что
код возврата равен нулю. Подробное описание переменных лежит в
[roles/http_checker/README.md](section3/roles/http_checker/README.md).

Каждая роль покрыта molecule-сценарием в `roles/<role>/molecule/default`.
Тестовая платформа `geerlingguy/docker-ubuntu2204-ansible`. 
Подготовка управляющей машины:

```bash
cd section3
ansible-galaxy collection install -r requirements.yml
```

Локальный прогон:

```bash
ansible-playbook -i inventories/local/hosts.yml site.yml --ask-become-pass
```

Удалённый прогон. 

```bash
ansible-playbook -i inventories/production/hosts.yml site.yml
```

Тестирование:

```bash
cd section3/roles/docker 
```
или
```bash
cd section3/roles/http_checker 
```

Запуск тестов:

```bash
molecule test
```