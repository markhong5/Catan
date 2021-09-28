
class ResourceTile:
    """
    A land tile that has a specific resource and a dice roll number
    TODO: the resources should be an enum instead of a str, same with the resource val

    It also has a list of neighboring vertices, where it can check if a settlement is on their tile
    It also knows when a robber is on the tile
    """
    def __init__(self, resource: str, resourceVal: int, isRobber=False):
        self.resource = resource
        self.num = resourceVal
        self.isRobber = isRobber
        self.vertices = set()

    def addVertice(self, vertice):
        self.vertices.add(vertice)

    def __repr__(self):
        return f"Tile: {self.resource} || Num: {self.num}"

