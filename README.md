# Upload service
Данное API позволяет загружать в MinIO хранилище
файлы форматов .dcm, .jpg, .png и .pdf.
Метаданные файлов находятся в постгресс базе.
Окружение поднимается с помощью докер компоуз через команду
"docker-compose up -d --build"
Документация по API находится по адресу http://localhost:8000/docs#/ через Swagger.
Работа осуществляется через приложение на FastAPI, MinIO и PostgreSQL.

ВАЖНО!
Для работы необходимо создать в корне проекта
файл .env по следующему шаблону ниже, 
подставить нужные данные:

DB_USER=Alister
DB_PASSWORD=123
DB_HOST=db_host
DB_NAME=db_host
MINIO_ENDPOINT=minio:9000
MINIO_EXTERNAL_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=admin
MINIO_SECRET_KEY=admin1234
MINIO_SECURE=False
MINIO_BUCKET_NAME=my-bucket
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=admin1234
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7
SECRET_KEY = d5d3b47832c146f1a6d5f4df9aa9e7e1084a0c2f993c63c5c6f3c5b231d8d573

Ключ сгенерировал рандомный.

Вся работа с файлами закрыта авторизацией по jwt токену.
Примеры запросов:
 - загрузка файлов
   curl -X 'POST' \
    'http://localhost:8000/api/v1/upload' \
    -H 'accept: application/json' \
    -H 'Content-Type: multipart/form-data' \
    -H 'Authorization: Bearer <ваш_JWT_токен>' \
    -F 'file=@2023-07-05 16.12.52.jpg;type=image/jpeg'
 - получение списка метаданных файлов
   curl -X 'GET' \
    'http://localhost:8000/api/v1/files' \
    -H 'Authorization: Bearer <ваш_JWT_токен>' \
    -H 'accept: application/json'
 - изменение метаданных файла в БД
   curl -X 'PUT' \
        'http://localhost:8000/api/v1/files/3fa85f64-5717-4562-b3fc-2c963f66afa6' \
        -H 'accept: application/json' \
        -H 'Content-Type: application/json' \
        -H 'Authorization: Bearer <ваш_JWT_токен>' \
        -d '{
        "id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
        "hash": "string",
        "file_name": "string",
        "url": "string"
    }'
 - удаление записи из базы и MinIO
   curl -X 'DELETE' \
    'http://localhost:8000/api/v1/files/3fa85f64-5717-4562-b3fc-2c963f66afa6' \
    -H 'Authorization: Bearer <ваш_JWT_токен>' \
    -H 'accept: application/json'

Запросы авторизации:
 - регистрация
    curl -X 'POST' \
      'http://localhost:8000/api/v1/register' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "username": "string",
      "password": "string"
    }'
 - логин
   curl -X 'POST' \
     'http://localhost:8000/api/v1/login' \
     -H 'accept: application/json' \
     -H 'Content-Type: application/json' \
     -d '{
     "username": "string",
     "password": "string"
   }'
 - обновление аксесс токена
    curl -X 'POST' \
      'http://localhost:8000/api/v1/refresh' \
      -H 'accept: application/json' \
      -H 'Content-Type: application/json' \
      -d '{
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJzdHJpbmciLCJleHAiOjE3NDczNTIyODB9.eOd1nrEU-SxA7eroK3LmURfs6jGZNCJrIFKsjJMLyDk"
    }'