# ❓ `?` и `!` в C\#

В C# символы `?` и `!` — важные части языка, особенно при работе с `nullable`-типами и логикой. Ниже — наглядная шпаргалка с примерами.

---

## 🔹 `!` — логическое отрицание и подавление предупреждений

| Пример       | Описание                                                |
| ------------ | ------------------------------------------------------- |
| `!true`      | Логическое отрицание: `false`                           |
| `!isReady`   | Инвертирует булевое значение                            |
| `someVar!`   | Подавление предупреждения компилятора об `null`         |
| `user!.Name` | Компилятор «поверит», что `user` не `null`, но риск NRE |

### 📌 Пример:

```csharp
string? name = null;
Console.WriteLine(name!); // NullReferenceException в рантайме, но предупреждения нет
```

---

## 🔹 `?` — nullable-тип, безопасный доступ, null-объединение

| Синтаксис             | Назначение                                           | Пример                 |
| --------------------- | ---------------------------------------------------- | ---------------------- |
| `int?`                | Nullable тип (`int`, который может быть `null`)      | `int? age = null;`     |
| `string?`             | Nullable ссылочный тип                               | `string? name = null;` |
| `obj?.Method()`       | Null-условный вызов метода                           | `person?.PrintInfo();` |
| `obj?.Property`       | Null-условный доступ к свойству                      | `person?.Name`         |
| `value ?? defaultVal` | Null-объединение (если null, то использовать другое) | `name ?? "Гость"`      |
| `value ??= newValue`  | Присваивание, если значение равно `null`             | `name ??= "Гость";`    |

---

## 🧠 Таблица-подсказка

| Оператор     | Название                    | Пример               | Что делает                                 |
| ------------ | --------------------------- | -------------------- | ------------------------------------------ |
| `!`          | Логическое отрицание        | `!isOnline`          | `true → false`, `false → true`             |
| `!` (после)  | Подавление nullable-warning | `user!.Name`         | Говорит: "здесь точно не null"             |
| `?` (в типе) | Nullable тип                | `int? x = null;`     | Позволяет значимому типу быть `null`       |
| `?.`         | Null-условный доступ        | `user?.Name`         | Вернёт `null`, если `user == null`         |
| `?.()`       | Null-условный вызов метода  | `user?.Print();`     | Не вызовет исключение, если `user == null` |
| `??`         | Null-объединение            | `name ?? "Default"`  | Если слева `null`, вернёт значение справа  |
| `??=`        | Null-объединение + присв.   | `name ??= "Default"` | Присвоит, если значение `null`             |

---

### **Pattern Matching с `is not null` / `is null`**

```csharp
if (person is not null)
{
    Console.WriteLine(person.Name);
}
```

> Современный способ проверки на `null` без использования `!=`.

---

## 📦 Полный пример

```csharp
class Person
{
    public string? Name { get; set; }

    public void PrintInfo()
    {
        Console.WriteLine($"Имя: {Name}");
    }
}

class Program
{
    static void Main()
    {
        Person? user = null;

        // Null-условный доступ
        Console.WriteLine(user?.Name); // Не вызовет исключение

        // Подавление предупреждения — опасно!
        Console.WriteLine(user!.Name); // Бросит NullReferenceException

        // Null-объединение
        string? name = null;
        string finalName = name ?? "Гость";
        Console.WriteLine(finalName); // Гость

        // Null-объединение с присваиванием
        name ??= "Пользователь";
        Console.WriteLine(name); // Пользователь

        // Обычное отрицание
        bool isOnline = false;
        if (!isOnline)
        {
            Console.WriteLine("Не в сети");
        }
    }
}
```

---

## 💡 Советы

* `!` стоит использовать с осторожностью — это **обещание компилятору**, и если ты ошибся, то получишь `NullReferenceException`.
* `?.` безопаснее, особенно в цепочках: `obj?.Child?.Name`
* Старайся избегать `!`, если можно обойтись `if (obj != null)` или pattern matching
* `??` и `??=` помогают установить **значения по умолчанию**

---

## 📚 Полезные ссылки

* [Nullable Reference Types — Microsoft Docs](https://learn.microsoft.com/dotnet/csharp/nullable-references)
* [Оператор null-объединения (??) — Microsoft Docs](https://learn.microsoft.com/dotnet/csharp/language-reference/operators/null-coalescing-operator)
