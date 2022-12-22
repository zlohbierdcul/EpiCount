import datetime
import time

messageid = {}


async def clear_chat(channel):
    global messageid

    def is_main_msg(m):
        is_main = False
        if messageid:
            for x in messageid:
                if m.id == messageid[x]:
                    is_main = True
        return not is_main

    await channel.purge(check=is_main_msg)


async def countdown(s, channel):
    no_message = False

    # Calculate the total number of seconds
    total_seconds = s

    # While loop that checks if total_seconds reaches zero
    # If not zero, decrement total time by one second
    while total_seconds > 0:
        # Timer represents time left on countdown
        timer = datetime.timedelta(seconds=total_seconds)

        # Prints the time left on the timer
        print(timer, end="\r")

        # Delays the program one second
        time.sleep(1)

        # Reduces total time by one second
        total_seconds -= 1

    await clear_chat(channel)
