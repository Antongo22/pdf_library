# 📦 Файловая структура ASP.NET Core

Файлы в ASP.NET Core организуются по-разному в зависимости от подхода:

---

## 📁 1. **Классическое MVC (Model-View-Controller)**

```plaintext
/Controllers/         ← Контроллеры
/Models/              ← Модели данных
/Views/               ← Razor-шаблоны (*.cshtml)
/wwwroot/             ← Статические файлы (JS, CSS, изображения)
/obj/                 ← Промежуточные артефакты сборки
/bin/                 ← Скомпилированные сборки (DLL, exe)
/appsettings.json     ← Конфигурации
/Program.cs           ← Точка входа
/Startup.cs           ← Конфигурация приложения
```

> Подходит для серверных приложений с Razor Pages, MVC и server-side логикой.

---

## 📁 2. **Minimal API (с .NET 6+)**

```plaintext
/Program.cs           ← Вся конфигурация и роутинг прямо здесь
/appsettings.json     ← Конфигурации
/Endpoints/           ← (необязательно) группа минимальных API-роутов
/bin/
/obj/
/wwwroot/
```

> Подходит для REST API, микросервисов и легких бэкендов.

---

## 📁 3. **Чистая архитектура (Clean Architecture)**

```plaintext
/src/
  Web/                ← ASP.NET Core проект (UI слой)
  Application/        ← Бизнес-логика, интерфейсы
  Domain/             ← Сущности и модели
  Infrastructure/     ← Реализация интерфейсов (EF Core, API и пр.)

/tests/               ← Unit/integration тесты
```

> Подходит для масштабируемых, модульных решений. Зависимости строго направлены от внешнего к внутреннему (инверсия зависимостей).

---

## 📁 wwwroot/

Каталог `wwwroot/` — это **публичная статическая директория**, доступная по URL:

```plaintext
wwwroot/
 ├── css/
 ├── js/
 ├── images/
 └── favicon.ico
```

Если туда положить файл `logo.png`, он будет доступен по пути:
`https://localhost:5001/logo.png`

> Используется для Bootstrap, JavaScript, favicon, frontend-ассетов.

---

# ⚙️ Как запускается ASP.NET Core проект

---

## 🛠 1. `Program.cs` — точка входа

```csharp
var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello, world!");
app.Run();
```

Содержит:

* Настройку DI-контейнера
* Конфигурацию логирования, `appsettings.json`
* Регистрацию middleware
* Создание и запуск `WebApplication`

---

## ⚙️ 2. `Startup.cs` (в .NET 5 и ниже)

Если используется, то:

```csharp
public class Startup
{
    public void ConfigureServices(IServiceCollection services) { ... }

    public void Configure(IApplicationBuilder app, IWebHostEnvironment env) { ... }
}
```

---

## 🌐 3. Веб-сервер Kestrel

* Встроенный HTTP-сервер на базе `libuv` или `Sockets`
* Принимает HTTP-запросы и прокидывает их в middleware пайплайн
* Используется по умолчанию в `Program.cs`

```bash
Hosting environment: Development
Content root path: /home/anton/myproject/
Now listening on: https://localhost:5001
```

---

## 🧩 4. Middleware pipeline

Каждый `UseXxx` в `Program.cs` добавляет **промежуточный обработчик**:

```csharp
app.UseStaticFiles();      // Обрабатывает файлы из wwwroot
app.UseRouting();          // Включает маршрутизацию
app.UseAuthorization();    // Авторизация
app.MapControllers();      // Маппинг контроллеров
```

---

# 🗃 bin/ в ASP.NET Core

### Путь:

```plaintext
/bin/Debug/net8.0/
       или
/bin/Release/net8.0/
```

### Что в нём:

* `MyApp.dll` — основное приложение
* `MyApp.pdb` — отладка
* `*.deps.json`, `*.runtimeconfig.json` — зависимости и runtime-информация
* Все зависимости (`.dll`) пакетов, библиотек, проектов

### Особенности:

* **Фактический запуск** идёт не из папки проекта, а из `bin/`
* В ASP.NET Core может генерироваться файл `web.config` (если сборка под IIS)
* Если используется Razor, то шаблоны `.cshtml` копируются в bin для рендеринга

---

# 🧠 Как запустить ASP.NET Core

### Через Visual Studio:

* F5: запускает с отладчиком (`Debug`)
* Ctrl+F5: без отладчика

### Через CLI:

```bash
dotnet run            # по умолчанию Debug
dotnet run --configuration Release
```

### При запуске:

1. `dotnet` запускает ваш `*.dll` из `bin/`
2. Поднимается Kestrel-сервер
3. Middleware начинает обрабатывать входящие запросы
4. Логика в `Controllers`, `Razor Pages` или `Minimal API` формирует ответ

---

# 🧪 Как влияет структура на работу

| Структура          | Влияние                                               |
| ------------------ | ----------------------------------------------------- |
| 📁 Views           | Должны быть в правильной папке и названы по конвенции |
| 📁 wwwroot         | Только отсюда можно отдать статику                    |
| Program.cs         | Всё начинается отсюда                                 |
| bin/ и obj/        | Не коммитятся, но участвуют в запуске                 |
| Clean Architecture | Улучшает масштабируемость                             |

---

## ✅ Итог

* **`Program.cs` — точка входа**, конфигурирует всё
* **`Startup.cs` (до .NET 6)** разделяет `services` и `pipeline`
* **Kestrel** — веб-сервер, запускает приложение
* **`bin/` и `obj/`** — ключевые технические папки: в `bin/` находится то, что реально исполняется
* **Структура проекта может быть гибкой**, но понимание базовой архитектуры важно
