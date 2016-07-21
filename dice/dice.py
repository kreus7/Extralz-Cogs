import discord
from discord.ext import commands
from .utils.chat_formatting import *
from __main__ import send_cmd_help
import dice

class Dice:
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def dice(self, ctx, *text):
        """Rolls dice. Limit to two operators (extensible with parenthesis). Can use Fudge dice (dF).

           Multiple dice can be supplied, giving each of the results and displaying the largest.

           Usage: [p]dice [expression]
           Example: !dice 2d6
           Example: !dice 3d4 d20"""
        # If there is one dice, roll it and give the result
        if len(text) == 1:
            text = list(text)
            text[0] += "p"
            fudgeCounter = fudgeCheck(text[0])
            diceRoll = rollDice(text[0], fudgeCounter)
            await self.bot.say(":game_die: {} :game_die:".format(diceRoll))
        # If there are multiple dice, roll all of them and give the largest number
        elif len(text) > 1:
            diceRoll = ['']*len(text) # Initializes diceRoll as a list with the amount of dice rolls
            output = ":game_die:"

            # Picks each dice and rolls them
            for diceNumber in range(0, len(text)):
                text = list(text)
                text[diceNumber] += "p"
                fudgeCounter = fudgeCheck(text[diceNumber])
                diceRoll[diceNumber] = rollDice(text[diceNumber], fudgeCounter)

                # Attempts to compare the last rolled dice to the current largest number
                # If it succeeds or gives an error, that one is now considered the largest
                try:
                    if diceRoll[diceNumber] > largestRoll:
                        largestRoll = diceRoll[diceNumber]
                except:
                    largestRoll = diceRoll[diceNumber]
                output += " {} :game_die:".format(diceRoll[diceNumber])

            # Pastes the output, displaying the largest result at the end
            await self.bot.say("{} = **{}**".format(output, largestRoll))
        # If there are no dice, send the help message for the command
        else:
            await send_cmd_help(ctx)

# Checks how many fudge dice exist in the supplied string
def fudgeCheck(string):
    fudgeNumber = 0
    for character in range(0, len(string)):
        if string[character] == 'd':
            if string[character+1].lower() == 'f':
                fudgeCounter = countDice(string, character, "")

                # If the result can be converted to a number, return that number, otherwise return 1
                try:
                    fudgeNumber += int(fudgeCounter)
                except:
                    fudgeNumber += 1

    # Return the number of fudge dice available.
    return fudgeNumber

# Rolls the dice, subtracting 2 per fudge dice
def rollDice(string, fudgeCounter : int=1):
    if fudgeCounter > 0:
        string = string.replace('F', '3')
        string = string.replace('f', '3')
    string = string.replace('p', '')
    diceRoll = dice.roll("0+({})".format(string))
    diceRoll += fudgeCounter * -2
    return diceRoll

# Returns a full number in a recursive check of characters in reverse from an index from a string
def countDice(string, currentIndex, output):
    try:
        int(string[currentIndex-1])
        output = "{}{}".format(countDice(string, currentIndex-1, output), string[currentIndex-1])
        return output
    except:
        return ""

def setup(bot):
    bot.add_cog(Dice(bot))
