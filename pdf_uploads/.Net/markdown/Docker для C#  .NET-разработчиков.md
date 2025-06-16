# 🐳 Docker для C# / .NET-разработчиков

## 📌 Что такое Docker?

**Docker** — это платформа для упаковки, распространения и запуска приложений в изолированных контейнерах. Вместо установки зависимостей вручную, ты один раз собираешь **образ**, и можешь запускать его где угодно.

---

## ⚙️ Зачем C#-разработчику Docker?

* ✅ Запуск .NET-приложения в любом окружении (без установки .NET SDK)
* 🧪 Изоляция от системы разработчика
* 🐞 Возможность легко тестировать разные версии .NET
* 🚀 Упрощённый деплой в облако (Azure, AWS, Kubernetes)

---

## 🏗️ Базовая структура .NET проекта с Docker

Пример `Dockerfile` для ASP.NET Core приложения:

```dockerfile
# 1. Строим образ (stage build)
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /app

COPY *.csproj ./
RUN dotnet restore

COPY . ./
RUN dotnet publish -c Release -o out

# 2. Запускаемый образ
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/out ./

ENTRYPOINT ["dotnet", "MyApp.dll"]
```

---

## 📦 Основные команды Docker

| Команда                       | Назначение                    |
| ----------------------------- | ----------------------------- |
| `docker build -t myapp .`     | Собрать образ                 |
| `docker run -p 8080:80 myapp` | Запустить контейнер           |
| `docker ps`                   | Список запущенных контейнеров |
| `docker stop <id>`            | Остановить контейнер          |
| `docker images`               | Список образов                |

---

## 📁 Пример Docker Compose

Если у тебя есть база данных и API — удобно использовать `docker-compose.yml`:

```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "5000:80"
    environment:
      - ASPNETCORE_ENVIRONMENT=Development
    depends_on:
      - db

  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: pass
      POSTGRES_DB: mydb
    volumes:
      - pgdata:/var/lib/postgresql/data

volumes:
  pgdata:
```

---

## 🧪 Пример запуска

```bash
# Сборка
docker build -t myapp .

# Запуск
docker run -p 5000:80 myapp
```

Перейди по адресу [http://localhost:5000](http://localhost:5000), чтобы увидеть результат.

---

## 🧠 Что нужно помнить

* Используй `sdk`-образ для сборки и `aspnet`-образ для запуска (multi-stage build)
* Не забудь про `.dockerignore`, чтобы не копировать лишнее
* Для dev-режима удобнее использовать `docker-compose`

---

## 📂 Пример .dockerignore

```dockerignore
bin/
obj/
*.user
*.suo
.vscode/
*.log
```

---

## 🔐 Дополнительно

* Используй `.env` файл для переменных среды
* Прокидывай `volumes`, если хочешь сохранять данные (например, в PostgreSQL)
* В проде используй `ENTRYPOINT` и `HEALTHCHECK`

---

## 📚 Заключение

Docker в .NET — это:

* 💼 Портируемость
* 🧹 Чистота среды
* 🚀 Быстрый деплой
* 🔁 Отличный вариант для CI/CD

