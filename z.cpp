#include <iostream>
#include "expressionEvaluator.h"

int main()
{
    ExpressionEvaluator evaluator;
    std::string expression = "3 + 2 * 2";
    std::cout << "Result: " << evaluator.evaluateExpression(expression) << std::endl;
    return 0;
}