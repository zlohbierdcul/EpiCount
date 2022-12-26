import discord

from message.message_sender import send_message, create_embeded
from managers.file_manager import write_data


def not_configured(config):
    if "channel" not in config or "prefix" not in config or "admin" not in config:
        return True
    else:
        return False


async def configure_bot(config, bot, channel, admin, configuring):
    configuring = True
    config["channel"] = channel.id
    write_data(config, "data/config.json")
    config_msg = await send_message(channel, create_embeded("Please send the prefix you want to use!",
                                                                    "Suggestions: **!**, **.** or **?**",
                                                                    discord.Color.from_rgb(0, 255, 255)))
    response = await bot.wait_for('message', check=lambda messages: messages.author == messages.author)
    await config_msg.delete()
    config["prefix"] = response.content
    bot.activity = discord.Game(name=f'prefix: {config["prefix"]}')
    config["admin"] = admin
    write_data(config, "data/config.json")


