import unittest
from typing import List, Tuple
from unittest.mock import MagicMock, Mock, patch

from numpy import power

from components.ai import BaseAI, HostileEnemy, ConfusedEnemy
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Entity, Actor
from game_map import GameMap
from engine import Engine
from actions import MeleeAction, MovementAction, WaitAction
import tile_types


class Test_BaseAI(unittest.TestCase):
    def test_entity_set(self):
        '''
        tests that the entity can be set correctly
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5))
        self.assertEqual(actor, actor.ai.entity)

        ai = BaseAI(actor)
        ai.entity = actor
        self.assertEqual(actor, ai.entity)

    def test_perform(self):
        '''
        all perform of this AI will be handled
        elsewhere
        '''
        ent = Entity()
        ai = BaseAI(entity=ent)
        with self.assertRaises(NotImplementedError):
            ai.perform()

    def test_get_path_to_straight_line(self):
        '''
        test get_path_to function
        1. test that it returns a short path in a straight line
        '''
        ent = Entity(x=0, y=0)
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        # GameMaps are initialized as all wall, convert to floor
        gm.tiles[:, :] = tile_types.floor
        ent.parent = gm
        ai = BaseAI(entity=ent)
        #  ent starts at 0,0 - get the path straight down to 0,9 (bottom of map)
        path = ai.get_path_to(dest_x=0, dest_y=9)
        # path should be...
        # (0,1)...(0,9)
        path_should_be: List[Tuple[int, int]] = [
            (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9)]
        self.assertEqual(path, path_should_be)

    def test_get_path_to_avoid_wall(self):
        '''
        test get_path_to function
        2. test that it avoids walls
        '''
        ent = Entity(x=0, y=0)
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        # GameMaps are initialized as all wall, convert to floor
        gm.tiles[:, :] = tile_types.floor
        # change a couple of the path tiles to a wall (unwalkable)
        gm.tiles[0, 5] = tile_types.wall
        gm.tiles[1, 5] = tile_types.wall
        ent.parent = gm
        ai = BaseAI(entity=ent)
        #  ent starts at 0,0 - get the path straight down to 0,9 (bottom of map)
        path = ai.get_path_to(dest_x=0, dest_y=9)
        # straight path should be (0,1)...(0,9)
        # but since (0,5) and (1, 5) are unwalkable,
        # the path increases to go around them (diagonal to (1,4) and (2,5) then
        # back to (1,6) before straightening out)
        path_should_be: List[Tuple[int, int]] = [
            (0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (1, 6), (0, 7), (0, 8), (0, 9)]
        self.assertEqual(path, path_should_be)

    def test_get_path_to_avoid_entities(self):
        '''
        test get_path_to function
        3. test that it avoids blocking entities
        '''
        ent = Entity(x=0, y=0)
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        # GameMaps are initialized as all wall, convert to floor
        gm.tiles[:, :] = tile_types.floor
        # add a couple entities to the gamemap that are in the way
        ent1 = Entity(x=0, y=5, blocks_movement=True)
        ent2 = Entity(x=1, y=5, blocks_movement=True)
        gm.entities = {ent1, ent2}
        ent.parent = gm
        ai = BaseAI(entity=ent)
        #  ent starts at 0,0 - get the path straight down to 0,9 (bottom of map)
        path = ai.get_path_to(dest_x=0, dest_y=9)
        # straight path should be (0,1)...(0,9)
        # but since (0,5) and (1, 5) have blocking entities,
        # the path increases to go around them (diagonal to (1,4) and (2,5) then
        # back to (1,6) before straightening out)
        path_should_be: List[Tuple[int, int]] = [
            (0, 1), (0, 2), (0, 3), (1, 4), (2, 5), (1, 6), (0, 7), (0, 8), (0, 9)]
        self.assertEqual(path, path_should_be)


class TestConfusedEnemy(unittest.TestCase):
    def test_init(self):
        '''
        test that the confused enemy can be initized without issues
        '''
        actor = Actor(ai_cls=HostileEnemy, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5))
        ai = ConfusedEnemy(
            entity=actor, previous_ai=HostileEnemy, turns_remaining=5)
        self.assertEqual(ai.previous_ai, HostileEnemy)
        self.assertEqual(ai.turns_remaining, 5)


class TestHostileEnemy(unittest.TestCase):
    def test_init(self):
        '''
        test that the hostile enemy class can be initialized without issues
        '''
        # instantiating an actor will automatically instantiate the ai class under actor.ai
        actor = Actor(ai_cls=HostileEnemy, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5))
        self.assertEqual(actor, actor.ai.entity)
        self.assertEqual([], actor.ai.path)

    def test_perform_wait(self):
        '''
        test that perform() with no path will call WaitAction.perform
        '''
        # run the setup code
        player = Entity(x=0, y=0)
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.tiles[:, :] = tile_types.floor
        gm.entities.add(player)

        hostile_ent = Actor(x=0, y=2, ai_cls=HostileEnemy, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5))
        gm.entities.add(hostile_ent)

        player.parent = gm
        hostile_ent.parent = gm
        eng.game_map = gm

        # since update_fov has not been run, there is no 'visible' tiles
        # for the player to see the hostile entity
        # eng.update_fov()

        # patch the class we want to test for then run the code
        with patch('actions.WaitAction.perform') as mock_WaitAction_perform:
            hostile_ent.ai.perform()

        # verify the WaitAction.perform was called
        mock_WaitAction_perform.assert_called()

    def test_perform_movement(self):
        '''
        test that perform() with a path will call MovementAction.perform
        '''
        # run the setup code
        player = Entity(x=0, y=0)
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.tiles[:, :] = tile_types.floor
        gm.entities.add(player)

        # hostile entity is 2 spaces away
        hostile_ent = Actor(x=0, y=2, ai_cls=HostileEnemy, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5))
        gm.entities.add(hostile_ent)

        player.parent = gm
        hostile_ent.parent = gm
        eng.game_map = gm

        # run update_fov to update the visible tiles
        eng.update_fov()

        # patch the class we want to test for then run the code
        with patch('actions.MovementAction.perform') as mock_MovementAction_perform:
            hostile_ent.ai.perform()

        # verify the WaitAction.perform was called
        mock_MovementAction_perform.assert_called()

    def test_perform_melee(self):
        '''
        test that perform() while next to the player object will 
        peform a melee action
        '''
        # run the setup code
        player = Entity(x=0, y=0)
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.tiles[:, :] = tile_types.floor
        gm.entities.add(player)

        # hostile entity is 1 spaces away
        hostile_ent = Actor(x=0, y=1, ai_cls=HostileEnemy, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5))
        gm.entities.add(hostile_ent)

        player.parent = gm
        hostile_ent.parent = gm
        eng.game_map = gm

        # run update_fov to update the visible tiles
        eng.update_fov()

        # patch the class we want to test for then run the code
        with patch('actions.MeleeAction.perform') as mock_MeleeAction_perform:
            hostile_ent.ai.perform()

        # verify the WaitAction.perform was called
        mock_MeleeAction_perform.assert_called()
