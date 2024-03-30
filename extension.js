const vscode = require('vscode');

class CotiaraFormatter {
    provideDocumentFormattingEdits(document) {
        const edits = [];
        let indentLevel = 0;
        const indentSize = 4;

        for (let i = 0; i < document.lineCount; i++) {
            const line = document.lineAt(i);

            if (line.text.trim().startsWith('}')) {
                indentLevel = Math.max(0, indentLevel - 1);
            }

            let formattedText = line.text
                .trim()
                .replace(/(\S)([+\-*/><=]{1,2})(\S)/g, '$1 $2 $3') // Отступы вокруг операторов
                .replace(/,(\S)/g, ', $1') // Пробелы после запятых
                .replace(/\)\s*{/, ') {') // Добавление пробела между ) и {
                .replace(/(\S)\s+{/, '$1 {'); // Убеждаемся, что перед { только один пробел

            const currentIndent = ' '.repeat(indentLevel * indentSize);
            formattedText = currentIndent + formattedText;

            const range = new vscode.Range(i, 0, i, line.text.length);
            edits.push(vscode.TextEdit.replace(range, formattedText));

            if (line.text.includes('{')) {
                indentLevel++;
            }
        }

        return edits;
    }


}

function activate(context) {
    let disposable = vscode.commands.registerCommand('cotiara.runFile', function () {
        const editor = vscode.window.activeTextEditor;
        if (!editor) {
            return;
        }

        const config = vscode.workspace.getConfiguration('cotiara');
        const useLocalInterpreter = config.get('useLocalInterpreter');

        const filePath = editor.document.fileName;
        const terminal = vscode.window.createTerminal("Cotiara");

        if (useLocalInterpreter) {
            const interpreterPath = config.get('pathToInterpreter');

            if (!interpreterPath) {
                vscode.window.showErrorMessage("The use of a local interpreter is enabled and the path to the interpreter is not entered");
                return;
            }

            terminal.show();
            terminal.sendText(`python "${interpreterPath}" "${filePath}"`);
        } else {
            terminal.show();
            terminal.sendText(`cotiara "${filePath}"`);
        }
    });

    context.subscriptions.push(disposable);
    context.subscriptions.push(vscode.languages.registerDocumentFormattingEditProvider('cotiara', new CotiaraFormatter()));
}

exports.activate = activate;