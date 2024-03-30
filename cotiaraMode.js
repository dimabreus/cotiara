CodeMirror.defineSimpleMode("cotiara", {
    // Правила для начала строки
    start: [
        // Блочные комментарии /** ... */
        { regex: /\/\*\*(?!\/)/, token: "comment", next: "commentdoc" },
        // Обычные блочные комментарии /* ... */
        { regex: /\/\*/, token: "comment", next: "comment" },
        // Комментарии в стиле //...
        { regex: /(\/\/).*/, token: "comment" },
        // Ключевые слова
        { regex: /\b(var|loop|if|move|leftClick|rightClick|press|func|call)\b/, token: "keyword" },
        // Числа
        { regex: /\b[0-9]+\b/, token: "number" },
        // Операторы
        { regex: /(==|!=|>|<|>=|<=|\+|-|\*|\/|&&|\|\|)/, token: "operator" },
        // Переменные %name%
        { regex: /%[a-zA-Z_][a-zA-Z0-9_]*%/, token: "variable-2" },
        // func ... ( - начало функции
        { regex: /\bfunc\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(/, token: ["keyword", "def"], next: "function" },
        // call ...
        { regex: /\bcall\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(/, token: ["keyword", "variable-3"] },
        // echo
        { regex: /\b(echo)\b/, token: "keyword" },
        // Параметры функции и переменные
        { regex: /\b[a-zA-Z_][a-zA-Z0-9_]*\b/, token: "variable" },
        // Скобки
        { regex: /\)/, token: "bracket" },
    ],
    // Режим для комментариев /** ... */
    commentdoc: [
        { regex: /.*?\*\//, token: "comment", next: "start" },
        { regex: /.*/, token: "comment" }
    ],
    // Режим для комментариев /* ... */
    comment: [
        { regex: /.*?\*\//, token: "comment", next: "start" },
        { regex: /.*/, token: "comment" }
    ],
    // Режим для функций func name(args) {
    function: [
        { regex: /\)/, token: "bracket", next: "start" },
        { regex: /([a-zA-Z_][a-zA-Z0-9_]*)/, token: "variable-3" },
    ],
    // Метаданные
    meta: {
        dontIndentStates: ["comment"],
        lineComment: "//"
    }
});

