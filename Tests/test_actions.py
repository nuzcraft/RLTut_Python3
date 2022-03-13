import unittest
from unittest.mock import patch

from actions import Action, ActionWithDirection, MovementAction, EscapeAction, MeleeAction, BumpAction
from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap
from engine import Engine
import tile_types


class Test_Actions_Action(unittest.TestCase):
    def test_init(self):
        '''
        test that an action can be initialized
        '''
        ent = Entity()
        action = Action(entity=ent)
        self.assertEqual(action.entity, ent)

    def test_get_engine(self):
        '''
        test that getting the action engine will match the 
        engine of the game_map of the entity
        '''
        ent = Entity()
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        ent.gamemap = gm
        action = Action(ent)
        self.assertEqual(eng, action.engine)

    def test_perform(self):
        '''
        make sure a basic action will return a NotImplementedError
        '''
        ent = Entity()
        action = Action(entity=ent)
        with self.assertRaises(NotImplementedError):
            action.perform()

class Test_Actions_EscapeAction(unittest.TestCase):
    def test_perform(self):
        '''
        make sure an EscapeAction will return a SystemExit
        '''
        ent1 = Entity()
        action = EscapeAction(ent1)
        with self.assertRaises(SystemExit):
            action.perform()

class Test_Actions_ActionWithDirection(unittest.TestCase):
    def test_init(self):
        '''
        test that an ActionWithDirection assigns values
        '''
        x_val = 1
        y_val = -2
        ent = Entity()
        action = ActionWithDirection(entity=ent, dx=x_val, dy=y_val)
        self.assertEqual(action.dx, x_val)
        self.assertEqual(action.dy, y_val)

    def test_get_dest_xy(self):
        '''
        test that dest_xy returns a correct tuple
        '''
        ent = Entity(x=1, y=-2)
        dx, dy = 1, -2
        # dest = ent.x+dx, ent.y+dy
        dest = 2, -4
        action = ActionWithDirection(entity=ent, dx=dx, dy=dy)
        self.assertEqual(dest, action.dest_xy)

    def test_get_blocking_entity_exists(self):
        '''
        test that blocking_entity will return an entity if its blocking
        the destination location
        '''
        pl = Entity() # player at 0,0
        ent = Entity(x=1, y=1, blocks_movement=True) # blocking entity at 1,1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.gamemap = gm
        dx, dy = 1, 1
        action = ActionWithDirection(entity=pl, dx=dx, dy=dy)
        self.assertEqual(ent, action.blocking_entity)

    def test_get_blocking_entity_not_exists(self):
        '''
        test that blocking_entity will return None if no blocking entity
        the destination location
        '''
        pl = Entity() # player at 0,0
        ent = Entity(x=1, y=1, blocks_movement=False) # non-blocking entity at 1,1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add non-blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.gamemap = gm
        dx, dy = 1, 1
        action = ActionWithDirection(entity=pl, dx=dx, dy=dy)
        self.assertIsNone(action.blocking_entity)

class Test_Actions_MeleeAction(unittest.TestCase):
    def test_perform_no_target(self):
        '''
        test that a MeleeAction with no target returns with no change
        '''
        pl = Entity() # player at 0,0
        ent = Entity(x=1, y=1, blocks_movement=False) # nonblocking entity at 1,1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.gamemap = gm
        dx, dy = 1, 1
        action = MeleeAction(entity=pl, dx=dx, dy=dy)
        action.perform()
        self.assertEqual(pl.x, 0)
        self.assertEqual(pl.y, 0)

    @patch('builtins.print')
    def test_perform_with_target(self, mock_print):
        '''
        test that a Melee Action with a target will do something
        '''
        pl = Entity() # player at 0,0
        ent = Entity(x=1, y=1, blocks_movement=True) # blocking entity at 1,1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.gamemap = gm
        dx, dy = 1, 1
        action = MeleeAction(entity=pl, dx=dx, dy=dy)
        action.perform()
        # verify that print was called as it will only be called if there
        # is a blocking entity
        mock_print.assert_called_once()


