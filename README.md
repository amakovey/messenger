## server.py - скрипт запуска сервера
## client.py - скрипт запуска клиента
## JIM.py - обработчик команд сервера и клиента по протоколу JIM
## dbclient.py - скрипт работы с БД клиента
## dbserver.py - скрипт работы с БД сервера
## log_config.py - скрипт логгирования
## Функционал сервера:
### * Обработка нескольких клиентов одновременно
### * Хранение в БД историю сообщений клиентов, историю входов клиентов, IP последнего входа клиента, списки контактов клиентов
## Функционал клиента:
### * Обработка ответов сервера в отдельном потоке
### * Добавление/удаление пользователя в список контактов
### * Отправка сообщений всем клиентам
### * Отправка сообщений персональному клиенту
### * Хранение в БД истории сообщений
### * Хранение в БД списка контактов


