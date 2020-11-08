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
      return
    
    # Get away from the base
    if self.state == 'init':
      if self.side == 'left':
        self.miner.move(self.miner.tile.tile_east)
      else:
        self.miner.move(self.miner.tile.tile_west)
      self.miner.move(self.miner.tile.tile_south)
      self.state = 'mine'
    
    if self.getCurrentCargo() >= self.miner.current_upgrade.cargo_capacity * 0.8 \
      or self.miner.building_materials <=20:
      self.state = 'dump'
    elif self.getCurrentCargo() <= self.miner.current_upgrade.cargo_capacity * 0.3 \
      and self.miner.building_materials >= 5 and self.state != 'drop':
      self.state = 'mine'
    
    # TODO: Evasive maneuvers

    
    # Go out and get ore
    if self.state == 'mine':
      goalPos = helperfuncs.findLocationOfNearest(helperfuncs.getOrelist(game), self.miner.tile)
      if helperfuncs.Distance(goalPos, self.miner.tile) > 15:
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
      goalPos = helperfuncs.findLocationOfNearest(self.miner.owner.hopper_tiles, self.miner.tile)
      if self.side == 'left':
        goalPos = goalPos.tile_east
      else:
        goalPos = goalPos.tile_west

      # mine if possible, otherwise path intelligishently
      if self.miner.building_materials >= 5 and self.getCurrentCargo() < self.miner.current_upgrade.cargo_capacity * 0.9:
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
      self.miner.dump(sellTile, "dirt", -1)
      self.miner.dump(sellTile, "ore", -1)
  
  def restock(self):
    self.miner.buy('buildingMaterials', 60-self.miner.building_materials)

