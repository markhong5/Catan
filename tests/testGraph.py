import unittest

from Board import Board


class TestGraph(unittest.TestCase):
    def setUp(self) -> None:
        board = Board()
        self.board = board.board
        self.graph = board.nodeGraph
        # self.graph.printGraph()

    def testTopRowIsCorrectlyConnected(self):

        for i in range(1, 12):
            self.assertIn(i - 1, self.graph.graph[i])
            self.assertIn(i + 1, self.graph.graph[i])

        downCounter = 13
        for i in range(0, 11, 4):
            self.assertIn(i + 1, self.graph.graph[i])
            self.assertIn(downCounter, self.graph.graph[i])
            downCounter += 1
        self.assertIn(11, self.graph.graph[12])
        self.assertIn(downCounter, self.graph.graph[12])


        downCounter = 19
        upCounter = 0
        for i in range(13, 17):
            self.assertIn(upCounter,self.graph.graph[i])
            self.assertIn(downCounter, self.graph.graph[i])
            upCounter += 4
            downCounter += 4

    def testThatTopRowNodesHaveCorrectResources(self):
        nodes = self.graph.nodeMap

        for i in range(0, 13):
            node = nodes[i]
            if i % 2 == 1:
                self.assertEqual("Road", node.type)
            else:
                self.assertEqual("Settlement", node.type)
                if i <= 2:
                    self.assertEqual(node.resources, set([self.board[1][1]]))
                elif i == 4:
                    self.assertEqual(node.resources, set([self.board[1][1], self.board[1][2]]))
                elif i == 6:
                    self.assertEqual(node.resources, set([self.board[1][2]]))
                elif i == 8:
                    self.assertEqual(node.resources, set([self.board[1][2], self.board[1][3]]))
                else:
                    self.assertEqual(node.resources, set([self.board[1][3]]))

        for i in range(13, 17):
            node = nodes[i]
            self.assertEqual("Road", node.type)

    def testSecondRowIsCorrectlyConnected(self):

        for i in range(18, 33):
            self.assertIn(i - 1, self.graph.graph[i])
            self.assertIn(i + 1, self.graph.graph[i])

        downCounter = 34
        for i in range(17, 33, 4):
            self.assertIn(i + 1, self.graph.graph[i])
            self.assertIn(downCounter, self.graph.graph[i])
            downCounter += 1
        self.assertIn(32, self.graph.graph[33])
        self.assertIn(downCounter, self.graph.graph[33])


        downCounter = 41
        upCounter = 17
        for i in range(34, 39):
            self.assertIn(upCounter,self.graph.graph[i])
            self.assertIn(downCounter, self.graph.graph[i])
            upCounter += 4
            downCounter += 4

    def testThatSecondRowNodesHaveCorrectResources(self):
        nodes = self.graph.nodeMap

        for i in range(17, 34):
            node = nodes[i]
            if i % 2 == 0:
                self.assertEqual("Road", node.type)
            else:
                self.assertEqual("Settlement", node.type)
                if i == 17:
                    self.assertEqual(set(node.resources), set([self.board[2][1]]))
                elif i == 19:
                    self.assertEqual(set(node.resources), set([self.board[1][1], self.board[2][1]]))
                elif i == 21:
                    self.assertEqual(set(node.resources), set([self.board[1][1], self.board[2][1], self.board[2][2]]))
                elif i == 23:
                    self.assertEqual(set(node.resources), set([self.board[1][1], self.board[1][2], self.board[2][2]]))
                elif i == 25:
                    self.assertEqual(set(node.resources), set([self.board[2][3], self.board[1][2], self.board[2][2]]))
                elif i == 27:
                    self.assertEqual(set(node.resources), set([self.board[2][3], self.board[1][2], self.board[1][3]]))
                elif i == 29:
                    self.assertEqual(set(node.resources), set([self.board[2][3], self.board[2][4], self.board[1][3]]))
                elif i == 31:
                    self.assertEqual(set(node.resources), set([self.board[1][3], self.board[2][4]]))
                else:
                    self.assertEqual(set(node.resources), set([self.board[2][4]]))

        for i in range(34, 39):
            node = nodes[i]
            self.assertEqual("Road", node.type)

    def testThirdRowIsCorrectlyConnected(self):

        for i in range(40, 59):
            self.assertIn(i - 1, self.graph.graph[i])
            self.assertIn(i + 1, self.graph.graph[i])

        downCounter = 60
        for i in range(39, 59, 4):
            self.assertIn(i + 1, self.graph.graph[i])
            self.assertIn(downCounter, self.graph.graph[i])
            downCounter += 1
        self.assertIn(58, self.graph.graph[59])
        self.assertIn(downCounter, self.graph.graph[59])


        downCounter = 66
        upCounter = 39
        for i in range(60, 66):
            self.assertIn(upCounter,self.graph.graph[i])
            self.assertIn(downCounter, self.graph.graph[i])
            upCounter += 4
            downCounter += 4

    def testThatThirdRowNodesHaveCorrectResources(self):
        nodes = self.graph.nodeMap

        for i in range(39, 60):
            node = nodes[i]
            if i % 2 == 0:
                self.assertEqual("Road", node.type)
            else:
                self.assertEqual("Settlement", node.type)
                if i == 39:
                    self.assertEqual(set(node.resources), set([self.board[3][1]]))
                elif i == 41:
                    self.assertEqual(set(node.resources), set([self.board[3][1], self.board[2][1]]))
                elif i == 43:
                    self.assertEqual(set(node.resources), set([self.board[3][1], self.board[2][1], self.board[3][2]]))
                elif i == 49:
                    self.assertEqual(set(node.resources), set([self.board[2][2], self.board[2][3], self.board[3][3]]))
                elif i == 51:
                    self.assertEqual(set(node.resources), set([self.board[2][3], self.board[3][3], self.board[3][4]]))
                elif i == 57:
                    self.assertEqual(set(node.resources), set([self.board[2][4], self.board[3][5]]))
                elif i == 59:
                    self.assertEqual(set(node.resources), set([self.board[3][5]]))

        for i in range(60, 66):
            node = nodes[i]
            self.assertEqual("Road", node.type)



    def testFourthRowIsCorrectlyConnected(self):

        self.assertIn(60, self.graph.graph[66])
        self.assertIn(67, self.graph.graph[66])

        for i in range(67, 84):
            self.assertIn(i - 1, self.graph.graph[i])
            self.assertIn(i + 1, self.graph.graph[i])

        downCounter = 87
        for i in range(68, 85, 4):
            self.assertIn(i + 1, self.graph.graph[i])
            self.assertIn(downCounter, self.graph.graph[i])
            downCounter += 1
        # self.assertIn(58, self.graph.graph[59])
        # self.assertIn(downCounter, self.graph.graph[59])

        self.assertIn(65, self.graph.graph[86])
        self.assertIn(85, self.graph.graph[86])


        downCounter = 92
        upCounter = 68
        for i in range(87, 92):
            self.assertIn(upCounter,self.graph.graph[i])
            self.assertIn(downCounter, self.graph.graph[i])
            upCounter += 4
            downCounter += 4

    def testThatFourthRowNodesHaveCorrectResources(self):
        nodes = self.graph.nodeMap

        for i in range(66, 87):
            node = nodes[i]
            if i % 2 == 1:
                self.assertEqual("Road", node.type)
            else:
                self.assertEqual("Settlement", node.type)
                if i == 66:
                    self.assertEqual(set(node.resources), set([self.board[3][1]]))
                elif i == 68:
                    self.assertEqual(set(node.resources), set([self.board[3][1], self.board[4][1]]))
                elif i == 70:
                    self.assertEqual(set(node.resources), set([self.board[3][1], self.board[4][1], self.board[3][2]]))
                elif i == 76:
                    self.assertEqual(set(node.resources), set([self.board[4][2], self.board[4][3], self.board[3][3]]))
                elif i == 82:
                    self.assertEqual(set(node.resources), set([self.board[3][5], self.board[4][4], self.board[3][4]]))
                elif i == 84:
                    self.assertEqual(set(node.resources), set([self.board[4][4], self.board[3][5]]))
                elif i == 86:
                    self.assertEqual(set(node.resources), set([self.board[3][5]]))

        for i in range(87, 92):
            node = nodes[i]
            self.assertEqual("Road", node.type)

    def testFifthRowIsCorrectlyConnected(self):

        self.assertIn(87, self.graph.graph[92])
        self.assertIn(93, self.graph.graph[92])

        for i in range(93, 107):
            self.assertIn(i - 1, self.graph.graph[i])
            self.assertIn(i + 1, self.graph.graph[i])

        downCounter = 109
        for i in range(94, 107, 4):
            self.assertIn(i + 1, self.graph.graph[i])
            self.assertIn(downCounter, self.graph.graph[i])
            downCounter += 1

        self.assertIn(91, self.graph.graph[108])
        self.assertIn(107, self.graph.graph[108])


        downCounter = 113
        upCounter = 94
        for i in range(109, 113):
            self.assertIn(upCounter,self.graph.graph[i])
            self.assertIn(downCounter, self.graph.graph[i])
            upCounter += 4
            downCounter += 4

    def testThatFifththRowNodesHaveCorrectResources(self):
        nodes = self.graph.nodeMap

        for i in range(113, 125):
            node = nodes[i]
            if i % 2 == 0:
                self.assertEqual("Road", node.type)
            else:
                self.assertEqual("Settlement", node.type)
                if i == 113:
                    self.assertEqual(node.resources, set([self.board[5][1]]))
                elif i == 115:
                    self.assertEqual(node.resources, set([self.board[5][1]]))
                elif i == 117:
                    self.assertEqual(node.resources, set([self.board[5][1], self.board[5][2]]))
                elif i == 119:
                    self.assertEqual(node.resources, set([self.board[5][2]]))
                elif i == 121:
                    self.assertEqual(node.resources, set([self.board[5][3], self.board[5][2]]))
                elif i == 123:
                    self.assertEqual(node.resources, set([self.board[5][3]]))
                elif i == 125:
                    self.assertEqual(node.resources, set([self.board[5][3]]))

    def testEveryNodeHasLessThanThreeResources(self):
        for key, value in self.graph.nodeMap.items():
            self.assertLess(len(value.resources), 4)

    def testCorrectNodesHavePorts(self):
        self.assertEqual(self.graph.nodeMap[0].trade, self.board[0][0].trade)
        self.assertEqual(self.graph.nodeMap[2].trade, self.board[0][0].trade)
        self.assertEqual(self.graph.nodeMap[6].trade, self.board[0][2].trade)
        self.assertEqual(self.graph.nodeMap[8].trade, self.board[0][2].trade)
        self.assertEqual(self.graph.nodeMap[31].trade, self.board[1][4].trade)
        self.assertEqual(self.graph.nodeMap[33].trade, self.board[1][4].trade)
        self.assertEqual(self.graph.nodeMap[17].trade, self.board[2][0].trade)
        self.assertEqual(self.graph.nodeMap[41].trade, self.board[2][0].trade)
        self.assertEqual(self.graph.nodeMap[59].trade, self.board[3][6].trade)
        self.assertEqual(self.graph.nodeMap[86].trade, self.board[3][6].trade)
        self.assertEqual(self.graph.nodeMap[68].trade, self.board[4][0].trade)
        self.assertEqual(self.graph.nodeMap[92].trade, self.board[4][0].trade)

        self.assertEqual(self.graph.nodeMap[106].trade, self.board[5][4].trade)
        self.assertEqual(self.graph.nodeMap[108].trade, self.board[5][4].trade)
        self.assertEqual(self.graph.nodeMap[113].trade, self.board[6][0].trade)
        self.assertEqual(self.graph.nodeMap[115].trade, self.board[6][0].trade)
        self.assertEqual(self.graph.nodeMap[119].trade, self.board[6][2].trade)
        self.assertEqual(self.graph.nodeMap[121].trade, self.board[6][2].trade)

    def testTilesHaveTheCorrectVertices(self):
        self.assertEqual(set([0, 2, 4, 19, 21, 23]), self.board[1][1].vertices)
        self.assertEqual(set([6, 8, 4, 25, 27, 23]), self.board[1][2].vertices)
        self.assertEqual(set([8, 27, 29, 31, 10, 12]), self.board[1][3].vertices)

        self.assertEqual(set([17, 41, 43, 19, 21, 45]), self.board[2][1].vertices)
        self.assertEqual(set([21, 23, 25, 45, 47, 49]), self.board[2][2].vertices)
        self.assertEqual(set([25, 27, 29, 49, 51, 53]), self.board[2][3].vertices)
        self.assertEqual(set([29, 31, 33, 53, 55, 57]), self.board[2][4].vertices)

        self.assertEqual(set([39, 41, 43, 66, 68, 70 ]), self.board[3][1].vertices)
        self.assertEqual(set([43, 45, 47, 70, 72, 74]), self.board[3][2].vertices)
        self.assertEqual(set([47, 49, 51, 74, 76, 78]), self.board[3][3].vertices)
        self.assertEqual(set([51, 53, 55, 78, 80, 82]), self.board[3][4].vertices)
        self.assertEqual(set([55, 57, 59, 82, 84, 86]), self.board[3][5].vertices)

        self.assertEqual(set([68, 70, 72, 92, 94, 96]), self.board[4][1].vertices)
        self.assertEqual(set([72, 74, 76, 96, 98, 100]), self.board[4][2].vertices)
        self.assertEqual(set([76, 78, 80, 100, 102, 104]), self.board[4][3].vertices)
        self.assertEqual(set([80, 82, 84, 104, 106, 108]), self.board[4][4].vertices)

        self.assertEqual(set([94, 96, 98, 113, 115, 117]), self.board[5][1].vertices)
        self.assertEqual(set([98, 100, 102, 117, 119, 121]), self.board[5][2].vertices)
        self.assertEqual(set([102, 104, 106, 121, 123, 125]), self.board[5][3].vertices)
if __name__ == '__main__':
    unittest.main()