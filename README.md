# Upload service
Данное API позволяет загружать в MinIO хранилище
файлы форматов .dcm, .jpg, .png и .pdf.
Метаданные файлов находятся в постгресс базе.
Окружение поднимается с помощью докер компоуз через команду
"docker-compose up -d --build"
Документация по API находится по адресу http://localhost:8000/docs#/ через Swagger.
Работа осуществляется через приложение на FastAPI, MinIO и PostgreSQL.

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