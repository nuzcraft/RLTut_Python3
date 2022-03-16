from entity import Entity
from game_map import GameMap
from engine import Engine
import unittest


class Test_Entity(unittest.TestCase):
    def test_init_no_gamemap(self):
        '''
        tests initializing a new entity assigns values correctly
        '''
        x_val = 1
        y_val = 2
        char = '@'
        color = [100, 100, 100]
        name = 'nuzcraft'
        blocks_movement = True
        ent = Entity(
            x=x_val,
            y=y_val,
            char=char,
            color=color,
            name=name,
            blocks_movement=blocks_movement,
        )
        self.assertEqual(ent.x, x_val)
        self.assertEqual(ent.y, y_val)
        self.assertEqual(ent.char, char)
        self.assertEqual(ent.color, color)
        self.assertEqual(ent.name, name)
        self.assertEqual(ent.blocks_movement, blocks_movement)

    def test_init_with_gamemap(self):
        '''
        tests that creating an entity with a gamemap will
        set the gamemap and add the entity to it
        '''
        player = Entity()
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        ent = Entity(gamemap=gm)
        self.assertEqual(ent.gamemap, gm)
        # make sure the entity gets added to the gamemap
        self.assertIn(ent, ent.gamemap.entities)

    def test_spawn(self):
        '''
        tests that spawn will copy the entity
        '''
        player = Entity()
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        ent = Entity(name="test")
        ent.spawn(gm, 5, 5)
        # check that entities is filled with something
        self.assertTrue(gm.entities)
        # pull the entity out, make sure it matches as expected
        ents = gm.entities
        ent2 = list(ents)[0]
        self.assertEqual(ent2.name, "test")
        self.assertEqual(ent2.x, 5)
        self.assertEqual(ent2.y, 5)

    def test_place_no_gamemap(self):
        '''
        place the entity at a new location
        do not switch game maps
        '''
        ent = Entity()
        ent.place(x=10, y=10)
        self.assertEqual(ent.x, 10)
        self.assertEqual(ent.y, 10)

    def test_place_with_gamemap(self):
        '''
        place the entity at a new location in a new
        game map
        '''
        player = Entity()
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        gm2 = GameMap(engine=eng, width=10, height=10)
        ent = Entity(gamemap=gm)
        # place the entity at a new gamemap with a new location
        ent.place(x=10, y=10, gamemap=gm2)
        self.assertEqual(ent.x, 10)
        self.assertEqual(ent.y, 10)
        self.assertEqual(ent.gamemap, gm2)
        # make sure the entity gets removed from the old entity list
        # and added to the new one
        self.assertNotIn(ent, gm.entities)
        self.assertIn(ent, gm2.entities)

    def test_move(self):
        '''
        tests moving an entity
        '''
        x_val = 1
        y_val = 2
        dx = 1
        dy = 2
        ent = Entity(x=x_val, y=y_val)
        ent.move(dx, dy)
        self.assertEqual(ent.x, x_val + dx)
        self.assertEqual(ent.y, y_val + dy)


class TestActor(unittest.TestCase):
    def test_init(self):
        '''
        test that initializing an
        '''
