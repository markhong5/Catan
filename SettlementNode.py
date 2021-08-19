"""
FIXME set up house nodes
1) for the first row, set up the first and last node
    *pattern for first row is [0,0] -> [0,0] and [0, 1] -> [0, 1] etc
2) for the next 2 rows, set up the first 2 nodes and last 2 nodes
    Pattern for row 1:
        && left = board[1][0]
            above = board[0][0]
            right = board[1][1]
            * add left, above, right to the node
            *move up and to the right
        next loop:
            left = above
            below = right
            right = above[index Above][index Above + 1]
        next loop
            left = below
            above = right
            right = below[index below][index below + 1]
    repeat

for the next 2 rows, same idea except below and above a reveresed
for the last row, repeat the opening for the first row

Also need to add a node inbetween, a so called road node


    *+ [1, 0]+ [0, 0] + [1, 1] -> [0, 0] + [1, 1] + [0, 1] -> [1,1] + [0,1] + [1,2]
"""

class SettlementNode:
    def __init__(self, type, resources= set(), trade=None, isOwened=False, isCity = False):
        self.type = type
        self.trade = trade
        self.resources = resources
        self.isOwened = isOwened
        self.isCity = isCity
        self.next = None






