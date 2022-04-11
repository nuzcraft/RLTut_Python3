from turtle import width
import unittest
from unittest.mock import patch

from numpy import power

from actions import (
    Action, ActionWithDirection,
    MovementAction,
    MeleeAction,
    BumpAction,
    PickupAction,
    ItemAction,
    DropItem,
    TakeStairAction,
    EquipAction,
)
from entity import Entity, Actor, Item
from game_map import GameMap, GameWorld
from engine import Engine
from components.ai import BaseAI, HostileEnemy
from components.equipment import Equipment
from components.equippable import Dagger
from components.fighter import Fighter
from components.consumable import Consumable
from components.inventory import Inventory
from components.level import Level
import tile_types
import color
from exceptions import Impossible


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
        ent.parent = gm
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


class Test_Actions_WaitAction(unittest.TestCase):
    def test_perform(self):
        '''
        nothing to test here since the wait action just 
        passes for now
        '''


class Test_Actions_TakeStairsAction(unittest.TestCase):
    def test_perform_with_stairs(self):
        actor = Actor(
            ai_cls=BaseAI, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        eng.game_world = GameWorld(
            engine=eng,
            map_width=10,
            map_height=10,
            max_rooms=5,
            room_min_size=3,
            room_max_size=4,
        )
        eng.game_world.generate_floor()
        actor.x, actor.y = eng.game_map.downstairs_location
        action = TakeStairAction(entity=actor)

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            action.perform()

        self.assertEqual(action.engine.game_world.current_floor, 2)
        patch_add_message.assert_called_once()

    def test_perform_no_stairs(self):
        actor = Actor(
            ai_cls=BaseAI, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        eng.game_world = GameWorld(
            engine=eng,
            map_width=10,
            map_height=10,
            max_rooms=5,
            room_min_size=3,
            room_max_size=4,
        )
        eng.game_world.generate_floor()
        # actor.x, actor.y = eng.game_map.downstairs_location
        action = TakeStairAction(entity=actor)

        with self.assertRaises(Impossible):
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
        pl = Entity()  # player at 0,0
        ent = Entity(x=1, y=1, blocks_movement=True)  # blocking entity at 1,1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.parent = gm
        dx, dy = 1, 1
        action = ActionWithDirection(entity=pl, dx=dx, dy=dy)
        self.assertEqual(ent, action.blocking_entity)

    def test_get_blocking_entity_not_exists(self):
        '''
        test that blocking_entity will return None if no blocking entity
        the destination location
        '''
        pl = Entity()  # player at 0,0
        # non-blocking entity at 1,1
        ent = Entity(x=1, y=1, blocks_movement=False)
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add non-blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.parent = gm
        dx, dy = 1, 1
        action = ActionWithDirection(entity=pl, dx=dx, dy=dy)
        self.assertIsNone(action.blocking_entity)

    def test_target_actor_with_actor(self):
        '''
        test that target_actor returns and actor if one exists at the location 
        of the action
        '''
        pl = Actor(
            ai_cls=BaseAI, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=5),
            level=Level(),
        )  # player at 0, 0
        ent = Actor(
            x=1,
            y=1,
            ai_cls=BaseAI, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=5),
            level=Level(),
        )  # entity at 1, 1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.entities = {pl, ent}
        eng.game_map = gm
        pl.parent = gm
        action = ActionWithDirection(entity=pl, dx=1, dy=1)
        returned_actor = action.target_actor
        self.assertEqual(returned_actor, ent)

    def test_target_actor_noner(self):
        '''
        test that target_actor returns nothing when none exists at the location 
        of the action
        '''
        pl = Actor(
            ai_cls=BaseAI, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )  # player at 0, 0
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.entities = {pl, }
        eng.game_map = gm
        pl.parent = gm
        action = ActionWithDirection(entity=pl, dx=1, dy=1)
        returned_actor = action.target_actor
        self.assertIsNone(returned_actor)


