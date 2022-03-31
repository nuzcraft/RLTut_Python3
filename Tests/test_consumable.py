import unittest
from unittest.mock import patch
from components.consumable import (
    Consumable,
    HealingConsumable,
    LightningDamageConsumable,
    ConfusionConsumable,
    FireballDamageConsumable,
)
from components.ai import BaseAI, ConfusedEnemy
from components.fighter import Fighter
from components.inventory import Inventory
from entity import Item, Actor
from actions import ItemAction
from engine import Engine
from game_map import GameMap
from exceptions import Impossible
from input_handlers import SingleRangedAttackHandler, AreaRangedAttackHandler


class TestConsumable(unittest.TestCase):
    def test_parent(self):
        '''
        test that an item assigned as a parent to a consumable
        works as expected
        '''
        cm = Consumable()
        item = Item(consumable=cm)
        cm.parent = item
        self.assertEqual(cm.parent, item)

    def test_get_action(self):
        '''
        test that get action returns the correct item action
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5))
        consumable = Consumable()
        item = Item(consumable=consumable)
        consumable.parent = item
        action = consumable.get_action(consumer=actor)
        self.assertIsInstance(action, ItemAction)
        # ideally we'd check that the item action was created correctly
        # but I'm not sure how :)

    def test_activate(self):
        '''
        test that for a base consumable this returns an not implemented error
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5))
        consumable = Consumable()
        item = Item(consumable=consumable)
        consumable.parent = item
        action = consumable.get_action(consumer=actor)

        with self.assertRaises(NotImplementedError):
            consumable.activate(action)

    def test_consume(self):
        '''
        test that consume will remove item from inventory
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        consumable = Consumable()
        item = Item(consumable=consumable)
        consumable.parent = item
        item.parent = actor.inventory
        actor.inventory.items.append(item)
        self.assertIn(item, actor.inventory.items)
        consumable.consume()
        self.assertNotIn(item, actor.inventory.items)


class TestConfusionConsumable(unittest.TestCase):
    def test_init(self):
        '''
        test that initializing a confusion consumable works as expected
        '''
        number_of_turns = 5
        cm = ConfusionConsumable(number_of_turns=number_of_turns)
        self.assertEqual(cm.number_of_turns, number_of_turns)

    def test_get_action(self):
        '''
        test that get_action will add a message tot eh log and update the 
        event handler
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        actor.parent = gm
        cm = ConfusionConsumable(number_of_turns=5)
        item = Item(consumable=cm)
        item.parent = actor.inventory
        cm.parent = item
        with patch('message_log.MessageLog.add_message') as patch_add_message:
            action = cm.get_action(consumer=actor)
        self.assertIsNone(action)
        patch_add_message.assert_called_once()
        self.assertIsInstance(cm.engine.event_handler,
                              SingleRangedAttackHandler)

    def test_activate_good_target(self):
        '''
        test that activating a confusion consumable on a good target will:
        add a message to the log, update the ai of the target, consume the item
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        ent = Actor(
            x=1, y=1,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.visible[:] = True
        actor.parent = gm
        eng.game_map = gm
        gm.entities.add(ent)
        cm = ConfusionConsumable(number_of_turns=5)
        item = Item(consumable=cm)
        item.parent = actor.inventory
        cm.parent = item
        # get_action will initiate user input phase
        cm.get_action(consumer=actor)
        # calling the callback with the target tile will return
        # the action we need
        action = cm.engine.event_handler.callback((1, 1))

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            with patch('components.consumable.Consumable.consume') as patch_consume:
                cm.activate(action=action)

        patch_add_message.assert_called_once()
        self.assertIsInstance(ent.ai, ConfusedEnemy)
        patch_consume.assert_called_once()

    def test_activate_not_visible(self):
        '''
        test that activating on a non-visible tile will raise an exception
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        ent = Actor(
            x=1, y=1,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.visible[:] = False
        actor.parent = gm
        eng.game_map = gm
        gm.entities.add(ent)
        cm = ConfusionConsumable(number_of_turns=5)
        item = Item(consumable=cm)
        item.parent = actor.inventory
        cm.parent = item
        # get_action will initiate user input phase
        cm.get_action(consumer=actor)
        # calling the callback with the target tile will return
        # the action we need
        action = cm.engine.event_handler.callback((1, 1))

        with self.assertRaises(Impossible):
            cm.activate(action=action)

    def test_activate_no_target(self):
        '''
        test that activating without a target actor will raise an exception
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        ent = Actor(
            x=1, y=1,
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.visible[:] = True
        actor.parent = gm
        eng.game_map = gm
        gm.entities.add(ent)
        cm = ConfusionConsumable(number_of_turns=5)
        item = Item(consumable=cm)
        item.parent = actor.inventory
        cm.parent = item
        # get_action will initiate user input phase
        cm.get_action(consumer=actor)
        # calling the callback with the target tile will return
        # the action we need NOTE target does not match ent location
        action = cm.engine.event_handler.callback((2, 2))

        with self.assertRaises(Impossible):
            cm.activate(action=action)

    def test_activate_self(self):
        '''
        test that activating on self(player) will raise an exception
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.visible[:] = True
        actor.parent = gm
        eng.game_map = gm
        cm = ConfusionConsumable(number_of_turns=5)
        item = Item(consumable=cm)
        item.parent = actor.inventory
        cm.parent = item
        # get_action will initiate user input phase
        cm.get_action(consumer=actor)
        # calling the callback with the target tile will return
        # the action we need NOTE target does not match ent location
        action = cm.engine.event_handler.callback((0, 0))

        with self.assertRaises(Impossible):
            cm.activate(action=action)


class TestHealingConsumable(unittest.TestCase):
    def test_init(self):
        '''
        test that a healing consumable amount initializes without issues
        '''
        amt = 5
        cm = HealingConsumable(amount=amt)
        self.assertEqual(cm.amount, amt)

    def test_activate_with_recovery(self):
        '''
        test that activate will heal the fighter
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        actor.fighter.hp = 3
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        consumable = HealingConsumable(amount=5)
        item = Item(consumable=consumable)
        actor.parent = gm
        item.parent = actor.inventory
        consumable.parent = item
        actor.inventory.items.append(item)
        action = consumable.get_action(consumer=actor)

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            consumable.activate(action=action)

        patch_add_message.assert_called_once()
        self.assertEqual(actor.fighter.hp, 8)
        self.assertNotIn(item, actor.inventory.items)

    def test_activate_without_recovery(self):
        '''
        test that activate raise Impossible when it cannot heal
        '''
        actor = Actor(ai_cls=BaseAI, fighter=Fighter(
            hp=10, defense=10, power=10), inventory=Inventory(capacity=5))
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        consumable = HealingConsumable(amount=5)
        item = Item(consumable=consumable)
        item.parent = gm
        consumable.parent = item
        action = consumable.get_action(consumer=actor)

        with self.assertRaises(Impossible):
            consumable.activate(action=action)

class TestFireballDamageConsumable(unittest.TestCase):
    def test_init(self):
        '''
        test that initial values are initialized as expected
        '''
        consumable = FireballDamageConsumable(damage=5, radius=3)
        self.assertEqual(consumable.damage, 5)
        self.assertEqual(consumable.radius, 3)

    def test_get_action(self):
        '''
        test that get_action will add a message to the message log
        and set the event handler to AreaRangedAttackHandler
        '''
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        actor.parent = gm
        cm = FireballDamageConsumable(damage=5, radius=3)
        item = Item(consumable=cm)
        item.parent = actor.inventory
        cm.parent = item
        with patch('message_log.MessageLog.add_message') as patch_add_message:
            action = cm.get_action(consumer=actor)
        self.assertIsNone(action)
        patch_add_message.assert_called_once()
        self.assertIsInstance(cm.engine.event_handler,
                              AreaRangedAttackHandler)

class TestLightningDamageConsumable(unittest.TestCase):
    def test_init(self):
        '''
        test that initializing the consumable sets the values as expected
        '''
        consumable = LightningDamageConsumable(damage=5, maximum_range=6)
        self.assertEqual(consumable.damage, 5)
        self.assertEqual(consumable.maximum_range, 6)

    def test_activate_with_actor(self):
        '''
        test that if there is an actor close enough, the consumable will 
        damage it and be consumed
        '''
        player = Actor(ai_cls=BaseAI, fighter=Fighter(
            hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        actor1 = Actor(
            x=2, y=2,
            ai_cls=BaseAI, fighter=Fighter(
                hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.visible[:] = True
        gm.entities.add(actor1)
        eng.game_map = gm
        player.parent = gm
        consumable = LightningDamageConsumable(damage=5, maximum_range=6)
        item = Item(consumable=consumable)
        player.inventory.items.append(item)
        item.parent = player.inventory
        consumable.parent = item
        action = consumable.get_action(consumer=player)

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            consumable.activate(action=action)

        patch_add_message.assert_called()
        self.assertEqual(actor1.fighter.hp, 5)
        self.assertNotIn(item, player.inventory.items)

    def test_activate_2_actors(self):
        '''
        test that if there are 2 actors close enough, the consumable will
        damage the closer one and not the one further away
        '''
        player = Actor(ai_cls=BaseAI, fighter=Fighter(
            hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        actor1 = Actor(
            x=2, y=2,
            ai_cls=BaseAI, fighter=Fighter(
                hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        actor2 = Actor(
            x=7, y=7,
            ai_cls=BaseAI, fighter=Fighter(
                hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.visible[:] = True
        gm.entities.add(actor1)
        gm.entities.add(actor2)
        eng.game_map = gm
        player.parent = gm
        consumable = LightningDamageConsumable(damage=5, maximum_range=6)
        item = Item(consumable=consumable)
        player.inventory.items.append(item)
        item.parent = player.inventory
        consumable.parent = item
        action = consumable.get_action(consumer=player)

        with patch('message_log.MessageLog.add_message') as patch_add_message:
            consumable.activate(action=action)

        patch_add_message.assert_called()
        self.assertEqual(actor1.fighter.hp, 5)
        self.assertEqual(actor2.fighter.hp, 10)
        self.assertNotIn(item, player.inventory.items)

    def test_activate_no_actors(self):
        '''
        test that if there are no actors, an Impossible exception is raised
        '''
        player = Actor(ai_cls=BaseAI, fighter=Fighter(
            hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.visible[:] = True
        eng.game_map = gm
        player.parent = gm
        consumable = LightningDamageConsumable(damage=5, maximum_range=6)
        item = Item(consumable=consumable)
        player.inventory.items.append(item)
        item.parent = player.inventory
        consumable.parent = item
        action = consumable.get_action(consumer=player)

        with self.assertRaises(Impossible):
            consumable.activate(action=action)

    def test_activate_no_visible_actors(self):
        '''
        test that if there are no visible actors, an Impossible exception is raised
        '''
        player = Actor(ai_cls=BaseAI, fighter=Fighter(
            hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        actor1 = Actor(
            x=2, y=2,
            ai_cls=BaseAI, fighter=Fighter(
                hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.visible[:] = False
        gm.entities.add(actor1)
        eng.game_map = gm
        player.parent = gm
        consumable = LightningDamageConsumable(damage=5, maximum_range=6)
        item = Item(consumable=consumable)
        player.inventory.items.append(item)
        item.parent = player.inventory
        consumable.parent = item
        action = consumable.get_action(consumer=player)

        with self.assertRaises(Impossible):
            consumable.activate(action=action)

    def test_activate_no_actors_in_range(self):
        '''
        test that if there are no actors in range, an Impossible exception is raised
        '''
        player = Actor(ai_cls=BaseAI, fighter=Fighter(
            hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        actor1 = Actor(
            x=5, y=5,
            ai_cls=BaseAI, fighter=Fighter(
                hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5)
        )
        eng = Engine(player=player)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.visible[:] = True
        gm.entities.add(actor1)
        eng.game_map = gm
        player.parent = gm
        consumable = LightningDamageConsumable(damage=5, maximum_range=2)
        item = Item(consumable=consumable)
        player.inventory.items.append(item)
        item.parent = player.inventory
        consumable.parent = item
        action = consumable.get_action(consumer=player)

        with self.assertRaises(Impossible):
            consumable.activate(action=action)
