#include <iostream>
#include <stack>
#include <functional>
#include <unordered_map>
#include <vector>
#include <string>

class ExpressionEvaluator {
public:
    ExpressionEvaluator() {
        // Инициализация операций
        ops['+'] = {1, [](int a, int b) { return a + b; }};
        ops['-'] = {1, [](int a, int b) { return a - b; }};
        ops['*'] = {2, [](int a, int b) { return a * b; }};
        ops['/'] = {2, [](int a, int b) { return a / b; }};
        // Добавьте остальные операции по аналогии
    }

    int evaluateExpression(const std::string& expression) {
        std::stack<int> values;
        std::stack<char> operators;
        
        for (char token : expression) {
            if (isdigit(token)) {
                values.push(token - '0'); // Преобразование символа в число
            } else if (token == '(') {
                operators.push(token);
            } else if (token == ')') {
                while (!operators.empty() && operators.top() != '(') {
                    applyOperator(operators, values);
                }
                operators.pop(); // Удаление '('
            } else if (ops.find(token) != ops.end()) {
                while (!operators.empty() && ops[operators.top()].first >= ops[token].first) {
                    applyOperator(operators, values);
                }
                operators.push(token);
            }
        }

        while (!operators.empty()) {
            applyOperator(operators, values);
        }

        return values.top();
    }

private:
    std::unordered_map<char, std::pair<int, std::function<int(int, int)>>> ops;

    void applyOperator(std::stack<char>& operators, std::stack<int>& values) {
        char op = operators.top();
        operators.pop();

        int b = values.top();
        values.pop();

        int a = values.top();
        values.pop();

        // Вычисление и возврат результата
        values.push(ops[op].second(a, b));
    }
};