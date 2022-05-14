from .ResourceTile import ResourceTile
from .OceanTile import OceanTile
from .SettlementNode import SettlementNode

class SettlementGraph:
    """Graph that connects the roads/settlements with the tiles on the board"""
    def __init__(self, board, startCord, endCord):
        self.board = board
        assert type(board[startCord[0]][startCord[1]]) == ResourceTile, "starting cord does not start with a resource tile"
        assert type(board[endCord[0]][endCord[1]]) == ResourceTile, "ending cord does not start with a resource tile"
        self.start = startCord
        self.graph = [None] * 126 #an adjacency list of every node and there connections
        self.nodeMap = {} #a map of Settlement and Road nodes using the numbers given to them on my Catan Graph
            #AKA 0:settlement, 1:road

        self.__addRow(startNodeNum=0, downRoadNodeNum=13, downSettlementNodeNum=19, lenOfRow=13)

        self.__addRow(startNodeNum=17, downRoadNodeNum=34, downSettlementNodeNum=41, lenOfRow=17)
        self.__addRow(startNodeNum=39, downRoadNodeNum=60, downSettlementNodeNum=66, lenOfRow=21)
        self.__addLowerRow(startNodeNum=66, downRoadNodeNum=87, downSettlementNodeNum=92, lenOfRow=21,
                           prevStartRoad=60, prevEndRoad=65)
        self.__addLowerRow(startNodeNum=92, downRoadNodeNum=109, downSettlementNodeNum=113, lenOfRow=17,
                           prevStartRoad=87, prevEndRoad=91)
        self.__addBottomRow(startNodeNum=113, upRoadCounter=109, lenOfRow=13)

        #Add the ports manually since they follow no rule according to my counting system
        self._addAllPorts()


    def _addPort(self, node1, node2, trade):
        """
        Every trade has 2 ports
        if there is a Trade, then give those 2 settlements the ports
        :param node1: SettlementNode
        :param node2: SettlementNode
        :param trade: str
        :return:
        """
        assert trade != None, "Trade is None"
        node1.trade = trade
        node2.trade = trade

    def _addAllPorts(self):
        """
        Manually gives each ports based on my catan Graph in tests the correct trade
        :return:
        """
        self._addPort(self.nodeMap[0], self.nodeMap[2], self.board[0][0].trade)
        self._addPort(self.nodeMap[6], self.nodeMap[8], self.board[0][2].trade)
        self._addPort(self.nodeMap[31], self.nodeMap[33], self.board[1][4].trade)
        self._addPort(self.nodeMap[17], self.nodeMap[41], self.board[2][0].trade)
        self._addPort(self.nodeMap[59], self.nodeMap[86], self.board[3][6].trade)
        self._addPort(self.nodeMap[68], self.nodeMap[92], self.board[4][0].trade)
        self._addPort(self.nodeMap[106], self.nodeMap[108], self.board[5][4].trade)
        self._addPort(self.nodeMap[113], self.nodeMap[115], self.board[6][0].trade)
        self._addPort(self.nodeMap[119], self.nodeMap[121], self.board[6][2].trade)


    def __addRow(self, startNodeNum, downRoadNodeNum, downSettlementNodeNum, lenOfRow, increasingTile=True):
        """

        :param startNodeNum: top left node of a tile. The number is based on my drawing
        :param downRoadNodeNum: the bottom road on my map
        :param downSettlementNodeNum: the node that connects my bottom road and the top left node
        :param lenOfRow: How many nodes there are
        :param increasingTile: If the number of tiles are increasing every row
        :return:
        """
        downCounter = downRoadNodeNum
        ycounter = 0
        startingNodeEven = True if startNodeNum % 2 == 0 else False
        for i in range(startNodeNum, lenOfRow + startNodeNum):
            #FIXME Repeat code alert for __addRow and bottom row. See If I can create a function for this
            if (i % 2 == 0 and startingNodeEven) or (i % 2 == 1 and not startingNodeEven):
                if (i - startNodeNum) % 4 == 0:
                    #Create a down settlement every 4 nodes
                    if i != startNodeNum:
                        ycounter += 1
                    self.addEdge(i, downCounter)
                    self.nodeMap[i] = SettlementNode("Settlement", self.__getResourcetile(self.start[0], self.start[1] + ycounter,
                                                                                  "Bottom", increasingTile))
                    downCounter += 1

                else:
                    self.nodeMap[i] = SettlementNode("Settlement", self.__getResourcetile(self.start[0], self.start[1] + ycounter,
                                                                                               "Top", increasingTile))
            elif (i % 2 == 1 and startingNodeEven) or (i % 2 == 0 and not startingNodeEven):
                self.addEdge(i, i - 1)
                self.addEdge(i, i + 1)
                self.nodeMap[i] = SettlementNode("Road")
        self.start[0] += 1

        #Calculate the ending node for the down nodes
        numOfDownNodes = ((lenOfRow // 4) + 1) + downRoadNodeNum
        # create the node edges for 13, 14, 15, 16
        downCounter = downSettlementNodeNum#19
        for i in range(downRoadNodeNum, numOfDownNodes):
            self.addEdge(i, downCounter)
            self.nodeMap[i] = SettlementNode("Road")
            downCounter += 4

    def __addLowerRow(self, startNodeNum, downRoadNodeNum, downSettlementNodeNum, lenOfRow, prevStartRoad, prevEndRoad):
        #Very similar to addRow, but adds 2 nodes before and after addRow, to account for the board shrinking
        # instead of growing
        self.addEdge(startNodeNum, startNodeNum + 1)
        self.addEdge(startNodeNum, prevStartRoad)
        self.nodeMap[startNodeNum] = SettlementNode("Settlement", self.__getResourcetile(self.start[0] - 1, self.start[1],
                                                                              "Bottom"))
        self.addEdge(startNodeNum + 1, startNodeNum)
        self.addEdge(startNodeNum + 1, startNodeNum + 2)
        self.nodeMap[startNodeNum + 1] = SettlementNode("Road")

        self.__addRow(startNodeNum + 2, downRoadNodeNum, downSettlementNodeNum, lenOfRow - 4, False)

        secondToLast = lenOfRow - 2 + startNodeNum
        self.addEdge(secondToLast, secondToLast + 1)
        self.addEdge(secondToLast, secondToLast - 1)
        self.nodeMap[secondToLast] = SettlementNode("Road")

        self.addEdge(secondToLast + 1, prevEndRoad)
        self.addEdge(secondToLast + 1, secondToLast - 1)
        self.nodeMap[secondToLast + 1] = SettlementNode("Settlement", self.__getResourcetile(self.start[0] - 2, len(self.board[self.start[0] - 1]),
                                                                              "Bottom"))

    def __addBottomRow(self, startNodeNum, upRoadCounter, lenOfRow):
        #Add an extra ocean tile to make tiling for the bottom row work
        self.board[self.start[0]].append(OceanTile())
        upCounter = upRoadCounter
        ycounter = 0
        startingNodeEven = True if startNodeNum % 2 == 0 else False

        for i in range(startNodeNum, lenOfRow + startNodeNum):
            if (i % 2 == 0 and startingNodeEven) or (i % 2 == 1 and not startingNodeEven):
                if (i - startNodeNum) % 4 == 0:
                    #Create a down settlement every 4 nodes
                    if i != startNodeNum:
                        ycounter += 1
                    self.addEdge(i, upRoadCounter)
                    self.nodeMap[i] = SettlementNode("Settlement", self.__getResourcetile(self.start[0], self.start[1] + ycounter,
                                                                                  "Top"))
                    upCounter += 1

                else:
                    self.nodeMap[i] = SettlementNode("Settlement", self.__getResourcetile(self.start[0], self.start[1] + ycounter,
                                                                                               "Bottom", False))
            elif (i % 2 == 1 and startingNodeEven) or (i % 2 == 0 and not startingNodeEven):
                self.addEdge(i, i - 1)
                self.addEdge(i, i + 1)
                self.nodeMap[i] = SettlementNode("Road")

        self.board[self.start[0]].pop()
        #removes this extra row at the end
    def __getResourcetile(self, x, y, direction, increasingTiles=True):
        """
        Gets the correct amount of resources that a node is next to
        FIXME: Direction should be an enum
        :param direction:
            Top: look at the previous row and look left and right, as well as x, y
            bottom: look left and right, as well as one above
            None: only take the x,y tile
            x,y is the right node for bottom
            x,y is the lower node for top
            increasingTiles: if true, then every row I am gaining tiles, else every row I am losing tiles
        :return:
        """
        resources = set()
        if direction == None:
            if self.__notOcean(self.board[x][y]):
                resources.add(self.board[x][y])
        elif direction == "Top":
            if increasingTiles:
                if self.__notOcean(self.board[x][y]):
                    #Center
                    resources.add(self.board[x][y])
                if self.__notOcean(self.board[x - 1][y - 1]):
                    # Top left
                    resources.add(self.board[x-1][y-1])
                if self.__notOcean(self.board[x - 1][y]):
                    #Top Right
                    resources.add(self.board[x-1][y])
            else:
                if self.__notOcean(self.board[x][y]):
                    #Center
                    resources.add(self.board[x][y])
                if self.__notOcean(self.board[x - 1][y]):
                    # Top left
                    resources.add(self.board[x-1][y])
                if self.__notOcean(self.board[x - 1][y + 1]):
                    #Top Right
                    resources.add(self.board[x-1][y + 1])
        elif direction == "Bottom":
            if increasingTiles:
                if self.__notOcean(self.board[x][y]):
                    #right
                    resources.add(self.board[x][y])
                if self.__notOcean(self.board[x][y - 1]):
                    #left
                    resources.add(self.board[x][y-1])
                if self.__notOcean(self.board[x - 1][y - 1]):
                    #Top
                    resources.add(self.board[x-1][y-1])
            else:
                if self.__notOcean(self.board[x][y]):
                    #right
                    resources.add(self.board[x][y])
                if self.__notOcean(self.board[x][y - 1]):
                    #left
                    resources.add(self.board[x][y-1])
                if self.__notOcean(self.board[x - 1][y]):
                    #Top
                    resources.add(self.board[x-1][y])

        return resources

    def __notOcean(self, tile):
        if type(tile) == OceanTile:
            return False
        return True

    def addEdge(self, src, dest):
        """adds an undirected edge to my graph"""
        #makeNode src
        if self.graph[src] == None:
            self.graph[src] = set()
        self.graph[src].add(dest)

        #makeNode dest
        if self.graph[dest] == None:
            self.graph[dest] = set()
        self.graph[dest].add(src)

    def printGraph(self):
        for i in range(125):
            print("Vertex " + str(i) + ":", end="")
            temps = self.graph[i]
            if temps != [] or temps != None:
                print(temps)
            else:
                print("\n")

