import re

import pyautogui


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


class Interpreter:
    def __init__(self):
        self.vars = {}  # Словарь для хранения переменных

    # Метод для интерпретации выражения
    def interpret(self, expression):
        if expression.startswith("var"):
            match = re.match(r"^var\s(\w+)\s*=\s*(.*)$", expression)
            if match:
                self._create_var(expression)
            else:
                raise SyntaxError("Invalid syntax for variable declaration. Expected 'var variable_name = value'.")

        elif expression.startswith("echo"):
            match = re.match(r"^echo .+$", expression)
            if match:
                self._echo(expression)
            else:
                raise SyntaxError("Invalid syntax for echo. Expected 'echo <text>'.")

        elif expression.startswith("press"):
            match = re.match(r"^press .+$", expression)
            if match:
                self._press(expression)
            else:
                raise SyntaxError("Invalid syntax for echo. Expected 'echo <text>'.")

        else:
            raise NotImplementedError("This expression type is not supported.")

    def _create_var(self, expression):
        tokens = re.match(r"var\s(\w+)\s*=\s*(.*)", expression).groups()

        var_name = tokens[0]

        evaluator = ExpressionEvaluator(self.vars)

        result = evaluator.evaluate_expression(tokens[1])

        # Присваивание значения переменной
        self.vars[var_name] = result

    def _echo(self, expression):
        output = re.match(r"^echo (.*)$", expression).group(1)

        for var_name, var_value in self.vars.items():
            output = output.replace(f"%{var_name}%", str(var_value))

        print(output)

    def _press(self, expression):
        button = re.match(r"^press (.*)$", expression).group(1)

        for var_name, var_value in self.vars.items():
            button = button.replace(f"%{var_name}%", str(var_value))
        pyautogui.press(button)


# Пример использования интерпретатора
if __name__ == "__main__":
    interpreter = Interpreter()
    while True:
        try:
            expression = input(">> ")
            interpreter.interpret(expression)
            print(interpreter.vars)
        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Error:", e)
