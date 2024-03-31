#include <iostream>
#include <unordered_map>
#include <string>
#include <regex>
#include <vector>
#include "expressionEvaluator.h"

class Interpreter
{
private:
    std::unordered_map<std::string, std::string> variables;
    std::vector<std::string> codeBlock;
    bool ifConditionMet;
    bool inIfBlock;

public:
    Interpreter() : ifConditionMet(false), inIfBlock(false) {}

    void AssignVar(std::string varType, std::string varName, std::string value)
    {
        if (varType == "int")
        {
            ExpressionEvaluator evaluator;
            try
            {
                // Evaluate the expression if it's an arithmetic operation
                int intValue = evaluator.evaluateExpression(value);
                variables[varName] = std::to_string(intValue);
            }
            catch (const std::invalid_argument &)
            {
                std::cout << "Invalid value for int variable." << std::endl;
            }
        }
        else if (varType == "str")
        {
            variables[varName] = value;
        }
        else
        {
            std::cout << "Invalid variable type." << std::endl;
        }
    }

    std::string GetVarValue(std::string varName)
    {
        if (variables.find(varName) != variables.end())
        {
            return variables[varName];
        }
        else
        {
            return "Variable not found.";
        }
    }

    void ExecuteCodeBlock(const std::vector<std::string> &block)
    {
        for (const auto &line : block)
        {
            ProcessInput(line);
        }
    }

    void ProcessInput(const std::string &input)
    {
        std::regex assignmentRegex("^\\s*(int|str)\\s+([a-zA-Z_][a-zA-Z0-9_]*)\\s*=\\s*(.*)$");
        std::regex ifStatementRegex("^\\s*if\\s+([a-zA-Z_][a-zA-Z0-9_]*)\\s*(==|!=|<|>)\\s*(.*)\\s*\\{\\s*$");
        std::regex endIfStatementRegex("^\\s*\\}\\s*$");
        std::regex multilineInputRegex("^\\.\\.\\.$");

        std::smatch match;

        if (std::regex_match(input, match, assignmentRegex))
        {
            std::string varType = match[1];
            std::string varName = match[2];
            std::string value = match[3];
            AssignVar(varType, varName, value);
        }
        else if (std::regex_match(input, match, ifStatementRegex))
        {
            std::string varName = match[1];
            std::string op = match[2];
            std::string value = match[3];

            std::string varValue = GetVarValue(varName);
            bool condition = false;
            if (varValue != "Variable not found.")
            {
                if (op == "==")
                {
                    condition = (varValue == value);
                }
                else if (op == "!=")
                {
                    condition = (varValue != value);
                }
                else if (op == "<")
                {
                    condition = (varValue < value);
                }
                else if (op == ">")
                {
                    condition = (varValue > value);
                }
            }
            else
            {
                std::cout << "Variable not found." << std::endl;
            }

            if (condition)
            {
                ifConditionMet = true;
                inIfBlock = true; // Мы вошли в блок if
            }
        }
        else if (std::regex_match(input, match, endIfStatementRegex))
        {
            if (inIfBlock)
            {
                ExecuteCodeBlock(codeBlock);
                inIfBlock = false; // Мы покинули блок if
                codeBlock.clear(); // Очищаем блок кода после выполнения
            }
        }
        else if (std::regex_match(input, match, multilineInputRegex))
        {
            std::string multilineInput;
            while (true)
            {
                std::string line;
                std::getline(std::cin, line);
                if (line == "...")
                {
                    break;
                }
                multilineInput += line + "\n";
            }
            if (inIfBlock)
            {
                codeBlock.push_back(multilineInput); // Добавляем код в блок, если находимся внутри блока if
            }
        }
        else
        {
            if (ifConditionMet && inIfBlock)
            { // Проверяем, находимся ли мы внутри блока if
                codeBlock.push_back(input);
            }
            else if (input.substr(0, 4) == "echo")
            {
                std::string output = input.substr(4);
                std::regex variableRegex("%([a-zA-Z_][a-zA-Z0-9_]*)%");
                std::smatch variableMatch;
                while (std::regex_search(output, variableMatch, variableRegex))
                {
                    std::string varName = variableMatch[1];
                    std::string varValue = GetVarValue(varName);
                    output.replace(variableMatch.position(), variableMatch.length(), varValue);
                }
                std::cout << output << std::endl;
            }
            else if (variables.find(input) != variables.end())
            {
                std::cout << variables[input] << std::endl;
            }
            else
            {
                std::cout << "Command not found." << std::endl;
            }
        }
    }

    void Run()
    {
        std::cout << "Interpreter is running. Type 'exit' to quit." << std::endl;

        while (true)
        {
            std::cout << "> ";
            std::string input;
            std::getline(std::cin, input);
            input.erase(0, input.find_first_not_of(" \t\r\n")); // Trim leading whitespace

            if (input == "exit")
            {
                break;
            }

            ProcessInput(input);
        }
    }
};

int main()
{
    Interpreter interpreter;
    interpreter.Run();
    return 0;
}