class Test_Actions_MeleeAction(unittest.TestCase):
    def test_perform_no_target(self):
        '''
        test that a MeleeAction with no target raises an
        exception and the entity does not move
        '''
        pl = Entity()  # player at 0,0
        # nonblocking entity at 1,1
        ent = Entity(x=1, y=1, blocks_movement=False)
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.parent = gm
        dx, dy = 1, 1
        action = MeleeAction(entity=pl, dx=dx, dy=dy)
        with self.assertRaises(Impossible):
            action.perform()
        self.assertEqual(pl.x, 0)
        self.assertEqual(pl.y, 0)

    @patch('message_log.MessageLog.add_message')
    def test_perform_player_with_target_and_damage(self, mock_add_message):
        '''
        test that a Melee Action from a player with a target will do damage
        put out a message with the correct color
        '''
        pl = Actor(x=0, y=0, ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=0, base_power=5), inventory=Inventory(capacity=5),
            level=Level())  # player at 0,0
        ent = Actor(x=1, y=1, ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=0, base_power=5), inventory=Inventory(capacity=5),
            level=Level())  # blocking entity at 1,1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.parent = gm
        dx, dy = 1, 1

        attack_desc = f"{pl.name.capitalize()} attacks {ent.name} for 5 hit points."
        attack_color = color.player_atk

        action = MeleeAction(entity=pl, dx=dx, dy=dy)
        action.perform()
        # verify that print was called as it will only be called if there
        # is a blocking entity
        mock_add_message.assert_called_once_with(attack_desc, attack_color)
        # make sure the target's hp is decreased from 10 to 5
        self.assertEqual(ent.fighter.hp, 5)

    @patch('message_log.MessageLog.add_message')
    def test_perform_enemy_with_target_and_damage(self, mock_add_message):
        '''
        test that a Melee Action from a enemy with a target will do damage
        put out a message with the correct color
        '''
        pl = Actor(x=0, y=0, ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=0, base_power=5), inventory=Inventory(capacity=5),
            level=Level())  # player at 0,0
        ent = Actor(x=1, y=1, ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=0, base_power=5), inventory=Inventory(capacity=5),
            level=Level())  # blocking entity at 1,1
        ent2 = Actor(x=2, y=2, ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=0, base_power=5), inventory=Inventory(capacity=5),
            level=Level())  # blocking entity at 1,1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add blocking entity to the game map, add game map to engine and player
        gm.entities = {ent, ent2}
        eng.game_map = gm
        pl.parent = gm
        ent.parent = gm
        dx, dy = 1, 1

        attack_desc = f"{ent.name.capitalize()} attacks {ent2.name} for 5 hit points."
        attack_color = color.enemy_atk

        action = MeleeAction(entity=ent, dx=dx, dy=dy)
        action.perform()
        # verify that print was called as it will only be called if there
        # is a blocking entity
        mock_add_message.assert_called_once_with(attack_desc, attack_color)
        # make sure the target's hp is decreased from 10 to 5
        self.assertEqual(ent2.fighter.hp, 5)

    @patch('message_log.MessageLog.add_message')
    def test_perform_with_target_and_no_damage(self, mock_add_message):
        '''
        test that a Melee Action with a target will print when no damage is done
        '''
        pl = Actor(x=0, y=0, ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=0, base_power=5), inventory=Inventory(capacity=5),
            level=Level())  # player at 0,0
        ent = Actor(x=1, y=1, ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=5, base_power=5), inventory=Inventory(capacity=5),
            level=Level())  # blocking entity at 1,1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.parent = gm
        dx, dy = 1, 1
        action = MeleeAction(entity=pl, dx=dx, dy=dy)
        action.perform()
        # verify that print was called as it will only be called if there
        # is a blocking entity
        mock_add_message.assert_called_once()
        # make sure the target's hp is not decreased from 10
        self.assertEqual(ent.fighter.hp, 10)


class Test_Actions_MovementAction(unittest.TestCase):
    def test_perform_out_of_bounds(self):
        '''
        test that moving a player out of bounds does nothing
        and raises an exception
        '''
        pl = Entity()  # player at 0,0
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        pl.parent = gm
        dx, dy = -1, -1
        action = MovementAction(entity=pl, dx=dx, dy=dy)

        with self.assertRaises(Impossible):
            action.perform()
        # moving out of bounds will do nothing, so x, y should still be 0, 0
        self.assertEqual(pl.x, 0)
        self.assertEqual(pl.y, 0)

    def test_perform_not_walkable(self):
        '''
        test that moving a player into a wall does nothing
        '''
        pl = Entity()  # player at 0,0
        goal_x, goal_y = 1, 1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # set the goal to a wall
        gm.tiles[goal_x, goal_y] = tile_types.wall
        eng.game_map = gm
        pl.parent = gm
        dx, dy = 1, 1
        action = MovementAction(entity=pl, dx=dx, dy=dy)
        with self.assertRaises(Impossible):
            action.perform()
        # nothing changes because the goal is a wall
        self.assertEqual(pl.x, 0)
        self.assertEqual(pl.y, 0)

    def test_perform_blocked_by_entity(self):
        '''
        tests that moving an entity into a blocking entity will not
        actually move the entity
        '''
        pl = Entity()  # player at 0,0
        # nonblocking entity at 1,1
        ent = Entity(x=1, y=1, blocks_movement=True)
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.parent = gm
        dx, dy = 1, 1
        action = MovementAction(entity=pl, dx=dx, dy=dy)
        with self.assertRaises(Impossible):
            action.perform()
        # nothing happens because the goal location is blocked by an entity
        self.assertEqual(pl.x, 0)
        self.assertEqual(pl.y, 0)

    def test_perform_walkable(self):
        '''
        test that moving a player to a floor tile moves the player
        '''
        pl = Entity()  # player at 0,0
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.tiles[1, 1] = tile_types.floor
        eng.game_map = gm
        pl.parent = gm
        dx, dy = 1, 1
        action = MovementAction(entity=pl, dx=dx, dy=dy)
        action.perform()
        # since the goal x, y is walkable, make sure the entity moved there
        self.assertEqual(pl.x, 1)
        self.assertEqual(pl.y, 1)


