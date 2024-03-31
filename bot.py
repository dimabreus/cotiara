import re

import disnake
from disnake.ext import commands

from interpreter.main import Interpreter
from tokenn import token

bot = commands.Bot(command_prefix="!", intents=disnake.Intents.all(), help_command=None)


@bot.event
async def on_ready():
    print(f'Бот {bot.user} готов к работе!')


# Bot Commands


@bot.command()
async def run(ctx):
    content = ctx.message.content

    content = re.sub(r"^!run\n?", "", content)

    match = re.match("```\w*?\n(.*)?```", content, re.DOTALL)

    if match:
        code = match.group(1)
    else:
        code = content

    output = []

    interpreter = Interpreter(
        lambda text: output.append(text),
        lambda key: output.append(f"pressed {key}"),
        lambda x, y: output.append(f"moved to {x}, {y}"),
        lambda x, y: output.append(f"left click on {x}, {y}"),
        lambda x, y: output.append(f"right click on {x}, {y}"),
    )

    code = [line.strip() for line in code.split('\n')]
    code = re.sub(r"\n?/\*.*?\*/\n?", "", "\n".join(code), flags=re.DOTALL).split("\n")

    interpreter.interpret(iter(code))

    await ctx.reply("\n".join(output))


bot.run(token)
