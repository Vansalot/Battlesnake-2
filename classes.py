import server

from enum import Enum

###
### Classes used in Battlesnake    
###


class Gameboard():

    def __init__(self, costmatrix, data):
        '''
        Gameboard object, contains information about the board, based on json data received from the battlesnake engine. 
        '''
        self.costMatrix = costmatrix
        self.boardSize = [data["board"]["height"], data["board"]["width"]]
        self.foodCoords = data["board"]["food"] # dict with locations for food
        self.foodCount = len(self.foodCoords) # how many food tiles are available
        self.ownSnake = data["you"]["body"]
        self.ownSnakeHead = data["you"]["body"][0] # location of your snake head
        self.ownSnakeSize = len(self.ownSnake) # size of your snake, might be used in the future. 

        self.tiles = self.createTiles(self.boardsize)
        self.updateTiles(data)


    def createTiles(self, boardSize):
        '''
        First/one time setup of the tiles on the board, creates an object of each tile on the board.
        '''

        tiles = []
        for x in range(boardSize[0]):
            templist = []
            for y in range(boardSize[1]):
                templist.append(Tile())
            tiles.append(templist)
        return tiles

    def updateTiles(self, data):
        '''
        Update the cost of each tile every round
        '''

        ### update cost for edges and corners ###
        for indexX, listX in enumerate(self.tiles):
            # enumerate to simplify accessing the objects.
            for indexY, listY in enumerate(listX):
                # 
                if indexX == 0 or indexY == 0:
                    self.tiles[indexX][indexY].cost = self.costMatrix["edge"]
                if indexX == 0 and indexY == 0:
                    self.tiles[indexX][indexY].cost = self.costMatrix["corner"]

class Tile():
    '''
    one object for every tile on the board
    '''
    def __init__(self):
        self.cost = 1