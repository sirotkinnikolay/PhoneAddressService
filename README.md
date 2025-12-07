### 1. Клонируйте репозиторий:
git clone <url>

### 2. Создайте .env файл.
В корне проекта находится образец для заполнения .env.example
### 3. Запустите сервисы:
docker compose up -d --build

### 4. Просмотр логов:
docker compose logs -f api
docker compose logs -f redis

### 5. Swagger, Redoc:
Swagger : http://localhost:8000/docs
Redoc: http://localhost:8000/redoc
