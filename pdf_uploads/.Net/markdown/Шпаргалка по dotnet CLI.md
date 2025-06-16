# 📦 Шпаргалка по dotnet CLI

`.NET CLI (Command Line Interface)` — основной инструмент работы с проектами .NET из терминала.

---

## 📁 Создание и управление проектами и решениями

| Команда                            | Описание                                   |
| ---------------------------------- | ------------------------------------------ |
| `dotnet new console -n MyApp`      | Создать консольный проект с именем `MyApp` |
| `dotnet new webapi -n MyApi`       | Создать проект Web API                     |
| `dotnet new classlib -n MyLibrary` | Создать библиотеку классов                 |
| `dotnet new sln -n MySolution`     | Создать новое решение                      |
| `dotnet sln add <путь>`            | Добавить проект в `.sln`                   |
| `dotnet sln list`                  | Показать все проекты в решении             |
| `dotnet new list`                  | Показать все доступные шаблоны             |

🔹 **Примеры:**

```bash
dotnet new console -n MyApp
dotnet new sln -n MySolution
dotnet sln add ./MyApp/MyApp.csproj
```

---

## 📦 Работа с зависимостями

### 📦 NuGet-пакеты

| Команда                                 | Описание                    |
| --------------------------------------- | --------------------------- |
| `dotnet add package Newtonsoft.Json`    | Установить пакет            |
| `dotnet remove package Newtonsoft.Json` | Удалить пакет               |
| `dotnet list package`                   | Список всех пакетов проекта |
| `dotnet restore`                        | Восстановить зависимости    |

🔹 **Пример:**

```bash
dotnet add package Dapper
dotnet remove package Newtonsoft.Json
```

### 🔗 Ссылки на проекты

| Команда                                    | Описание                         |
| ------------------------------------------ | -------------------------------- |
| `dotnet add reference <Project.csproj>`    | Добавить ссылку на другой проект |
| `dotnet list reference`                    | Показать текущие ссылки          |
| `dotnet remove reference <Project.csproj>` | Удалить ссылку                   |

🔹 **Пример:**

```bash
dotnet add reference ../MyLibrary/MyLibrary.csproj
```

---

## ⚙️ Сборка и запуск

| Команда            | Описание                                         |
| ------------------ | ------------------------------------------------ |
| `dotnet build`     | Сборка проекта                                   |
| `dotnet run`       | Запуск проекта                                   |
| `dotnet clean`     | Очистка временных файлов сборки (`bin/`, `obj/`) |
| `dotnet publish`   | Подготовка к публикации                          |
| `dotnet watch run` | Автоперезапуск при изменениях в коде             |

🔹 **Пример:**

```bash
dotnet build --configuration Release
dotnet run --project ./MyApp/MyApp.csproj
dotnet publish -c Release -o ./publish
```

---

## 🧪 Тестирование

| Команда                                             | Описание                 |
| --------------------------------------------------- | ------------------------ |
| `dotnet new xunit -n MyTests`                       | Создать проект с тестами |
| `dotnet test`                                       | Запустить все тесты      |
| `dotnet test --filter "Category=Fast"`              | Запуск по категории      |
| `dotnet test --logger:"console;verbosity=detailed"` | Вывод подробного лога    |

🔹 **Пример:**

```bash
dotnet new xunit -n MyApp.Tests
dotnet add reference ../MyApp/MyApp.csproj
dotnet test
```

---

## 🔁 Работа с миграциями (Entity Framework Core)

> Требуется пакет `Microsoft.EntityFrameworkCore.Tools`.

| Команда                                                                                     | Описание                   |
| ------------------------------------------------------------------------------------------- | -------------------------- |
| `dotnet ef migrations add InitialCreate`                                                    | Добавить миграцию          |
| `dotnet ef database update`                                                                 | Применить миграции         |
| `dotnet ef migrations remove`                                                               | Удалить последнюю миграцию |
| `dotnet ef database drop`                                                                   | Удалить базу данных        |
| `dotnet ef dbcontext info`                                                                  | Информация о DbContext     |
| `dotnet ef migrations list`                                                                 | Список миграций            |
| `dotnet ef dbcontext scaffold <строка_подключения> Microsoft.EntityFrameworkCore.SqlServer` | Генерация модели из БД     |

🔹 **Пример:**

```bash
dotnet ef migrations add AddUsersTable
dotnet ef database update
```

---

## 🧰 Инструменты и общая информация

| Команда                        | Описание                            |
| ------------------------------ | ----------------------------------- |
| `dotnet --info`                | Информация о SDK и среде выполнения |
| `dotnet --version`             | Версия SDK                          |
| `dotnet workload list`         | Список установленных workload’ов    |
| `dotnet workload install maui` | Установка workload                  |
| `dotnet help`                  | Список всех доступных команд        |

---

## ⚙️ Полезные параметры

| Параметр                  | Описание                  |
| ------------------------- | ------------------------- |
| `--configuration Release` | Сборка в релиз-режиме     |
| `--framework net8.0`      | Указать целевую платформу |
| `--output ./publish`      | Указать путь вывода       |
| `--verbosity detailed`    | Подробный вывод           |

---

## 🧠 Рекомендации

* Создавай `sln` и добавляй туда все проекты — так проще управлять и в CLI, и в IDE
* Используй `dotnet watch run` в разработке для горячей перезагрузки
* Автоматизируй с помощью `Makefile`, `bash` или `PowerShell` скриптов

---

## 📚 Полезные ссылки

* 📘 [Документация по dotnet CLI](https://learn.microsoft.com/dotnet/core/tools/)
* 📘 [EF Core CLI](https://learn.microsoft.com/ef/core/cli/dotnet)
