# 🚀 Что такое Kestrel?

**Kestrel** — это *встроенный кросс-платформенный веб-сервер*, который используется по умолчанию в ASP.NET Core-приложениях.

Он:

* написан на C# и работает на .NET
* запускается автоматически при старте приложения (`dotnet run`)
* **не зависит от IIS или Apache** (хотя может работать совместно)
* быстро обрабатывает HTTP/HTTPS-запросы

> 📌 С 2016 года (ASP.NET Core 1.0) Kestrel стал стандартным сервером .NET-приложений.

---

# 🔧 Как он запускается?

В `Program.cs`:

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.Run(); // ← Запуск Kestrel
```

Внутри `WebApplication.CreateBuilder()` и `app.Run()` происходит:

1. Чтение конфигураций (`appsettings.json`, переменные среды)
2. Настройка `IHost` (Generic Host)
3. Создание `KestrelServer`
4. Привязка к портам, запуск прослушки входящих HTTP-запросов

---

# 🧠 Архитектура (упрощённо)

```plaintext
Client (Browser)
    ↓
Kestrel (HTTP Listener)
    ↓
Middleware pipeline (app.UseXXX, app.MapXXX)
    ↓
Controllers / Endpoints
    ↓
Response
```

---

# ⚙️ Настройка Kestrel

## 1. Через `appsettings.json`

```json
"Kestrel": {
  "Endpoints": {
    "Http": {
      "Url": "http://localhost:5000"
    },
    "Https": {
      "Url": "https://localhost:5001",
      "Certificate": {
        "Path": "cert.pfx",
        "Password": "123456"
      }
    }
  }
}
```

## 2. Через `Program.cs`

```csharp
builder.WebHost.ConfigureKestrel(serverOptions =>
{
    serverOptions.Limits.MaxRequestBodySize = 10 * 1024 * 1024; // 10MB
    serverOptions.ListenAnyIP(5000); // HTTP
    serverOptions.ListenAnyIP(5001, listenOptions =>
    {
        listenOptions.UseHttps("cert.pfx", "password");
    });
});
```

---

# 🔐 HTTPS и сертификаты

Kestrel поддерживает HTTPS:

* Локально можно использовать **dev-сертификат** (`dotnet dev-certs https --trust`)
* В бою — подключается `*.pfx` файл или используется `Let's Encrypt` через `Reverse Proxy`

---

# ⚠️ Ограничения Kestrel

| Возможность                  | Поддержка                                 |
| ---------------------------- | ----------------------------------------- |
| Поддержка HTTP/1.1, 2.0      | ✅ Да                                      |
| Поддержка HTTPS              | ✅ Да                                      |
| Поддержка HTTP/3             | 🧪 Частично (в .NET 8+)                   |
| CGI, PHP и SSI               | ❌ Нет                                     |
| Автоматическая сжатие        | ✅ Да (через middleware)                   |
| Обработка статических файлов | ✅ Да (`UseStaticFiles`)                   |
| Обратный прокси              | ❌ Нет (но можно использовать с Nginx/IIS) |

---

# 🧱 Kestrel + Reverse Proxy (в продакшене)

В реальных проектах Kestrel часто **не торчит напрямую в интернет**, а работает **за Nginx, Apache или IIS**:

```plaintext
Internet
   ↓
Nginx / IIS (TLS, сжатие, маршрутизация)
   ↓
Kestrel
   ↓
ASP.NET Core приложение
```

Зачем это нужно:

* Безопасность (TLS терминируется на прокси)
* Балансировка нагрузки
* Поддержка дополнительных протоколов
* Обработка других приложений (например, PHP, Node.js)

---

# 📉 Параметры ограничения и настройки

```csharp
serverOptions.Limits.MaxConcurrentConnections = 100;
serverOptions.Limits.MaxConcurrentUpgradedConnections = 10;
serverOptions.Limits.KeepAliveTimeout = TimeSpan.FromSeconds(30);
serverOptions.Limits.RequestHeadersTimeout = TimeSpan.FromSeconds(10);
```

---

# 🧪 Как проверить, что работает Kestrel?

1. Запусти приложение: `dotnet run`
2. Перейди по адресу: `http://localhost:5000`
3. Посмотри в логах:

```
Now listening on: http://localhost:5000
```

Можно также запустить вручную:

```bash
dotnet myapp.dll
```

---

# ✅ Вывод

| Особенность         | Описание                                                    |
| ------------------- | ----------------------------------------------------------- |
| Встроенный сервер   | Используется по умолчанию в ASP.NET Core                    |
| Очень быстрый       | Производительность сравнима с Nginx, Node.js                |
| Кросс-платформенный | Работает в Linux, Windows, macOS                            |
| Поддержка HTTPS     | Есть, можно подключать сертификаты                          |
| Гибкая настройка    | Через `appsettings.json`, `Program.cs` или `IConfiguration` |
| Не требует IIS      | Но может использовать его как Reverse Proxy                 |
