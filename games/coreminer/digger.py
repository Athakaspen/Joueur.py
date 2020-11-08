from typing import List
from .robot import Robot
from . import helperfuncs


class Digger(Robot):
  def __init__(self, miner):
    self.miner = miner
    self.goalPos = None
    self.state = 'init'
    if miner.owner.base_tile.tile_east:
      self.side = 'left'
    else: 
      self.side = 'right'
  
  def performTurn(self, game):
    
    if self.miner == None or self.miner.tile == None: #no point doin anythin if we dead
      self.state = 'dead'
      return
    
    # Things break if there's no ore
    if not helperfuncs.getOrelist(game):
      self.state = 'dump'
    
    # Get away from the base
    if self.state == 'init':
      if self.side == 'left':
        self.miner.move(self.miner.tile.tile_east)
      else:
        self.miner.move(self.miner.tile.tile_west)
      self.miner.move(self.miner.tile.tile_south)
      
      # send it to the bottom
      self.goalPos = helperfuncs.getBottomCorner(game, self.miner.owner)
      goalPos = helperfuncs.getBottomCorner(game, self.miner.owner)
      if self.side == 'left':
        goalPos = goalPos.tile_east
      else:
        goalPos = goalPos.tile_west
      while not goalPos.is_ladder or goalPos.y == 0:
        goalPos = goalPos.tile_north
      self.state = 'goto'
    
    if self.miner.tile.dirt + self.miner.tile.ore > 0:
      self.state = 'stuck'
    elif self.getCurrentCargo() >= self.miner.current_upgrade.cargo_capacity * 0.8 \
      or self.miner.building_materials <=20:
      self.state = 'dump'
    elif self.getCurrentCargo() <= self.miner.current_upgrade.cargo_capacity * 0.3 \
      and self.miner.building_materials >= 5 and self.state != 'drop':
      self.state = 'mine'
    
    
    # TODO: Evasive maneuvers

    # get out of the hopper
    if self.miner.tile.is_hopper:
      if self.side == 'left':
        self.miner.move(self.miner.tile.tile_east)
      else:
        self.miner.move(self.miner.tile.tile_west)

    # Go out and get ore
    if self.state == 'mine' and self.miner.tile:
      goalPos = helperfuncs.findLocationOfNearest(helperfuncs.getOrelist(game), self.miner.tile)
      
      if goalPos and self.miner.tile and helperfuncs.Distance(goalPos, self.miner.tile) > 15:
        self.state = 'drop'
      self.moveToward(goalPos)

    # Drop off ore and restock building materials
    elif self.state == 'dump':
      goalPos = helperfuncs.findLocationOfNearest(self.miner.owner.hopper_tiles, self.miner.tile)
      
      # mine if possible, otherwise path intelligishently
      # if self.miner.building_materials >= 5 and self.getCurrentCargo() < self.miner.current_upgrade.cargo_capacity * 0.9:
      #   self.moveToward(goalPos)
      # else:
      self.pathToward(goalPos)
      
      if self.miner.tile == goalPos:
        self.sellall()
        self.restock()
        while self.miner.owner.money >= 500 and self.miner.upgrade_level < 3 and self.miner.tile.is_hopper:
          self.miner.upgrade()
    
    elif self.state == 'drop':
      # get ladder column spot
      goalPos = helperfuncs.getBottomCorner(game, self.miner.owner)
      if self.side == 'left':
        goalPos = goalPos.tile_east
      else:
        goalPos = goalPos.tile_west
      
      if self.miner.tile == goalPos or helperfuncs.Distance(goalPos, self.miner.tile) < 10:
        self.state = 'mine'

      # mine if possible, otherwise path intelligishently
      if self.miner.building_materials >= 20 and self.getCurrentCargo() < self.miner.current_upgrade.cargo_capacity * 0.9:
        self.moveToward(goalPos)
      else:
        self.pathToward(goalPos)

    elif self.state == 'stuck':
      # dig self out, then retry performTurn()
      self.miner.mine(self.miner.tile, -1)
      self.performTurn(game)
      return
    

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

  def restock(self):
    self.miner.buy('buildingMaterials', 70-self.miner.building_materials)