class Test_Actions_MovementAction(unittest.TestCase):
    def test_perform_out_of_bounds(self):
        '''
        test that moving a player out of bounds does nothing
        '''
        pl = Entity() # player at 0,0
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        pl.gamemap = gm
        dx, dy = -1, -1
        action = MovementAction(entity=pl, dx=dx, dy=dy)
        action.perform()
        # moving out of bounds will do nothing, so x, y should still be 0, 0
        self.assertEqual(pl.x, 0)
        self.assertEqual(pl.y, 0)

    def test_perform_not_walkable(self):
        '''
        test that moving a player into a wall does nothing
        '''
        pl = Entity() # player at 0,0
        goal_x, goal_y = 1, 1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # set the goal to a wall
        gm.tiles[goal_x, goal_y] = tile_types.wall
        eng.game_map = gm
        pl.gamemap = gm
        dx, dy = 1, 1
        action = MovementAction(entity=pl, dx=dx, dy=dy)
        action.perform()
        # nothing changes because the goal is a wall
        self.assertEqual(pl.x, 0)
        self.assertEqual(pl.y, 0)

    def test_perform_blocked_by_entity(self):
        '''
        tests that moving an entity into a blocking entity will not
        actually move the entity
        '''
        pl = Entity() # player at 0,0
        ent = Entity(x=1, y=1, blocks_movement=True) # nonblocking entity at 1,1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.gamemap = gm
        dx, dy = 1, 1
        action = MovementAction(entity=pl, dx=dx, dy=dy)
        action.perform()
        # nothing happens because the goal location is blocked by an entity
        self.assertEqual(pl.x, 0)
        self.assertEqual(pl.y, 0)

    def test_perform_walkable(self):
        '''
        test that moving a player to a floor tile moves the player
        '''
        pl = Entity() # player at 0,0
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.tiles[1, 1] = tile_types.floor
        eng.game_map = gm
        pl.gamemap = gm
        dx, dy = 1, 1
        action = MovementAction(entity=pl, dx=dx, dy=dy)
        action.perform()
        # since the goal x, y is walkable, make sure the entity moved there
        self.assertEqual(pl.x, 1)
        self.assertEqual(pl.y, 1)

class Test_Actions_BumpAction(unittest.TestCase):
    @patch('builtins.print')
    def test_perform_melee(self, mock_print):
        '''
        verify that a BumpAction performs the same as a MeleeAction
        basically a copy of Test_Actions_MeleeAction.test_perform_with_target
        '''
        player_x, player_y = 1, 1
        ent_x, ent_y = 2, 2
        player = Entity(x=player_x, y=player_y)
        # note blocks_movement is false
        ent = Entity(x=ent_x, y=ent_y, blocks_movement=True)
        event_handler = EventHandler()
        gm = GameMap(10, 10, {ent})
        eng = Engine(event_handler=event_handler, game_map=gm, player=player)
        # move the player into the entity space
        action = BumpAction(ent_x-player_x, ent_y-player_y)
        action.perform(engine=eng, entity=player)
        # since the action will call the print function, assert that
        # it was, we don't care about the contents of the output
        mock_print.assert_called_once()

    def test_perform_movement(self):
        '''
        verify that a BumpAction performs the same as a MovementAction
        basically a copy of Test_Actions_MovementAction.test_perform_walkable
        '''
        player_x = 1
        player_y = 1
        goal_x = 2
        goal_y = 2
        player = Entity(player_x, player_y, "@", (0, 0, 0))
        event_handler = EventHandler()
        gm = GameMap(50, 50)
        # set the tile we'll try to move to as a floor
        gm.tiles[goal_x, goal_y] = tile_types.floor
        eng = Engine(event_handler=event_handler,
                     game_map=gm, player=player)
        # the below will always move the player out of bounds
        action = BumpAction(goal_x - player_x, goal_y - player_y)
        action.perform(engine=eng, entity=player)
        # we expect the player to have moved to the new location
        self.assertEqual(player.x, goal_x)
        self.assertEqual(player.y, goal_y)
