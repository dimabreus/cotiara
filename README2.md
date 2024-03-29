# Улучшенная документация Cotiara

## Введение

Cotiara — это язык программирования, предназначенный для автоматизации задач, связанных с управлением клавиатурой и мышью. Он позволяет быстро разрабатывать скрипты для имитации пользовательских действий, обработки условий и выполнения повторяющихся задач.

## Начало работы

Перед началом использования Cotiara убедитесь, что у вас установлено необходимое программное обеспечение. Вы можете скачать интерпретатор Cotiara как исполняемый файл (.exe) для Windows, как скрипт на Python для использования в других операционных системах, или попробовать онлайн-интерпретатор на официальном сайте. Также доступно расширение для Visual Studio Code, которое обеспечивает подсветку синтаксиса и улучшенное форматирование кода на Cotiara.

## Установка

```plaintext
- Скачайте интерпретатор Cotiara для вашей операционной системы с официального сайта.
- Для пользователей VS Code: установите расширение для Cotiara через Marketplace для подсветки синтаксиса и автоматического форматирования.
- Запустите интерпретатор локально или используйте онлайн-версию для выполнения ваших скриптов.
```

## Основы языка

### Работа с переменными

```cotiara
/* Объявление переменной */
var a = 1

/* Изменение значения переменной */
a = 2
```

### Арифметические операции

```cotiara
/* Сложение */
var sum = 2 + 3 /* 5 */

/* Вычитание */
var difference = 5 - 2 /* 3 */

/* Умножение */
var product = 2 * 3 /* 6 */

/* Деление */
var quotient = 6 / 2 /* 3 */
```

### Логические операции

```cotiara
/* Равенство */
var isEqual = 1 == 1 /* True */

/* Неравенство */
var isNotEqual = 1 != 2 /* True */
```

### Вывод текста на экран

```cotiara
echo Привет, мир! /* Выводит текст: Привет, мир! */
```

### Циклы и условные конструкции

```cotiara
/* Цикл */
loop 5 {
    echo hi
}

/* Условное ветвление */
if 1 == 1 {
    echo hi
}
```

### Функции

```cotiara
/* Объявление функции */
func sum (a, b) {
    var c = %a% + %b%
    echo %c%
}

/* Вызов функции */
call sum(2, 2) /* Выводит: 4 */
```

### Управление мышью и клавиатурой

```cotiara
/* Перемещение курсора */
move 200 200

/* Левый клик мышью */
leftClick 200 200

/* Правый клик мышью */
rightClick 200 200

/* Нажатие клавиши */
press a
```

## Дополнительные сведения

Для получения дополнительной информации, примеров использования и советов по оптимизации ваших скриптов на Cotiara, посетите официальный сайт и присоединяйтесь к сообществу пользователей.