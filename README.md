# Custom-Discord-Bot

## 

The bot handles command execution, file uploads to Discord, and file downloads from Discord to the bot's system. The bot also supports sending large command outputs in chunks, making it suitable for large data volumes.

Key Features:
Execute System Commands: The bot can run shell commands and return the output to the user.

Upload Files: Users can upload files from the bot's system to a Discord channel.

Download Files: Users can upload files to Discord, and the bot can download and save them to its working directory.

Handle Large Data: The bot handles large output from commands by chunking and sending it in multiple messages if necessary.


## Example usage 
Run a Command:

1. To run a system command: !cmd <command>
Example: !cmd ipconfig

2. Upload a File:
To upload a file: !cmd upload <file_path>
Example:  !cmd upload D:\Temp\file.txt

3. Download a File: 
To download an attached file:  !cmd download
