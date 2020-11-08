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
    
    if self.state == 'dead' or self.miner == None or self.miner.tile == None: #no point doin anythin if we dead
      self.state = 'dead'
      return
    
    # Things break if there's no ore
    if not helperfuncs.getOrelist(game):
      self.state = 'dump'
    
    # Get away from the base
    if self.state == 'init' and self.miner.tile == self.miner.owner.base_tile:
      self.restock()
      if self.side == 'left':
        self.miner.move(self.miner.tile.tile_east)
      else:
        self.miner.move(self.miner.tile.tile_west)
      self.miner.move(self.miner.tile.tile_south)
      
      # send it to the bottom
      if helperfuncs.Distance(helperfuncs.findLocationOfNearest(helperfuncs.getOrelist(game), self.miner.tile), self.miner.tile) > 15:
        self.goalPos = helperfuncs.getBottomCorner(game, self.miner.owner)
        if self.side == 'left':
          self.goalPos = self.goalPos.tile_east
        else:
          self.goalPos = self.goalPos.tile_west
        while not self.goalPos.is_ladder and self.goalPos.tile_north:
          self.goalPos = self.goalPos.tile_north
        self.state = 'goto'
      else:
        self.state = 'mine'
    elif self.state == 'init':
      self.state = 'mine'
    
    if self.miner.tile.dirt + self.miner.tile.ore > 0:
      self.state = 'stuck'
    elif self.getCurrentCargo() >= self.miner.current_upgrade.cargo_capacity * 0.8 \
      or self.miner.building_materials <=15:
      self.state = 'dump'
    elif self.state != 'goto':
      self.state = 'mine'
    
    if helperfuncs.getOrelist(game) == []:
      self.state = 'dump'
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
      
      # Intellipath TM
      path = helperfuncs.getIntelliPath(self.miner.tile, goalPos, self)
      if path:
        self.followPath(path)
      else:
        self.moveToward(goalPos)

    # Drop off ore and restock building materials
    elif self.state == 'dump':

      if not self.miner.tile.is_hopper:
        goalPos = helperfuncs.findLocationOfNearest(self.miner.owner.hopper_tiles, self.miner.tile)
        
        # Intellipath TM
        path = helperfuncs.getIntelliPath(self.miner.tile, goalPos, self)
        if path:
          self.followPath(path)
        else:
          if helperfuncs.alternate(game):
            self.moveToward(goalPos)
          else:
            self.pathToward(goalPos)
      
      if self.miner.tile.is_hopper:
        self.sellall()
        self.restock()
        while self.miner.owner.money >= 500 and self.miner.upgrade_level < 3 and self.miner.tile.is_hopper:
          self.miner.upgrade()
        self.state = 'mine'
    
    # elif self.state == 'drop':
    #   # get ladder column spot
    #   goalPos = helperfuncs.getBottomCorner(game, self.miner.owner)
    #   if self.side == 'left':
    #     goalPos = goalPos.tile_east
    #   else:
    #     goalPos = goalPos.tile_west
      
    #   if self.miner.tile == goalPos or helperfuncs.Distance(goalPos, self.miner.tile) < 10:
    #     self.state = 'mine'

    #   # mine if possible, otherwise path intelligishently
    #   if self.miner.building_materials >= 20 and self.getCurrentCargo() < self.miner.current_upgrade.cargo_capacity * 0.9:
    #     self.moveToward(goalPos)
    #   else:
    #     self.pathToward(goalPos)

    elif self.state == 'stuck':
      # dig self out, then retry performTurn()
      if self.miner.mining_power > 0 and self.getCurrentCargo() < self.miner.current_upgrade.cargo_capacity:
        self.miner.mine(self.miner.tile, -1)
        self.performTurn(game)
      return
    
    elif self.state == 'goto':
      self.pathToward(self.goalPos)
      self.moveToward(self.goalPos)
      if(self.miner.tile == self.goalPos):
        self.state = 'mine'
    

  def sellall(self):
    # Sell all materials
    sellTile = None
    for tile in self.miner.tile.get_neighbors():
      if tile.is_hopper or tile.is_base:
        sellTile = tile
    if self.miner.tile.is_hopper:
      sellTile = self.miner.tile

    if sellTile and sellTile.owner == self.miner.owner:
      if self.miner.dirt:
        self.miner.dump(sellTile, "dirt", -1)
      if self.miner.ore:
        self.miner.dump(sellTile, "ore", -1)

  def restock(self):
    stock = 55
    if self.miner.building_materials < stock and self.miner.owner.money >= stock-self.miner.building_materials:
      self.miner.buy('buildingMaterials', stock-self.miner.building_materials)

