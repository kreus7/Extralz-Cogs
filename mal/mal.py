import discord
from discord.ext import commands
from .utils.chat_formatting import *
from .utils import checks
from .utils.dataIO import dataIO
from __main__ import send_cmd_help
from xml.etree import ElementTree
import aiohttp
import html
import os

class AnimuAndMango:
    def __init__(self,bot):
        self.bot = bot
        self.credentials = dataIO.load_json("data/mal/credentials.json")

    # Searches for and fetches an anime
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

    # Searches for and fetches a manga
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

    # Command group for setting MyAnimeList credentials
    @commands.group(pass_context=True)
    async def malset(self, ctx):
        """Manages MyAnimeList settings"""
        if ctx.invoked_subcommand is None:
            await send_cmd_help(ctx)

    # Sets the username used to fetch articles from MyAnimeList
    @malset.command(name="username")
    @checks.is_owner()
    async def _username_malset(self, *username):
        """Sets the username used to log into MyAnimeList

           Please consider sending this to the bot privately"""
        if len(username) == 1:
            self.credentials["username"] = username
            dataIO.save_json("data/mal/credentials.json", self.credentials)
            await self.bot.say("Username set.")
        else:
            await self.bot.say("Invalid username.")

    # Sets the password used to fetch articles from MyAnimeList
    @malset.command(name="password")
    @checks.is_owner()
    async def _password_malset(self, *password):
        """Sets the password used to log into MyAnimeList

           Please consider sending this to the bot privately"""
        if len(password) > 0:
            msg = " ".join(password)
            self.credentials["password"] = msg
            dataIO.save_json("data/mal/credentials.json", self.credentials)
            await self.bot.say("Password set.")
        else:
            await self.bot.say("Invalid password.")

# Fetches a list of anime/manga, prompts the user to select one, and returns its information.
async def fetch_article(self, ctx, msg, nature):
    self.credentials = dataIO.load_json("data/mal/credentials.json")
    search =  "http://myanimelist.net/api/{}/search.xml?q={}".format(nature, msg)

    try:
        auth = aiohttp.BasicAuth(login = self.credentials["username"], password = self.credentials["password"])
        with aiohttp.ClientSession(auth=auth) as s:
            async with s.get(search) as r:
                data = await r.text()
        if not data:
            return "I didn't find anything :cry: ..."
        root = ElementTree.fromstring(data)
        if len(root) == 0:
            return "Sorry, I found nothing :cry:."
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

# Checks if the data folder exists and, if not, creates it
def check_folder():
    if not os.path.exists("data/mal"):
        print ("Creating data/mal folder...")
        os.makedirs("data/mal")

# Checks if the credentials json exists and, if not, initiates it with default values
def check_files():
    credentials = {"username":"undefined",
                   "password":"undefined"}

    if not dataIO.is_valid_json("data/mal/credentials.json"):
        print ("Creating default mal credentials.json...")
        dataIO.save_json("data/mal/credentials.json", credentials)

def setup(bot):
    check_folder()
    check_files()
    bot.add_cog(AnimuAndMango(bot))
