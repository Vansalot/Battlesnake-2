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
        self.foodCoords = data["board"]["food"] # dict with locations for food, could/should be removed
        self.foodCount = len(self.foodCoords) # how many food tiles are available
        self.ownSnakeSize = len(self.ownSnake) # size of your snake, might be used in the future. 
        self.dataPreviousRound = None # Data from the previous round/board, to be used to compare new rounds.

        self.tiles = self.startCreateTiles(self.boardSize) # Create an object for every tile
        self.startSetDefaultTilesCost(data) # set up default cost for the tiles on the board.
        self.startSetFoodTiles(data["board"]["food"]) # set up cost for the food at the start. 
        self.updateSnakeLocations(data)
        
        #self.printTiles() # Print the tiles on the board, meant for debug, checking values.



    def updateBeforeProcessingMove(self, data):
        '''#!
        Meant to update certain values that might/will be used before processing where to move. 
        e.g, update the food tiles etc. 
        '''
        pass


    def updatedataPreviousRound(self, data):
        '''
        Set data from current round as previous round, so that next round can
        compare the data. 
        '''
        self.dataPreviousRound = data
        self.ownSnakeSize = data["you"]["length"]
    

    def updateFoodLocations(self, foodList):
        '''
        Go through the foodlist from previous round and current round and see if 
        anyone are missing/added, and update accordingly
        '''
        #! needs work. 
        if self.dataPreviousRound == None:
            pass
        else:
            pass
        

    def updateSnakeLocations(self, data):
        '''
        *** This must be run last, to ensure that costs are not overwritten. ***
        '''
        snakesList = data["board"]["snakes"] 
        ownSnakeHead = data["you"]["head"]
        deadSnakes = []

        if self.dataPreviousRound != None: 
            # if this isn't the first round, update snakes
            if len(self.dataPreviousRound["board"]["snakes"]) != len(data["board"]["snakes"]):
                # First, if there are dead snakes, update cost.
                deadSnakes = self.findDeadSnakes(data) # find the names of the dead snakes.
                self.removeDeadSnakesLocations(deadSnakes) # update dead snake locations, based on list.

            # Update cost for tiles that snakes have left
            self.updatePreviousSnakeLocations(data, deadSnakes)

        # Update cost for tiles where there are snakes.
        for snake in snakesList:
            self.updateTileCost(snake["body"], "snakebody")
        self.updateTileCost([ownSnakeHead], "ownsnakehead")
        #print("WTF: updateSnakeLocations() messed up")


    def updateTileCost(self, coordinateList, costType):
        '''
        coords -> [[x, x][x, x]], costType -> String
        Update tiles individually based on coordinate list received, it will be updated according to the costType parameter,
        which is referring to the costMatrix. 
        '''
        for coordinates in coordinateList:
            # iterating through cords in the received list of coords. 
            currentCord = self.tiles[coordinates["x"]][coordinates["y"]]
            #if costType in self.costMatrix and currentCord.cost >= self.costMatrix[costType] and self.dataPreviousRound == None:
                #pass
            if costType in self.costMatrix and currentCord.cost > self.costMatrix[costType] and self.dataPreviousRound != None:
                # if the current cost of the tile is higher than what we are updating to, do NOT update the cost. 
                print(coordinates, currentCord.cost, "newCostupdate", self.costMatrix[costType], "tile not updated.")
 
            if currentCord.cost == currentCord.originalCost or currentCord.cost == self.costMatrix[costType]:
                    # if the current cost is same as the existing cost, pass.
                    pass
            
            elif costType == "ownsnakehead":
                # update the ownsnakehead cost without checking values.
                currentCord.cost = self.costMatrix[costType]
                print("updated:", coordinates,"from value:", currentCord.cost, "to value:", self.costMatrix[costType], "ownsnakehead")

            elif costType == "originalCost":
                # If costtype is going back to default/originalCost.
                currentCord.cost = currentCord.originalCost
                print("updated:", coordinates,"from value:", currentCord.cost, "to value:", currentCord.originalCost, "originalCost")

            elif currentCord.cost < self.costMatrix[costType]:
                # if the current cost is lower than the existing cost, update the cost.
                currentCord.cost = self.costMatrix[costType]
                print("updated:", coordinates, "from value:", currentCord.cost, "to value:", self.costMatrix[costType], "currentcost < costmatrix")
            
            else:
                print("updateTileCost hit 'else' condition")


    def updatePreviousSnakeLocations(self, data, deadSnakes):
        '''
        Compare snakes locations from previous round and current round and
        update tiles that are empty and tiles that are occupied.
        '''
        coordsToUpdate = []

        for snakePrevious in self.dataPreviousRound["board"]["snakes"]:
            # iterate through snakes from previous round 
            for snakeCurrent in data["board"]["snakes"]:
                # iterate through snakes in the current round.
                
                if snakePrevious["name"] == snakeCurrent["name"] and snakePrevious["name"] not in deadSnakes:
                    # when you find the same snake, compare the coords
                    
                    if snakePrevious["body"][-1] not in snakeCurrent["body"]:
                        # If the last coord(the tail) is not present in the current snakes "body",
                        # update that tile, since it is not occupied.
                        coordsToUpdate.append(snakePrevious["body"][-1])
                   
                    else:
                        # if last cord is present in the current body, pass.
                        pass
                
                else:
                    # if names do not correspond, pass
                    pass
        
        if len(coordsToUpdate) > 0:
           # if there are anything to change, print to log.
           print("# Log: The following coords are not populated by a snake", coordsToUpdate)
        
        self.updateTileCost(coordsToUpdate, "originalCost")


    def findDeadSnakes(self, data):
        '''
        if snakes are dead, send data here, and function returns names of the dead snakes
        '''
        snakesPreviousRound = []
        snakesCurrentRound = []
        deadSnakeNameslist = []

        for snake in self.dataPreviousRound["board"]["snakes"]:
            # create a list of snake names from previous round
            snakesPreviousRound.append(snake["name"])
        for snake in data["board"]["snakes"]:
            # create a list of snake names from current round
            snakesCurrentRound.append(snake["name"])
        # check what names are missing from the previous round. 
        deadSnakeNameslist = set(snakesPreviousRound).difference(snakesCurrentRound)
        print("# Log: The following snakes have died:", deadSnakeNameslist)

        return deadSnakeNameslist


    def removeDeadSnakesLocations(self, deadSnakeNameslist):
        '''
        If snakes are dead, we reset the tile cost to the default value.
        '''
        # Go through the list of dead snakes and update cost of the tiles they used to occupy.
        for deadSnake in deadSnakeNameslist:
            for possibleDeadSnake in self.dataPreviousRound["board"]["snakes"]:
                
                if deadSnake == possibleDeadSnake["name"]:
                    print("# Log: Removing coords for dead snake:", possibleDeadSnake["body"])
                    self.updateTileCost(possibleDeadSnake["body"], "originalCost")
        

    ####
    ##  vvv Functions for setting up the board when a new game starts. vvv
    ####

    def printTiles(self):
        '''
        Test function, for printing cost of tiles and see if it looks ok.
        '''
        for indexX, listX in enumerate(self.tiles):
            for indexY, listY in enumerate(listX):
                
                if self.tiles[indexX][indexY].cost == 0:
                    print(indexX, indexY,":", self.tiles[indexX][indexY].cost, "* you are here *")
                
                elif self.tiles[indexX][indexY].cost == 300:
                    print(indexX, indexY,":", self.tiles[indexX][indexY].cost, "* Corner *")
                
                elif self.tiles[indexX][indexY].cost == 9999:
                    print(indexX, indexY,":", self.tiles[indexX][indexY].cost, "* snake/body *")    

                else:
                    print(indexX, indexY,":", self.tiles[indexX][indexY].cost)


    def startCreateTiles(self, boardSize):
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


    def startSetDefaultTilesCost(self, data):
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
                    self.tiles[indexX][indexY].cost = self.tiles[indexX][indexY].originalCost = self.costMatrix["edge"]
                
                if indexX == 0 and indexY == 0:
                    self.tiles[indexX][indexY].cost = self.tiles[indexX][indexY].originalCost = self.costMatrix["corner"]
                    pass

                # Cost for top right corner, and top and right edges.
                if indexX == self.boardSize[0] - 1 or indexY == self.boardSize[1] - 1:
                    self.tiles[indexX][indexY].cost = self.tiles[indexX][indexY].originalCost = self.costMatrix["edge"]
                
                if indexX == self.boardSize[0] - 1 and indexY == self.boardSize[0] - 1:
                    self.tiles[indexX][indexY].cost = self.tiles[indexX][indexY].originalCost = self.costMatrix["corner"]
                    pass

                # Cost for top left and bottom right corner
                if indexX == 0 and indexY == self.boardSize[1] - 1:
                    self.tiles[indexX][indexY].cost = self.tiles[indexX][indexY].originalCost = self.costMatrix["corner"]
                    pass
                
                if indexX == self.boardSize[0] - 1 and indexY == 0:
                    self.tiles[indexX][indexY].cost = self.tiles[indexX][indexY].originalCost = self.costMatrix["corner"]


    def startSetFoodTiles(self, foodlocs):
        '''
        Set up cost for the starting foodtiles. This function should only be used in the start game request. 
        '''
        self.updateTileCost(foodlocs, "food")


class Tile():
    '''
    one object for every tile on the board
    For now, only contains cost for moving onto the tile. 
    '''
    def __init__(self):
        self.cost = 1
        self.originalCost = 1