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
]