class OceanTile:

    def __init__(self, port = False, trade = None):
        self.port = port
        self.trade = trade

    def isPort(self):
        return self.port

    def setTrade(self, trade):
        self.trade = trade

    def collectResource(self):
        return -1

    def __repr__(self):
        return f"Tile: Ocean || isPort:{self.port} || trade:{self.trade}"