from discord.ext import commands
from discord import Member
import typing


class LiquidRescale(commands.Cog):
    """
    Commands relating to liquid rescaling images
    """
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=["liquidrescale", "lqr"])
    async def liquid_rescale(self, ctx, image: typing.Union[Member, str]):
        """
        Liquid rescale an images
        """
        print(image)


def setup(bot):
    bot.add_cog(LiquidRescale(bot))
