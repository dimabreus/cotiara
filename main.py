import re

import pyautogui

from expressionEvaluator import ExpressionEvaluator


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

        elif expression.startswith("loop"):
            match = re.match(r"loop (\d+) \{(.*)\}", expression, re.DOTALL)
            if match:
                self._loop(expression)
            else:
                raise SyntaxError("Invalid syntax for loop. Expected 'loop <count> {<code>}'.")

        else:
            raise NotImplementedError("This expression type is not supported.")

    # Создание переменной
    def _create_var(self, expression):
        tokens = re.match(r"var\s(\w+)\s*=\s*(.*)", expression).groups()

        var_name = tokens[0]

        evaluator = ExpressionEvaluator(self.vars)

        result = evaluator.evaluate_expression(tokens[1])

        # Присваивание значения переменной
        self.vars[var_name] = result

    # Вывод
    def _echo(self, expression):
        output = re.match(r"^echo (.*)$", expression).group(1)

        for var_name, var_value in self.vars.items():
            output = output.replace(f"%{var_name}%", str(var_value))

        print(output)

    # Нажатие на клавишу
    def _press(self, expression):
        button = re.match(r"^press (.*)$", expression).group(1)

        for var_name, var_value in self.vars.items():
            button = button.replace(f"%{var_name}%", str(var_value))
        pyautogui.press(button)

    def _loop(self, expression):
        # Разбор выражения цикла и выполнение блока кода
        match = re.match(r"loop (\d+) \{(.*)\}", expression, re.DOTALL)
        if not match:
            raise SyntaxError("Invalid syntax for loop. Expected 'loop <count> {<code>}'.")

        count = int(match.group(1))
        code_block = match.group(2).strip().splitlines()

        for _ in range(count):
            for line in code_block:
                self.interpret(line)


# Пример использования интерпретатора
if __name__ == "__main__":
    interpreter = Interpreter()
    multiline_command = ""  # Для хранения многострочных команд
    inside_loop = False  # Флаг, указывающий на то, что мы внутри блока loop

    while True:
        try:
            # Если мы не внутри многострочной команды, читаем новую строку
            if not inside_loop:
                expression = input(">> ")
            else:
                # Добавляем строки к многострочной команде
                expression = input(".. ")
                multiline_command += "\n" + expression

            # Проверяем, начинается ли строка с loop и устанавливаем флаг
            if expression.startswith("loop") and not inside_loop:
                inside_loop = True
                multiline_command = expression
                continue  # Пропускаем дальнейшую обработку и ждем следующий ввод

            # Если мы находим закрывающую скобку, обрабатываем многострочную команду
            if inside_loop and expression.rstrip().endswith("}"):
                inside_loop = False
                interpreter.interpret(multiline_command)
                multiline_command = ""  # Сбрасываем многострочную команду
                continue  # Пропускаем дальнейшую обработку и ждем следующий ввод

            # Обычная обработка команды, если мы не в многострочном режиме
            if not inside_loop:
                interpreter.interpret(expression)
                print(interpreter.vars)

        except KeyboardInterrupt:
            break
        except Exception as e:
            print("Error:", e)
