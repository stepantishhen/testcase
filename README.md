### Запуск приложения сокращения ссылок

1. Сначала склонируйте репозиторий с помощью следующей команды:

    ```bash
    git clone https://github.com/stepantishhen/testcase.git
    ```

2. Перейдите в папку проекта:

    ```bash
    cd testcase
    ```

3. Запустите контейнеры с помощью Docker Compose:

    ```bash
    docker-compose up
    ```

4. После запуска контейнеров выполните миграции для базы данных Django:

    ```bash
    docker-compose run web python manage.py migrate
    ```

5. Теперь создайте суперпользователя для доступа к админке:

    ```bash
    docker-compose run web python manage.py createsuperuser
    ```
6. После этого создайте токен для авторизации с помощью команды:

    ```bash
    docker-compose run web python manage.py drf_create_token <username>
    ```

7. После этого снова поднимите контейнеры:

    ```bash
    docker-compose up
    ```
   Авторизироваться можно через UI Swagger(кнопка Authorize) http://0.0.0.0:8000/swagger/ либо через Postman передав в Header:
   ```Authorization: Token <сгенерированный_ранее_токен>```
   
   Чтобы запустить тесты: ```docker-compose run web python manage.py test```