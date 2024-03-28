import re

import pyautogui

from expressionEvaluator import ExpressionEvaluator


class Interpreter:
    def __init__(self):
        self.vars = {}  # Словарь для хранения переменных

    # Метод для интерпретации выражения
    def interpret(self, expression):
        expression = re.sub(r"/\*.*?\*/", "", expression, flags=re.DOTALL)

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

        elif expression.startswith("loop"):
            match = re.match(r"loop (\d+) \{(.*)\}", expression, re.DOTALL)
            if match:
                self._loop(expression)
            else:
                raise SyntaxError("Invalid syntax for loop. Expected 'loop <count> {<code>}'.")

        elif expression.startswith("if"):
            match = re.match(r"if (.+) \{(.*)\}", expression, re.DOTALL)
            if match:
                self._if(expression)
            else:
                raise SyntaxError("Invalid syntax for if. Expected 'if <condition> {<code>}'.")

        elif expression.startswith("press"):
            match = re.match(r"^press .+$", expression)
            if match:
                self._press(expression)
            else:
                raise SyntaxError("Invalid syntax for press. Expected 'press <key>'.")

        elif expression.startswith("move"):
            match = re.match(r"^move \d+ \d+$", expression)
            if match:
                self._move(expression)
            else:
                raise SyntaxError("Invalid syntax for move. Expected 'move <x> <y>'.")

        elif expression.startswith("leftClick"):
            match = re.match(r"^leftClick \d+ \d+$", expression)
            if match:
                self._leftClick(expression)
            else:
                raise SyntaxError("Invalid syntax for move. Expected 'leftClick <x> <y>'.")

        elif expression.startswith("rightClick"):
            match = re.match(r"^rightClick \d+ \d+$", expression)
            if match:
                self._rightClick(expression)
            else:
                raise SyntaxError("Invalid syntax for move. Expected 'rightClick <x> <y>'.")

        else:
            raise NotImplementedError("This expression type is not supported.")

    # Создание переменной
    def _create_var(self, expression):
        tokens = re.match(r"var\s(\w+)\s*=\s*(.*)", expression).groups()

        var_name = tokens[0]

        evaluator = ExpressionEvaluator(self.vars)

        result = evaluator.evaluate_expression(tokens[1])

        self.vars[var_name] = result

    # Вывод
    def _echo(self, expression):
        output = re.match(r"^echo (.*)$", expression).group(1)

        for var_name, var_value in self.vars.items():
            output = output.replace(f"%{var_name}%", str(var_value))

        print(output)

    def _loop(self, expression):
        match = re.match(r"loop (\d+) \{(.*)\}", expression, re.DOTALL)
        count = int(match.group(1))
        code_block = match.group(2).strip().splitlines()

        for _ in range(count):
            for line in code_block:
                self.interpret(line)

    def _if(self, expression):
        match = re.match(r"if (.+) \{(.*)\}", expression, re.DOTALL)
        condition = match.group(1)
        code_block = match.group(2).strip().splitlines()

        evaluator = ExpressionEvaluator(self.vars)
        result = evaluator.evaluate_expression(condition)

        if result:
            for line in code_block:
                self.interpret(line)

    # Нажатие на клавишу
    def _press(self, expression):
        button = re.match(r"^press (.*)$", expression).group(1)

        for var_name, var_value in self.vars.items():
            button = button.replace(f"%{var_name}%", str(var_value))
        pyautogui.press(button)

    # Перемещение курсора
    def _move(self, expression):
        for var_name, var_value in self.vars.items():
            expression = expression.replace(f"%{var_name}%", str(var_value))

        x, y = re.match(r"^move (\d+) (\d+)$", expression).groups()

        pyautogui.moveTo(int(x), int(y))

    def _leftClick(self, expression):
        for var_name, var_value in self.vars.items():
            expression = expression.replace(f"%{var_name}%", str(var_value))

        x, y = re.match(r"^leftClick (\d+) (\d+)$", expression).groups()

        pyautogui.leftClick(int(x), int(y))

    def _rightClick(self, expression):
        for var_name, var_value in self.vars.items():
            expression = expression.replace(f"%{var_name}%", str(var_value))

        print(expression)

        x, y = re.match(r"^rightClick (\d+) (\d+)$", expression).groups()

        pyautogui.rightClick(int(x), int(y))




if __name__ == "__main__":
    interpreter = Interpreter()
    multiline_command = ""  # Для хранения многострочных команд
    inside_multi_line = False  # Флаг, указывающий на то, что мы внутри блока loop или if
    multi_line_type = None  # Тип многострочного блока: loop или if

    with open("code.cot", "r") as file:  # Открываем файл для чтения
        for line in file:  # Читаем файл построчно
            expression = line.strip()  # Убираем пробельные символы с начала и конца строки

            if not expression:  # Пропускаем пустые строки
                continue

            # Проверяем, начинается ли строка с loop или if и устанавливаем флаги
            if (expression.startswith("loop") or expression.startswith("if")) and not inside_multi_line:
                inside_multi_line = True
                multi_line_type = "loop" if expression.startswith("loop") else "if"
                multiline_command = expression
                continue  # Пропускаем дальнейшую обработку и ждем следующий ввод

            if inside_multi_line:
                # Добавляем строки к многострочной команде
                multiline_command += "\n" + expression

            # Если мы находим закрывающую скобку, обрабатываем многострочную команду
            if inside_multi_line and expression.rstrip().endswith("}"):
                inside_multi_line = False
                if multi_line_type == "if":
                    interpreter.interpret(multiline_command)  # Обработка if
                elif multi_line_type == "loop":
                    interpreter.interpret(multiline_command)  # Обработка loop
                multiline_command = ""  # Сбрасываем многострочную команду
                multi_line_type = None  # Сбрасываем тип многострочного блока
                continue  # Пропускаем дальнейшую обработку

            # Обычная обработка команды, если мы не в многострочном режиме
            if not inside_multi_line:
                interpreter.interpret(expression)
                print(interpreter.vars)
