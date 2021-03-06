#. .T.h.i.s. .is where you build your AI for the Coreminer game.

from typing import List
from joueur.base_ai import BaseAI
from . import helperfuncs
from .terminator import terminator
from .robot import Robot
from .pitman import Pitman
from .digger import Digger

# <<-- Creer-Merge: imports -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
# you can add additional import(s) here
# <<-- /Creer-Merge: imports -->>

class AI(BaseAI):
    """ The AI you add and improve code inside to play Coreminer. """

    def __init__(self, game):
        self._game = game
        self._player = None
        self._settings = {}
        self._robots = []
        self._spawnorder = ['pitman', 't-100', 'digger', 'pitman', 't-100', 'digger', 'pitman', 'digger', 'digger']
        self._turnCount = 0

    @property
    def game(self) -> 'games.coreminer.game.Game':
        """games.coreminer.game.Game: The reference to the Game instance this AI is playing.
        """
        return self._game # don't directly touch this "private" variable pls

    @property
    def player(self) -> 'games.coreminer.player.Player':
        """games.coreminer.player.Player: The reference to the Player this AI controls in the Game.
        """
        return self._player # don't directly touch this "private" variable pls
    
    @property
    def robots(self) -> List:
        return self._robots # don't directly touch this "private" variable pls
    
    @property
    def spawnorder(self) -> List:
        return self._spawnorder # don't directly touch this "private" variable pls
    
    @property   
    def turnCount(self) -> List:
        return self._turnCount # don't directly touch this "private" variable pls
    @turnCount.setter
    def turnCount(self, value):
      self._turnCount = value

    def get_name(self) -> str:
        """This is the name you send to the server so your AI will control the player named this string.

        Returns:
            str: The name of your Player.
        """
        # <<-- Creer-Merge: get-name -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        return "Big_Bean_Samurai" # REPLACE THIS WITH YOUR TEAM NAME
        # <<-- /Creer-Merge: get-name -->>

    def start(self) -> None:
        """This is called once the game starts and your AI knows its player and game. You can initialize your AI here.
        """
        # <<-- Creer-Merge: start -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your start logic

        # orelist = helperfuncs.getOrelist(self.game)
        # for ore in orelist:
        #     print(ore.ore, ore.dirt, ore.x, ore.y)
        # closestOreTile = helperfuncs.findLocationOfNearest(orelist, self.player.base_tile)

        # print(closestOreTile.x, closestOreTile.y)

        print(helperfuncs.getBottomCorner(self.game, self.player).x, helperfuncs.getBottomCorner(self.game, self.player).y )
        
        # <<-- /Creer-Merge: start -->>

    def game_updated(self) -> None:
        """This is called every time the game's state updates, so if you are tracking anything you can update it here.
        """
        # <<-- Creer-Merge: game-updated -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your game updated logic
        # <<-- /Creer-Merge: game-updated -->>

    def end(self, won: bool, reason: str) -> None:
        """This is called when the game ends, you can clean up your data and dump files here if need be.

        Args:
            won (bool): True means you won, False means you lost.
            reason (str): The human readable string explaining why your AI won or lost.
        """
        # <<-- Creer-Merge: end -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # replace with your end logic
        for bot in self.robots:
          if bot.miner.tile:
            print(bot.miner.tile.x, bot.miner.tile.y, bot.miner.id, type(bot), bot.state)
          else:
            print('DEAD', type(bot), bot.state)
        # <<-- /Creer-Merge: end -->>

    def run_turn(self) -> bool:
        """This is called every time it is this AI.player's turn.

        Returns:
            bool: Represents if you want to end your turn. True means end your turn, False means to keep your turn going and re-call this function.
        """
        # <<-- Creer-Merge: runTurn -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
        # Put your game logic here for runTurn

        self.turnCount += 1
        print('Turn', self.turnCount)

        # If we have no miners and can afford one, spawn 1 more
        if len(self.player.miners) < 50 and self.player.money >= self.game.spawn_price+500:

          nextType = 'digger' # default
          if self.spawnorder:
            nextType = self.spawnorder.pop(0)

          if nextType == 'pitman':
            print ("Spawning Pitman...")
            self.player.spawn_miner()
            self.robots.append( Pitman(self.player.miners[-1]) )
          elif nextType == 'digger': # or (nextType == 't-100' and self.player.base_tile.x == 0):
            print ("Spawning Digger...")
            self.player.spawn_miner()
            self.robots.append( Digger(self.player.miners[-1]) )
          elif nextType == 't-100':
            print ("Spawning Terminator...")
            self.player.spawn_miner()
            self.robots.append( terminator(self.player.miners[-1], self.player) )
          self.robots[-1].miner.upgrade()
          self.robots[-1].miner.upgrade()
          self.robots[-1].miner.upgrade()

        for bot in self.robots:
          bot.performTurn(self.game)
          if bot.state == 'idle':
            print("caught idle")
            self.robots.append(Digger(bot.miner))
            self.robots.remove(bot)
          if bot.state == 'dead':
            print("caught dead")
            self.robots.remove(bot)
            if bot is terminator: # or bot is terminator2:
              self.spawnorder.insert(0, 't-100')
          # bot.sellall()

        # if self.robots[0].miner.dirt > 200 and self.player.base_tile.tile_east:
        #   self.robots[0].moveToward(self.player.base_tile.tile_east.tile_east.tile_east.tile_east.tile_east.tile_east.tile_east.tile_east.tile_east.tile_east.tile_south.tile_south.tile_south.tile_south.tile_south.tile_south.tile_south.tile_south.tile_south.tile_south.tile_south.tile_south)
        
        return True
        # <<-- /Creer-Merge: runTurn -->>

    def find_path(self, start: 'games.coreminer.tile.Tile', goal: 'games.coreminer.tile.Tile') -> List['games.coreminer.tile.Tile']:
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

    # <<-- Creer-Merge: functions -->> - Code you add between this comment and the end comment will be preserved between Creer re-runs.
    # if you need additional functions for your AI you can add them here
    # <<-- /Creer-Merge: functions -->>
