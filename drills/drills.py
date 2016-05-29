import discord
from discord.ext import commands

class Drills:
    """Posts drills"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def drills(self):
        """Posts drills"""

        await self.bot.say("http://i.imgur.com/DewESrv.jpg")

def setup(bot):
    bot.add_cog(Drills(bot))
