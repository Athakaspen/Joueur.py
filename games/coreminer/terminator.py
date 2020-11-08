from typing import List
from .robot import Robot
from . import helperfuncs
from . import *

class terminator(Robot):
    def __init__(self, miner, game, player):
        Robot.__init__(self, miner)
        self.game = game
        self.player = player

    def getEnemyList(self):
        enemyTileList = []
        minerList = self.game.miners

        for aminer in minerList:
            if(aminer.owner != self.miner.owner):
                enemyTileList.append(aminer.tile)

        return enemyTileList

    def doJob(self):
        #Find the nearest enemy to terminate.
        closestRobo = helperfuncs.findLocationOfNearest(self.getEnemyList(), self.miner.tile)
        closestHopper = helperfuncs.findLocationOfNearest(self.player.hopper_tiles, self.miner.tile)

        if ((self.miner.dirt + self.miner.ore + self.miner.bombs) > 240):

            surroundingTiles = self.miner.tile.get_neighbors()
            for nextTile in surroundingTiles:
                if(nextTile == closestHopper):
                    self.miner.dump(nextTile, 'dirt', -1)
                    self.miner.dump(nextTile, 'ore', -1)
            if(closestHopper != None):
                self.moveToward(closestHopper)

        else:
            surroundingTiles = self.miner.tile.get_neighbors()
            for nextTile in surroundingTiles:
                if(nextTile == closestRobo):
                    self.miner.dump(nextTile, 'bomb', 1)
                elif(nextTile == closestHopper):
                    self.miner.buy('bomb', 5)
                    self.miner.buy('buildingMaterials', 50)

            if(self.miner.bombs < 1):
                if(closestHopper != None):
                    self.moveToward(closestHopper)
            else:
                
                if(closestRobo != None):
                    self.moveToward(closestRobo)
