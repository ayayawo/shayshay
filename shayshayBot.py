from orchestrator import Orchestrator

import discord
from discord import app_commands
from datetime import datetime

orchestrator = Orchestrator()
help_file_name = "help.txt"
command_interpreter = orchestrator.create_command_interpreter(help_file_name)
logger = orchestrator.create_logger()
pre = "שישי"
bot = orchestrator.create_bot(pre)
client = orchestrator.create_client()
tree = app_commands.CommandTree(client)

# functions
server_id = 843477859020308510


@tree.command(name="שבת", description="Tells you when Avishay comes back, so the grind can continue",
              guild=discord.Object(id=server_id))
async def app_get_shabat(ctx):
    await ctx.response.send_message(command_interpreter.get_shabat("hello אבישי"))


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=server_id))


@client.event
async def on_message(message):
    try:
        if message.author == client.user:
            return

        if message.content.startswith(pre):
            text = message.content[len(pre):].strip()

            if message.guild is not None:
                logging_data = (str(message.id), message.guild.name, message.channel.name, message.author.name, text)
                identifier = message.guild.id
            else:
                identifier = message.author.id
                logging_data = (str(message.id), message.author.name, text)
            logger.info("<->".join(logging_data))

            response, file = command_interpreter.choose_command(message, text, identifier)

            logging_data = (str(message.id), response)
            logger.info("<->".join(logging_data))

            if response != "":
                await message.channel.send(response, file=file)

    except Exception as e:
        with open("log.txt", "w") as filer:
            filer.write(str(e))
            filer.write("\n")
            filer.write(str(datetime.now()))
        raise


# running bot
token = orchestrator.create_token()
client.run(token)
