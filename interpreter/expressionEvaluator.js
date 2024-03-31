console.log('executing expressionEvaluator.js')
class ExpressionEvaluator {
    constructor(variables = {}) {
        this.ops = {
            '+': [1, (a, b) => a + b],
            '-': [1, (a, b) => a - b],
            '*': [2, (a, b) => a * b],
            '/': [2, (a, b) => a / b],
            '==': [0, (a, b) => a === b],
            '!=': [0, (a, b) => a !== b],
            '>': [0, (a, b) => a > b],
            '<': [0, (a, b) => a < b],
            '>=': [0, (a, b) => a >= b],
            '<=': [0, (a, b) => a <= b],
            '&&': [-1, (a, b) => a && b],
            '||': [-1, (a, b) => a || b]
        };
        this.variables = variables;
    }

    _applyOperator(operators, values) {
        const operator = operators.pop();
        const b = values.pop();
        const a = values.pop();
        const operation = this.ops[operator][1];
        values.push(operation(a, b));
    }

    evaluateExpression(expression) {
        expression = expression.replace(/\s+/g, '');
        const tokens = expression.match(/\d+|[+\-*/()]|==|!=|>=|<=|>|<|&&|\|\||\b[a-zA-Z]\b/g);
        let values = [];
        let operators = [];

        tokens.forEach(token => {
            if (!isNaN(parseInt(token))) {
                values.push(parseInt(token));
            } else if (token in this.variables) {
                const val = this.variables[token];
                values.push(typeof val === 'boolean' ? val : parseInt(val));
            } else if (token === '(') {
                operators.push(token);
            } else if (token === ')') {
                while (operators[operators.length - 1] !== '(') {
                    this._applyOperator(operators, values);
                }
                operators.pop(); // Remove '('
            } else if (token in this.ops) {
                while (operators.length > 0 && operators[operators.length - 1] in this.ops &&
                    this.ops[operators[operators.length - 1]][0] >= this.ops[token][0]) {
                    this._applyOperator(operators, values);
                }
                operators.push(token);
            }
        });

        while (operators.length > 0) {
            this._applyOperator(operators, values);
        }

        return values.pop();
    }
}

module.exports = ExpressionEvaluator;