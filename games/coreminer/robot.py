from typing import List
from enum import Enum
from . import helperfuncs


class Robot:

  def __init__(self, miner):
    self.miner = miner
    self.goalPos = None
    self.state = 'init'
    if miner.owner.base_tile.tile_east:
      self.side = 'right'
    else: 
      self.side = 'left'
  
  def moveToward(self, goal):
    path = []
    if self.miner.tile and goal:
      path = self.getPath(self.miner.tile, goal)
    
    while path and self.miner.moves > 0:

      # get next path tile
      nextPos = path.pop(0)

      # Check that we haven't overstepped somehow
      if nextPos not in self.miner.tile.get_neighbors():
        break

      # Mine if needed
      if nextPos.ore + nextPos.dirt > 0:
        if self.miner.mining_power > 0:
          self.miner.mine(nextPos, -1)
        else:
          break

      # Place ladder if needed
      if nextPos.dirt + nextPos.ore <= 0 and not nextPos.is_ladder and not nextPos.is_hopper:
        # print("Build 1") # FILLED
        self.miner.build(nextPos, 'ladder')
      
      if nextPos.dirt + nextPos.ore <= 0 and not (nextPos.is_hopper and nextPos == self.miner.tile.tile_south):
        self.miner.move(nextPos)
    # self.miner.build(self.miner.tile, 'ladder')

  def pathToward(self, goal):
    path = helperfuncs.find_path(self.miner.tile, goal)
    while path and self.miner.moves > 0:

      # get next path tile
      nextPos = path.pop(0)

      # Place ladder/support if needed
      if nextPos.is_pathable and not nextPos.is_ladder and not nextPos.is_hopper:
        # print("Build 2")
        self.miner.build(nextPos, 'ladder')
      
      if not (nextPos.is_hopper and nextPos == self.miner.tile.tile_south):
        self.miner.move(nextPos)
    

  
  def getPath(self, start:'games.coreminer.tile.Tile', end:'games.coreminer.tile.Tile') -> List:
    
    if start == end: return [] # No need to path if we're already there!

    path = [start]

    xdiff = end.x - start.x
    ydiff = start.y - end.y
    
    if self.side == 'left':
      while xdiff < 0:
        path.append(path[-1].tile_west)
        xdiff += 1
      while ydiff > 0:
        path.append(path[-1].tile_north)
        ydiff -= 1
      while ydiff < 0:
        path.append(path[-1].tile_south)
        ydiff += 1
      while xdiff > 0:
        path.append(path[-1].tile_east)
        xdiff -= 1
      
    else:
      while xdiff > 0:
        path.append(path[-1].tile_east)
        xdiff -= 1
      while ydiff > 0:
        path.append(path[-1].tile_north)
        ydiff -= 1
      while ydiff < 0:
        path.append(path[-1].tile_south)
        ydiff += 1
      while xdiff < 0:
        path.append(path[-1].tile_west)
        xdiff += 1
    
    return path[1:]

  def sellall(self):
    # Sell all materials
    sellTile = None
    for tile in self.miner.tile.get_neighbors():
      if tile.is_hopper or tile.is_base:
        sellTile = tile
    if sellTile and sellTile.owner == self.miner.owner:
      if self.miner.dirt:
        self.miner.dump(sellTile, "dirt", -1)
      if self.miner.ore:
        self.miner.dump(sellTile, "ore", -1)

  def getCurrentCargo(self):
    return self.miner.dirt + self.miner.ore + self.miner.building_materials + self.miner.bombs * 10 # 10 is the bomb size