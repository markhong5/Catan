class OceanTile:
    """
    A tile that only knows if it has a port and a trade
    """
    def __init__(self, port=False, trade=None):
        self.port = port
        self.trade = trade
        #TODO: trade should also be an enum instead of a str

    def isPort(self):
        return self.port

    def setTrade(self, trade):
        self.trade = trade

    def collectResource(self):
        #TODO: Does this function need to exist?
        return -1

    def __repr__(self):
        return f"Tile: Ocean || isPort:{self.port} || trade:{self.trade}"