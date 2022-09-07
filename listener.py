from src            import objects
from src            import commands
from src            import subprocess
import asyncio
from edamino import Bot, Context, Client, api

loop = False

def main():
    #server = objects.Server()
    bot = commands.login()

    @bot.event(message_types=api.MessageType.ALL, media_types=api.MediaType.ALL)
    async def on_message(ctx: Context):
        global loop
        if loop is False: loop = asyncio.get_event_loop()
        subprocess.run(loop, ctx)
        await commands.message(ctx);

    try:
        bot.start();
    except Exception as e:
        print("Login failed!")
        print("Exception caught:", e)
        objects.botStats.write()


if __name__ == "__main__":
	main()
