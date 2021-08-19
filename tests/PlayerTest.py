from Player import Player, RESOURCETYPES
from Player import InvalidSettlementError
from Player import InvalidRoadError
from Board import Board
import unittest

class PlayerTest(unittest.TestCase):
    def setUp(self) -> None:
        board = Board()
        self.board = board.board
        self.graph = board.nodeGraph
        self.player1 = Player("Green")
        self.game = board

    def testCanOnlyPlaceSettlementOnValidNode(self):
        #out of range
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, -1, self.graph)
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 126, self.graph)

        #road node
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 1, self.graph)
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 63, self.graph)
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 124, self.graph)

        #settlement position is already owened
        self.graph.nodeMap[12].isOwened = True
        self.graph.nodeMap[72].isOwened = True
        self.graph.nodeMap[51].isOwened = True
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 12, self.graph)
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 72, self.graph)
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 51, self.graph)
        self.graph.nodeMap[12].isOwened = False
        self.graph.nodeMap[72].isOwened = False
        self.graph.nodeMap[51].isOwened = False

        #SettlementPosition must be 1 intersection away from another settlement
        self.graph.nodeMap[27].isOwened = True
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 25, self.graph)
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 29, self.graph)
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 8, self.graph)
        self.graph.nodeMap[113].isOwened = True
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 94, self.graph)
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 115, self.graph)
        self.graph.nodeMap[59].isOwened = True
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 57, self.graph)
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 86, self.graph)
        self.graph.nodeMap[27].isOwened = False
        self.graph.nodeMap[113].isOwened = False
        self.graph.nodeMap[59].isOwened = False

    def testPlayerCanPlaceSettlementsWithoutRoadsAtBegginingOfGame(self):
        self.player1.placeSettlement(25, self.graph, True)
        self.assertIn(self.graph.nodeMap[25], self.player1.settlementNodesOwned)
        self.assertTrue(self.graph.nodeMap[25])

    def testPlayerNeedsRoadConnectedToPlaceSettlement(self):
        self.player1.placeSettlement(80, self.graph, True)
        self.player1.placeRoad(81, self.graph)
        self.assertIn(self.graph.nodeMap[81], self.player1.roadNodesOwened)
        self.assertTrue(self.graph.nodeMap[81].isOwened)

        self.player1.placeRoad(64, self.graph)
        #not 1 intersection away
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 82, self.graph)
        #Roads are not connecting this intersection
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 84, self.graph)
        self.assertRaises(InvalidSettlementError, self.player1.placeSettlement, 53, self.graph)

        self.player1.placeSettlement(55, self.graph, True)
        self.assertIn(self.graph.nodeMap[55], self.player1.settlementNodesOwned)
        self.assertIn(self.graph.nodeMap[80], self.player1.settlementNodesOwned)
        self.assertTrue(self.graph.nodeMap[55])
    def testInvalidRoads(self):
        #out of range
        self.assertRaises(InvalidRoadError, self.player1.placeRoad, -1, self.graph)
        self.assertRaises(InvalidRoadError, self.player1.placeRoad, 126, self.graph)
        #settlementnodes
        self.assertRaises(InvalidRoadError, self.player1.placeRoad, 78, self.graph)
        self.assertRaises(InvalidRoadError, self.player1.placeRoad, 121, self.graph)
        #Road position is already owened
        self.graph.nodeMap[13].isOwened = True
        self.graph.nodeMap[47].isOwened = True
        self.graph.nodeMap[93].isOwened = True
        self.assertRaises(InvalidRoadError, self.player1.placeRoad, 13, self.graph)
        self.assertRaises(InvalidRoadError, self.player1.placeRoad, 47, self.graph)
        self.assertRaises(InvalidRoadError, self.player1.placeRoad, 93, self.graph)
        self.graph.nodeMap[13].isOwened = False
        self.graph.nodeMap[47].isOwened = False
        self.graph.nodeMap[93].isOwened = False

        #Can Only Place a road if it is connected by another road or settlement
        self.assertRaises(InvalidRoadError, self.player1.placeRoad, 1, self.graph)
        self.assertRaises(InvalidRoadError, self.player1.placeRoad, 90, self.graph)

    def testPlayerGetsResourceEdge(self):
        if self.board[1][1].num != -1:
            self.player1.placeSettlement(0, self.graph, True)
            self.player1.collectResources(self.board[1][1].num)
            self.assertEqual(1, self.player1.totalResources[RESOURCETYPES[self.board[1][1].resource]])

    def testPlayerGetsResourceMiddle(self):
        if self.board[2][2].num != -1 and self.board[2][3].num != -1 and self.board[3][3].num != -1:
            self.player1.placeSettlement(49, self.graph, True)
            self.player1.collectResources(self.board[2][2].num)
            self.assertGreaterEqual(self.player1.totalResources[RESOURCETYPES[self.board[2][2].resource]], 1)
            self.player1.collectResources(self.board[2][3].num)
            self.assertGreaterEqual(self.player1.totalResources[RESOURCETYPES[self.board[2][3].resource]], 1)
            self.player1.collectResources(self.board[3][3].num)
            self.assertGreaterEqual(self.player1.totalResources[RESOURCETYPES[self.board[3][3].resource]], 1)

    def testPlayerDoesntGetResourceIfRobberOnTile(self):
        if self.board[1][1].num != -1:
            self.game.placeRobber([1,1])
            self.player1.placeSettlement(0, self.graph, True)
            self.player1.collectResources(self.board[1][1].num)
            self.assertEqual(0, self.player1.totalResources[RESOURCETYPES[self.board[1][1].resource]])
            self.game.placeRobber([1, 2])
            self.player1.collectResources(self.board[1][1].num)
            self.assertEqual(1, self.player1.totalResources[RESOURCETYPES[self.board[1][1].resource]])
            self.player1.collectResources(self.board[1][1].num)
            self.assertEqual(2, self.player1.totalResources[RESOURCETYPES[self.board[1][1].resource]])

    def testGetRoadFromTwoSettlementNodes(self):
        self.assertEqual(1, self.player1.getRoadFromTwoSettlementNodes(0, 2,self.graph))