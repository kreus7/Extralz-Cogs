import discord
from discord.ext import commands
from .utils.chat_formatting import *
from __main__ import send_cmd_help
import aiohttp
import random

class XKCD:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def xkcd(self, ctx, comicID="latest"):
        """Fetches a comic from XKCD

           Accepts \"latest\", \"random\", or a number"""
        try:
            # Fetches the specified comic
            if int(comicID) != None:
                search = "http://xkcd.com/{}/info.0.json".format(comicID)
            url = await fetch_comic(self, comic=search)
            await self.bot.say(url)
        # Checks if one of a few particular non-number options are supplied
        except:
            if comicID == "random":
                # Grabs the amount of comics available to randomize through by getting the number of the latest comic
                search = "http://xkcd.com/info.0.json"
                async with aiohttp.get(search) as r:
                    website = await r.json()
                search = "http://xkcd.com/{}/info.0.json".format(random.randint(1, int(website["num"])))

                # Fetches the randomized comic and posts it
                url = await fetch_comic(self, comic=search)
                await self.bot.say(url)
            elif comicID == "latest":
                # Fetches the latest comic
                search = "http://xkcd.com/info.0.json".format(comicID)
                url = await fetch_comic(self, comic=search)
                await self.bot.say(url)
            else:
                # Displays the help dialog
                await send_cmd_help(ctx)

# Fetches a comic from a supplied URL
async def fetch_comic(self, comic):
    try:
        # Grabs a web page and turns it into a list
        async with aiohttp.get(comic) as r:
            website = await r.json()

        # If the list contains an expected image, return the title and url of the image
        if website["img"]:
            return "**{}** {}".format(website["title"], website["img"])

    # If an error occurs, assume it couldn't find the comic and return an error
    except:
        return "Could not find comic with that ID"

def setup(bot):
    bot.add_cog(XKCD(bot))
