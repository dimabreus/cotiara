import re

import pyautogui
import sys
from commands import commands
from expressionEvaluator import ExpressionEvaluator

pyautogui.FAILSAFE = False


class Interpreter:
    def __init__(self):
        self.vars = {}  # Словарь для хранения переменных
        self.evaluator = ExpressionEvaluator(self.vars)

    # Метод для интерпретации выражения
    def interpret(self, expressions):
        for expression in expressions:
            expression = re.sub(r"/\*.*?\*/", "", expression, flags=re.DOTALL)

            for var_name, var_value in self.vars.items():
                expression = expression.replace(f"%{var_name}%", str(var_value))

            if not expression:
                continue

            matched = False

            for command in commands:
                if expression.startswith(command["name"]):
                    if "flags" in command.keys():
                        match = re.match(command["regular"], expression, flags=command["flags"])
                    else:
                        match = re.match(command["regular"], expression)
                    if match:
                        matched = True
                        if command["parameters"] == 1:
                            getattr(self, command["method"])(expression)
                        else:
                            getattr(self, command["method"])(expression, expressions)
                        break
                    else:
                        raise SyntaxError(f"Invalid syntax for {command['name']}. Expected '{command['syntax']}'.")

            if not matched:
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

    def _start_loop(self, expression, all_expressions):
        times = int(re.match(r"loop (\d+)", expression).group(1))
        block_expressions = self._collect_block(all_expressions)
        for _ in range(times):
            self.interpret(iter(block_expressions))

    def _start_if(self, expression, all_expressions):
        condition = re.match(r"if (.+)", expression).group(1)
        block_expressions = self._collect_block(all_expressions)
        condition_result = self.evaluator.evaluate_expression(condition)
        if condition_result:
            self.interpret(iter(block_expressions))

    @staticmethod
    def _collect_block(all_expressions):
        block_expressions = []
        depth = 1
        while depth != 0:
            expression = next(all_expressions).strip()
            if expression.startswith(("loop", "if")):
                depth += 1
            elif expression == "}":
                depth -= 1
            if depth > 0:
                block_expressions.append(expression)
        return block_expressions

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

    def _left_click(self, expression):
        for var_name, var_value in self.vars.items():
            expression = expression.replace(f"%{var_name}%", str(var_value))

        x, y = re.match(r"^leftClick (\d+) (\d+)$", expression).groups()

        pyautogui.leftClick(int(x), int(y))

    def _right_click(self, expression):
        for var_name, var_value in self.vars.items():
            expression = expression.replace(f"%{var_name}%", str(var_value))

        print(expression)

        x, y = re.match(r"^rightClick (\d+) (\d+)$", expression).groups()

        pyautogui.rightClick(int(x), int(y))


FILENAME = "".join(sys.argv[1:2]) or "code.cot"

if __name__ == "__main__":
    interpreter = Interpreter()
    with open(FILENAME, "r", encoding="utf8") as file:
        code = [line.strip() for line in file]
        code = re.sub(r"\n?/\*.*?\*/\n?", "", "\n".join(code), flags=re.DOTALL).split("\n")

    interpreter.interpret(iter(code))
