from typing import List
from enum import Enum
from .robot import Robot

class STATE(Enum):
  IDLE = 0
  MOVE = 1
  MINE = 2

class Pitman(Robot):

  def __init__(self, miner):
    self.miner = miner
    self.goalPos = None
    self.state = STATE.IDLE
    if miner.owner.base_tile.tile_east:
      self.side = 'right'
    else: 
      self.side = 'left'

  def performTurn(self):

    # Move to tile next to base
    if self.miner.tile.is_base:
      if self.miner.tile.tile_east:
        self.miner.move(self.miner.tile.tile_east)
      else:
        self.miner.move(self.miner.tile.tile_west)

    # Mine hopper side tile
    self.miner.mine(self.miner.tile.tile_south, -1)

    # Mine hopper side tile
    if self.side == 'left':
      self.miner.mine(self.miner.tile.east_tile, -1)
    else:
      self.miner.mine(self.miner.tile.east_tile, -1)
    
    # # Sell all materials
    # sellTile = self.game.get_tile_at(self.player.base_tile.x, self.miner.tile.y)
    # if sellTile and sellTile.owner == self.player:
    #   self.miner.dump(sellTile, "dirt", -1)
    #   self.miner.dump(sellTile, "ore", -1)