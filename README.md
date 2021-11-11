# TheBestChat
Проект "Чат для друзей"

## Требования
- [Python 3.9.x](https://www.python.org/downloads/)
- [Git](https://git-scm.com)
- [Redis Server](https://disk.yandex.ru/d/wxE9QgX8MMADTQ) (не обязательно)

## Деплой проекта

### 1. Склонировать репозиторий. 
```
git clone https://github.com/bibilka/rsue_chat.git
```
### 2. Создание виртуальной среды.
Переходим в папку с проектом и выполняем команду:
```
python -m venv venv
```
Активируем виртуальную среду:
```
.\venv\Scripts\activate
```
### 3. Настройка проекта (env, зависимости, миграции).

Подгружаем зависимости проекта (пакеты):
```
pip install -r requirements.txt
```
Переходим в папку приложения.
```
cd thebestchat
```
Выполняем команду: ```cp .env.example .env```. Затем редактируем параметры в конфигурационном файле `.env`, если требуется.

Для настройки и заполнения базы данных с помощью миграций выполняем команды:
```
python manage.py makemigrations
python manage.py migrate
```
Создаем пользователя для админ-панели с помощью команды:
```
python manage.py createsuperuser
```

### 4. Запуск.

Запускаем веб-сервер Django через команду:
```
python manage.py runserver 80
```
#### Дополнительно:
Если требуется использовать Redis:
в файле `.env` указываем `REDIS_ENABLE=True` и запускаем Redis сервер на локальной машине на порту 6379 (порт по умолчанию).

_____
:white_check_mark: <b>Готово!</b> :+1: :tada: 

Проект запущен и доступен по адресу: `http://localhost/` или `http://127.0.0.1/`