class Test_Actions_BumpAction(unittest.TestCase):
    @patch('message_log.MessageLog.add_message')
    def test_perform_melee(self, mock_add_message):
        '''
        verify that a BumpAction performs the same as a MeleeAction
        basically a copy of Test_Actions_MeleeAction.test_perform_with_target
        '''
        pl = Actor(
            x=0,
            y=0,
            ai_cls=HostileEnemy, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=0, base_power=5),
            inventory=Inventory(capacity=5),
            level=Level()
        )  # player at 0,0
        ent = Actor(
            x=1,
            y=1,
            ai_cls=HostileEnemy, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=0, base_power=5),
            inventory=Inventory(capacity=5),
            level=Level()
        )  # blocking entity at 1,1
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        # add blocking entity to the game map, add game map to engine and player
        gm.entities = {ent}
        eng.game_map = gm
        pl.parent = gm
        dx, dy = 1, 1

        attack_desc = f"{pl.name.capitalize()} attacks {ent.name} for 5 hit points."
        attack_color = color.player_atk

        action = BumpAction(entity=pl, dx=dx, dy=dy)
        action.perform()
        # verify that print was called as it will only be called if there
        # is a blocking entity
        mock_add_message.assert_called_once_with(attack_desc, attack_color)
        # make sure the target's hp is decreased from 10 to 5
        self.assertEqual(ent.fighter.hp, 5)

    def test_perform_movement(self):
        '''
        verify that a BumpAction performs the same as a MovementAction
        basically a copy of Test_Actions_MovementAction.test_perform_walkable
        '''
        pl = Entity()  # player at 0,0
        eng = Engine(player=pl)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.tiles[1, 1] = tile_types.floor
        eng.game_map = gm
        pl.parent = gm
        dx, dy = 1, 1
        action = BumpAction(entity=pl, dx=dx, dy=dy)
        action.perform()
        # since the goal x, y is walkable, make sure the entity moved there
        self.assertEqual(pl.x, 1)
        self.assertEqual(pl.y, 1)


