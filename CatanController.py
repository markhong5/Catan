import random
import math
from Board import Board, RESOURCETYPES
import arcade
from Player import *
DEVCARDS = (["Knight"] * 14) + (["Victory Points"] * 5) + (["Road Building"] * 2) + (["Monopoly"] * 2) + (["YearOfPlenty"] * 2)
class CatanController:
    def __init__(self, board, graph, numPlayers=2):
        self.players = self._getPlayers(numPlayers)
        self.devCards = DEVCARDS
        random.shuffle(self.devCards)

        self.currentTurn = 1
        self.currentPlayer = self.players[0]
        self.lengthOfSetUpPhase = 2
        self.roadBuffer = []
        self.playerToTrade = None

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
            self.endTurn(flags)

        if self.lengthOfSetUpPhase == 0:
            flags["setUpPhase"] = False

    def mainGame(self, flags):
        """Main Game flow
        Start Of Turn -> collect resources for all players -> Choose to Trade/Build/Use dev Card -> end turn
        Game Ends when a player has 10 victory points
        """
    def endTurn(self, flags):
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

    def _resetFlags(self, flags):
        flags["startTurn"] = True
        flags["placedSettlement"] = False
        flags["placedRoad"] = False
        flags["canPlaceSettlement"] = False
        flags["canPlaceRoad"] = False
        self.printed = False
    def _getPlayers(self, numPlayers):
        #FIXME actually write this function, for now manually add players
        playerList = []
        playerList.append(Player(arcade.color.BLUE))
        playerList.append(Player(arcade.color.RED))
        return playerList