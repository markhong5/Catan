import random
import arcade
import arcade.gui
import math
from Board import Board, RESOURCETYPES
from Player import *
from CatanController import CatanController
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800
HEXAGON_SIZE = 50
HEXAGON_XOFFSET = 350
HEXAGON_YOFFSET = 650
SCREEN_TITLE = "Catan"
RESOURCECOLOR= {
    "forest": arcade.color.GREEN,
    "hill":arcade.color.BROWN,
    "mountain":arcade.color.ASH_GREY,
    "farm":arcade.color.YELLOW,
    "grassland":arcade.color.LIGHT_GREEN,
    "desert": arcade.color.BLOND
}
PLAYERCOLORS = {
    0:arcade.color.RED,
    1:arcade.color.BLUE,
    2:arcade.color.GREEN,
    3:arcade.color.PURPLE,
}
DEBUG = False
"""
TODO: Clean and comment code
#FIXME: Add port functionality and draw the ports on the map
    #Done, but could use tests to make sure that the ports shown are actually the correct ports
    #Done
#FIXME: Add the ability to trade to others
    #Done
#FIXME: Add the ability to build a settlement/road/devcard/city
    #need costs for buildings and to go back in case there is an invalid trade
    #need to add dev cards
#FIXME: Add dev cards and their functionality
#FIXME: Make the robber visible on the tiles (and allow the player to choose where to place the robber)
#FIXME: change the color of 6 and 8 to a red text
#FIXME: allow My version of CATAN to be played over the internet (LAST THING TO DO)
"""
DEVCARDS = (["Knight"] * 14) + (["Victory Points"] * 5) + (["Road Building"] * 2) + (["Monopoly"] * 2) + (["YearOfPlenty"] * 2)
class getTextButton(arcade.gui.UIGhostFlatButton):
    """
    This button is linked to a UIInputBox, which will save the text inputed after click
    """
    def __init__(self, center_x, center_y, width, input_box):
        super().__init__(
            "Enter",
            center_x=center_x,
            center_y=center_y,
            width=width,
            id="button"
        )
        self.inputBox = input_box
        self.clickedButton = False
        self.text = ""
    def on_click(self):
        #Start Trade -> while you haven't clicked on button, do nothing -> when you do click on button run the trade and unset clicked on button
        if DEBUG:
            print(f"clicked on box:{self.inputBox.text}")
        self.text = self.inputBox.text
        self.inputBox.text = ""
        self.clickedButton = True
    def resetButton(self):
        self.clickedButton = False

class HexagonGenerator:
    """
    returns 6 vertices based on edgelength and a given offset
    """
    def __init__(self, edgeLength, offSetx, offSety):
        self.edgeLength = edgeLength
        self.offSetx = offSetx
        self.offSety = offSety
    def __call__(self):
        x = self.offSetx
        y = self.offSety
        for angle in range(0, 360, 60):
            y += math.cos(math.radians(angle)) * self.edgeLength
            x += math.sin(math.radians(angle)) * self.edgeLength
            yield x, y

