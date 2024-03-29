import re
import sys

import keyboard
import pyautogui

from commands import commands
from expressionEvaluator import ExpressionEvaluator

pyautogui.FAILSAFE = False


class Function:
    def __init__(self, name, parameters, expressions):
        self.name = name
        self.parameters = parameters
        self.expressions = expressions


class Interpreter:
    def __init__(self):
        self.vars = {}
        self.functions = {}  # Словарь для хранения функций
        self.evaluator = ExpressionEvaluator(self.vars)

    def interpret(self, expressions):
        for expression in expressions:
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

    def _define_function(self, expression, all_expressions):
        func_declaration = re.match(r"func\s(\w+)\s*\((.*)\)\s*{", expression)
        func_name = func_declaration.group(1)
        parameters = [param.strip() for param in func_declaration.group(2).split(",")]
        block_expressions = self._collect_block(all_expressions)
        function = Function(func_name, parameters, block_expressions)
        self.functions[func_name] = function

    def _call_function(self, expression):
        func_call = re.match(r"call\s(\w+)\s*\((.*)\)", expression)
        func_name = func_call.group(1)
        args = [arg.strip() for arg in func_call.group(2).split(",")]
        if func_name in self.functions:
            function = self.functions[func_name]
            if len(args) != len(function.parameters):
                raise ValueError(
                    f"Function {func_name} expects {len(function.parameters)} arguments, {len(args)} provided.")
            else:
                # Заменяем параметры функции на переданные аргументы
                for param, arg in zip(function.parameters, args):
                    self.vars[param] = arg
                # Интерпретируем выражения внутри функции
                self.interpret(iter(function.expressions))
        else:
            raise ValueError(f"Function {func_name} is not defined.")

    def _collect_block(self, all_expressions):
        block_expressions = []
        depth = 1
        while depth != 0:
            expression = next(all_expressions).strip()
            if expression.startswith(("loop", "if", "func")):
                depth += 1
            elif expression == "}":
                depth -= 1
            if depth > 0:
                block_expressions.append(expression)
        return block_expressions

    def _create_var(self, expression):
        tokens = re.match(r"var\s(\w+)\s*=\s*(.*)", expression).groups()

        var_name = tokens[0]

        evaluator = ExpressionEvaluator(self.vars)

        result = evaluator.evaluate_expression(tokens[1])

        self.vars[var_name] = result

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

    def _press(self, expression):
        button = re.match(r"^press (.*)$", expression).group(1)

        for var_name, var_value in self.vars.items():
            button = button.replace(f"%{var_name}%", str(var_value))
        pyautogui.press(button)

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

    def listen_for_key_events(self):
        if 'on_press' in self.functions:
            def on_event(event, state):
                try:
                    if event.event_type in ['down', 'up']:  # Проверяем тип события: нажатие или отпускание
                        state = 0 if event.event_type == 'down' else 1
                        function = self.functions['on_press']
                        # Первым аргументом передаем состояние клавиши, вторым - код клавиши
                        self.vars[function.parameters[0]] = state
                        self.vars[function.parameters[1]] = event.scan_code
                        self.interpret(iter(function.expressions))
                except Exception as e:
                    print(f"Error during key event handling: {e}")

            keyboard.hook(lambda event: on_event(event, state=0))


FILENAME = "".join(sys.argv[1:2]) or "code.cot"

if __name__ == "__main__":
    interpreter = Interpreter()
    with open(FILENAME, "r", encoding="utf8") as file:
        code = [line.strip() for line in file]
        code = re.sub(r"\n?/\*.*?\*/\n?", "", "\n".join(code), flags=re.DOTALL).split("\n")

    interpreter.interpret(iter(code))
    interpreter.listen_for_key_events()  # Вызов метода для начала отслеживания нажатий клавиш
    keyboard.wait('esc')
