from message.chat_clearer import messageid


async def remove_counter(key, channel):
    # print(f'messageid: {messageid}')

    def should_be_removed(m):
        should_be_removed = False
        if m.id == messageid[key]:
            should_be_removed = True
        return should_be_removed

    if key in messageid:
        await channel.purge(check=should_be_removed)
        del messageid[key]
        return
    else:
        print(f"{id} was not found")
