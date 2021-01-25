import discord
from redbot.core import commands
from redbot.core.utils.chat_formatting import *
import aiohttp
import random

class XKCD(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def xkcd(self, ctx, comicID="latest"):
        """
        Fetches a comic from XKCD.

        Accepts \"latest\", \"random\", or a number.
        """
        try:
            if int(comicID) != None:
                search = "http://xkcd.com/{}/info.0.json".format(comicID)
            url = await fetch_comic(self, comic=search)
            await ctx.send(url)
        except:
            if comicID == "random":
                search = "http://xkcd.com/info.0.json"
                async with aiohttp.get(search) as r:
                    website = await r.json()
                search = "http://xkcd.com/{}/info.0.json".format(random.randint(1, int(website["num"])))

                url = await fetch_comic(self, comic=search)
                await self.bot.say(url)
            if comicID == "latest":
                search = "http://xkcd.com/info.0.json".format(comicID)
                url = await fetch_comic(self, comic=search)
                await self.bot.say(url)

async def fetch_comic(self, comic):
    try:
        async with aiohttp.get(comic) as r:
            website = await r.json()

        if website["img"]:
            return "**{}** {}\nAlt: {}".format(website["title"], website["img"], website["alt"])

    except:
        return "Could not find comic with that ID"

def setup(bot):
    bot.add_cog(XKCD(bot))