class TestPickupAction(unittest.TestCase):
    def test_init(self):
        '''
        test that a pickup action can be initialized okay
        '''
        actor = Actor(ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=10, base_power=10), inventory=Inventory(capacity=5),
            level=Level())
        action = PickupAction(entity=actor)
        self.assertIsInstance(action, PickupAction)

    def test_perform_with_item_and_capacity(self):
        '''
        test that a pickup action (with an item at the correct location)
        (and capacity in inventory) will remove the item from the gamemap
        and add it to the inventory
        '''
        actor = Actor(
            x=5, y=6,
            ai_cls=HostileEnemy, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        item = Item(
            x=5, y=6,
            consumable=Consumable()
        )
        gm.entities = {item}
        item.parent = gm
        eng.game_map = gm
        actor.parent = gm

        action = PickupAction(entity=actor)

        self.assertIn(item, gm.entities)
        self.assertNotIn(item, actor.inventory.items)

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            action.perform()

        self.assertNotIn(item, gm.entities)
        self.assertIn(item, actor.inventory.items)
        patch_add_message.assert_called_once()

    def test_perform_with_no_item_on_map(self):
        '''
        test that a pickup action with no items on the map
        will raise an exception
        '''
        actor = Actor(
            x=5, y=6,
            ai_cls=HostileEnemy, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        # item = Item(
        #     x=5, y=6,
        #     consumable=Consumable()
        # )
        # gm.entities = {item}
        # item.parent = gm
        eng.game_map = gm
        actor.parent = gm

        action = PickupAction(entity=actor)

        with self.assertRaises(Impossible):
            action.perform()

    def test_perform_with_item_in_wrong_spot(self):
        '''
        test that a pickup action with an item on the map,
        but not at the entity's location will raise an exception
        '''
        actor = Actor(
            x=5, y=6,
            ai_cls=HostileEnemy, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        item = Item(
            x=3, y=4,
            consumable=Consumable()
        )
        gm.entities = {item}
        item.parent = gm
        eng.game_map = gm
        actor.parent = gm

        action = PickupAction(entity=actor)

        with self.assertRaises(Impossible):
            action.perform()

    def test_perform_with_no_capacity(self):
        '''
        test that a pickup action with the actor having no capacity
        will raise an exception
        '''
        actor = Actor(
            x=5, y=6,
            ai_cls=HostileEnemy, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=0),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        item = Item(
            x=5, y=6,
            consumable=Consumable()
        )
        gm.entities = {item}
        item.parent = gm
        eng.game_map = gm
        actor.parent = gm

        action = PickupAction(entity=actor)

        with self.assertRaises(Impossible):
            action.perform()


class TestItemAction(unittest.TestCase):
    def test_init_no_targetxy(self):
        '''
        test that an item action can get initialized okay
        and the target_xy gets set to the x, y of the entity
        '''
        actor = Actor(x=5, y=6, ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=10, base_power=10), inventory=Inventory(capacity=5),
            level=Level())
        item = Item(consumable=Consumable())
        item_action = ItemAction(entity=actor, item=item)
        self.assertEqual(item_action.item, item)
        self.assertEqual(item_action.target_xy, (5, 6))

    def test_init_with_targetxy(self):
        '''
        test that an item action can get initialized okay
        and the target_xy gets set
        '''
        actor = Actor(ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=10, base_power=10), inventory=Inventory(capacity=5),
            level=Level())
        item = Item(consumable=Consumable())
        item_action = ItemAction(entity=actor, item=item, target_xy=(5, 6))
        self.assertEqual(item_action.item, item)
        self.assertEqual(item_action.target_xy, (5, 6))

    def test_property_target_actor(self):
        '''
        test that get_actor_at_location is called with the correct inputs
        '''
        actor = Actor(ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=10, base_power=10), inventory=Inventory(capacity=5),
            level=Level())
        item = Item(consumable=Consumable())
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        actor.parent = gm
        item_action = ItemAction(entity=actor, item=item, target_xy=(5, 6))

        with patch('game_map.GameMap.get_actor_at_location') as patch_get_actor:
            target = item_action.target_actor()

        patch_get_actor.assert_called_once_with(5, 6)

    def test_perform(self):
        '''
        test that the activeate command on the consumable is called
        passing in the existing itemAction
        '''
        actor = Actor(ai_cls=HostileEnemy, equipment=Equipment(), fighter=Fighter(
            hp=10, base_defense=10, base_power=10), inventory=Inventory(capacity=5),
            level=Level())
        item = Item(consumable=Consumable())
        item_action = ItemAction(entity=actor, item=item)

        with patch('components.consumable.Consumable.activate') as patch_activate:
            item_action.perform()

        patch_activate.assert_called_once_with(item_action)


class TestDropItem(unittest.TestCase):
    def test_perform(self):
        '''
        test that this will call the drop command of the inventory
        '''
        ent = Actor(
            ai_cls=BaseAI, equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=1),
            level=Level()
        )
        item = Item(consumable=Consumable())
        ent.inventory.items.append(item)
        action = DropItem(
            entity=ent,
            item=item,
        )
        with patch('components.inventory.Inventory.drop') as patch_drop:
            action.perform()
        patch_drop.assert_called_once_with(item)


class TestEquipAction(unittest.TestCase):
    def test_init(self):
        '''
        test that the equip action can be initialized
        '''
        ent = Actor(
            ai_cls=BaseAI,
            equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=1),
            level=Level()
        )
        item = Item(equippable=Dagger())
        ea = EquipAction(entity=ent, item=item)
        self.assertEqual(ea.item, item)

    def test_perform(self):
        '''
        test that perform will call toggle_equip
        '''
        ent = Actor(
            ai_cls=BaseAI,
            equipment=Equipment(),
            fighter=Fighter(hp=10, base_defense=10, base_power=10),
            inventory=Inventory(capacity=1),
            level=Level()
        )
        item = Item(equippable=Dagger())
        ea = EquipAction(entity=ent, item=item)
        with patch('components.equipment.Equipment.toggle_equip') as patch_toggle_equip:
            ea.perform()
        patch_toggle_equip.assert_called_once_with(item)


if __name__ == '__main__':
    unittest.main()
