from typing import List
from .robot import Robot
from . import helperfuncs

class Pitman(Robot):

  def __init__(self, miner):
    self.miner = miner
    self.goalPos = None
    self.state = 'mine'
    if miner.owner.base_tile.tile_east:
      self.side = 'left'
    else: 
      self.side = 'right'

  def performTurn(self, game):

    if self.state == 'dead' or self.miner == None or self.miner.tile == None: #no point doin anythin if we dead
      self.state = 'dead'
      return

    if self.state == 'mine':
      # Move to tile next to base
      if self.miner.tile.x == self.miner.owner.base_tile.x:
        if self.side == 'left':
          self.miner.move(self.miner.tile.tile_east)
        else:
          self.miner.move(self.miner.tile.tile_west)
      
      # start by resetting
      self.sellall()
      self.restock()
      if self.miner.owner.money > 600 and self.miner.upgrade_level < 3 and self.miner.moves > 0:
        if self.side == 'left' and self.miner.tile.tile_west:
          self.miner.move(self.miner.tile.tile_west)
        elif self.miner.tile.tile_east:
          self.miner.move(self.miner.tile.tile_east)
        
        while self.miner.owner.money > 600 and self.miner.upgrade_level < 3 and self.miner.tile.is_hopper:
          self.miner.upgrade()
        return
      
      # move to bottom
      while self.miner.tile.tile_south and self.miner.tile.tile_south.is_ladder and self.miner.moves > 0:
        self.miner.move(self.miner.tile.tile_south)

      # build ladder
      if not self.miner.tile.is_ladder and not self.miner.tile.is_hopper:
        # print("Build 3")
        self.miner.build(self.miner.tile, 'ladder')

      # Mine hopper side tile
      if game.get_tile_at(self.miner.owner.base_tile.x, self.miner.tile.y).dirt!=0:
        if self.side == 'left':
          self.miner.mine(self.miner.tile.tile_west, -1)
        else:
          self.miner.mine(self.miner.tile.tile_east, -1)

      while game.get_tile_at(self.miner.owner.base_tile.x, self.miner.tile.y).dirt==0 and \
        self.miner.moves > 1 and self.miner.mining_power > 0 \
        and self.miner.current_upgrade.cargo_capacity > self.getCurrentCargo():

        # mining the blocks below
        if self.miner.tile.tile_south and not self.miner.tile.tile_south.is_ladder:
          self.miner.mine(self.miner.tile.tile_south, -1)
        if self.miner.tile.tile_south:
          self.miner.move(self.miner.tile.tile_south)
        else:
          break

        # build ladder
        if not self.miner.tile.is_ladder:
          # print("Build 4") # MINING POWER
          self.miner.build(self.miner.tile, 'ladder')

        # Mine hopper side tile
        if self.side == 'left' and self.miner.tile.tile_west.dirt + self.miner.tile.tile_west.ore > 0 and self.miner.mining_power > 0:
          self.miner.mine(self.miner.tile.tile_west, -1)
        elif self.miner.tile.tile_east.dirt + self.miner.tile.tile_east.ore > 0 and self.miner.mining_power > 0:
          self.miner.mine(self.miner.tile.tile_east, -1)
        
      # detect reaching ground
      if game.get_tile_at(self.miner.owner.base_tile.x, 29).is_hopper:
        print("pitman idling")
        self.state = 'idle'
        
      # move up  
      if game.get_tile_at(self.miner.owner.base_tile.x, self.miner.tile.y).dirt!=0 and self.miner.tile.tile_north:
        self.miner.move(self.miner.tile.tile_north)
      
      
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
    stock = 25
    if self.miner.building_materials < stock and self.miner.owner.money >= stock-self.miner.building_materials:
      self.miner.buy('buildingMaterials', stock-self.miner.building_materials)