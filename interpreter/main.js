console.log('executing main.js')

import commands from "./commands.js";
import ExpressionEvaluator from "./expressionEvaluator.js";
import ScriptFunction from "./scriptFunction.js";


class Interpreter {
    constructor(echo, press, move, leftClick, rightClick, debug_echo) {
        this.vars = {};
        this.functions = {};
        this.evaluator = new ExpressionEvaluator(this.vars);
        this.echo = echo;
        this.press = press;
        this.move = move;
        this.leftClick = leftClick;
        this.rightClick = rightClick;
        this.debug_echo = debug_echo
    }

    interpret(expressions) {
        for (let expression of expressions) {
            this.debug_echo(`in progress expression ${expression}`)
            for (const [varName, varValue] of Object.entries(this.vars)) {
                this.debug_echo(`%${varName}% has been replaced by ${varValue}`)
                expression = expression.replaceAll(`%${varName}%`, String(varValue));
            }

            if (!expression) {
                continue;
            }

            let matched = false;

            for (const command of commands) {
                if (expression.startsWith(command.name)) {
                    const match = new RegExp(command.regular, command.flags ? command.flags : '').exec(expression);
                    if (match) {
                        matched = true;
                        if (command.parameters === 1) {
                            this[command.method](expression);
                        } else {
                            this[command.method](expression, expressions);
                        }
                        break;
                    } else {
                        throw new SyntaxError(`Invalid syntax for ${command.name}. Expected '${command.syntax}'.`);
                    }
                }
            }

            if (!matched) {
                throw new Error("This expression type is not supported.");
            }
        };
    }

    _defineFunction(expression, allExpressions) {
        const funcDeclaration = expression.match(/func\s(\w+)\s*\((.*)\)\s*{/);
        const funcName = funcDeclaration[1];
        const parameters = funcDeclaration[2].split(",").map(param => param.trim());
        const blockExpressions = Interpreter._collectBlock(allExpressions);
        const functionObj = new ScriptFunction(funcName, parameters, blockExpressions);
        this.functions[funcName] = functionObj;
    }

    _callFunction(expression) {
        const funcCall = expression.match(/call\s(\w+)\s*\((.*)\)/);
        const funcName = funcCall[1];
        const args = funcCall[2].split(",").map(arg => arg.trim());
        if (this.functions.hasOwnProperty(funcName)) {
            const functionObj = this.functions[funcName];
            if (args.length !== functionObj.parameters.length) {
                throw new Error(`ScriptFunction ${funcName} expects ${functionObj.parameters.length} arguments, ${args.length} provided.`);
            } else {
                const newVars = {};
                functionObj.parameters.forEach((param, index) => {
                    newVars[param] = args[index];
                });
                this.interpret(functionObj.expressions, newVars);
            }
        } else {
            throw new Error(`ScriptFunction ${funcName} is not defined.`);
        }
    }

    static _collectBlock(allExpressions) {
        const blockExpressions = [];
        let depth = 1;
        while (depth !== 0) {
            const expression = allExpressions.next().value.trim();
            if (/^(loop|if|func)/.test(expression)) {
                depth += 1;
            } else if (expression === "}") {
                depth -= 1;
            }
            if (depth > 0) {
                blockExpressions.push(expression);
            }
        }
        return blockExpressions;
    }

    _createVar(expression) {
        const tokens = expression.match(/var\s(\w+)\s*=\s*(.*)/);

        const varName = tokens[1];

        const evaluator = new ExpressionEvaluator(this.vars);

        const result = evaluator.evaluateExpression(tokens[2]);

        this.vars[varName] = result;
    }

    _echo(expression) {
        const output = expression.match(/^echo (.*)$/)[1];
        this.echo(output)
    }

    _startLoop(expression, allExpressions) {
        const times = parseInt(expression.match(/loop (\d+)/)[1], 10);
        const blockExpressions = Interpreter._collectBlock(allExpressions);
        for (let i = 0; i < times; i++) {
            this.interpret(blockExpressions[Symbol.iterator]());
        }
    }

    _startIf(expression, allExpressions) {
        const condition = expression.match(/if (.+)/)[1];
        const blockExpressions = Interpreter._collectBlock(allExpressions);
        const conditionResult = this.evaluator.evaluateExpression(condition);
        if (conditionResult) {
            this.interpret(blockExpressions[Symbol.iterator]());
        }
    }

    _press(expression) {
        const button = expression.match(/^press (.*)$/)[1];
        this.press(button)
    }

    _move(expression) {
        const [x, y] = expression.match(/^move (\d+) (\d+)$/).slice(1);

        this.move(parseInt(x, 10), parseInt(y, 10))
    }

    _leftClick(expression) {
        const [x, y] = expression.match(/^leftClick (\d+) (\d+)$/).slice(1);

        this.leftClick(parseInt(x, 10), parseInt(y, 10))
    }

    _rightClick(expression) {
        const [x, y] = expression.match(/^rightClick (\d+) (\d+)$/).slice(1);

        this.rightClick(parseInt(x, 10), parseInt(y, 10))
    }


    // Добавьте здесь оставшиеся методы...

}

window.interpreter = Interpreter;   