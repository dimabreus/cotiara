# Cotiara

## Введение

Cotiara — это язык программирования, предназначенный для автоматизации задач, связанных с управлением клавиатурой и мышью. Он позволяет быстро разрабатывать скрипты для имитации пользовательских действий, обработки условий и выполнения повторяющихся задач.

## Начало работы


Перед использованием Cotiara убедитесь, что у вас есть интерпретатор.
Можно скачать интерпретатор Cotiara как библиотеку используя pip.
Доступен также [онлайн-интерпретатор](https://dimabreus.ru/cotiara/).
Также есть [расширение для Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=dimabreus.cotiara),
которое обеспечивает подсветку синтаксиса и форматирование кода на Cotiara.

### Установка

Для установки интерпретатора просто используйте pip
```bash
pip install cotiara
```

### Запуск

#### Для пользователей VS Code с [расширением](https://marketplace.visualstudio.com/items?itemName=dimabreus.cotiara): 

- Выключить в настройках расширения локальный интерпретатор
- Находясь в файле с расширением `.cot` нажать на кнопку запуска файла

#### Ручной запуск

- Выполнить следующую команду в терминале:
```bash
cotiara "path/to/file.cot" 
```

## Основы языка

### Работа с переменными

```cotiara
/* Объявление переменной */
var a = 1

/* Изменение значения переменной */
var a = 2
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

### Операторы сравнения

```cotiara
/* Равенство */
var isEqual = 1 == 1 /* True */

/* Неравенство */
var isNotEqual = 1 != 2 /* True */

/* Больше */
var isGreaterThan = 5 > 3 /* True */

/* Меньше */
var isLessThan = 3 < 5 /* True */

/* Больше или равно */
var isGreaterOrEqual = 5 >= 5 /* True */

/* Меньше или равно */
var isLessOrEqual = 3 <= 5 /* True */
```

### Логические операторы

```cotiara
/* Логическое И (AND) */
var andResult = true && false /* False */

/* Логическое ИЛИ (OR) */
var orResult = true || false /* True */
```


### Вывод текста на экран

```cotiara
echo Привет, мир! /* Выводит текст: Привет, мир! */
```

### Комментарии

```cotiara
/* Комментарий */

/*
Многострочный комментарий
*/
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

### Импорты

#### import
Интерпретация кода файла, не передавая переменные и функции

##### Правильное использование:

```cotiara
/* hello.cot */

echo Hello, World!
```

```cotiara
/* main.cot */

import hello.cot
/* 
Hello, World!
*/
```

##### Неправильное использование:

```cotiara
/* variables.cot */

var a = 2
var b = 4
```

```cotiara
/* main.cot */

import variables.cot

echo %a% /* %a% (переменная не найдена) */
```

### import from
Интерпретация кода и получение переменной или функции

```cotiara
/* variables.cot */

var a = 2
var b = 4
```

```cotiara
/* main.cot */

import a from variables.cot

echo %a% /* 2 */
echo %b% /* %b% (переменная не найдена) */
```

---

```cotiara
/* functions.cot */

func sum(a, b) {
    var c = %a% + %b%
    echo %c%
}
```

```cotiara
/* main.cot */

import sum from functions.cot

call sum(5, 5) /* 10 */
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

[Дискорд сообщество](https://discord.gg/g9nwE2Ekjt)