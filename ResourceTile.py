
class ResourceTile:
    def __init__(self, resource: str, resourceVal: int, isRobber = False):
        self.resource = resource
        self.num = resourceVal
        self.isRobber = isRobber

    def __repr__(self):
        return f"Tile: {self.resource} || Num: {self.num}"

