# Role: http_checker

Тянет образ `http-checker` из реестра, запускает контейнер, дожидается
завершения и валидирует exit code. Дополнительно читает stdout
контейнера через `docker logs` и печатает его в выводе плейбука.

Роль зависит от роли `docker`. Если её ещё не катали, она поднимется
автоматически как зависимость через `meta/main.yml`.

## Переменные

`http_checker_image_repository`. Имя образа в реестре. По умолчанию
`imm174/http-checker`, публичный образ на Docker Hub.

`http_checker_image_tag`. Тег. Дефолт `1.0.0`, синхронизирован с тегом
сборки из `section2`.

`http_checker_image_pull`. Перетягивать ли образ при каждом запуске. По
умолчанию `true` для гарантии свежего образа. Для офлайн-проверок на
хостах с уже подгруженным образом ставится `false`.

`http_checker_container_name`. Имя контейнера. Дефолт `http-checker`.
Меняется, если на хосте крутится несколько инстансов.

`http_checker_status_codes`. Список кодов, которые скрипт пробивает по
`httpstat.us`. Дефолт `[100, 200, 301, 404, 500]`, по одному из каждой
категории.

`http_checker_wait_retries` и `http_checker_wait_delay`. Сколько раз и с
каким интервалом опрашивается `docker_container_info` в ожидании статуса
`exited`. Дефолты `30 × 2s = 60s`.

`http_checker_remove_after_run`. Удалять ли контейнер после проверки. По
умолчанию `false`, чтобы можно было руками сделать `docker logs` после
плейбука.

## Тестирование с molecule

```bash
cd roles/http_checker
molecule test
```

Сценарий поднимает контейнер `geerlingguy/docker-ubuntu2204-ansible`, внутри инициализируется vfs storage driver, потом зависимая роль `docker` ставит и стартует Docker Engine, после чего сама
роль тянет `imm174/http-checker:1.0.0`, отправляет один запрос и валидирует
exit code.
