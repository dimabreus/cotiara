import re

class ExpressionEvaluator:
    def __init__(self, variables=None):
        self.ops = {
            '+': (1, lambda a, b: a + b),
            '-': (1, lambda a, b: a - b),
            '*': (2, lambda a, b: a * b),
            '/': (2, lambda a, b: a / b),
            '==': (0, lambda a, b: a == b),  # Оператор сравнения равенства
            '!=': (0, lambda a, b: a != b),  # Оператор сравнения неравенства
            '>': (0, lambda a, b: a > b),    # Оператор сравнения больше
            '<': (0, lambda a, b: a < b),    # Оператор сравнения меньше
            '&&': (-1, lambda a, b: a and b),  # Логический оператор И
            '||': (-1, lambda a, b: a or b)    # Логический оператор ИЛИ
        }
        self.variables = variables if variables is not None else {}

    def _apply_operator(self, operators, values):
        operator = operators.pop()
        b = values.pop()
        a = values.pop()
        operation = self.ops[operator][1]
        values.append(operation(a, b))

    def evaluate_expression(self, expression):
        expression = re.sub(r'\s+', '', expression)
        # Обновленная регулярка для корректного разделения всех операторов, включая && и ||
        tokens = re.findall(r'\d+|[+\-*/()]|==|!=|>|<|&&|\|\||\b[a-zA-Z]\b', expression)
        values = []
        operators = []

        for token in tokens:
            if token.isdigit():
                values.append(int(token))
            elif token in self.variables:
                val = self.variables[token]
                values.append(val if isinstance(val, bool) else int(val))
            elif token == '(':
                operators.append(token)
            elif token == ')':
                while operators[-1] != '(':
                    self._apply_operator(operators, values)
                operators.pop()
            elif token in self.ops:
                while (operators and operators[-1] in self.ops and
                       self.ops[operators[-1]][0] >= self.ops[token][0]):
                    self._apply_operator(operators, values)
                operators.append(token)

        while operators:
            self._apply_operator(operators, values)

        return values.pop()
