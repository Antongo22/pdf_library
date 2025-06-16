# 🔐 `appsettings.json` + `dotnet user-secrets` в ASP.NET Core

## 🧩 Общая концепция

ASP.NET Core использует **многоуровневую конфигурацию**. Это значит, что ты можешь комбинировать разные источники конфигурации:

🔢 Приоритет (от низшего к высшему):

1. `appsettings.json`
2. `appsettings.{Environment}.json`
3. Secret Manager (`dotnet user-secrets`)
4. Переменные окружения
5. Аргументы командной строки

> То есть, `user-secrets` может переопределить значения из `appsettings.json`, но сам будет переопределён переменными окружения, если они заданы.

---

## 📂 Что такое `dotnet user-secrets`?

Это инструмент, который позволяет **безопасно хранить чувствительные данные (ключи, токены, пароли)** вне проекта — в зашифрованном хранилище пользователя.

🧪 Используется **только в среде разработки** и **не попадает в git**. Идеален для:

* API ключей
* Подключений к базам данных
* Конфиденциальных параметров

---

## 🛠️ Как подключить `user-secrets`

### 1. ✅ Добавь UserSecretsId в `.csproj`

```xml
<PropertyGroup>
  <TargetFramework>net8.0</TargetFramework>
  <UserSecretsId>myapp-3c2b6f1a</UserSecretsId>
</PropertyGroup>
```

> `UserSecretsId` — уникальный GUID или строка, которая определяет, где хранятся секреты. Visual Studio может сгенерировать его автоматически.

---

### 2. ⚙️ Установи секреты

В терминале из папки проекта:

```bash
dotnet user-secrets set "MySecrets:ApiKey" "super-secret-key"
```

Можно задать любое количество значений:

```bash
dotnet user-secrets set "ConnectionStrings:Postgres" "Host=localhost;Port=5432"
```

---

### 3. 🔄 Используй в `Program.cs`

Секреты подгружаются автоматически в `CreateDefaultBuilder`, но можно явно указать:

```csharp
Host.CreateDefaultBuilder(args)
    .ConfigureAppConfiguration((context, config) =>
    {
        if (context.HostingEnvironment.IsDevelopment())
        {
            config.AddUserSecrets<Program>();
        }
    })
```

---

### 4. 📖 Чтение в коде

**Через IConfiguration**:

```csharp
var apiKey = configuration["MySecrets:ApiKey"];
```

**Через POCO + Bind**:

```csharp
public class MySecretsOptions
{
    public string ApiKey { get; set; }
}
```

```csharp
services.Configure<MySecretsOptions>(configuration.GetSection("MySecrets"));
```

---

## 🗃 Где хранятся секреты?

На Windows:

```bash
%APPDATA%\Microsoft\UserSecrets\<userSecretsId>\secrets.json
```

На Linux/macOS:

```bash
~/.microsoft/usersecrets/<userSecretsId>/secrets.json
```

Пример файла:

```json
{
  "MySecrets:ApiKey": "super-secret-key"
}
```

---

## ✅ Пример полной связки

### `appsettings.json`:

```json
{
  "MySecrets": {
    "ApiKey": "dev-placeholder"
  }
}
```

### `secrets.json` (автоматически подставляется):

```json
{
  "MySecrets:ApiKey": "real-key-from-secrets"
}
```

> На запуске приложение прочитает ключ из `user-secrets`, если запущено в `Development`.

---

## 🧪 Проверка

Вывести секрет в лог:

```csharp
logger.LogInformation("API Key: {ApiKey}", configuration["MySecrets:ApiKey"]);
```

---

## 🧠 Когда использовать `user-secrets`?

| Сценарий                                 | Использовать? |
| ---------------------------------------- | ------------- |
| Локальная разработка                     | ✅ Да          |
| Docker / CI / Production                 | ❌ Лучше ENV   |
| Хранение API-ключей, паролей, connection | ✅ Да          |
| GitHub, открытый проект                  | ✅ Обязательно |

---

## 🧼 Советы

* Не храни секреты в `appsettings.json` — только заглушки
* Никогда не коммить `secrets.json`
* Для продакшена используй ENV или `Azure Key Vault`

---

## 🔚 Вывод

* `appsettings.json` — база конфигурации
* `user-secrets` — удобный инструмент для хранения чувствительных данных локально
* Работает в связке с `IConfiguration`, и легко настраивается
* Безопасен, гибок и идеально подходит для разработки
