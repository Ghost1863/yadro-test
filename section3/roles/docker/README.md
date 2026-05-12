# Role: docker

Ставит Docker Engine и плагины (`buildx`, `compose`) на хосты семейства
Debian (проверено на Ubuntu 22.04 и 24.04). Подключает официальный
apt-репозиторий Docker, кладёт ключ в `/etc/apt/keyrings/docker.asc`,
добавляет указанных пользователей в группу `docker`, поднимает и включает
службу `docker.service`. Дополнительно ставит `python3-docker` (с
зависимостью `requests`), чтобы все последующие модули `community.docker.*`
находили Python SDK на хосте. В конце выполняется `docker --version` и
результат печатается в вывод плейбука.

## Переменные

Все переменные роли типизированы в `meta/argument_specs.yml`. Неверный
тип или неполный набор обязательных параметров
отлавливается до запуска задач.

`docker_users`. Список логинов, которые попадают в группу `docker`. По
умолчанию пустой; конкретные пользователи задаются в инвентаре
(`vars.docker_users` в `inventories/*/hosts.yml`).

`docker_apt_gpg_key_checksum`. SHA256 публичного ключа Docker в формате
`sha256:<hex>`. Дефолт зафиксирован на текущее значение ключа Docker;
если Docker ротирует ключ, переменная переопределяется или очищается
для пропуска проверки.

`docker_packages`. Список пакетов из репозитория Docker, которые ставятся.
Дефолт `docker-ce`, `docker-ce-cli`, `containerd.io`, `docker-buildx-plugin`,
`docker-compose-plugin`. Если compose не нужен, последний пункт
исключается.

`docker_apt_repository_url` и `docker_apt_gpg_key_url`. Источник
репозитория и GPG-ключа. Дефолты ведут на `download.docker.com/linux/ubuntu`.
Для Debian или зеркала меняются оба URL и при необходимости
`docker_apt_keyring_path`.

`docker_apt_arch`. Архитектура для apt-репозитория. По умолчанию выводится
из `ansible_facts['architecture']`: `amd64` для `x86_64`, иначе как есть.

`docker_service_state` и `docker_service_enabled`. Желаемое состояние
службы. Дефолты `started` и `true`. Меняются только если хост сознательно
держит docker отключённым.

## Тэги

Задачи помечены гранулярными тэгами: `pkg` (apt-пакеты), `gpg`/`repo`
(ключ и репозиторий), `service` (docker.service), `users` (группа и
участники), `verify` (`docker --version`). Можно запускать 
через `--tags` / `--skip-tags`.

## Тестирование с molecule

```bash
cd roles/docker
molecule test
```

Сценарий поднимает контейнер `geerlingguy/docker-ubuntu2204-ansible`
 с systemd внутри, в `prepare.yml` пишется
`/etc/docker/daemon.json` со `"storage-driver": "vfs"` , потом катается роль и проверяется наличие
бинаря `docker`, активной службы `docker.service` и группы `docker`.
