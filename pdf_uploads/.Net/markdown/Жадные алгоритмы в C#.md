# 📘 Жадные алгоритмы в C\#

Жадные (greedy) алгоритмы — это стратегия, при которой на каждом шаге выбирается **локально оптимальное** решение с надеждой на получение **глобального оптимума**. Они не всегда дают наилучший результат, но часто работают эффективно для большого класса задач.

---

## 🔍 Основная идея

Жадный алгоритм строит решение шаг за шагом, принимая на каждом этапе **наилучшее с точки зрения текущего состояния** решение, не оглядываясь назад и не анализируя последствия.

---

## ✅ Когда работают

* Когда задача обладает **свойством жадности (greedy-choice property)** — локальный выбор приводит к глобально оптимальному решению.
* Когда задача обладает **оптимальной подструктурой** — оптимальное решение задачи включает в себя оптимальные решения её подзадач.

---

## 📦 Пример 1: Задача о сдаче (монетах)

**Условие:** Дано количество денег и список монет. Найти минимальное количество монет для выдачи суммы.

> ⚠️ Работает корректно только при жадной системе монет (например, 1, 5, 10, 25).

```csharp
int[] coins = { 25, 10, 5, 1 }; // отсортированы по убыванию
int amount = 63;
var result = new List<int>();

foreach (int coin in coins)
{
    while (amount >= coin)
    {
        amount -= coin;
        result.Add(coin);
    }
}

Console.WriteLine("Монеты: " + string.Join(", ", result));
```

---

## 📦 Пример 2: Активности с максимальным количеством (Activity Selection)

**Условие:** Дано N мероприятий с временем начала и окончания. Нужно выбрать максимальное число непересекающихся.

**Жадная стратегия:** Всегда выбирать мероприятие, которое заканчивается раньше всех.

```csharp
class Activity
{
    public int Start { get; set; }
    public int End { get; set; }
}

var activities = new List<Activity>
{
    new() { Start = 1, End = 3 },
    new() { Start = 2, End = 5 },
    new() { Start = 4, End = 6 },
    new() { Start = 6, End = 7 },
    new() { Start = 5, End = 9 },
    new() { Start = 8, End = 9 }
};

var sorted = activities.OrderBy(a => a.End).ToList();
var result = new List<Activity>();

int lastEnd = 0;
foreach (var act in sorted)
{
    if (act.Start >= lastEnd)
    {
        result.Add(act);
        lastEnd = act.End;
    }
}

foreach (var a in result)
    Console.WriteLine($"({a.Start}, {a.End})");
```

---

## 📦 Пример 3: Задача о покрытии отрезков (Interval Covering)

**Условие:** Покрыть отрезок `[0, M]` минимальным числом отрезков из заданного набора.

**Жадный подход:** Всегда выбираем отрезок, который начинается до текущей позиции и имеет максимальное правое окончание.

```csharp
class Segment
{
    public int Start { get; set; }
    public int End { get; set; }
}

int M = 10;
var segments = new List<Segment>
{
    new() { Start = 0, End = 5 },
    new() { Start = 3, End = 7 },
    new() { Start = 6, End = 10 },
    new() { Start = 8, End = 11 }
};

segments = segments.OrderBy(s => s.Start).ToList();
var result = new List<Segment>();
int current = 0, i = 0;

while (current < M)
{
    int maxEnd = -1;
    Segment chosen = null;

    while (i < segments.Count && segments[i].Start <= current)
    {
        if (segments[i].End > maxEnd)
        {
            maxEnd = segments[i].End;
            chosen = segments[i];
        }
        i++;
    }

    if (chosen == null)
    {
        Console.WriteLine("Невозможно покрыть отрезок");
        break;
    }

    result.Add(chosen);
    current = chosen.End;
}

foreach (var s in result)
    Console.WriteLine($"[{s.Start}, {s.End}]");
```

---

## 📦 Пример 4: Минимум платформ на вокзале (Train Platforms)

**Условие:** Дано время прибытия и отбытия поездов. Определить минимальное количество платформ, чтобы избежать пересечений.

```csharp
int[] arrival = { 900, 940, 950, 1100, 1500, 1800 };
int[] departure = { 910, 1200, 1120, 1130, 1900, 2000 };

Array.Sort(arrival);
Array.Sort(departure);

int i = 0, j = 0;
int platforms = 0, maxPlatforms = 0;

while (i < arrival.Length && j < departure.Length)
{
    if (arrival[i] <= departure[j])
    {
        platforms++;
        i++;
        maxPlatforms = Math.Max(maxPlatforms, platforms);
    }
    else
    {
        platforms--;
        j++;
    }
}

Console.WriteLine($"Минимум платформ: {maxPlatforms}");
```

---

## ❗ Пример, где жадность не работает: размен монет

Если монеты: `[1, 3, 4]`, сумма = `6`

Жадный выберет: `4 + 1 + 1 = 3 монеты`, но оптимально: `3 + 3 = 2 монеты`.

➡ Используйте **динамическое программирование**, если:

* есть пересекающиеся подзадачи;
* жадный выбор может привести к неоптимальному результату.

---

## 🧠 Заключение

Жадные алгоритмы:

* Просты и быстры (обычно `O(n log n)` из-за сортировки).
* Отличны для задач с локальным выбором (задачи покрытия, задачи тайминга).
* Но **не универсальны** — важно проверять применимость.

