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

6. После этого снова поднимите контейнеры:

    ```bash
    docker-compose up
    ```

7. Теперь вы можете зайти, используя созданные учетные данные, перейдя по ссылке [http://localhost:8000](http://localhost:8000). Введите логин и пароль созданного суперпользователя.
