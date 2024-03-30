console.log('executing commands.js')

const commands = [
    {
        name: "var",
        regular: /^var\s(\w+)\s*=\s*(.*)$/,
        syntax: "var variable_name = value",
        method: "_createVar",
        parameters: 1
    },
    {
        name: "echo",
        regular: /^echo .+$/,
        syntax: "echo <text>",
        method: "_echo",
        parameters: 1
    },
    {
        name: "loop",
        regular: /^loop (\d+) \{(.*)\}?$/,
        flags: "s", // В JavaScript 's' флаг включает режим DOTALL
        syntax: "loop <count> {<code>}",
        method: "_startLoop",
        parameters: 2
    },
    {
        name: "if",
        regular: /^if (.+) \{(.*)\}?$/,
        flags: "s",
        syntax: "if <condition> {<code>}",
        method: "_startIf",
        parameters: 2
    },
    {
        name: "press",
        regular: /^press .+$/,
        syntax: "press <key>",
        method: "_press",
        parameters: 1
    },
    {
        name: "move",
        regular: /^move \d+ \d+$/,
        syntax: "move <x> <y>",
        method: "_move",
        parameters: 1
    },
    {
        name: "leftClick",
        regular: /^leftClick \d+ \d+$/,
        syntax: "leftClick <x> <y>",
        method: "_leftClick",
        parameters: 1
    },
    {
        name: "rightClick",
        regular: /^rightClick \d+ \d+$/,
        syntax: "rightClick <x> <y>",
        method: "_rightClick",
        parameters: 1
    },
    {
        name: "func",
        regular: /^func\s+\w+\s*\([^)]*\)\s*{/,
        syntax: "func <function_name>(<parameters>) {...}",
        method: "_defineFunction",
        parameters: 2
    },
    {
        name: "call",
        regular: /^call\s+\w+\s*\([^)]*\)/,
        syntax: "call <function_name>(<arguments>)",
        method: "_callFunction",
        parameters: 1
    }
];

export default commands;

// Пример использования 's' флага в регулярных выражениях
// const exampleRegex = new RegExp("^example$", "s");
