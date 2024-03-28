# Cotiara

## Переменные

### Объявление переменных:

```cotiara
var a = 1
```

### Перезапись переменных:

```cotiara
var a = 2
```

## Операторы:

### Оператор +

```cotiara
var a = 2 + 2
```

### Оператор -

```cotiara
var a = 2 - 2
```

### Оператор *

```cotiara
var a = 2 * 2
```

### Оператор /

```cotiara
var a = 2 / 2
```

## Логические операторы:

### Оператор ==

```cotiara
var a = 1 == 1
```

### Оператор !=

```cotiara
var a = 1 != 1
```

### Оператор >

```cotiara
var a = 2 > 1
```

### Оператор <

```cotiara
var a = 1 < 2
```

### Оператор >=

```cotiara
var a = 1 >= 1
```

### Оператор <=

```cotiara
var a = 1 <= 1
```

### Оператор && (И)

```cotiara
var a = 1 == 1
var b = 1 == 2
var c = a && b /* False */
```

```cotiara
var a = 1 == 1
var b = 2 == 2
var c = a && b /* True */
```

### Оператор || (ИЛИ)

```cotiara
var a = 1 == 1
var b = 1 == 2
var c = a || b /* True */
```

```cotiara
var a = 1 == 1
var b = 2 == 2
var c = a || b /* True */
```

## Вывод текста

### echo

```cotiara
echo aboba /* aboba */
```

```cotiara
var a = 1
echo %a% /* 1 */
```
## Комментарии

```cotiara
/* Комментарий */
```

## Циклы

### loop

```cotiara
loop 5 {
echo hi
}
/*
hi
hi
hi
hi
hi
*/
```

## Проверки

### if

```cotiara
if 1 == 1 {
echo hi
}
/* hi */
```

## Основные функции языка:

### move
#### Перемещение курсора на заданные координаты

```cotiara
move 200 200
```

```cotiara
var x = 200
var y = 200
move %x% %y%
```

### leftClick
#### Левый клик мышью по заданным координатам

```cotiara
leftClick 200 200
```

```cotiara
var x = 200
var y = 200
leftClick %x% %y%
```

### rightClick
#### Левый клик мышью по заданным координатам

```cotiara
rightClick 200 200
```

```cotiara
var x = 200
var y = 200
rightClick %x% %y%
```

### press
#### Нажатие клавиши

```cotiara
press a
```

```cotiara
var button = a
press %button%
```