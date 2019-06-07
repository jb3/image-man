import glob
import logging
import urllib.request


from discord.ext import commands
from discord import Embed, Color

from config import config
from log import DiscordHandler

description = """
Solving your image needs
"""

logging.basicConfig(level=logging.INFO)

log = logging.getLogger()


print(urllib.request.urlopen("http://163.172.163.196"))


class ImageMan(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="im ", description=description,
                         pm_help=None)

    async def on_ready(self):
        log.info(f"Logged in as {self.user.name}")
        await self.load_cogs()

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

    async def on_command_error(self, ctx, error):
        # Try provide some user feedback instead of logging all errors.

        if isinstance(error, commands.CommandNotFound):
            return  # No need to unknown commands anywhere or return feedback

        if isinstance(error, commands.MissingRequiredArgument):
            # Missing arguments are likely human error so do not need logging
            parameter_name = error.param.name
            return await ctx.send(f"\N{NO ENTRY SIGN} Required argument "
                                  f"{parameter_name} was missing")
        elif isinstance(error, commands.CheckFailure):
            return await ctx.send("\N{NO ENTRY SIGN} You do not have "
                                  "permission to use that command")
        elif isinstance(error, commands.CommandOnCooldown):
            retry_after = round(error.retry_after)
            return await ctx.send(f"\N{HOURGLASS} Command is on cooldown, try"
                                  f"again after {retry_after} seconds")

        # All errors below this need reporting and so do not return

        if isinstance(error, commands.ArgumentParsingError):
            # Provide feedback & report error
            await ctx.send("\N{NO ENTRY SIGN} An issue occurred while"
                           "attempting to parse an argument")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("\N{NO ENTRY SIGN} Conversion of an argument"
                           "failed")
        else:
            await ctx.send("\N{NO ENTRY SIGN} An error occured during "
                           "execution, the error has been reported.")

        extra_context = {
            "discord_info": {
                "Channel": ctx.channel.mention,
                "User": ctx.author.mention,
                "Command": ctx.message.content
            }
        }

        if ctx.guild is not None:
            # We are NOT in a DM
            extra_context["discord_info"]["Message"] = (
                f'[{ctx.message.id}](https://discordapp.com/channels/'
                f'{ctx.guild.id}/{ctx.channel.id}/{ctx.message.id})'
            )
        else:
            extra_context["discord_info"]["Message"] = f"{ctx.message.id} (DM)"

        log.exception(error, extra=extra_context)


if __name__ == "__main__":
    bot = ImageMan()
    log.addHandler(DiscordHandler(bot))
    bot.run(config.token)
