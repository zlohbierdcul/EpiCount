import discord
import json

messageid = {}

async def clear_chat(channel):
    global messageid
    def is_main_msg(m):
        is_main = False 
        if messageid != []:
            for x in messageid:
                if m.id == messageid[x]:
                    is_main = True
        return not is_main
    await channel.purge(check=is_main_msg)