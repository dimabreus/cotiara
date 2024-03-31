import re

from .commands import commands
from .expressionEvaluator import ExpressionEvaluator
from .function import Function


class Interpreter:
    def __init__(self, echo, press, move, left_click, right_click):
        self.vars = {}
        self.functions = {}
        self.evaluator = ExpressionEvaluator(self.vars)
        self.echo = echo
        self.press = press
        self.move = move
        self.left_click = left_click
        self.right_click = right_click

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
                for param, arg in zip(function.parameters, args):
                    self.vars[param] = arg
                self.interpret(iter(function.expressions))
        else:
            raise ValueError(f"Function {func_name} is not defined.")

    @staticmethod
    def _collect_block(all_expressions):
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
        self.echo(output)

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
        self.press(button)

    def _move(self, expression):
        x, y = re.match(r"^move (\d+) (\d+)$", expression).groups()
        self.move(int(x), int(y))

    def _left_click(self, expression):
        x, y = re.match(r"^leftClick (\d+) (\d+)$", expression).groups()
        self.left_click(int(x), int(y))

    def _right_click(self, expression):
        x, y = re.match(r"^rightClick (\d+) (\d+)$", expression).groups()
        self.right_click(int(x), int(y))
