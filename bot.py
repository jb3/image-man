import glob
import logging

from discord.ext import commands
from discord import Embed, Color

from config import config
from log import DiscordHandler

description = """
Solving your image needs
"""

logging.basicConfig(level=logging.INFO)

log = logging.getLogger()


class ImageMan(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="im ", description=description,
                         pm_help=None)

    async def on_ready(self):
        log.info(f"Logged in as {self.user.name}")
        await self.load_cogs()

    async def on_command_error(self, ctx, exception):
        await self.log_error(
            exception.original.args[0],
            title=exception.original.__class__.__name__
        )

    async def log_error(self, exception, title="Error"):
        error_embed = Embed(title=title, color=Color.red())
        error_embed.description = exception

        error_channel = self.get_channel(config.channels.errors)

        log.error(exception)

        await error_channel.send(embed=error_embed)

    async def load_cogs(self):
        files = glob.glob("cogs/*.py")

        module_names = [name.replace("/", ".")[:-3] for name in files]

        for module in module_names:
            try:
                self.load_extension(module)
                log.info(f"[+] Loaded {module}")
            except Exception as e:
                await self.log_error(f"{e.name}: {e.args[0]}",
                                     title="Could not load cog")
                log.error(f"[-] Could not load {module}")


if __name__ == "__main__":
    bot = ImageMan()
    log.addHandler(DiscordHandler(bot))
    bot.run(config.token)
