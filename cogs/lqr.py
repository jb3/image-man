import aiohttp
from discord.ext import commands
from discord import File, Member
from wand.image import Image

import logging
import typing
from io import BytesIO

log = logging.getLogger(__name__)


class LiquidRescale(commands.Cog):
    """
    Commands relating to liquid rescaling images
    """
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def download_image(self, url):
        async with self.session.get(url) as response:
            return await response.read()

    def liquid_rescale(self, image_data):
        with Image(blob=image_data) as im:

            if im.height > 500:
                rescale_factor = 500 / im.width
                im.resize(int(im.width * rescale_factor),
                          int(im.height * rescale_factor))
            elif im.width > 500:
                rescale_factor = 500 / im.width
                im.resize(int(im.width * rescale_factor),
                          int(im.height * rescale_factor))

            original_height = im.height
            original_width = im.width

            im.liquid_rescale(width=int(im.width * 0.5),
                              height=int(im.height * 0.5),
                              delta_x=1, rigidity=0)

            im.resize(original_width, original_height)

            binary = im.make_blob('png')

        return binary

    @commands.Cog.cog_unload
    def unload(self):
        self.bot.loop.create_task(self.session.close())

    @commands.command(aliases=["liquidrescale", "lqr"])
    async def liquid_rescale(
        self,
        ctx,
        image: typing.Union[Member, str] = None
    ):
        """
        Liquid rescale an images
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

        rescaling_message = await ctx.send(":information_source: Rescaling...")

        storage = BytesIO()

        binary = self.bot.loop.run_in_executor(
            None,
            self.liquid_rescale,
            image_data
        )

        storage.write(binary)

        await rescaling_message.delete()

        storage.seek(0)
        fil = File(storage, filename="lqr.png")

        await ctx.send(file=fil)




def setup(bot):
    bot.add_cog(LiquidRescale(bot))
