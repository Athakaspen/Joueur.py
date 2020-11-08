from typing import List
from enum import Enum
from .robot import Robot
from . import helperfuncs

class STATE(Enum):
  IDLE = 0
  MOVE = 1
  MINE = 2

class Pitman(Robot):

  def __init__(self, miner):
    self.miner = miner
    self.goalPos = None
    self.state = STATE.MINE
    if miner.owner.base_tile.tile_east:
      self.side = 'left'
    else: 
      self.side = 'right'

  def performTurn(self, game):
    if(self.miner.tile == None):
        #if(self.miner.health == 0):
      return
    if self.state == STATE.MINE and self.miner:
      # Move to tile next to base
      if self.miner.tile.x == self.miner.owner.base_tile.x:
        if self.miner.tile.tile_east:
          self.miner.move(self.miner.tile.tile_east)
        else:
          self.miner.move(self.miner.tile.tile_west)
      
      # start by resetting
      self.sellall()
      self.restock()
      if self.miner.owner.money > 600 and self.miner.upgrade_level < 3 and self.miner.moves > 0:
        if self.side == 'left':
          self.miner.move(self.miner.tile.tile_west)
        else:
          self.miner.move(self.miner.tile.tile_east)
        
        while self.miner.owner.money > 600 and self.miner.upgrade_level < 3:
          self.miner.upgrade()
        return
      
      # move to bottom
      while self.miner.tile.tile_south and self.miner.tile.tile_south.is_ladder and self.miner.moves > 0:
        self.miner.move(self.miner.tile.tile_south)

      # build ladder
      if not self.miner.tile.is_ladder:
        self.miner.build(self.miner.tile, 'ladder')

      # Mine hopper side tile
      if game.get_tile_at(self.miner.owner.base_tile.x, self.miner.tile.y).dirt!=0:
        if self.side == 'left':
          self.miner.mine(self.miner.tile.tile_west, -1)
        else:
          self.miner.mine(self.miner.tile.tile_east, -1)

      while game.get_tile_at(self.miner.owner.base_tile.x, self.miner.tile.y).dirt==0 and \
        self.miner.moves > 0 and self.miner.mining_power > 0 and self.state == STATE.MINE \
        and self.miner.current_upgrade.cargo_capacity > self.getCurrentCargo():

        # mining the blocks below
        if self.miner.tile.tile_south:
          self.miner.mine(self.miner.tile.tile_south, -1)
        self.miner.move(self.miner.tile.tile_south)

        # build ladder
        self.miner.build(self.miner.tile, 'ladder')

        # Mine hopper side tile
        if self.side == 'left':
          self.miner.mine(self.miner.tile.tile_west, -1)
        else:
          self.miner.mine(self.miner.tile.tile_east, -1)
        
        # detect reaching ground
        if self.miner.tile.y >= 29 and game.get_tile_at(self.miner.owner.base_tile.x, self.miner.tile.y).dirt==0:
          self.state = STATE.IDLE
        
      # move up  
      # if game.get_tile_at(self.miner.owner.base_tile.x, self.miner.tile.y).dirt!=0:
      #   self.miner.move(self.miner.tile.tile_north)
      
      
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
    self.miner.buy('buildingMaterials', 20-self.miner.building_materials)