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
        self.dataPreviousRound = None # Data from the previous round/board, to be used to compare new rounds.

        self.tiles = self.createTiles(self.boardSize) # Create an object for every tile
        self.setStartingTilesCost(data) # set up default cost for the tiles on the board.

        
        
        self.printTiles()


    def updatedataPreviousRound(data):
        '''
        Set data from current round as previous round, so that next round can
        compare the data. 
        '''
        dataPreviousRound = data

    def updateFoodLocations(self, foodList):
        '''
        Go through the foodlist from previous round and current round and see if 
        anyone are missing/added, and update accordingly
        '''
        if self.dataPreviousRound == None:
        

        

    def updateSnakeLocations(self, data):
        '''
        Compare snakes locations from previous round and current round and
        update tiles that are empty and tiles that are occupied.
        *** This must be run last, to ensure that costs are not overwritten. ***
        '''
        pass

    def updateTiles(self, data):
        '''
        Update tiles individually based on input coords from functions that 
        extrapolate data from json.
        '''
        pass
        
def printTiles(self):
        '''
        Test function, for printing cost of tiles and see if it looks ok.
        '''
        for indexX, listX in enumerate(self.tiles):
            for indexY, listY in enumerate(listX):
                print(indexX, indexY, self.tiles[indexX][indexY].cost)

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

    def setStartingTilesCost(self, data):
        '''
        Setting up the cost for the tiles on the starting board.
        Updating the board will/should be done by other functions. 
        '''
        ### update cost for edges and corners ###
        for indexX, listX in enumerate(self.tiles):
            # enumerate to simplify accessing the objects.
            for indexY, listY in enumerate(listX):
                # Cost for bottom left corner, and bottom and left edges.
                if indexX == 0 or indexY == 0:
                    self.tiles[indexX][indexY].cost = self.costMatrix["edge"]
                if indexX == 0 and indexY == 0:
                    self.tiles[indexX][indexY].cost = self.costMatrix["corner"]
                    pass

                # Cost for top right corner, and top and right edges.
                if indexX == self.boardSize[0] - 1 or indexY == self.boardSize[1] - 1:
                    self.tiles[indexX][indexY].cost = self.costMatrix["edge"]
                if indexX == self.boardSize[0] - 1 and indexY == self.boardSize[0] - 1:
                    self.tiles[indexX][indexY].cost = self.costMatrix["corner"]
                    pass

                # Cost for top left and bottom right corner
                if indexX == 0 and indexY == self.boardSize[1] - 1:
                    self.tiles[indexX][indexY].cost = self.costMatrix["corner"]
                    pass
                if indexX == self.boardSize[0] - 1 and indexY == 0:
                    self.tiles[indexX][indexY].cost = self.costMatrix["corner"]


class Tile():
    '''
    one object for every tile on the board
    For now, only contains cost for moving onto the tile. 
    '''
    def __init__(self):
        self.cost = 1