class Catan(arcade.View):
    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.OCEAN_BOAT_BLUE)
        self.board = Board()
        self.graph = self.board.nodeGraph
        self.tileCordinates = {} #Maps tile number to its 6 vertexes
        self.settlementMap = {} #maps cordinates with its appropriate node number

        self.gameController = CatanController(self.board, self.graph, 2)
        #Goal: integrate nearly everything below me into the game controller
        # self.players = self.gameController.players
        # self.devCards = DEVCARDS
        # random.shuffle(self.devCards)
        #FIXME: REMOVE THESE LINE OF CODE WHEN I CAN SPECIFY THE NUMBER OF PLAYERS
        # self.players.append(Player(arcade.color.BLUE))
        # self.players.append(Player(arcade.color.RED))
        # self.currentTurn = 1 #keeps track of the current turn, will loop around once it hits the last Player
        # self.currentPlayer = self.players[0]
        #These flags are for the on_update() function, controling when an update occurs
        self.flags ={
            "endTurn":False,
            "startTurn":True,
            "setUpPhase": True,
            "robber" : False,
            "canPlaceSettlement":False,
            "placedSettlement":False,
            "canPlaceRoad": False,
            "placedRoad":False,
            "tradePhase": False,
            "playerTrade":False,
            "portTrade":False,
            "choosePlayerPhase":False,
            "choosePortPhase":False,
            "makeTradePhase":False,
            "acceptTrade":False,
            "buildPhase":False,
            "upgradeCity":False,
            "devCardPhase":False,
            "selectDevCard":False,
        }
        # self.lengthOfSetUpPhase = 2
        self.roadsToDraw = [] # stores the location of roads to draw
        self.settlementsToDraw = []
        self.citiesToDraw = []
        self.roadBuffer = [] #stores cordinates of where a road should be placed
        # self.playerToTrade = None
        # self.tradeBuffer = []
        self.ui_manager = arcade.gui.UIManager()


    def setup(self):
        """
        This is setting up my Gui: my text box and button to get the text
        :return:
        """
        self.ui_manager.purge_ui_elements()
        #Todo get rid of these preset values
        uiInputBox = arcade.gui.UIInputBox(center_x=300, center_y=100,width=600,text="", id=1)
        uiInputBox.cursor_index = 20
        self.ui_manager.add_ui_element(uiInputBox)
        textButton = getTextButton(center_x= 650, center_y=100, width=100, input_box=uiInputBox)
        self.ui_manager.add_ui_element(textButton)

    def on_draw(self):
        arcade.start_render()
        self._drawMap()
        self._mapSettlementSpots()
        self._drawSettlementSpots()
        self._drawCities()
        self._drawRoads()
        self._drawAllPorts()

        return

    def on_mouse_press(self, x: float, y: float, button: int, modifiers: int):
        """
        if you are building a settlement, click a settlement node and it will check if you can build a settlement there
        Same idea with roads
        :return:
        """
        #FIXME: locks the game if you fail to build a city/settlement
        if self.flags["canPlaceSettlement"]:
            try:
                for cord in self.settlementMap.keys():
                    x2, y2 = cord
                    if math.sqrt((x - x2) * (x - x2) + (y - y2) * (y - y2)) < 7:
                        # node = self.graph.nodeMap[self.settlementMap[cord]]
                        self.gameController.currentPlayer.placeSettlement(self.settlementMap[cord], self.graph, self.flags["setUpPhase"])
                        print(f"placed Settlement at node {self.settlementMap[cord]}")
                        #FIXME perhaps this should be a named tuple?
                        self.settlementsToDraw.append((x2, y2, 7, self.gameController.currentPlayer.color))
                        self.flags["canPlaceSettlement"] = False
                        self.flags["placedSettlement"] = True
                        self.gameController.printed = False
                        break
                #Didn't click on a node
                else:
                    print("Click on one of the nodes")
            except InvalidSettlementError as e:
                print(e.message)
                print(f"Player {self.gameController.currentTurn}, place a settlement")

        if self.flags["canPlaceRoad"]:
            for cord in self.settlementMap.keys():
                x2, y2 = cord
                if math.sqrt((x - x2) * (x - x2) + (y - y2) * (y - y2)) < 7:
                    self.roadBuffer.append(cord)
                    print(f"cord{cord}")
                    break
            if len(self.roadBuffer) == 2:
                try:
                    node1 = self.settlementMap[self.roadBuffer[0]]
                    node2 = self.settlementMap[self.roadBuffer[1]]

                    currentPlayer = self.gameController.currentPlayer
                    roadNode = currentPlayer.getRoadFromTwoSettlementNodes(node1, node2, self.graph)
                    currentPlayer.placeRoad(roadNode, self.graph)
                    self.roadsToDraw.append(
                        (self.roadBuffer[0], self.roadBuffer[1], currentPlayer.color))
                    self.flags["canPlaceRoad"] = False
                    self.flags["placedRoad"] = True
                    self.gameController.printed = False
                    print("placed Road")
                except InvalidRoadError as e:
                    print(e.message)
                    print("Click another 2 Roads")
                self.roadBuffer = []
        #FIXME: REMOVE currentPlayer When I get there
        if self.flags["upgradeCity"]:
            try:
                for cord in self.settlementMap.keys():
                    x2, y2 = cord
                    if math.sqrt((x - x2) * (x - x2) + (y - y2) * (y - y2)) < 7:
                        node = self.graph.nodeMap[self.settlementMap[cord]]
                        currentPlayer = self.gameController.currentPlayer
                        currentPlayer.upgradeSettlementToCity(node)
                        print(f"placed City at node {self.settlementMap[cord]}")
                        #FIXME perhaps this should be a named tuple?
                        self.citiesToDraw.append((x2, y2, 15, currentPlayer.color))
                        self.flags["upgradeCity"] = False
                        break
                else:
                    print("Click on one of the Cities")
            except InvalidSettlementError as e:
                print(e.message)
                print(f"Player {self.gameController.currentTurn}, place a City")
                self.flags["upgradeCity"] = False

    def on_update(self, delta_time):
        """Main game logic"""
        if self.flags["setUpPhase"]:
            self.gameController.setUpPhase(self.flags)
            #self._setUpPhase()
        else:
            self.gameController.mainGame(self.flags, self.ui_manager.find_by_id("button"))
            # self._mainGame()

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.ENTER:
            self.ui_manager.find_by_id("button").on_click()

    def _mainGame(self):

        if self.flags["endTurn"]:
            self.flags["startTurn"] = True

            if self.currentTurn + 1 <= len(self.players):
                self.currentTurn += 1
            else:
                self.currentTurn = 1
            self.currentPlayer = self.players[self.currentTurn - 1]

            self.flags["endTurn"] = False
        else:
            textButton = self.ui_manager.find_by_id("button")
            if self.flags["startTurn"]:
                print(f"Player {self.currentTurn}, it is your turn")
                roll = random.randint(1,6) + random.randint(1,6)
                print(f"Player {self.currentTurn} rolled a {roll}")
                print("Collecting resources...")
                for player in self.players:
                    player.collectResources(roll)
                print(f"Player {self.currentTurn}, resources: {self.currentPlayer.totalResources}")
                #TODO DEV cards can be played at any time, and should be implemented in this menu
                print("Press T for Trade, B for Build, D for devCards, or N to go to the next turn")
                self.flags["startTurn"] = False
                self.flags["tradePhase"] = True

            #FIXME there is no backing out of a trade, unless you are willing to end your turn
            if textButton.clickedButton:
                if self._formatTextButton(textButton.text) == "n" and not self.flags["startTurn"]:
                    print("End Turn\n")
                    self._resetFlags()
                    self.flags["endTurn"] = True
                elif self.flags["tradePhase"]:
                    if self.flags["playerTrade"]:
                        self._tradePhase(textButton)
                    elif self.flags["portTrade"]:
                        self._portTrade(textButton)
                    else:
                        if self._formatTextButton(textButton.text) == "pt":
                            self.flags["portTrade"] = True
                            self._portTrade(textButton)
                        elif self._formatTextButton(textButton.text) == "p":
                            self.flags["playerTrade"] = True
                            self._tradePhase(textButton)
                        elif self._formatTextButton(textButton.text) == "t":
                            print("Do you want a PortTrade or PlayerTrade? (PT for port, P for player)")

                if self._formatTextButton(textButton.text) == "b" or self.flags["buildPhase"]:
                    self.flags["buildPhase"] = True
                    self._buildPhase(textButton)
                elif self._formatTextButton(textButton.text) == "n":
                    pass
                elif self._formatTextButton(textButton.text) == "d" or self.flags["devCardPhase"]:
                    self._playDevCards(textButton)
                else:
                    print(f"Invalid Text:{textButton.text}")

                textButton.resetButton()

    def _tradePhase(self, textButton):
        """
        simulates the trade phase of catan which is
        Player chooses to trade -> Player chooses another player to trade with and sends offer -> other player accepts/decline trade->
        if accepted player makes trade
        if declined, go back to the start of the trade phase

        Also, if the player has a port trade, allow them to trade if available

        Ideally, you should be able to go back a step. Currently you can not go back a step. You either commit to the Trade, or you end your turn
        :param textButton:
        :return:
        """
        if self._formatTextButton(textButton.text) == "t" and not self.flags["choosePlayerPhase"]:
            print("Who do you want to trade with?")
            for i, player in enumerate(self.players):
                # FIXME You are not suppose to know other players resources, but for the sake of not having a
                # Better GUI, I will let the player know what resources other players have
                if player != self.currentPlayer:
                    print(f"Player {i + 1} resources:{player.totalResources}")
            self.flags["choosePlayerPhase"] = True

        elif self._formatTextButton(textButton.text) in [str(i + 1) for i, player in enumerate(self.players) if
                                                         player != self.currentPlayer] \
                and self.flags["choosePlayerPhase"] and not self.flags["makeTradePhase"]:
            print(f"Picked Player {textButton.text}")
            # TODO add a step where the picked player can confirm if they want to trade
            self.playerToTrade = self.players[int(self._formatTextButton(textButton.text)) - 1]
            print(f"What do you want to trade? (formatted as send:recieve. i.e lumber-2,ore-1:livestock-2,wheat-1)")
            self.flags["makeTradePhase"] = True

        elif self.flags["makeTradePhase"] and not self.flags["acceptTrade"]:
            tradeToMake = self._formatTextButton(textButton.text)
            if ":" not in tradeToMake:
                print(f"Invalid Trade:{textButton.text}")
            else:
                trades = tradeToMake.split(":")
                if len(trades) != 2:
                    print(f"Invalid Trade: more than two :'s")
                else:
                    send = None
                    give = None
                    for i, trade in enumerate(trades):
                        # FIXME need to have better error management control, what if there is no comma or dash?
                        resourcesToTrade = trade.split(",")
                        resources = []
                        amounts = []
                        for resource in resourcesToTrade:
                            resourceAmount = resource.split("-")
                            resources.append(resourceAmount[0])
                            amounts.append(int(resourceAmount[1]))
                        if i == 0:
                            send = list(zip(resources, amounts))
                        else:
                            give = list(zip(resources, amounts))
                    print(f"Player {self._findPlayer(self.currentPlayer)} sends {send} and recieves {give}")
                    print(f"Player {self._findPlayer(self.playerToTrade)}, do you accept this trade? (y/n)")
                    self.tradeBuffer.append(send)
                    self.tradeBuffer.append(give)
                    self.flags["acceptTrade"] = True

        elif self._formatTextButton(textButton.text) == "y" and self.flags["acceptTrade"]:
            try:
                self.currentPlayer.makeTrade(self.playerToTrade, self.tradeBuffer[0], self.tradeBuffer[1])
                print("Press T for Trade, B for Build, or N to go to the next turn\n")
                self._resetTradeFlags()
            except InvalidTradeError as e:
                #if there is an error with the trade, go back to the start of the trade phase
                print(e.message)
                self._resetTradeFlags()
        #FIXME Ideally, the other player would input this text, but for now we have a GM controlling the board and controlling
        #what the players are saying
        elif self._formatTextButton(textButton.text) == "n" and self.flags["acceptTrade"]:
            print("Press T for Trade, B for Build, or N to go to the next turn\n")
            self._resetTradeFlags()
        elif self._formatTextButton(textButton.text) == "b":
            print("Do you want to build a road, settlement, city, or devCard\n")
            self._resetTradeFlags()
            self.flags["tradePhase"] = False
            self.flags["buildPhase"] = True

    def _portTrade(self, textButton):
        if self._formatTextButton(textButton.text) == "pt":
            tradesAvailable = [settlement.trade for settlement in self.currentPlayer.settlementNodesOwned if settlement.trade != None]
            tradesAvailable += ["4:1"] #always can do a 4-1 option
            print(f"trades Available {tradesAvailable}")
            print(f"Which trade do you want? (enter 1 for the first trade, 2 for the second etc)")
            self.flags["choosePortPhase"] = True
        elif self.flags["choosePortPhase"]:
            text = self._formatTextButton(textButton.text)
            #If the text is only 1 character, and that character is between 0 and 6 (since you can only have 5 + 1 free trade settlements in theory)
            if len(text) == 1 and ord(text) >= 48 and ord(text) <= 54:
                selection = int(text) - 1
                trades = [settlement.trade for settlement in self.currentPlayer.settlementNodesOwned if settlement.trade != None]
                trades += ["4:1"]
                if selection >= 0 and selection < len(trades):
                    # Try making the trade
                    trade = None
                    trade = trades[selection]
                    if DEBUG:
                        print(trade)
                    trade = trade.split(" ")
                    if len(trade) == 2:
                        #If it's a 2:1
                        print("What do you want to trade for? (ore, lumber, etc)")
                    else:
                        #its a 3:1 or 4:1
                        print("what are you sending recieving? (lumber:ore)")
                    self.tradeBuffer.append(trade)
                    self.flags["choosePortPhase"] = False
                    self.flags["makeTradePhase"] = True

                else:
                    print(f"invalid number for port trade: {text}")
            else:
                print(f"{text} is not a number between 1-7")
        elif self.flags["makeTradePhase"]:
            #Should either be in the format of ore || ore:lumber
            text = self._formatTextButton(textButton.text)
            trade = self.tradeBuffer[0]
            if len(trade) == 2:
                try:
                    self.currentPlayer.portTrade(trade, trade[0], text)
                    self._resetTradeFlags()
                    print("Press T for Trade, B for Build, or N to go to the next turn\n")
                except InvalidTradeError as e:
                    print(e.message)
                    self._resetTradeFlags()
            elif len(trade) == 1:
                try:
                    sending, recieving = text.split(":")
                    self.currentPlayer.portTrade(trade, sending, recieving)
                    self._resetTradeFlags()
                    print("Press T for Trade, B for Build, or N to go to the next turn\n")
                except InvalidTradeError as e:
                    print(e.message)
                    self._resetTradeFlags()

    def _buildPhase(self, textButton):
        if self.flags["canPlaceRoad"] or self.flags["canPlaceSettlement"] or self.flags["upgradeCity"]:
            pass
        else:
            text = self._formatTextButton(textButton.text)
            if text == "b":
                print("Do you want to build a road, settlement, city, or devCard?")
            if text == "road":
                #Pay for road, else error
                #Build a road
                print("Building Road")
                self.flags["canPlaceRoad"] = True
            elif text == "settlement":
                #Pay for settlement, else error
                #Build a settlement
                print("Building settlement")
                self.flags["canPlaceSettlement"] = True
            elif text == "city":
                #Pay for city, else error
                #Build a city
                print("Building city")
                self.flags["upgradeCity"] = True
            elif text == "devcard":
                #Pay for devCard, else error
                #Build a devCard
                print("giving devCard")
                if len(self.devCards) > 0:
                    devcard = self.devCards.pop(0)
                    print(devcard)
                    if devcard == "Victory Point":
                        self.currentPlayer.victoryPoints += 1
                    else:
                        self.currentPlayer.devCards.append(devcard)
                    if devcard == "knight":
                        self.currentPlayer.totalKnights += 1
                else:
                    print("Out of devCards")

    def _playDevCards(self, textButton):
        text = self._formatTextButton(textButton.text)

        if text == "d":
            print(self.currentPlayer.devCards)
            print("which devcard do you want to play? (select 1, 2, etc)")
            self.flags["selectDevCard"] = True
        elif self.flags["selectDevCard"]:
            #Assumes no one will have over 9 devcards
            if len(text) == 1 and ord(text) >= 48 and ord(text) <= 57:
                val = int(text)
                if val < len(self.currentPlayer.devCards):
                    devcard = self.currentPlayer.devCards[val]
                    if devcard == "knight":
                        pass
                        #Do knight effect: Choose where the robber goes -> steal card from a player
                    elif devcard == "Road Building":
                        pass
                        #Build 2 roads
                    elif devcard == "Year Of Plenty":
                        pass
                        #Specify what resource the player wants, and give 2 of that resource
                    elif devcard == "Monopoly":
                        pass
                        #Specify what resource the player Wants, and take all of that resource from the player

                else:
                    print(f"{val} is greater than your total number of dev cards: {len(self.currentPlayer.devCards)}")

            else:
                print(f"{text} is not a number between 1-9")

    def _hasPortTrade(self, player):
        for settlement in player.settlementNodesOwned:
            if settlement.trade != None:
                return True
        return False
    def _resetFlags(self):
        self.flags["tradePhase"] = False
        self._resetTradeFlags()
        self.flags["buildPhase"] = False
        self.flags["canPlaceSettlement"] = False
        self.flags["upgradeCity"] = False
        self.flags["canPlaceRoad"] = False
        self.flags["devCardPhase"] = False
        self.flags["selectDevCard"] = False

    def _resetTradeFlags(self):
        self.flags["makeTradePhase"] = False
        self.flags["choosePlayerPhase"] = False
        self.flags["acceptTrade"] = False
        self.flags["choosePortPhase"] = False
        self.flags["makeTradePhase"] = False
        self.flags["playerTrade"] = False
        self.flags["portTrade"] = False
        self.tradeBuffer = []

    def _formatTextButton(self, text):
            formattedText = text.lower().strip()
            return formattedText
    def _findPlayer(self, player):
        for i, pla in enumerate(self.players):
            if pla == player:
                return i + 1

        return -1

    # def _setUpPhase(self):
    #     """
    #     Set up phase:  every player places 2 settlements and roads
    #     :return:
    #     """
    #     if self.flags["endTurn"]:
    #         self.flags["startTurn"] = True
    #         self.flags["canPlaceSettlement"] = False
    #         self.flags["canPlaceRoad"] = False
    #         self.flags["placedRoad"] = False
    #         self.flags["placedSettlement"] = False
    #
    #         #Snake around Order, goes 1st -> 2nd -> 3rd -> 3rd -> 2nd -> 1st
    #         if self.lengthOfSetUpPhase == 2:
    #             if self.currentTurn + 1 <= len(self.players):
    #                 self.currentTurn += 1
    #             else:
    #                 self.lengthOfSetUpPhase -= 1
    #         elif self.lengthOfSetUpPhase == 1:
    #             if self.currentTurn - 1 > 0:
    #                 self.currentTurn -= 1
    #             else:
    #                 self.lengthOfSetUpPhase -= 1
    #         self.currentPlayer = self.players[self.currentTurn - 1]
    #         self.flags["endTurn"] = False
    #
    #         if self.lengthOfSetUpPhase == 0:
    #             self.flags["setUpPhase"] = False
    #     else:
    #         if self.flags["startTurn"]:
    #             print(f"Player {self.currentTurn}, it is your turn")
    #             self.flags["startTurn"] = False
    #
    #         elif not self.flags["placedSettlement"] and not self.flags["canPlaceSettlement"]:
    #             print(f"Player {self.currentTurn}, place a settlement")
    #             self.flags["canPlaceSettlement"] = True
    #             # self.placeSettlement = False
    #         elif not self.flags["placedRoad"] and not self.flags["canPlaceRoad"] and not self.flags["canPlaceSettlement"]:
    #             print(f"Player {self.currentTurn}, place a road down")
    #             self.flags["canPlaceRoad"] = True
    #         elif self.flags["placedRoad"] and not self.flags["canPlaceRoad"]:
    #             self.flags["endTurn"] = True

    def _drawMap(self):
        newX = HEXAGON_XOFFSET
        newY = HEXAGON_YOFFSET
        hexagonPoints = None
        rowNum = 3
        previousXValue = [newX]
        totalTiles = 0
        boardStart = [1, 1]
        for y in range(3):
            hexagonGen = HexagonGenerator(HEXAGON_SIZE, newX, newY)
            hexagon = hexagonGen()
            hexagonPoints = list(hexagon)
            self._drawTile(hexagonPoints, self._getResourceTileColor(boardStart), self._getResourceTileNum(boardStart), self._getTileIsRobber(boardStart))
            self.tileCordinates[totalTiles] = hexagonPoints
            totalTiles += 1
            boardStart[1] += 1
            for i in range(1, rowNum):
                hexagonGen = HexagonGenerator(HEXAGON_SIZE, newX + (hexagonPoints[2][0] - hexagonPoints[0][0]) * i, newY)
                hexagon = hexagonGen()
                cords = list(hexagon)
                # arcade.draw_polygon_outline(cords, arcade.color.BLACK)
                self._drawTile(cords,self._getResourceTileColor(boardStart), self._getResourceTileNum(boardStart),self._getTileIsRobber(boardStart))
                self.tileCordinates[totalTiles] = cords
                totalTiles += 1
                boardStart[1] += 1

            newX = newX - (hexagonPoints[2][0] - hexagonPoints[0][0]) / 2
            newY = newY - ((hexagonPoints[0][1] - hexagonPoints[5][1]) * 1.5)
            rowNum += 1
            previousXValue.append(newX)
            boardStart[0] += 1
            boardStart[1] = 1
        rowNum = 4
        previousXValue.pop()
        previousXValue.pop()
        newX = previousXValue.pop()
        for y in range(2):

            hexagonGen = HexagonGenerator(HEXAGON_SIZE, newX, newY)
            hexagon = hexagonGen()
            hexagonPoints = list(hexagon)
            # arcade.draw_polygon_outline(hexagonPoints, arcade.color.BLACK)
            self._drawTile(hexagonPoints, self._getResourceTileColor(boardStart), self._getResourceTileNum(boardStart),self._getTileIsRobber(boardStart))

            self.tileCordinates[totalTiles] = hexagonPoints
            totalTiles += 1
            boardStart[1] += 1
            for i in range(1, rowNum):
                hexagonGen = HexagonGenerator(HEXAGON_SIZE, newX + (hexagonPoints[2][0] - hexagonPoints[0][0]) * i, newY)
                hexagon = hexagonGen()
                cords = list(hexagon)
                self._drawTile(cords,self._getResourceTileColor(boardStart), self._getResourceTileNum(boardStart),self._getTileIsRobber(boardStart))
                boardStart[1] += 1
                self.tileCordinates[totalTiles] = cords
                totalTiles += 1
            if previousXValue != []:
                newX = previousXValue.pop()
            newY = newY - ((hexagonPoints[0][1] - hexagonPoints[5][1]) * 1.5)
            rowNum -= 1
            boardStart[0] += 1
            boardStart[1] = 1

    def _drawSettlementSpots(self):
        for tile in self.tileCordinates.values():
            for cord in tile:
                arcade.draw_circle_filled(cord[0], cord[1], 7, arcade.color.DUTCH_WHITE)

        #This code was put in when a cord was not in the settlementMap, but was so close that it would draw over the
        #original settlement circle
        for settlement in self.settlementsToDraw:
            arcade.draw_circle_filled(settlement[0], settlement[1],settlement[2], settlement[3])
        return

    def _drawCities(self):
        for city in self.citiesToDraw:
            arcade.draw_rectangle_filled(center_x=city[0], center_y= city[1], width= city[2], height=city[2], color= city[3])

    def _drawRoads(self):

        for road in self.roadsToDraw:
            cord1 = road[0]
            cord2 = road[1]
            color = road[2]
            arcade.draw_line(cord1[0], cord1[1], cord2[0], cord2[1], color, 3)

    def _getHexCenter(self, cord1, cord2):
        return (cord1[0], cord1[1] - (cord1[1] - cord2[1]) / 2)

    def _drawTile(self, vertexes, color, text, isRobber = False):
        arcade.draw_polygon_filled(vertexes, color)
        arcade.draw_polygon_outline(vertexes, arcade.color.BLACK)

        hexCenter = self._getHexCenter((vertexes[1][0], vertexes[1][1]),
                                       (vertexes[4][0], vertexes[4][1]))
        if not isRobber:
            arcade.draw_text(text, hexCenter[0], hexCenter[1], arcade.color.BLACK, align="center", anchor_x="center",
                             anchor_y="center")
        else:
            arcade.draw_text("R", hexCenter[0], hexCenter[1], arcade.color.BLACK, align="center", anchor_x="center",
                             anchor_y="center")

    def _getResourceTileColor(self, boardPosition):
        return RESOURCECOLOR[self.board.board[boardPosition[0]][boardPosition[1]].resource]

    def _getTileIsRobber(self, boardPosition):
        return self.board.board[boardPosition[0]][boardPosition[1]].isRobber

    def _getResourceTileNum(self, boardPosition):
        return str(self.board.board[boardPosition[0]][boardPosition[1]].num)

    def _mapSettlementSpots(self):
        settlementSpots = 0
        #FIXME a lot of these calculations are basically hand calculated by my node counting system
        #A better way would have a mathematical solution to mapping out the nodes
        self.settlementMap = {}
        starting = 0
        ending = 3
        settlementSpot = 0
        self._addGrowingRow(starting, ending, settlementSpot)
        starting = ending
        ending += 4
        settlementSpot += 17
        self._addGrowingRow(starting, ending, settlementSpot)
        starting = ending
        ending += 5
        settlementSpot += 22
        self._addGrowingRow(starting, ending, settlementSpot)

        settlementSpot += 27
        self._addShrinkingRow(starting, ending, settlementSpot)
        starting = ending
        ending += 4
        settlementSpot += 26
        self._addShrinkingRow(starting, ending, settlementSpot)
        starting = ending
        ending += 3
        settlementSpot += 21
        self._addShrinkingRow(starting, ending, settlementSpot)

    def _addGrowingRow(self, startingTile, endingTile, startingSettlement):
        """Maps settlement nodes for a row that increases in tiles"""
        tileNum = startingTile
        colNum = endingTile
        settlementSpots = startingSettlement
        for i in range(0, 3):
            self.settlementMap[self.tileCordinates[tileNum][i]] = settlementSpots
            settlementSpots += 2
        for i in range(tileNum + 1, colNum):
            for y in range(1, 3):
                self.settlementMap[self.tileCordinates[i][y]] = settlementSpots
                settlementSpots += 2
    def _addShrinkingRow(self, startingTile, endingTile, startingSettlement):
        "Maps settlement Nodes for a row that decreases in tiles compared to the previous row"
        tileNum = startingTile
        colNum = endingTile
        settlementSpots = startingSettlement
        for i in range(5, 2, -1):
            self.settlementMap[self.tileCordinates[tileNum][i]] = settlementSpots
            settlementSpots += 2
        for i in range(tileNum + 1, colNum):
            for y in range(4, 2, -1):
                self.settlementMap[self.tileCordinates[i][y]] = settlementSpots
                settlementSpots += 2

    def _drawPort(self, cord1, cord2, trade, direction):
        """
        Tries to make an equalaterial triangle from 2 cordinates, putting down the text of my port
        FIXME: my math for making the 2d triangles is not correct, but functional
        :param cord1: cordinate of the first dot
        :param cord2: cordinate of the second dot
        :param trade: What the text trade will be
        :return:
        """
        # offset = 30
        offsetx = math.cos(math.radians(60)) * HEXAGON_SIZE
        offsety = math.sin(math.radians(60)) * HEXAGON_SIZE
        offsetTextx = 0
        offsetTexty = 0
        if direction == "Up":
            centerX = ((cord1[0] + cord2[0]) / 2) - offsetx
            centerY = ((cord1[1] + cord2[1]) / 2) + offsety
            offsetTexty = 7
        elif direction == "Down":
            centerX = ((cord1[0] + cord2[0]) / 2) - offsetx
            centerY = ((cord1[1] + cord2[1]) / 2) - offsety
            offsetTexty = -7
        elif direction == "RightUp":
            centerX = ((cord1[0] + cord2[0]) / 2) + offsetx
            centerY = ((cord1[1] + cord2[1]) / 2) + offsety
            offsetTextx = 7
            offsetTexty = 7
        elif direction == "DownRight":
            centerX = ((cord1[0] + cord2[0]) / 2) + offsetx
            centerY = ((cord1[1] + cord2[1]) / 2) - offsety
            offsetTexty = -7
            offsetTextx = 7
        arcade.draw_line(cord1[0], cord1[1], centerX, centerY, arcade.color.BLACK, 3)
        arcade.draw_line(cord2[0], cord2[1], centerX, centerY, arcade.color.BLACK, 3)
        arcade.draw_text(trade, centerX + offsetTextx, centerY + offsetTexty, arcade.color.BLACK, align="center", anchor_x="center",
                         anchor_y="center")

    def _drawAllPorts(self):
        """
        Manually inputs where each port should be drawn and what trade it represents
        :return:
        """
        self._drawPort(self.tileCordinates[0][0], self.tileCordinates[0][1], self.board.board[0][0].trade, "Up")
        self._drawPort(self.tileCordinates[1][1], self.tileCordinates[1][2], self.board.board[0][2].trade, "RightUp")
        self._drawPort(self.tileCordinates[3][0], self.tileCordinates[3][5], self.board.board[2][0].trade, "Up")
        self._drawPort(self.tileCordinates[6][1], self.tileCordinates[6][2], self.board.board[1][4].trade, "RightUp")
        self._drawPort(self.tileCordinates[11][2], self.tileCordinates[11][3], self.board.board[3][6].trade, "RightUp")
        self._drawPort(self.tileCordinates[12][0], self.tileCordinates[12][5], self.board.board[4][0].trade, "Down")
        self._drawPort(self.tileCordinates[15][3], self.tileCordinates[15][4], self.board.board[5][4].trade, "DownRight")
        self._drawPort(self.tileCordinates[16][4], self.tileCordinates[16][5], self.board.board[6][0].trade, "Down")
        self._drawPort(self.tileCordinates[17][3], self.tileCordinates[17][4], self.board.board[6][2].trade, "DownRight")




def main():
    #FIXME add a argument that states how many players will be in the game
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    catan = Catan()
    window.show_view(catan)
    catan.setup()
    arcade.run()

if __name__ == "__main__":
    main()