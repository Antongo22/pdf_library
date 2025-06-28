# ⚙️ Lazy vs Eager Loading в C\#

В C# часто используется подход **"отложенной" (Lazy)** или **"жадной" (Eager)** инициализации объектов или загрузки данных. Понимание разницы между этими подходами особенно важно при работе с большими объёмами данных, Entity Framework, коллекциями, ресурсозатратными операциями и многопоточностью.

---

## 🟢 Что такое Eager Loading?

**Eager Loading (жадная загрузка)** — это подход, при котором объект и все его зависимости инициализируются **немедленно**, в момент создания или обращения.

### 🔸 Пример

```csharp
public class DataService
{
    private readonly HeavyResource _resource = new HeavyResource(); // сразу создается

    public void UseResource()
    {
        _resource.Execute();
    }
}
```

### ✅ Преимущества

* Простота кода: всё доступно сразу.
* Не требует дополнительных проверок (null, состояние).
* Полезен, если объект **точно будет использоваться**.

### ❌ Недостатки

* Может потребовать много памяти и ресурсов при старте.
* Замедляет запуск программы.
* Может загрузить ненужные данные.

---

## 🟡 Что такое Lazy Loading?

**Lazy Loading (отложенная загрузка)** — это подход, при котором объект **не создается**, пока не потребуется впервые. В .NET для этого предусмотрен тип `Lazy<T>`.

### 🔸 Пример с `Lazy<T>`

```csharp
public class DataService
{
    private readonly Lazy<HeavyResource> _resource = new(() => new HeavyResource());

    public void UseResource()
    {
        _resource.Value.Execute(); // создается только при первом вызове
    }
}
```

### ✅ Преимущества

* Экономия памяти и ресурсов.
* Быстрый старт приложения.
* Подходит для объектов, которые могут **никогда не понадобиться**.

### ❌ Недостатки

* Усложнение логики (особенно при многопоточности).
* Задержка в момент первого доступа.
* Возможны ошибки, если ленивый объект не был проинициализирован корректно.

---

## 🔍 Использование Lazy<T> в C\#

`Lazy<T>` — это обёртка вокруг значения, которое будет вычислено **единожды** и **только при первом доступе**.

### Конструкторы

```csharp
var lazy = new Lazy<MyObject>();               // требует MyObject иметь публичный конструктор
var lazy = new Lazy<MyObject>(() => new MyObject("param")); // кастомная инициализация
```

### Потокобезопасность

По умолчанию `Lazy<T>` потокобезопасен (режим `LazyThreadSafetyMode.ExecutionAndPublication`).

```csharp
var lazy = new Lazy<MyObject>(() => new MyObject(), true);
```

Вы можете настроить поведение с помощью `LazyThreadSafetyMode`:

* `None`: без потокобезопасности.
* `PublicationOnly`: создаёт объект несколько раз, но публикует только один.
* `ExecutionAndPublication`: полностью потокобезопасен.

---

## 🧠 Когда использовать Lazy Loading

| Сценарий                             | Подходит для Lazy? |
| ------------------------------------ | ------------------ |
| Загрузка больших коллекций           | ✅ Да               |
| Инстанциирование тяжёлых объектов    | ✅ Да               |
| Инициализация сервисов по требованию | ✅ Да               |
| Часто используемые объекты           | ❌ Лучше Eager      |
| Конфигурация или DI                  | ⚠️ По ситуации     |

---

## 🏗 Пример: Ленивое свойство

```csharp
public class UserProfile
{
    private readonly Lazy<List<string>> _permissions = new(() => LoadPermissions());

    public List<string> Permissions => _permissions.Value;

    private static List<string> LoadPermissions()
    {
        // Долгая операция
        Thread.Sleep(1000);
        return new List<string> { "Read", "Write", "Delete" };
    }
}
```

---

## 🗂 Eager vs Lazy в Entity Framework

### Eager Loading

```csharp
var orders = context.Users
    .Include(u => u.Orders)
    .ToList();
```

* Загрузит пользователей **и** их заказы в **одном** SQL-запросе.
* Используется `Include(...)`.

### Lazy Loading (требует прокси и виртуальных свойств)

```csharp
public class User
{
    public virtual ICollection<Order> Orders { get; set; }
}

var user = context.Users.First();
var orders = user.Orders; // загрузка происходит здесь, при первом доступе
```

* Загрузка происходит **по требованию**, при первом обращении к навигационному свойству.
* Требует поддержки `virtual`, прокси и настройки в `DbContext`.

---

## 🔄 Сравнительная таблица

| Характеристика       | Eager Loading       | Lazy Loading                 |
| -------------------- | ------------------- | ---------------------------- |
| Время инициализации  | Немедленно          | При первом доступе           |
| Использование памяти | Всегда используется | Только если объект нужен     |
| Скорость старта      | Медленнее           | Быстрее                      |
| Сложность            | Ниже                | Выше                         |
| Поддержка в EF       | `Include(...)`      | `virtual`, прокси, настройки |

---

## 💡 Полезные паттерны

* **Lazy Singleton**:

```csharp
public class Singleton
{
    private static readonly Lazy<Singleton> _instance = new(() => new Singleton());

    public static Singleton Instance => _instance.Value;

    private Singleton() { }
}
```

* **Dependency Injection + Lazy**:

```csharp
public class MyService
{
    private readonly Lazy<INotificationService> _notification;

    public MyService(Lazy<INotificationService> notification)
    {
        _notification = notification;
    }

    public void Notify() => _notification.Value.Send();
}
```

---

## 📌 Заключение

* **Eager**, если:

  * Зависимость **всегда используется**.
  * Нужно быстро получить доступ без задержек.
* **Lazy**, если:

  * Объект затратен по ресурсам.
  * Есть вероятность, что он **не понадобится**.
  * Необходимо **отложить** инициализацию до последнего момента.

