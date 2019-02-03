from redbot.core import checks, commands
import random

class Sweeper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def sweeper(self, ctx, width : int=7, height : int=7, mineCount : int=10, gameSeed : int=-1):
        """Generates a random Minesweeper board with optional dimensions, mine count, and seed.

           Example: !sweep random 9 9 10 345"""
        # Generates a seed if one is not supplied.
        if gameSeed < 0:
            gameSeed = generateSeed()

        # Displays a temporary message saying that the board is being generated.
        message = await ctx.send("Generating...")
        messageText = displayBoard(generateBoard(width, height, mineCount, gameSeed))
        # Edits the temporary message with a board or an error message.
        await message.edit(content=messageText)

def generateBoard(width : int, height : int, mineCount : int, gameSeed : int):
    """Generates the board using the supplied attributes"""
    # Return an error code if there are no free spaces.
    freeSpaceCount = (width * height) - mineCount
    if (freeSpaceCount <= 0):
        return -1
    # Return an error code if the height or width are too small.
    if (height <= 0 or width <= 0):
        return -2

    # Initialize the board with 0's.
    sweeperBoard = [[0 for x in range(width)] for y in range(height)]

    # Sets the seed in which the mines will be generated.
    random.seed(gameSeed)

    x = mineCount
    # Generate the mines, continuing until there are no more mines to be placed.
    while (x > 0):
        # Randomly determines the position that the next mine will be placed.
        nextMineX = random.randint(0, width - 1)
        nextMineY = random.randint(0, height - 1)
        
        # If there is no mine there, place one. Otherwise try again.
        if (sweeperBoard[nextMineX][nextMineY] != 9):
            sweeperBoard[nextMineX][nextMineY] = 9
            x -= 1

    # loops through each tile on the board to set the mine count.
    for y in range(len(sweeperBoard)):
        for x in range(len(sweeperBoard[x])):
            # If the active tile has a mine, ignore it.
            if (sweeperBoard[x][y] != 9):
                # Loops through the tiles surrounding the active tile.
                for a in range(-1, 2):
                    # Ensures the checked tile is horizontally on the board.
                    if (((x + a) >= 0) and ((x + a) <= (width - 1))):
                        for b in range(-1, 2):
                            # Ensures the checked tile is vertically on the board.
                            if (((y + b) >= 0) and ((y + b) <= (height - 1)) and not ((a == 0) and (b == 0))):
                                # If the checked tile is a mine, increase the number on the active tile to display the
                                # number of mines surrounding it.
                                sweeperBoard[x][y] += (sweeperBoard[x + a][y + b] == 9)
    
    return sweeperBoard

def displayBoard(sweeperBoard : int):
    """Generates a visual representation of the board using emoticons and spoilers"""
    # If the provided sweeperBoard is simply an integer instead of a list, provide an error
    if (isinstance(sweeperBoard, int)):
        error = "Invalid Board."
        if (sweeperBoard == -1):
            error += " Ensure there will be more than 0 free spaces."
        if (sweeperBoard == -2):
            error += " Ensure the width and height are greater than 0."
        return error
    
    # Checks each tile and adds an emoticon depending on the number on the tile. 9 is a mine.
    boardResult = "Sweeper"
    for y in sweeperBoard:
        boardResult += "\n"
        for x in y:
            if (x == 0):
                boardResult += "||:zero:||"
            elif (x == 1):
                boardResult += "||:one:||"
            elif (x == 2):
                boardResult += "||:two:||"
            elif (x == 3):
                boardResult += "||:three:||"
            elif (x == 4):
                boardResult += "||:four:||"
            elif (x == 5):
                boardResult += "||:five:||"
            elif (x == 6):
                boardResult += "||:six:||"
            elif (x == 7):
                boardResult += "||:seven:||"
            elif (x == 8):
                boardResult += "||:eight:||"
            elif (x == 9):
                boardResult += "||:bomb:||"
    return boardResult


def generateSeed():
    return random.seed()
    

def setup(bot):
    bot.add_cog(Sweep(bot))
