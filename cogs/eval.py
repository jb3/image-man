from discord.ext import commands


async def is_owner(ctx):
    return ctx.author.id == 165023948638126080


class Eval(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(name="eval")
    @commands.check(is_owner)
    async def _eval(self, ctx, *, code):
        """
        Hahayes!
        """
        await ctx.send(eval(code))


def setup(bot):
    bot.add_cog(Eval(bot))
