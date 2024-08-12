# network
Проект network, не знаешь, что приготовить? Здесь ты найдешь себе рецепт на любой случай жизни.
Зарегистрируйся и сможешь добавлять рецепты в избранное, или подписаться на пользователя, Чтобы 
отслеживать его новые рецепты. Добавь рецепт в список покупок, после чего ты можешь скачать
список всех ингредиентов необходимых для приготовления рецептов.

## :hammer_and_wrench: Инструменты и технологии :
- Python

- Django

- djangorestframework

- djoser

- pytest

- PostgreSQL

- JavaScript

- CSS

- HTML


## Установка 

1. Клонировать репозиторий и перейти в него в командной строке:

    ```BASH
    git@github.com:NumiViX/pet.git
    ```

2. Устанавливаем Docker
   - Windows.Скачате Docker с официального сайта

      [Docker.com](https://www.docker.com/products/docker-desktop/)

   - Установка Docker на Linux 

        ```BASH
        sudo apt update
        ```
        ```BASH
        sudo apt install curl
        ```
        ```BASH
        curl -fSL https://get.docker.com -o get-docker.sh
        ```
        ```BASH
        sudo sh ./get-docker.sh
        ```
        ```BASH    
        sudo apt-get install docker-compose-plugin
        ```
        ```BASH    
        sudo systemctl status docker
        ```

   - Установка Docker на macOS

        [Docker.com](https://www.docker.com/products/docker-desktop/)

3. Запустить проект:

    ```BASH
    docker-compose up
    ```
    ```BASH    
    # Выполняет миграции
    docker-compose backend python manage.py migrate
    ```
    ```BASH    
    # Сбор статики
    docker-compose backend python manage.py collectstatic
    ```
    ```BASH
    # Копирование статики
    docker-compose exec backend cp -r /app/collected_static/. /backend_static/static/
    ```
    ```BASH 
    # перезагружает nginx
    sudo systemctl restart nginx
    ```
### Пример запроса по API 
1. Регистрация. Отправляем POST запрос по адресу https://localhost/api/users/
   ```
   {
        "email": "vpupkin@yandex.ru",
        "username": "vasya.pupkin",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "password": "Qwerty123"
    }   
   ```
2. Получаем профиль пользователя http://localhost/api/users/{id}/
   ```
    {
        "email": "user@example.com",
        "id": 0,
        "username": "string",
        "first_name": "Вася",
        "last_name": "Пупкин",
        "is_subscribed": false
    }
   ```
3. Делаем GET запрос пользователя по адресу http://localhost/api/recipes/ для создания рецепта:
    ```
        {
            "ingredients": [
                {
                "id": 1123,
                "amount": 10
                }
            ],
            "tags": [
                1,
                2
            ],
            "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABAgMAAABieywaAAAACVBMVEUAAAD///9fX1/S0ecCAAAACXBIWXMAAA7EAAAOxAGVKw4bAAAACklEQVQImWNoAAAAggCByxOyYQAAAABJRU5ErkJggg==",
            "name": "string",
            "text": "string",
            "cooking_time": 1
        }
    ```


### Об авторе

NumiViX

