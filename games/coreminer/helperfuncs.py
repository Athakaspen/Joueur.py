from typing import List
from . import *

#Gives the added x and y distance of two tiles.
def Distance(tile1, tile2):
    xDis = abs(tile1.x - tile2.x)
    yDis = abs(tile1.y - tile2.y)

    return xDis + yDis

#Creates a list of all tiles containing ores in the map.
def getOrelist(game):
    orelist = []
    for i in range(int(game.map_height)):
        for j in range(int(game.map_width)):
            curTile = game.get_tile_at(j, i)
            if(curTile.ore > 0):
                orelist.append(curTile)
    return orelist


def findLocationOfNearest(tileList, startingTile):
    closestile = tileList[0]

    for tile in tileList:
        if (Distance(tile, startingTile) < Distance(closestile, startingTile)):
            closestile = tile
    
    return closestile
    



