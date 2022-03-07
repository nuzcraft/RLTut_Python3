import unittest
from unittest.mock import patch

from actions import Action, ActionWithDirection, MovementAction, EscapeAction, MeleeAction
from entity import Entity
from input_handlers import EventHandler
from game_map import GameMap
from engine import Engine
import tile_types


class Test_Actions_Action(unittest.TestCase):
    def test_perform(self):
        '''
        make sure a basic action will return a NotImplementedError
        '''
        ent1 = Entity(0, 0, "@", (0, 0, 0))
        event_handler = EventHandler()
        gm = GameMap(50, 50)
        eng = Engine(event_handler=event_handler,
                     game_map=gm, player=ent1)
        action = Action()
        with self.assertRaises(NotImplementedError):
            action.perform(eng, ent1)


class Test_Actions_ActionWithDirection(unittest.TestCase):
    def test_init(self):
        '''
        test that an ActionWithDirection assigns values
        '''
        x_val = 1
        y_val = -2
        action = ActionWithDirection(x_val, y_val)
        self.assertEqual(action.dx, x_val)
        self.assertEqual(action.dy, y_val)


class Test_Actions_MeleeAction(unittest.TestCase):
    def test_perform_no_target(self):
        '''
        test that a MeleeAction with no target returns with no change
        '''
        player_x, player_y = 1, 1
        ent_x, ent_y = 2, 2
        player = Entity(x=player_x, y=player_y)
        # note blocks_movement is false
        ent = Entity(x=ent_x, y=ent_y, blocks_movement=False)
        event_handler = EventHandler()
        gm = GameMap(10, 10, {ent})
        eng = Engine(event_handler=event_handler, game_map=gm, player=player)
        # move the player into the entity space
        action = MeleeAction(ent_x-player_x, ent_y-player_y)
        action.perform(engine=eng, entity=player)
        # since the action returns, we expect the player to have not moved
        self.assertEqual(player.x, player_x)
        self.assertEqual(player.y, player_y)

    @patch('builtins.print')
    def test_perform_with_target(self, mock_print):
        '''
        test that a Melee Actino with a target will do something
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
        action = MeleeAction(ent_x-player_x, ent_y-player_y)
        action.perform(engine=eng, entity=player)
        # since the action will call the print function, assert that
        # it was, we don't care about the contents of the output
        mock_print.assert_called_once()


class Test_Actions_MovementAction(unittest.TestCase):
    def test_perform_out_of_bounds(self):
        '''
        test that moving a player out of bounds does nothing
        '''
        player_x = 1
        player_y = 1
        player = Entity(player_x, player_y, "@", (0, 0, 0))
        event_handler = EventHandler()
        gm = GameMap(50, 50)
        eng = Engine(event_handler=event_handler,
                     game_map=gm, player=player)
        # the below will always move the player out of bounds
        action = MovementAction((player_x + 1) * -1, (player_y + 1) * -1)
        action.perform(engine=eng, entity=player)
        # since the action returns, we expect the player to have not moved
        self.assertEqual(player.x, player_x)
        self.assertEqual(player.y, player_y)

    def test_perform_not_walkable(self):
        '''
        test that moving a player into a wall does nothing
        '''
        player_x = 1
        player_y = 1
        goal_x = 2
        goal_y = 2
        player = Entity(player_x, player_y, "@", (0, 0, 0))
        event_handler = EventHandler()
        gm = GameMap(50, 50)
        # set the tile we'll try to move to as a wall
        gm.tiles[goal_x, goal_y] = tile_types.wall
        eng = Engine(event_handler=event_handler,
                     game_map=gm, player=player)
        # the below will move the player towards the goal
        action = MovementAction(goal_x - player_x, goal_y - player_y)
        action.perform(engine=eng, entity=player)
        # since the action returns, we expect the player to have not moved
        self.assertEqual(player.x, player_x)
        self.assertEqual(player.y, player_y)

    def test_perform_blocked_by_entity(self):
        '''
        tests that moving an entity into a blocking entity will not
        actually move the entity
        '''
        player_x, player_y = 1, 1
        ent_x, ent_y = 2, 2
        player = Entity(x=player_x, y=player_y)
        ent = Entity(x=ent_x, y=ent_y, blocks_movement=True)
        event_handler = EventHandler()
        gm = GameMap(10, 10, {ent})
        eng = Engine(event_handler=event_handler, game_map=gm, player=player)
        # move the player into the entity space
        action = MovementAction(ent_x-player_x, ent_y-player_y)
        action.perform(engine=eng, entity=player)
        # since the action returns, we expect the player to have not moved
        self.assertEqual(player.x, player_x)
        self.assertEqual(player.y, player_y)

    def test_perform_walkable(self):
        '''
        test that moving a player to a floor tile moves the player
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
        action = MovementAction(goal_x - player_x, goal_y - player_y)
        action.perform(engine=eng, entity=player)
        # we expect the player to have moved to the new location
        self.assertEqual(player.x, goal_x)
        self.assertEqual(player.y, goal_y)


class Test_Actions_EscapeAction(unittest.TestCase):
    def test_perform(self):
        '''
        make sure an EscapeAction will return a SystemExit
        '''
        ent1 = Entity(0, 0, "@", (0, 0, 0))
        event_handler = EventHandler()
        gm = GameMap(50, 50)
        eng = Engine(event_handler=event_handler,
                     game_map=gm, player=ent1)
        action = EscapeAction()
        with self.assertRaises(SystemExit):
            action.perform(eng, ent1)
