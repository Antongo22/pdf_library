**Moq Шпаргалка**

**1. Создать mock**
```csharp
var mock = new Mock<IMyService>();
```

**2. Передать mock в код**
```csharp
var service = new MyClass(mock.Object);
```

**3. Проверить, что метод вызвался 1 раз**
```csharp
mock.Verify(x => x.DoWork(), Times.Once);
```

**4. Проверить, что метод не вызывался**
```csharp
mock.Verify(x => x.DoWork(), Times.Never);
```

**5. Проверить вызов с любым аргументом**
```csharp
mock.Verify(x => x.Send(It.IsAny<string>()), Times.Once);
```

**6. Проверить вызов с конкретным аргументом**
```csharp
mock.Verify(x => x.Send("hello"), Times.Once);
```

**7. Проверить вызов с условием на аргумент**
```csharp
mock.Verify(x => x.Send(It.Is<string>(s => s.StartsWith("he"))), Times.Once);
```

**8. Настроить возврат значения**
```csharp
mock.Setup(x => x.GetNumber()).Returns(42);
```

**9. Настроить возврат по аргументу**
```csharp
mock.Setup(x => x.Exists(It.IsAny<int>())).Returns(true);
```

**10. Настроить выброс исключения**
```csharp
mock.Setup(x => x.Send(It.IsAny<string>()))
    .Throws(new InvalidOperationException());
```

**11. Асинхронный возврат**
```csharp
mock.Setup(x => x.GetByIdAsync(It.IsAny<int>()))
    .ReturnsAsync(item);
```

**12. Асинхронное исключение**
```csharp
mock.Setup(x => x.GetByIdAsync(It.IsAny<int>()))
    .ThrowsAsync(new Exception("fail"));
```

**13. Частые `Times`**
```csharp
Times.Once
Times.Never
Times.Exactly(2)
Times.AtLeastOnce()
```

**14. Базовый шаблон теста**
```csharp
[Fact]
public void Test()
{
    // Arrange
    var mock = new Mock<IMyDependency>();
    var service = new MyService(mock.Object);

    // Act
    service.DoSomething();

    // Assert
    mock.Verify(x => x.SomeMethod(), Times.Once);
}
```

**15. Пример для `ITaskNotifier`**
```csharp
[Fact]
public void Create_CallsNotifier()
{
    var notifierMock = new Mock<ITaskNotifier>();
    var service = new TaskService(notifierMock.Object);

    var request = new CreateTaskRequest
    {
        Title = "Task",
        AssigneeEmail = "user@example.com"
    };

    service.Create(request);

    notifierMock.Verify(
        x => x.NotifyAssigned(It.IsAny<TaskItem>()),
        Times.Once);
}
```

**16. Проверка аргумента у `NotifyAssigned`**
```csharp
notifierMock.Verify(
    x => x.NotifyAssigned(It.Is<TaskItem>(t =>
        t.Title == "Task" &&
        t.AssigneeEmail == "user@example.com")),
    Times.Once);
```

**17. Проверка, что вызова не было**
```csharp
Assert.Throws<ArgumentException>(() => service.Create(request));

notifierMock.Verify(
    x => x.NotifyAssigned(It.IsAny<TaskItem>()),
    Times.Never);
```

**18. Что помнить**
- `Setup` = как mock себя ведёт
- `Verify` = как его использовали
- `Object` = поддельная реализация интерфейса
- `It.IsAny<T>()` = любой аргумент
- `It.Is<T>(...)` = аргумент по условию
