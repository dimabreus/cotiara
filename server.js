const express = require('express');
const { runInNewContext } = require('vm');
const Interpreter = require('./interpreter/main');

const app = express();
app.use(express.json()); // Для разбора JSON-запросов

app.post('/run', (req, res) => {
    let { code } = req.body;

    try {



        let output = [];
        let debug = [];

        const interpreter = new Interpreter(
            text => { output.push(text); },
            key => { output.push(`pressed: ${key}`); },
            (x, y) => { output.push(`moved to: ${x}, ${y}`); },
            (x, y) => { output.push(`leftclick on: ${x}, ${y}`); },
            (x, y) => { output.push(`rightclick on: ${x}, ${y}: ${x}, ${y}`); },
            (t) => { debug.push(t) }
        );

        code = code.replace(/\n?\/\*.*?\*\/\n?/gs, '');

        code = code.split('\n').map(line => line.trim());

        console.log(code)

        const start = new Date();

        debug.push("Код запущен");

        interpreter.interpret(code[Symbol.iterator]());

        const end = new Date();
        const dif = end - start;

        debug.push(`Код завершен, затраченное время: ${dif}мс`)
        console.log(output)




        console.log(code)
        res.json({ success: true, output, debug });
    } catch (error) {
        res.json({ success: false, error: error.message });
    }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Сервер запущен на порту ${PORT}`);
});
