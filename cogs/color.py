import aiohttp
from discord.ext import commands
from discord import File, Member
from wand.image import Image

import logging
import typing
from io import BytesIO

log = logging.getLogger(__name__)


class Color(commands.Cog):
    """
    Commands relating to liquid rescaling images
    """
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def download_image(self, url):
        async with self.session.get(url) as response:
            return await response.read()

    def do_negate(self, image_data):
        with Image(blob=image_data) as im:

            im.negate()

            binary = im.make_blob('png')

        return binary

    @commands.Cog.cog_unload
    def unload(self):
        self.bot.loop.create_task(self.session.close())

    @commands.command(aliases=["negative", "neg"])
    async def negate(
        self,
        ctx,
        image: typing.Union[Member, str] = None
    ):
        """
        Negates the colours in an image (black to white and vice versa)
        """

        if image is None:
            if len(ctx.message.attachments) == 0:
                image = ""
            else:
                image = ctx.message.attachments[0].url

        if isinstance(image, Member):
            image = str(image.avatar_url_as(format="png"))

        if not image.startswith("http"):
            return await ctx.send(":warning: Make sure to use "
                                  "a proper image link or attach an image.")

        log.info(f"Downloading image from {image}")

        downloading_msg = await ctx.send(":information_source: Downloading...")

        image_data = await self.download_image(image)

        await downloading_msg.delete()

        rescaling_message = await ctx.send(":information_source: Negating...")

        storage = BytesIO()

        binary = await self.bot.loop.run_in_executor(
            None,
            self.do_negate,
            image_data
        )

        storage.write(binary)

        await rescaling_message.delete()

        storage.seek(0)
        fil = File(storage, filename="lqr.png")

        await ctx.send(file=fil)




def setup(bot):
    bot.add_cog(Negate(bot))
