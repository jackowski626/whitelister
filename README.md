# whitelister
Whitelister is a Discord bot written in [discord.py](https://discordpy.readthedocs.io/en/latest) in roughly twenty hours. It allows to whitelist Minecraft players from a Discord server. When a user reacts with an emote to a unique bot message, he receives a private message to which he has to reply with his username. If the username given by the user exists, the bot sends a message to a specific channel with three emotes. The user can react one of them to cancel the whitelist request. The two others permit moderators to approve or reject the request. The bot executes then an FTP request to fetch and update a server whitelist.json file. The code to verify Minecraft usernames and uuids is by Clemens Riese. The code could have been split up in modules but due to the current host of this bot, only one file is allowed. No database is available and Jsons are overriden, that is why the bot uses FTP to update or fetch its own configuration, which is located on an external hosting service. 
