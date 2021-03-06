from typing import List
from . import *
from .tile import Tile

#Gives the added x and y distance of two tiles.
def Distance(tile1:Tile, tile2:Tile):
    # if(type(tile1) != 'NoneType' and type(tile2) != 'NoneType'):
    #     xDis = abs(tile1.x - tile2.x)
    #     yDis = abs(tile1.y - tile2.y)
    # else:
    #     xDis, yDis = 0, 0

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


#Creates a list of all tiles containing ores in the map.
def getBomblist(game):
    bomblist = []
    for i in range(int(game.map_height)):
        for j in range(int(game.map_width)):
            curTile = game.get_tile_at(j, i)
            if(curTile.bombs):
                bomblist.append(curTile)
    return bomblist


def findLocationOfNearest(tileList:List['games.coreminer.tile.Tile'], startingTile):
    if tileList != []:
      closestile = tileList[0]
    else:
      closestile = None

    for tile in tileList:
        if (Distance(tile, startingTile) < Distance(closestile, startingTile)):
            closestile = tile
    
    return closestile
    
def getBottomCorner(game, player):
  return game.get_tile_at(player.base_tile.x, 29)

def alternate(game):
  return game.current_turn % 3
  

def find_path(start: 'games.coreminer.tile.Tile', goal: 'games.coreminer.tile.Tile') -> List['games.coreminer.tile.Tile']:
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

def getHardness(tile):
  return tile.ore + tile.dirt + 10 * int(tile.is_ladder or tile.is_support) + 10 * tile.shielding

def getIntelliPath(start: 'games.coreminer.tile.Tile', goal: 'games.coreminer.tile.Tile', bot) -> List['games.coreminer.tile.Tile']:
  """
  Args:
      start (games.coreminer.tile.Tile): The starting Tile to find a path from.
      goal (games.coreminer.tile.Tile): The goal (destination) Tile to find a path to.
      bot: the bot that corresponds to the moving miner
      

  Returns:
      list[games.coreminer.tile.Tile]: A list of Tiles representing the path, the the first element being a valid adjacent Tile to the start, and the last element being the goal.
  """
  #print("Generating IntelliPath for", bot.miner.id ,"...")
  #print(start.x, start.y, 'to', goal.x, goal.y)

  # Used to determine how many tiles we can mine 
  power = min( bot.miner.mining_power, (bot.miner.current_upgrade.cargo_capacity - bot.getCurrentCargo()) )
  #print('power:', power)

  material = bot.miner.building_materials

  if start == goal:
    # no need to make a path to here...
    return []

  # queue of the tiles that will have their neighbors searched for 'goal'
  fringe = []

  # How we got to each tile that went into the fringe.
  came_from = {}

  # Enqueue start as the first tile to have its neighbors searched.
  fringe.append((start, power, material))

  # keep exploring neighbors of neighbors... until there are no more.
  while len(fringe) > 0:
    # the tile we are currently exploring.
    inspect = fringe.pop(0)

    # cycle through the tile's neighbors.
    for neighbor in inspect[0].get_neighbors():
      # if we found the goal, we have the path!
      if neighbor == goal and getHardness(neighbor) <= inspect[1]  and 5 * int(not neighbor.is_ladder) <= inspect[2]:
        # Follow the path backward to the start from the goal and
        # return it.
        path = [goal]

        # Starting at the tile we are currently at, insert them
        # retracing our steps till we get to the starting tile
        while inspect[0] != start:
          path.insert(0, inspect[0])
          inspect = came_from[inspect[0].id]
        #print("Success!")
        return path
      # else we did not find the goal, so enqueue this tile's
      # neighbors to be inspected

      # if the tile exists, has not been explored or added to the
      # fringe yet, and it is pathable
      if neighbor and neighbor.id not in came_from and (
        getHardness(neighbor) <= inspect[1] and 5 * int(not neighbor.is_ladder) <= inspect[2]
      ):
        # add it to the tiles to be explored and add where it came
        # from for path reconstruction.
        fringe.append((neighbor, inspect[1]-getHardness(neighbor), inspect[2] - 5 * int(not neighbor.is_ladder)))
        came_from[neighbor.id] = inspect

  # if you're here, that means that there was not a path to get to where
  # you want to go; in that case, we'll just return an empty path.
  #print("No path found :(")
  return []

