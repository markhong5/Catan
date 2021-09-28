from game_mechanics.Board import Board, OceanTile

#outdated version of Catan. Was a text only version
SHORTHANDFORRESOURCES ={
    "forest":"FO",
    "hill":"H",
    "mountain":"M",
    "farm":"FA",
    "grassland":"G",
    "desert": "D"
}

class CatanText:
    #should I just start developing the pygameArcade version? YES
    def __init__(self):
        self.board = Board()
        self.catanBoard = self.board.board
        self.strBoard = ""
        self.makeBoard()

    def makeBoard(self):
        row = ""
        for i, tile in enumerate(self.catanBoard[1]):
            if isinstance(tile, OceanTile) and i == 0:
                row = self.__sideOceanRight(20, 3)
            elif i == 1:
                row = self.__joinStrHorizontally(row, self.__tile(SHORTHANDFORRESOURCES[tile.resource], tile.num, True))
            elif isinstance(tile, OceanTile):
                row = self.__joinStrHorizontally(row, self.__sideOceanLeft(3))
            else:
                row = self.__joinStrHorizontally(row, self.__tile(SHORTHANDFORRESOURCES[tile.resource], tile.num))

        self.strBoard += row
        padding = 17
        lessPadding = True
        verticallen = 2
        for y in range(2, 6):
            row = ""
            for i, tile in enumerate(self.catanBoard[y]):
                if isinstance(tile, OceanTile) and i == 0:
                    row = self.__sideOceanRight(padding, verticallen)
                elif i == 1:
                    row = self.__joinStrHorizontally(row, self.__bottomTile(SHORTHANDFORRESOURCES[tile.resource], tile.num, True))
                elif isinstance(tile, OceanTile):
                    row = self.__joinStrHorizontally(row, self.__sideOceanLeft(verticallen))
                else:
                    row = self.__joinStrHorizontally(row, self.__bottomTile(SHORTHANDFORRESOURCES[tile.resource],tile.num))
            self.strBoard += row
            if padding > 14 and lessPadding:
                padding -= 3
            else:
                padding += 3
                lessPadding = False
        row = " " * 20
        self.strBoard += self.__bottomRow()
        print(self.strBoard)


    def __topOcean(self):
        space = " "
        char = "@"
        piece = f"{space * 5}{char}\n" +\
                f"{space * 5}{char}\n" + \
                f"{space * 5}{char}\n" + \
                f"{char * 6}\n"
        return piece

    def __sideOceanRight(self, extraSpacing, size):
        space = " "
        char = "@"
        extraSpace = extraSpacing
        piece = ""
        for i in range(size):
            piece += f"{space * extraSpace}{char}{space:2}\n"
        # piece = f"{space * extraSpace}*{space:2}\n" +\
        #         f"{space * extraSpace}*{space:2}\n" + \
        #         f"{space * extraSpace}*{space:2}\n" #+ \
                # f"{space * extraSpace}*{space:2}\n"
        return piece
    def __sideOceanLeft(self, size):
        space = " "
        char = "@"
        piece = ""
        for i in range(size):
            piece += f"{space:2}{char}\n"
        # piece = f"{space:2}*\n" +\
        #         f"{space:2}*\n" + \
        #         f"{space:2}*\n"
                # f"{space:2}*\n"
        return piece
    def __tile(self, resource, num, first=False):
        space = " "
        star = "*"
        number = num
        type = resource
        piece = ""
        if first:
            piece = f"{space * 3}{star}{space * 3}\n" +\
                    f"{star}{number:^5}{star}\n" +\
                    f"{star}{type:^5}{star}\n" #+ \
                    # f"{space * 3}{star}{space * 3}\n"
        else:
            piece = f"{space * 3}{star}{space * 3}\n" +\
                    f"{space}{number:^5}{star}\n" +\
                    f"{space}{type:^5}{star}\n" #+ \
                    # f"{space * 3}{star}{space * 3}\n"

        return piece
    def __bottomTile(self, resource, num, first=False):
        space = " "
        star = "*"
        number = num
        type = resource
        piece = ""
        if first:
            piece = f"{star}{number:^5}{star}\n" +\
                    f"{star}{type:^5}{star}\n" #+ \
                    # f"{space * 3}{star}{space * 3}\n"
        else:
            piece = f"{space}{number:^5}{star}\n" +\
                    f"{space}{type:^5}{star}\n" #+ \
                    # f"{space * 3}{star}{space * 3}\n"

        return piece
    def __bottomRow(self):
        space = " "
        star = "*"
        char = "@"
        piece = f"{space * 20}{char}{space:2}"
        for i in range(3):
            piece += f"{space * 3}{star}{space*3}"
        piece += f"{space:2}{char}"
        return piece
    def __joinStrHorizontally(self, str1, str2):
        splitLines = zip(str1.split("\n"), str2.split("\n"))
        return "\n".join([x + y for x,y in splitLines])

