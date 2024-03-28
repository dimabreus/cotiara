import re

class ExpressionEvaluator:
    def __init__(self, variables=None):
        # Определение операторов и их приоритета
        self.ops = {
            '+': (1, lambda a, b: a + b),
            '-': (1, lambda a, b: a - b),
            '*': (2, lambda a, b: a * b),
            '/': (2, lambda a, b: a / b)
        }
        # Словарь переменных и их значений
        self.variables = variables if variables is not None else {}

    def _apply_operator(self, operators, values):
        # Выполняет операцию с двумя верхними значениями в стеке значений
        operator = operators.pop()
        b = values.pop()
        a = values.pop()
        operation = self.ops[operator][1]
        values.append(operation(a, b))

    def evaluate_expression(self, expression):
        # Подготовка выражения и разбиение на токены
        expression = re.sub(r'\s+', '', expression)  # Удаление пробелов
        tokens = re.findall(r'\d+|[+\-*/()]|\b[a-zA-Z]\b', expression)
        values = []  # Стек для чисел
        operators = []  # Стек для операторов

        for token in tokens:
            if token.isdigit():
                # Добавление числа в стек значений
                values.append(int(token))
            elif token in self.variables:
                # Замена переменной на её значение
                values.append(self.variables[token])
            elif token == '(':
                # Открывающую скобку помещаем в стек операторов
                operators.append(token)
            elif token == ')':
                # Вычисляем выражение внутри скобок
                while operators[-1] != '(':
                    self._apply_operator(operators, values)
                operators.pop()  # Удаление открывающей скобки '(' из стека операторов
            elif token in self.ops:
                # Применение операторов с учетом их приоритета
                while (operators and operators[-1] in self.ops and
                       self.ops[operators[-1]][0] >= self.ops[token][0]):
                    self._apply_operator(operators, values)
                operators.append(token)

        # Применяем оставшиеся операторы
        while operators:
            self._apply_operator(operators, values)

        # Возвращаем результат
        if len(values) != 1:
            return expression
            # raise SyntaxError("Invalid expression")
        return values.pop()