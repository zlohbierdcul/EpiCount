from message.chat_clearer import messageid


async def remove_counter(key, channel):
    def should_be_removed(m):
        removed = False
        if m.id == messageid[key]:
            removed = True
        return removed

    if key in messageid:
        await channel.purge(check=should_be_removed)
        del messageid[key]
        return
    else:
        print(f"{id} was not found")
