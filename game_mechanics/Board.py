from .ResourceTile import ResourceTile
from .OceanTile import OceanTile
from .SettlementGraph import SettlementGraph
import random
from .Config import RESOURCETYPES
#Should these by Enums. I think so
RESOURCEAMOUNT= {
    "forest":4,
    "hill":3,
    "mountain":3,
    "farm":4,
    "grassland":4,
    "desert": 1
}
PORTTRADES = ["3:1","3:1","3:1","3:1","lumber 2:1", "brick 2:1", "ore 2:1", "wheat 2:1", "livestock 2:1"]
TILENUMS = [2, 3, 3, 4, 4, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 11, 12]
class InvalidRobberError(Exception):
    def __init__(self, message="Invalid Robber Position"):
        self.message = message
        super().__init__(self.message)
    pass

class Board:
    """
    Sets up the Catan board, placing the ports, tiles, tilenums, and resources.
        As well as the robbers
    It made to work up to 4 players

    """
    def __init__(self):
        self.board = []
        self.tileNums = TILENUMS[:]
        self.resources = RESOURCEAMOUNT.copy()
        self.trades = PORTTRADES.copy()
        #set up resourceTiles
            #3 - 4 - 5 - 4 - 3
        self.board.append(self._setUpOceanRow(4))
        self.board.append(self.__setUpResourceTiles(3))
        self.board.append(self.__setUpResourceTiles(4))
        self.board.append(self.__setUpResourceTiles(5))
        self.board.append(self.__setUpResourceTiles(4))
        self.board.append(self.__setUpResourceTiles(3))
        self.board.append(self._setUpOceanRow(4))

        assert len(self.resources) == 0, "did not get all resourceTiles on board"
        assert len(self.tileNums) == 0, "did not get all tilenums assigned to tiles"
        assert len(self.trades) == 0, "did not get all ports assigned to ocean tiles"
        self.nodeGraph = SettlementGraph(self.board, [1,1], (5,3))

        self.robberLocation = None
        self._findRobber()
        self._setRobber(self.robberLocation)
        self.tileToVertices = {}

        #Creates the node graph, linking together all of the possible settlement nodes with there respective tiles
        self.mapTileToSettlements(startingTile=[1, 1], startingTop=0, startingBottom=19, length=3)
        self.mapTileToSettlements(startingTile=[2, 1], startingTop=17, startingBottom=41, length=4)
        self.mapTileToSettlements(startingTile=[3, 1], startingTop=39, startingBottom=66, length=5)
        self.mapTileToSettlements(startingTile=[4, 1], startingTop=68, startingBottom=92, length=4)
        self.mapTileToSettlements(startingTile=[5, 1], startingTop=94, startingBottom=113, length=3)


    def placeRobber(self, cord):
        """
        given a valid cord, places a robber on the tile
        :param cord: [int,int]
        :return: None
        """
        if cord[0] < 1 or cord[1] > 6:
            raise InvalidRobberError(f"location {cord} is not within 1-6")
        if isinstance(self.board[cord[0]][cord[1]], OceanTile):
            raise InvalidRobberError(f"location {cord} is not a tile")
        if self.board[cord[0]][cord[1]].isRobber:
            raise InvalidRobberError(f"location {cord} already has a robber")


        self.board[self.robberLocation[0]][self.robberLocation[1]].isRobber = False
        self.board[cord[0]][cord[1]].isRobber = True
        self.robberLocation = cord

    def mapTileToSettlements(self, startingTile=[1, 1], startingTop=0, startingBottom=19, length=3):
        """
        maps the settlement nodes to the tiles,
        :param startingTile: the tile to start maping the settlement node
        :param startingTop: the top left node for the first tile
        :param startingBottom: the bottom left settlement node for the first tile
        :param length: total number of tiles in the row
        :return:
        """
        top = startingTop
        bottom = startingBottom
        for y in range(length):
            tile = self.board[startingTile[0]][startingTile[1] + y]
            for i in range(3):
                tile.addVertice(top)
                tile.addVertice(bottom)
                top += 2
                bottom += 2
            top -= 2
            bottom -= 2

    def __setUpResourceTiles(self, amount) -> [ResourceTile]:
        """
        Creates a row of land tiles with ocean tiles by its side
        if the ocean tile is designated to have a trade, they are given a random trade

        :param amount: Number of resource tiles to create
        :return:
        """
        row = []
        #Set up the first and last ocean tile
        oceanToAddBegining = None
        oceanToAddAtEnd = None
        if amount % 2 == 1:
            trade = random.choice(self.trades)
            oceanToAddAtEnd = OceanTile(True, trade)
            self.trades.remove(trade)
            oceanToAddBegining = OceanTile()
        else:
            trade = random.choice(self.trades)
            oceanToAddBegining = OceanTile(True, trade)
            self.trades.remove(trade)
            oceanToAddAtEnd = OceanTile()
        row.append(oceanToAddBegining)
        #sets up the land tiles
        for i in range(amount):
            tileType = random.choice(list(self.resources.keys()))
            self.resources[tileType] -= 1
            if self.resources[tileType] == 0:
                del self.resources[tileType]
            if tileType == "desert":
                resTile = ResourceTile(tileType, -1)
            else:
                tileNum = random.choice(self.tileNums)
                resTile = ResourceTile(tileType, tileNum)
                self.tileNums.remove(tileNum)

            row.append(resTile)
        row.append(oceanToAddAtEnd)
        return row

    def _setUpOceanRow(self, amount):
        """
        row is set up as Resource row, but with only ocean tiles
        :param amount: number of tiles
        :return: [OceanTiles...]
        """
        row = []
        for i in range(amount):
            oceanTile = None
            if i == 0 or i == 2:
                trade = random.choice(self.trades)
                oceanTile = OceanTile(True, trade)
                self.trades.remove(trade)
            else:
                oceanTile = OceanTile()
            row.append(oceanTile)
        return row

    def _findRobber(self):
        """
        if the self.robberLocation is empty, then it will iterate through the board and look for where the robber is

        The reason I have to call this function is because my set up resource tile function does not record the position
        of my tiles
        :return:
        """
        if self.robberLocation == None:
            for i, row in enumerate(self.board):
                for y, tile in enumerate(row):
                    if not isinstance(tile, OceanTile) and tile.resource == "desert":
                        #this not isinstance(tile, OceanTile) is necessary in order to ask the tile.resource question
                        #since OceanTiles do not have this attribute
                        self.robberLocation = [i, y]

    def _setRobber(self, boardPosition):
        """
        removes the robber from its current position and sets it to its new position
        :param boardPosition: [x,y]
        :return:
        """
        self.board[self.robberLocation[0]][self.robberLocation[1]].isRobber = False
        self.board[boardPosition[0]][ boardPosition[1]].isRobber = True
        self.robberLocation = boardPosition




    def printBoard(self):
        """
        for debugging purposes, prints the hexagonal board
        :return:
        """
        boardstr = ""
        for i in range(len(self.board)):
            if i == 0 or i == len(self.board) - 1:
                boardstr += " " * 5 + "["
            elif i == 1 or i == len(self.board) - 2:
                boardstr += " " * 4 + "["
            else:
                boardstr += " " * 3 + "["
            for tile in self.board[i]:
                boardstr += tile.__repr__() + " ;"
            boardstr += "]\n"
        print(boardstr)



