import random
import math
from Board import Board, RESOURCETYPES, InvalidRobberError
import arcade
from Player import *
DEVCARDS = (["Knight"] * 14) + (["Victory Points"] * 5) + (["Road Building"] * 2) + (["Monopoly"] * 2) + (["YearOfPlenty"] * 2)
STARTOFTURNSTATEMENT = "Press T for Trade, B for Build, D for devCards, or N to go to the next turn"
BOARDTOCORDS ={ #Created solely to find players to steal from when a robber is moved
    (1,1): 0,
    (1,2) : 1,
    (1,3) : 2,
    (2,1) : 3,
    (2,2): 4,
    (2,3): 5,
    (2,4): 6,
    (3,1): 7,
    (3, 2): 8,
    (3, 3): 9,
    (3, 4): 10,
    (3, 5): 11,
    (4,1):12,
    (4,2):13,
    (4,3):14,
    (4,4):15,
    (5,1):16,
          (5,2): 17,
           (5,3): 18,
}
DEBUG = True
class CatanController:
    def __init__(self, board, graph, numPlayers=2):
        self.board = board
        self.graph = graph
        self.players = self._getPlayers(numPlayers)
        self.devCards = DEVCARDS
        random.shuffle(self.devCards)

        self.currentTurn = 1
        self.currentPlayer = self.players[0]
        self.lengthOfSetUpPhase = 2
        self.playerToTrade = None
        self.tradeBuffer = []
        self.printed = False


    def setUpPhase(self, flags):
        """
        Setup phase is each player builds 2 roads and 2 settlements
        :param flags:
        :return:
        """
        if flags["startTurn"]:
            print(f"Player {self.currentTurn}, it is your turn")
            flags["startTurn"] = False
        elif not flags["placedSettlement"]:
            if not self.printed:
                print(f"Player {self.currentTurn}, place a settlement")
                flags["canPlaceSettlement"] = True
                self.printed = True
        elif not flags["placedRoad"]:
            if not self.printed:
                print(f"Player {self.currentTurn}, place a road down")
                flags["canPlaceRoad"] = True
                self.printed = True
        elif flags["placedSettlement"] and flags["placedRoad"]:
            self.endTurnSetUP(flags)

        if self.lengthOfSetUpPhase == 0:
            flags["setUpPhase"] = False

    def endTurnSetUP(self, flags):
        self._resetFlags(flags)
        if self.lengthOfSetUpPhase == 2:
            if self.currentTurn + 1 <= len(self.players):
                self.currentTurn += 1
            else:
                self.lengthOfSetUpPhase -= 1
        elif self.lengthOfSetUpPhase == 1:
            if self.currentTurn - 1 > 0:
                self.currentTurn -= 1
            else:
                self.lengthOfSetUpPhase -= 1
        self.currentPlayer = self.players[self.currentTurn - 1]

    def mainGame(self, flags, textButton):
        """Main Game flow
        Start Of Turn -> collect resources for all players -> Choose to Trade/Build/Use dev Card -> end turn
        Game Ends when a player has 10 victory points
        """
        if flags["startTurn"]:
            print(f"Player {self.currentTurn}, it is your turn")
            roll = random.randint(1, 6) + random.randint(1, 6)
            print(f"Player {self.currentTurn} rolled a {roll}")
            if roll == 7:
                flags["robber"] = True
            print("Collecting resources...")
            for player in self.players:
                player.collectResources(roll)
            print(f"Player {self.currentTurn}, resources: {self.currentPlayer.totalResources}")
            print(STARTOFTURNSTATEMENT)
            flags["startTurn"] = False
            # self.flags["tradePhase"] = True
            if flags["robber"]:
                print(f"Player {self.currentTurn}, where do you want to place the robber?")
            #Follows the board notation, with the top left most tile being 1,1
        if textButton.clickedButton:
            text = self._formatTextButton(textButton.text)
            if flags["robber"]:
                self._moveRobber(flags, text)
            elif text == "n" and not flags["acceptTrade"]:
                print("End Turn\n")
                self.endTurn(flags)
            elif text == "t" or flags["tradePhase"]:
                flags["tradePhase"] = True
                if flags["playerTrade"]:
                    self._playerTrade(flags, text)
                elif flags["portTrade"]:
                    self._portTrade(flags, text)
                elif text == "pt":
                    flags["portTrade"] = True
                    self._portTrade(flags, text)
                elif text == "p":
                    flags["playerTrade"] = True
                    self._playerTrade(flags, text)
                else:
                    print("Do you want a PortTrade or PlayerTrade? (PT for port, P for player)")
            elif text == "b" or flags["buildPhase"]:
                flags["buildPhase"] = True
                self._buildPhase(flags, text)

            textButton.resetButton()

    def _playerTrade(self, flags, text):
        if not flags["choosePlayerPhase"]:
            print("Who do you want to trade with?")
            for i, player in enumerate(self.players):
                # FIXME You are not suppose to know other players resources, but for the sake of not having a
                # Better GUI, I will let the player know what resources other players have
                if player != self.currentPlayer:
                    print(f"Player {i + 1} resources:{player.totalResources}")
            flags["choosePlayerPhase"] = True
        elif not flags["makeTradePhase"]:
            if text not in [str(i + 1) for i, player in enumerate(self.players) if player != self.currentPlayer]:
                print(f"{text} is not a valid player number")
            else:
                print(f"Picked Player {text}")
                self.playerToTrade = self.players[int(text) - 1]
                print(f"What do you want to trade? (formatted as send:recieve. i.e lumber-2,ore-1:livestock-2,wheat-1)")
                flags["makeTradePhase"] = True
        elif not flags["acceptTrade"]:
            tradeToMake = text
            if ":" not in tradeToMake:# FIXME need to have better error management control, use regex to confirm string
                print(f"Invalid Trade:{text}")
            else:
                trades = tradeToMake.split(":")
                if len(trades) != 2:
                    print(f"Invalid Trade: more than two :'s")
                else:
                    send = None
                    give = None
                    for i, trade in enumerate(trades):
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
                    flags["acceptTrade"] = True
        elif flags["acceptTrade"]:
            if text == "y":
                try:
                    self.currentPlayer.makeTrade(self.playerToTrade, self.tradeBuffer[0], self.tradeBuffer[1])
                    print(self.currentPlayer.totalResources)
                    print(STARTOFTURNSTATEMENT)
                    self._resetTradeFlags(flags)
                except InvalidTradeError as e:
                    # if there is an error with the trade, go back to the start of the trade phase
                    print(e.message)
                    print("resetting Trade")
                    self._resetTradeFlags(flags)
            elif text == "n":
                print("trade declined")
                print(STARTOFTURNSTATEMENT)
                self._resetTradeFlags(flags)
        else:
            print(f"invalid input {text}")

    def _findPlayer(self, player):
        for i, pla in enumerate(self.players):
            if pla == player:
                return i + 1

        return -1

    def _portTrade(self, flags, text):
        if text == "pt": #A little different then my previous trade phase, as I have a text check instead of a flag check
            tradesAvailable = [settlement.trade for settlement in self.currentPlayer.settlementNodesOwned if settlement.trade != None]
            tradesAvailable += ["4:1"] #always can do a 4-1 option
            print(f"trades Available {tradesAvailable}")
            print(f"Which trade do you want? (enter 1 for the first trade, 2 for the second etc)")
            # self.flags["choosePortPhase"] = True
        elif not flags["choosePortPhase"]:
            # If the text is only 1 character, and that character is between 0 and 6 (since you can only have 5 + 1 free trade)
            if len(text) == 1 and ord(text) >= 48 and ord(text) <= 54:
                selection = int(text) - 1
                trades = [settlement.trade for settlement in self.currentPlayer.settlementNodesOwned if
                          settlement.trade != None]
                trades += ["4:1"]
                if selection >= 0 and selection < len(trades):
                    #find the trade
                    trade = None
                    trade = trades[selection]
                    if DEBUG:
                        print(trade)
                    trade = trade.split(" ")
                    if len(trade) == 2:
                        # If it's a 2:1, ask what the player wants to recieve
                        print("What do you want to trade for? (ore, lumber, etc)")
                    else:
                        # its a 3:1 or 4:1, ask what they are sending/recieving
                        print("what are you sending recieving? (lumber:ore)")
                    self.tradeBuffer.append(trade)
                    flags["choosePortPhase"] = True
                else:
                    print(f"invalid number for port trade: {text}")
            else:
                print(f"{text} is not a number between 1-7")
        elif not flags["makeTradePhase"]:
            # Should either be in the format of ore || ore:lumber
            trade = self.tradeBuffer[0]
            if len(trade) == 2:
                try:
                    self.currentPlayer.portTrade(trade, trade[0], text)
                    print(self.currentPlayer.totalResources)
                    self._resetTradeFlags(flags)
                    print(STARTOFTURNSTATEMENT)
                except InvalidTradeError as e:
                    print(e.message)

                    self._resetTradeFlags(flags)
            elif len(trade) == 1:
                try:
                    sending, recieving = text.split(":")
                    self.currentPlayer.portTrade(trade, sending, recieving)
                    print(self.currentPlayer.totalResources)
                    self._resetTradeFlags(flags)
                    print(STARTOFTURNSTATEMENT)
                except InvalidTradeError as e:
                    print(e.message)
                    self._resetTradeFlags(flags)
                except ValueError as e:
                    print("must be in the form (sending:recieving)")
                    self._resetTradeFlags(flags)

    def _buildPhase(self, flags, text):
        #Build phase is the last phase, so the only thing you can do after building is play a dev card or end your turn
        if flags["canPlaceRoad"] or flags["canPlaceSettlement"] or flags["upgradeCity"]:
            pass
        else:

            if text == "road":
                #Pay for road, else error
                #Build a road
                print("Building Road")
                flags["canPlaceRoad"] = True
            elif text == "settlement":
                #Pay for settlement, else error
                #Build a settlement
                print("Building settlement")
                flags["canPlaceSettlement"] = True
            elif text == "city":
                #Pay for city, else error
                #Build a city
                print("Building city")
                flags["upgradeCity"] = True
            elif text == "devcard":
                #Pay for devCard, else error
                #Build a devCard
                print("giving devCard")
                if len(self.devCards) > 0:
                    devcard = self.devCards.pop(0)
                    print(f"{devcard} recieved")
                    if devcard == "Victory Point":
                        self.currentPlayer.victoryPoints += 1
                    else:
                        self.currentPlayer.devCards.append(devcard)
                    if devcard == "knight":
                        self.currentPlayer.totalKnights += 1
                else:
                    print("Out of devCards")
            else:
                print("Do you want to build a road, settlement, city, or devCard?")

    def _moveRobber(self, flags, text):
        try:
            #FIXME: instead of checking for cords, just allow the player to click on the tile where they want to move the
            #robber
            cords = text.split(",")
            if self._validCords(cords):
                x,y = int(cords[0]), int(cords[1])
                self.board._setRobber([x,y])
                print(f"Placed the robber at tile {[x,y]}")

                #Find a player you can to steal from
                players = self._findNeighboringPlayers((x, y))
                if len(players) == 0:
                    flags["robber"] = False
                else:
                    allPlayers = ""
                    for player in players:
                        allPlayers += "Player:" + player.name
                        allPlayers += "\n"
                    print(allPlayers)
                    print("who do you want to steal from?")
            else:
                raise InvalidRobberError("Cords not within 1,1 or 5,3 ")

        except (ValueError, InvalidRobberError) as e:
            print(e.message)
            print("Not valid tile location ie (1,1 or 2,3)")

    def endTurn(self, flags):
        self._resetFlags(flags)
        if self.currentTurn + 1 <= len(self.players):
            self.currentTurn += 1
        else:
            self.currentTurn = 1
        self.currentPlayer = self.players[self.currentTurn - 1]

    def _findNeighboringPlayers(self, cords):
        surrondingnodes = self.board.board[cords[0]][cords[1]].vertices
        surrondingSettlements = []
        for node in surrondingnodes:
            surrondingSettlements.append(self.graph.nodeMap[node])
        surrondingPlayers = []

        #For every player, check to see if their settlements is a part of the surronding ndoes
        for player in self.players:
            if player != self.currentPlayer:
                for settlement in player.settlementNodesOwned:
                    if settlement in surrondingSettlements:
                        surrondingPlayers.append(player)
                        break
        return surrondingPlayers



    def _validCords(self, cords):
        xCords = ["1", "2", "3", "4", "5"]
        ycords = {"1":3, "2":4, "3":5, "4":4, "5":3}
        if len(cords) == 2 and len(cords[0]) == 1 and len(cords[1]) == 1 and cords[0] in xCords and cords[1] in xCords\
                and int(cords[1]) <= ycords[cords[0]]:
            return True
        else:
            return False
    def _formatTextButton(self, text):
            formattedText = text.lower().strip()
            return formattedText

    def _resetFlags(self, flags):
        flags["startTurn"] = True
        flags["placedSettlement"] = False
        flags["placedRoad"] = False
        flags["canPlaceSettlement"] = False
        flags["canPlaceRoad"] = False
        #Trade flags
        flags["tradePhase"] = False
        flags["playerTrade"] = False
        flags["portTrade"] = False
        flags["choosePlayerPhase"] = False
        flags["makeTradePhase"] = False
        flags["acceptTrade"] = False
        flags["choosePortPhase"] = False
        flags["makeTradePhase"] = False
        #build flags
        flags["canPlaceRoad"] = False
        flags["canPlaceSettlement"] = False
        flags["upgradeCity"] = False
        self.printed = False
        self.tradeBuffer.clear()
        flags["robber"] = False
    def _resetTradeFlags(self, flags):
        flags["tradePhase"] = False
        flags["playerTrade"] = False
        flags["portTrade"] = False
        flags["choosePlayerPhase"] = False
        flags["makeTradePhase"] = False
        flags["acceptTrade"] = False
        flags["choosePortPhase"] = False
        flags["makeTradePhase"] = False
        self.tradeBuffer.clear()

    def _getPlayers(self, numPlayers):
        #FIXME actually write this function, for now manually add players
        playerList = []
        playerList.append(Player(arcade.color.BLUE, "Blue"))
        playerList.append(Player(arcade.color.RED, "Red"))
        return playerList