# Vault
Сервис для хранения/выдачи 
- Прокси
- Youtube апи ключей
- Инстаграмм сессий

На один прокси приходится два сервиса yt, ig

Один прокси может вместить в себя одну сессию/ключ(далее ключ) сервиса

То есть имеем на один прокси сессию в инстаграме и ключ ютюб.  
Прокси-базовый юнит и если ключей>прокси,  
то стоит докупить прокси и только после этого  
складывать их иначе получим ошибку **NO_PROXY_AVAIL**

# Запуск
```
docker-compose build
docker-compose up
```

# Добавление прокси

```
POST /proxy
{
    "action":"store",
    "address":"1.1.1.1",
    "port": "8000",
    "user": "USERNAME",
    "password": "PASSWORD"
}
```

# Добавление инстаграмм сессий

```
POST /ig
{
    "action":"store",
    "session_name":"test_user",
    "session_password": "password_for_test_user",
}
```

# Добавление ютуб ключей

```
POST /ig
{
    "action":"store",
    "key":"12345678910ABCDEFGHIJK"
}
```

# Статусы

Vault учитывает статус ключа и имеет три значения:
- Ready: ключ готов к использованию
- Blocked: ключ был забанен сервисом, он будет автоматически считаться Ready после 24 часов
- Locked: ключ используется и он не доступен для выдачи

# Получение ключей
Ключи выдаются вместе с привязанным к нему прокси + его id

```
GET /ig >
{
    "session_id": 1,
    "session_name": "ig_username",
    "session_pass": "ig_password",
    "address": "1.1.1.1",
    "user": "proxy_user",
    "password": "proxy_password",
    "port": 8000
}
```
```
GET /yt >
{
    "key_id": 1,
    "key": "12345678910ABCDEFGHIJK",
    "address": "1.1.1.1",
    "user": "proxy_user",
    "password": "proxy_password",
    "port": 8000
}
```

# Обновление статуса ключа

После завершения работы программы или блокировки сервисом ключа  
стоит обновить статус ключа на соответсвующий
Так как этот функционал не реализован полностью необходимо  
так же указывать остальную мету  
типа key, session_name, session_pass

```
POST /yt
{
    "key_id": 1,
    "status": "Blocked" # "Ready"
}
```
```
POST /ig
{
    "session_id": 1,
    "status": "Blocked" # "Ready"
}
```
