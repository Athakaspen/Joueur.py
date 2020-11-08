from typing import List
from .robot import Robot
from . import helperfuncs
from . import *

class terminator(Robot):
    def __init__(self, miner, player):
        Robot.__init__(self, miner)
        
        self.player = player

    def getEnemyList(self):
        enemyTileList = []
        minerList = self.game.miners

        for aminer in minerList:
            if(aminer.owner != self.miner.owner):
                enemyTileList.append(aminer.tile)


        #print('enemyTileList:', enemyTileList)
        return enemyTileList

    def performTurn(self, game):
        if(self.miner.tile == None):
        #if(self.miner.health == 0):
            self.state = 'dead'
            return
        self.game = game
        #Find the nearest enemy to terminate.
        closestRobo = helperfuncs.findLocationOfNearest(self.getEnemyList(), self.miner.tile)
        closestHopper = game.get_tile_at(self.player.base_tile.x, self.miner.tile.y)
        print('closestRobo:', closestRobo)
        print('closestHopper:', closestHopper)

        # if ((self.miner.dirt + self.miner.ore + self.miner.bombs) > 240):

        #     surroundingTiles = self.miner.tile.get_neighbors()
        #     for nextTile in surroundingTiles:
        #         if(nextTile == closestHopper):
        #             self.miner.dump(nextTile, 'dirt', -1)
        #             self.miner.dump(nextTile, 'ore', -1)
        #     if(closestHopper != None):
        #         self.moveToward(closestHopper)

        # else:
        #     surroundingTiles = self.miner.tile.get_neighbors()
        #     for nextTile in surroundingTiles:
        #         if(nextTile == closestRobo):
        #             self.miner.dump(nextTile, 'bomb', 1)
        #         elif(nextTile == closestHopper):
        #             self.miner.buy('bomb', 5)
        #             self.miner.buy('buildingMaterials', 50)

        #     if(self.miner.bombs < 1):
        #         if(closestHopper != None):
        #             self.moveToward(closestHopper)
        #     else:
                
        #         if(closestRobo != None):
        #             self.moveToward(closestRobo)

        #Check if I need to dump shit
        if (self.getCurrentCargo() > 240):
            print('Dumping shit because cargo is:', self.getCurrentCargo)
            surroundingTiles = self.miner.tile.get_neighbors()
            for nextTile in surroundingTiles:
                if(nextTile == closestHopper):
                    self.miner.dump(nextTile, 'dirt', -1)
                    self.miner.dump(nextTile, 'ore', -1)
            if(closestHopper != None):
                self.moveToward(closestHopper)
        #Check if I need to buy shit
        elif(self.miner.building_materials < 5):
            print('Buying building materials')
            if(closestHopper != None):
                if(self.miner.tile != self.player.base_tile):
                    self.moveToward(closestHopper)
                else:
                    if(self.player.base_tile.x != 0):
                        self.moveToward(self.game.get_tile_at(self.miner.tile.x - 1, self.miner.tile.y))
                        self.moveToward(self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1))
                    else:
                        self.moveToward(self.game.get_tile_at(self.miner.tile.x + 1, self.miner.tile.y))
                        self.moveToward(self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1))

            if(self.miner.tile == closestHopper):
                self.miner.buy('buildingMaterials', 50)
        elif(self.miner.bombs < 1):
            print('Buying bombs')
            if(closestHopper != None):
                if(self.miner.tile != self.player.base_tile):
                    self.moveToward(closestHopper)
                else:
                    if(self.player.base_tile.x != 0):
                        self.moveToward(self.game.get_tile_at(self.miner.tile.x - 1, self.miner.tile.y))
                        self.moveToward(self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1))
                    else:
                        self.moveToward(self.game.get_tile_at(self.miner.tile.x + 1, self.miner.tile.y))
                        self.moveToward(self.game.get_tile_at(self.miner.tile.x, self.miner.tile.y + 1))

            if(self.miner.tile == closestHopper):
                self.miner.buy('bomb', 5)
        
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
                self.moveToward(closestRobo)