from typing import List
from .robot import Robot
from . import helperfuncs
from . import *

class terminator(Robot):
    def __init__(self, miner, player):
        Robot.__init__(self, miner)
        
        self.player = player
        self.pathList = []

    def getEnemyList(self):
        enemyTileList = []
        minerList = self.game.miners

        for aminer in minerList:
            if(aminer.owner != self.miner.owner):
                enemyTileList.append(aminer.tile)


        #print('enemyTileList:', enemyTileList)
        return enemyTileList

    def find_path(self, start: 'games.coreminer.tile.Tile', goal: 'games.coreminer.tile.Tile') -> List['games.coreminer.tile.Tile']:
        """A very basic path finding algorithm (Breadth First Search) that when given a starting Tile, will return a valid path to the goal Tile.

        Args:
            start (games.coreminer.tile.Tile): The starting Tile to find a path from.
            goal (games.coreminer.tile.Tile): The goal (destination) Tile to find a path to.

        Returns:
            list[games.coreminer.tile.Tile]: A list of Tiles representing the path, the the first element being a valid adjacent Tile to the start, and the last element being the goal.
        """

        if start == goal:
            # no need to make a path to here...
            return []

        # queue of the tiles that will have their neighbors searched for 'goal'
        fringe = []

        # How we got to each tile that went into the fringe.
        came_from = {}

        # Enqueue start as the first tile to have its neighbors searched.
        fringe.append(start)

        # keep exploring neighbors of neighbors... until there are no more.
        while len(fringe) > 0:
            # the tile we are currently exploring.
            inspect = fringe.pop(0)

            # cycle through the tile's neighbors.
            for neighbor in inspect.get_neighbors():
                # if we found the goal, we have the path!
                if neighbor == goal:
                    # Follow the path backward to the start from the goal and
                    # # return it.
                    path = [goal]

                    # Starting at the tile we are currently at, insert them
                    # retracing our steps till we get to the starting tile
                    while inspect != start:
                        path.insert(0, inspect)
                        inspect = came_from[inspect.id]
                    return path
                # else we did not find the goal, so enqueue this tile's
                # neighbors to be inspected

                # if the tile exists, has not been explored or added to the
                # fringe yet, and it is pathable
                if neighbor and neighbor.id not in came_from and (
                    neighbor.is_pathable()
                ):
                    # add it to the tiles to be explored and add where it came
                    # from for path reconstruction.
                    fringe.append(neighbor)
                    came_from[neighbor.id] = inspect

        # if you're here, that means that there was not a path to get to where
        # you want to go; in that case, we'll just return an empty path.
        return [] 

    def moveToward(self, aPath):
        path = aPath
        while path and self.miner.moves > 0:

            # get next path tile
            nextPos = path.pop(0)

            # Mine if needed
            if nextPos.ore + nextPos.dirt > 0:
                self.miner.mine(nextPos, -1)

            # Place ladder if needed
            if nextPos.is_pathable and not nextPos.is_ladder:
                self.miner.build(nextPos, 'ladder')
            
            self.miner.move(nextPos)
            # self.miner.build(self.miner.tile, 'ladder')


    def performTurn(self, game):
        if(self.miner.tile == None):
        #if(self.miner.health == 0):
            return
        self.game = game
        #Find the nearest enemy to terminate.
        closestRobo = helperfuncs.findLocationOfNearest(self.getEnemyList(), self.miner.tile)
        closestHopper = game.get_tile_at(self.player.base_tile.x, self.miner.tile.y)
        #print('closestRobo:', closestRobo)
        #print('closestHopper:', closestHopper)

        #Check if I need to dump shit
        if (self.getCurrentCargo() > self.miner.current_upgrade.cargo_capacity * 0.9):
            #print('Dumping shit because cargo is:', self.getCurrentCargo)
            surroundingTiles = self.miner.tile.get_neighbors()
            for nextTile in surroundingTiles:
                if(nextTile == closestHopper):
                    self.miner.dump(nextTile, 'dirt', -1)
                    self.miner.dump(nextTile, 'ore', -1)
            if(closestHopper != None):
                #self.moveToward(closestHopper)
                self.pathList = self.find_path(self.miner.tile, closestHopper)
                self.moveToward(self.pathList)

        #Check if I need to buy shit
        elif(self.miner.building_materials < 5):
            print('Buying building materials')
            if(closestHopper != None):
                if(self.miner.tile != self.player.base_tile):
                    #self.moveToward(closestHopper)
                    self.moveToward(self.find_path(self.miner.tile, closestHopper))
                else:
                    if(self.player.base_tile.x != 0):
                        #self.moveToward(self.game.get_tile_at(self.miner.tile.x - 1, self.miner.tile.y))
                        self.moveToward(self.find_path(self.miner.tile, self.game.get_tile_at(self.miner.tile.x - 1, self.miner.tile.y)))
                        #self.moveToward(self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1))
                        self.moveToward(self.find_path(self.miner.tile, self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1)))
                    else:
                        #self.moveToward(self.game.get_tile_at(self.miner.tile.x + 1, self.miner.tile.y))
                        self.moveToward(self.find_path(self.miner.tile, self.game.get_tile_at(self.miner.tile.x + 1, self.miner.tile.y)))
                        #self.moveToward(self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1))
                        self.moveToward(self.find_path(self.miner.tile, self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1)))

            if(self.miner.tile == closestHopper):
                self.miner.buy('buildingMaterials', 50)
                self.miner.upgrade()
        elif(self.miner.bombs < 1):
            print('Buying bombs')
            if(closestHopper != None):
                if(self.miner.tile != self.player.base_tile):
                    #self.moveToward(closestHopper)
                    self.moveToward(self.find_path(self.miner.tile, closestHopper))
                else:
                    if(self.player.base_tile.x != 0):
                        #self.moveToward(self.game.get_tile_at(self.miner.tile.x - 1, self.miner.tile.y))
                        self.moveToward(self.find_path(self.miner.tile, self.game.get_tile_at(self.miner.tile.x - 1, self.miner.tile.y)))
                        #self.moveToward(self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1))
                        self.moveToward(self.find_path(self.miner.tile, self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1)))
                    else:
                        #self.moveToward(self.game.get_tile_at(self.miner.tile.x + 1, self.miner.tile.y))
                        self.moveToward(self.find_path(self.miner.tile, self.game.get_tile_at(self.miner.tile.x + 1, self.miner.tile.y)))
                        #self.moveToward(self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1))
                        self.moveToward(self.find_path(self.miner.tile, self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1)))

            if(self.miner.tile == closestHopper):
                self.miner.buy('bomb', 5)
                self.miner.upgrade()
        
        #Check if I can terminate
        else:
            print('Moving towards enemy')
            # surroundingTiles = self.miner.tile.get_neighbors()
            # for nextTile in surroundingTiles:
            print(closestRobo)
            if(self.miner.tile == closestRobo):
                print('Im vibing with enemy')
                self.miner.dump(self.miner.tile, 'bomb', 1)

            if(closestRobo != None):
                #self.moveToward(closestRobo)
                self.moveToward(self.find_path(self.miner.tile, closestRobo))