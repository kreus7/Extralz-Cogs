import discord
from discord.ext import commands
from .utils.chat_formatting import *
from __main__ import send_cmd_help
import aiohttp
from xml.etree import ElementTree
import html

MAL_USERNAME = 'MAL_USERNAME'
MAL_PASSWORD = 'MAL_PASSWORD'

class AnimuAndMango:
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def animu(self, ctx, *text):
        """Gives you information about an animu."""
        if len(text) > 0:
            msg = "+".join(text)
            url = await fetch_article(self, ctx, msg=msg, nature="anime")
            if url != None:
                await self.bot.say(url)
            else:
                await self.bot.say("Something went wrong. Check your credentials?")
        else:
            await send_cmd_help(ctx)

    @commands.command(pass_context=True)
    async def mango(self, ctx, *text):
        """Gives you information about a mango."""
        if len(text) > 0:
            msg = "+".join(text)
            url = await fetch_article(self, ctx, msg=msg, nature="manga")
            if url != None:
                await self.bot.say(url)
            else:
                await self.bot.say("Something went wrong. Check your credentials?")
        else:
            await send_cmd_help(ctx)

async def fetch_article(self, ctx, msg, nature):
    search =  "http://myanimelist.net/api/{}/search.xml?q={}".format(nature, msg)
    try:
        auth = aiohttp.BasicAuth(login = MAL_USERNAME, password = MAL_PASSWORD)
        with aiohttp.ClientSession(auth=auth) as s:
            async with s.get(search) as r:
                data = await r.text()
        if not data:
            await self.bot.say("I didn't find anything :cry: ...")
            return
        root = ElementTree.fromstring(data)
        if len(root) == 0:
            await self.bot.say("Sorry, I found nothing :cry:.")
        elif len(root) == 1:
            entry = root[0]
        else:
            msg = "**Please choose one by giving its number.**\n"
            msg += "\n".join([ '{} - {}'.format(n+1, entry[1].text) for n, entry in enumerate(root) if n < 10 ])

            await self.bot.say(msg)

            check = lambda m: m.content in map(str, range(1, len(root)+1))
            resp = await self.bot.wait_for_message(author=ctx.message.author, timeout=20)
            if resp is None:
                return

            entry = root[int(resp.content)-1]

        switcher = [
            'english',
            'score',
            'type',
            'episodes',
            'volumes',
            'chapters',
            'status',
            'start_date',
            'end_date',
            'synopsis'
            ]

        msg = '\n**{}**\n\n'.format(entry.find('title').text)

        for k in switcher:
            spec = entry.find(k)
            if spec is not None and spec.text is not None:
                msg += '**{}** {}\n'.format(k.capitalize()+':', html.unescape(spec.text.replace('<br />', '')))

        msg += 'http://myanimelist.net/{}/{}'.format(nature, entry.find('id').text)

        return msg
    except:
        self.bot.say("Error fetching article")

def setup(bot):
    bot.add_cog(AnimuAndMango(bot))
