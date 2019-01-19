# TESL Card Bot
The bot must be hosted and a token must be provided for it to function.

For more info on how to make a bot account and generate a token, visit: https://twentysix26.github.io/Red-Docs/red_guide_bot_accounts/

Available commands as of now:

- !card : Syntax is !card "card name" Looks for the closest match between user entry and card database. All cards up to Morrowind, will be updated with IoM soon after release.

- !deck : Syntax is !deck "export code" Translates export code to readable list.

- !github : Posts link towards the open source code on GitHub.

- !commands: Shows all available commands.

Required permissions in order for the bot to work are Manage Messages and Embed Links.

Should there be any issues, please contact Mynx#6847 on Discord.

# ATTENTION

Visual CPP build tools are REQUIRED to install the python-Levenshtein module, without which you can NOT use the !card command. Make sure you have them before attempting to install the requirements, or it will error and the bot will not start up.

Download link: https://visualstudio.microsoft.com/downloads/#build-tools-for-visual-studio-2017
