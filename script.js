const codeEditor = CodeMirror.fromTextArea(document.getElementById('codeInput'), {
    mode: "cotiara",
    theme: "monokai",
    autoCloseBrackets: {
        pairs: "{}[]()\"\"''%%",
        explode: "{}[]()"
    },
    lineNumbers: true
});

var customPairs = "{}[]()\"'%;";
customPairs.split('').forEach(function (char) {
    codeEditor.setOption("extraKeys", {
        [char]: function (cm) {
            var selection = cm.getSelection();
            if (selection.length > 0) {
                var openChar = char;
                var closeChar = char;

                // Найти парный закрывающий символ
                switch (char) {
                    case '{': closeChar = '}'; break;
                    case '[': closeChar = ']'; break;
                    case '(': closeChar = ')'; break;
                    case '%': closeChar = '%'; break;
                    // для кавычек нет необходимости менять closeChar
                }

                cm.replaceSelection(openChar + selection + closeChar);
            } else {
                cm.replaceSelection(char);
                if (char !== closeChar) cm.execCommand("goCharLeft");
            }
        }
    });
});

document.getElementById('runBtn').addEventListener('click', function () {
    let code = codeEditor.getValue();
    let output = []

    const interpreter = new window.interpreter(
        text => { output.push(text); document.getElementById('output').innerHTML = `Результат выполнения вашего кода: <br/> ${output.join("<br/>")}` },
        key => { output.push(`pressed: ${key}`); document.getElementById('output').innerHTML = `Результат выполнения вашего кода: <br/> ${output.join("<br/>")}` },
        (x, y) => { output.push(`moved to: ${x}, ${y}`); document.getElementById('output').innerHTML = `Результат выполнения вашего кода: <br/> ${output.join("<br/>")}` },
        (x, y) => { output.push(`leftclick on: ${x}, ${y}`); document.getElementById('output').innerHTML = `Результат выполнения вашего кода: <br/> ${output.join("<br/>")}` },
        (x, y) => { output.push(`rightclick on: ${x}, ${y}`); document.getElementById('output').innerHTML = `Результат выполнения вашего кода: <br/> ${output.join("<br/>")}` },
        (t) => {addDebugLog(t)}
    );

    code = code.replace(/\n?\/\*.*?\*\/\n?/gs, '');

    code = code.split('\n').map(line => line.trim());

    console.log(code)

    const start = new Date();

    addDebugLog("Код запущен");

    interpreter.interpret(code[Symbol.iterator]());

    const end = new Date();

    const dif = end - start;

    addDebugLog(`Код завершен, затраченное время: ${dif}мс`)
    console.log(output)

    document.getElementById('output').innerHTML = `Результат выполнения вашего кода: <br/> ${output.join("<br/>")}`;
});

function addDebugLog(message) {
    const debugLogs = document.getElementById('debugLogs');
    const timestamp = new Date().toLocaleTimeString();
    debugLogs.innerHTML += `[${timestamp}] ${message}<br>`;
}


document.addEventListener('keydown', function (event) {
    if (event.shiftKey && event.altKey) {
        // Проверяем, что нажата буква F
        // event.keyCode === 70 для F
        // используется event.key === 'f' или 'F' для современных браузеров
        if (event.key === 'f' || event.key === 'F') {
            const currentCode = codeEditor.getValue();
            const formattedCode = formatCode(currentCode);

            codeEditor.setValue(formattedCode);

            document.getElementById('output').textContent = 'Код был отформатирован.';
        }
    }

    if (event.ctrlKey) {
        if (event.key === "Enter") {
            alert("Ага, ща, пошел нахуй!")
        }
    }
});




document.getElementById('formatBtn').addEventListener('click', function () {
    const currentCode = codeEditor.getValue();
    const formattedCode = formatCode(currentCode);

    codeEditor.setValue(formattedCode);

    document.getElementById('output').textContent = 'Код был отформатирован.';
});


function formatCode(documentContent) {
    let formattedText = '';
    let indentLevel = 0;
    const indentSize = 4;
    const lines = documentContent.split('\n');

    for (let i = 0; i < lines.length; i++) {
        let line = lines[i];

        if (line.trim().startsWith('}')) {
            indentLevel = Math.max(0, indentLevel - 1);
        }

        line = line
            .trim()
            .replace(/(\S)([+\-*/><=]{1,2})(\S)/g, '$1 $2 $3') // Spaces around operators
            .replace(/,(\S)/g, ', $1') // Spaces after commas
            .replace(/\)\s*{/, ') {') // Space between ) and {
            .replace(/(\S)\s+{/, '$1 {'); // Ensure only one space before {

        const currentIndent = ' '.repeat(indentLevel * indentSize);
        formattedText += currentIndent + line + '\n';

        if (line.includes('{')) {
            indentLevel++;
        }
    }

    return formattedText.trimEnd();
}
