import discord
from discord.ext import commands
from .utils.chat_formatting import *
from __main__ import send_cmd_help
import dice

class GroupList:
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def grouplist(self, ctx, group : discord.Role = None):
        """Lists all users from a group"""
        server = ctx.message.server
        onlineMembers = []
        offlineMembers = []
        sentMessage = ""
        for x in server.members:
            if group in x.roles:
                if str(x.status) != "offline":
                    onlineMembers.append("{}\n".format(x))
                else:
                    offlineMembers.append("{}\n".format(x))
        if onlineMembers != []:
            sentMessage += "Online members of {}: ```\n".format(group)
            for y in onlineMembers:
                sentMessage += y
            sentMessage += "```"
        if offlineMembers != []:
            sentMessage += "Offline members of {}: ```\n".format(group)
            for y in offlineMembers:
                sentMessage += y
            sentMessage += "```"
        if onlineMembers == [] and offlineMembers == []:
            await self.bot.say("No members in {}.".format(group))
        else:
            await self.bot.say("\n{}".format(sentMessage))

def setup(bot):
    bot.add_cog(GroupList(bot))
