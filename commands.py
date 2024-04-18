import re

commands = [
    {
        "name": "var",
        "regular": r"^var\s(\w+)\s*=\s*(.*)$",
        "syntax": "var variable_name = value",
        "method": "_create_var",
        "parameters": 1
    },
    {
        "name": "echo",
        "regular": r"^echo .+$",
        "syntax": "echo <text>",
        "method": "_echo",
        "parameters": 1
    },
    {
        "name": "loop",
        "regular": r"^loop (\d+) \{(.*)\}?$",
        "flags": re.DOTALL,
        "syntax": "loop <count> {<code>}",
        "method": "_start_loop",
        "parameters": 2
    },
    {
        "name": "if",
        "regular": r"^if (.+) \{(.*)\}?$",
        "flags": re.DOTALL,
        "syntax": "if <condition> {<code>}",
        "method": "_start_if",
        "parameters": 2
    },
    {
        "name": "press",
        "regular": r"^press .+$",
        "syntax": "press <key>",
        "method": "_press",
        "parameters": 1
    },
    {
        "name": "move",
        "regular": r"^move \d+ \d+$",
        "syntax": "move <x> <y>",
        "method": "_move",
        "parameters": 1
    },
    {
        "name": "leftClick",
        "regular": r"^leftClick \d+ \d+$",
        "syntax": "leftClick <x> <y>",
        "method": "_left_click",
        "parameters": 1
    },
    {
        "name": "rightClick",
        "regular": r"^rightClick \d+ \d+$",
        "syntax": "rightClick <x> <y>",
        "method": "_right_click",
        "parameters": 1
    },
    {
        "name": "func",
        "regular": r"^func\s+\w+\s*\([^)]*\)\s*{",
        "syntax": "func <function_name>(<parameters>) {...}",
        "method": "_define_function",
        "parameters": 2
    },
    {
        "name": "call",
        "regular": r"^call\s+\w+\s*\([^)]*\)",
        "syntax": "call <function_name>(<arguments>)",
        "method": "_call_function",
        "parameters": 1
    },
    {
        "name": "import",
        "regular": r"^import\s(\w+)\.cot|import\s(\w+)\sfrom\s(\w+)\.cot$",
        "method": "_import",
        "parameters": 1,
        "syntax": "import <filename>.cot or import <variable or function> from <filename>.cot",
    }
]
