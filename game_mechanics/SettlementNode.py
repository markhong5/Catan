class SettlementNode:
    """
    A settlement node is a node that lies around the Tiles
    Settlement Nodes come in 2 types "Settlement" and "Road"
        FIXME: Roads should be there own class
        There should also be an enum for this
    resources: A set of resourceTiles that surronds the settlement node
    trade: if a Settlement has a trade, represent it
    isOwned: True if a player owns this settlement node
    isCity: Checks if this settlement is a city
        Only for Settlement
    """
    def __init__(self, type, resources=set(), trade=None, isOwened=False, isCity=False):
        self.type = type
        self.trade = trade
        self.resources = resources
        self.isOwened = isOwened
        self.isCity = isCity







