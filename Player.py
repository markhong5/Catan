from ResourceTile import ResourceTile
from SettlementGraph import SettlementGraph
import copy
"""
FIXME make a Catan file, where the set up phase of the game is played
Then, write tests to make sure that everything works in the player class 
Also, need to set up the trades and ports in the game
"""
BASE_RESOURCES = {
    "lumber": 0,
    "brick": 0,
    "ore": 0,
    "wheat": 0,
    "livestock": 0
}
RESOURCETYPES = {
    "forest":"lumber",
    "hill":"brick",
    "mountain":"ore",
    "farm":"wheat",
    "grassland":"livestock",
    "desert": "empty"
}
class InvalidSettlementError(Exception):
    def __init__(self, message = "Invalid Settlement Position"):
        self.message = message
        super().__init__(self.message)
    pass

class InvalidRoadError(Exception):
    def __init__(self, message = "Invalid Road Position"):
        self.message = message
        super().__init__(self.message)
    pass

class InvalidTradeError(Exception):
    def __init__(self, message = "Invalid Road Position"):
        self.message = message
        super().__init__(self.message)
    pass

#Fixme Add Victory point gain
class Player:
    def __init__(self, color, name = ""):
        #Fixme: I don't use these first 3 variables
        self.totalSettlements = 5
        self.totalCities = 4
        self.totalRoads = 15
        self.color = color
        self.name = name
        self.settlementNodesOwned = []
        self.roadNodesOwened = []
        self.totalResources = copy.deepcopy(BASE_RESOURCES)
        self.victoryPoints = 0
        self.devCards = []
        self.totalKnights = 0

    def placeSettlement(self, locationOfSettlement:int, nodegraph:SettlementGraph, startOfGame=False):
        #Check that it is a valid node
        if locationOfSettlement < 0 or locationOfSettlement >= len(nodegraph.graph):
            raise InvalidSettlementError(f"Settlement position {locationOfSettlement} is not within the range 0 and "
                                         f"{len(nodegraph.graph)}")
        #Check that the location is a settlementLocation
        if nodegraph.nodeMap[locationOfSettlement].type != "Settlement":
            raise InvalidSettlementError(f"Settlement position {locationOfSettlement} is actually a road position")
        #Check that the location is not already owened
        if nodegraph.nodeMap[locationOfSettlement].isOwened:
            raise InvalidSettlementError(f"Settlement position {locationOfSettlement} is already Owened")
        #Ensure that there are no settlements owned by a player in the 3 adjacent intersections
        if self.__noAdjacentOwenedSettlements(locationOfSettlement, nodegraph) != True:
            raise InvalidSettlementError(f"Settlement position {locationOfSettlement} is 1 intersection away from "
                                         f"another Settlement")

        #if it's the start of the game, then you can place settlements anywhere
        #Otherwise you can only place a settlement where you have a road next to it

        if startOfGame == False and self.__roadConnected(locationOfSettlement, nodegraph) != True:
            raise InvalidSettlementError(f"Settlement position {locationOfSettlement} does not have a road connected")

        nodegraph.nodeMap[locationOfSettlement].isOwened = True
        self.settlementNodesOwned.append(nodegraph.nodeMap[locationOfSettlement])
        self.victoryPoints += 1

    def placeRoad(self, locationOfRoad:int, nodegraph:SettlementGraph):
        #Check that it is a valid node
        if locationOfRoad < 0 or locationOfRoad >= len(nodegraph.graph):
            raise InvalidRoadError(f"Road position {locationOfRoad} is not within the range 0 and "
                                         f"{len(nodegraph.graph)}")
        #Check that the location is a roadLocation
        if nodegraph.nodeMap[locationOfRoad].type != "Road":
            raise InvalidRoadError(f"Road position {locationOfRoad} is actually a Settlement position")

        #Check that the road is not already Owened
        if nodegraph.nodeMap[locationOfRoad].isOwened:
            raise InvalidRoadError(f"Road position {locationOfRoad} is already Owened")
        #Ensure that the player owns a road/settlement/city connecting to the road
        if self.__owensConnectedRoadSettlement(locationOfRoad, nodegraph) == False:
            raise InvalidRoadError(f"Road position {locationOfRoad} is not connected to a owened adjacent  road, "
                                   f"settlement, city")

        nodegraph.nodeMap[locationOfRoad].isOwened = True
        self.roadNodesOwened.append(nodegraph.nodeMap[locationOfRoad])

    def getRoadFromTwoSettlementNodes(self, node1, node2, nodegraph):
        val = list(nodegraph.graph[node1] & nodegraph.graph[node2])
        if len(val) != 1:
            raise InvalidRoadError(f"node {node1} and node {node2} do not have a valid node between them")
        return val[0]

    def collectResources(self, num):
        for settlement in self.settlementNodesOwned:
            for resource in settlement.resources:
                if resource.isRobber == False and num == resource.num:
                    if settlement.isCity:
                        self.totalResources[RESOURCETYPES[resource.resource]] += 2
                    else:
                        self.totalResources[RESOURCETYPES[resource.resource]] += 1

    def upgradeSettlementToCity(self, settlementNode):
        for settlement in self.settlementNodesOwned:
            if settlementNode == settlement:
                if not settlement.isCity:
                    settlement.isCity = True
                    return
                else:
                    raise InvalidSettlementError(f"No This node is already a city")
        else:
            raise InvalidSettlementError(f"No settlement Exists for this {settlementNode}")

    def makeTrade(self, tradingPlayer, resourcesToSend, resourcesToRecieve):
        """
        If the trading player has the resources to trade, make the trade
        otherwise raise InvalidTradeError
        Also, make sure the trade abides by the rules of
            1)can't trade for nothing
            2)can't trade for the same resource (i.e 1 lumber for 2 lumber or 1 ore for 1 ore and 2 lumber)
        :param tradingPlayer: player you want to make a trade with
        :param resourcesToSend: an array holding what resources are being sent
        :param resourcesToRecieve: an array holding pairs of what resources are being recieved by the player
        :return:
        """
        resourcesTrading = set()
        for resource in resourcesToSend:
            if len(resource) != 2:
                raise InvalidTradeError(f"Improper trade formatting")
            if resource[0] not in self.totalResources:
                raise InvalidTradeError(f"resource {resource[0]} is not a valid resource")
            if self.totalResources[resource[0]] < resource[1]:
                raise InvalidTradeError(f"Player {self.color} does not have enough {resource[0]} to make trade")
            if resource[1] <= 0:
                raise InvalidTradeError(f"Player {self.color} cannot trade for nothing")
            resourcesTrading.add(resource[0])

        for resource in resourcesToRecieve:
            if len(resource) != 2:
                raise InvalidTradeError(f"Improper trade formatting")
            if resource[0] not in tradingPlayer.totalResources:
                raise InvalidTradeError(f"resource {resource[0]} is not a valid resource")
            if tradingPlayer.totalResources[resource[0]] < resource[1]:
                raise InvalidTradeError(f"Player {tradingPlayer.color} does not have enough {resource[0]} to make trade")
            if resource[1] <= 0:
                raise InvalidTradeError(f"Player {tradingPlayer.color} cannot trade for nothing")
            if resource[0] in resourcesTrading:
                raise InvalidTradeError(f"Player {tradingPlayer.color} cannot trade for the same resource: {resource[1]}")

        for resource in resourcesToSend:
            self.totalResources[resource[0]] -= resource[1]
            tradingPlayer.totalResources[resource[0]] += resource[1]

        for resource in resourcesToRecieve:
            tradingPlayer.totalResources[resource[0]] -= resource[1]
            self.totalResources[resource[0]] += resource[1]
    #
    def portTrade(self, trade, sending, recieving):

        if sending not in self.totalResources or recieving not in self.totalResources:
            raise InvalidTradeError(f"{sending} or {recieving} is not a valid resource type to trade")

        if len(trade) == 2:
            #then it's a 2 for one
            if self.totalResources[sending] < 2:
                raise InvalidTradeError(f"Player {self.color} does not have enough materials to trade")
            else:
                self.totalResources[sending] -= 2
                self.totalResources[recieving] += 1
        elif len(trade) == 1:
            #it's a 3:1 or 4:1
            tradeX = trade[0].split(":") #Bad name
            if self.totalResources[sending] < int(tradeX[0]):
                raise InvalidTradeError(f"Player {self.color} does not have enough materials to trade")
            else:
                self.totalResources[sending] -= int(tradeX[0])
                self.totalResources[recieving] += 1
        else:
            raise InvalidTradeError(f"trade {trade} is invalid")


    def __noAdjacentOwenedSettlements(self, locationOfSettlement, nodegraph):
        adjacentRoads = nodegraph.graph[locationOfSettlement]

        for road in adjacentRoads:
            adjacentSettlements = nodegraph.graph[road]
            for settlement in adjacentSettlements:
                if settlement != locationOfSettlement:
                    settlementNode = nodegraph.nodeMap[settlement]
                    if settlementNode.isOwened:
                        return False
        return True

    def __roadConnected(self, locationOfSettlement, nodegraph):
        adjacentRoads = nodegraph.graph[locationOfSettlement]
        for road in adjacentRoads:
            roadnode = nodegraph.nodeMap[road]
            if roadnode.isOwened:
                return True
        return False

    def __owensConnectedRoadSettlement(self, locationOfRoad, nodegraph):
        adjacentSettlements = nodegraph.graph[locationOfRoad]

        for settlement in adjacentSettlements:
            settlementNode = nodegraph.nodeMap[settlement]
            if settlementNode in self.settlementNodesOwned:
                return True
            adjacentRoads = nodegraph.graph[settlement]
            for road in adjacentRoads:
                #If the adjacent road is not the same as the location of the road
                #though this doesn't really matter since the location of the road should not be owened
                if road != locationOfRoad:
                    roadNode = nodegraph.nodeMap[road]
                    if roadNode in self.roadNodesOwened:
                        return True

        return False
