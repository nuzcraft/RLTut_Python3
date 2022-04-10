from turtle import width
import unittest
from unittest.mock import patch

from numpy import power
from components.fighter import Fighter
from components.equipment import Equipment
from components.equippable import Equippable
from components.ai import HostileEnemy
from components.inventory import Inventory
from components.level import Level
from entity import Actor, Item
from engine import Engine
from game_map import GameMap
from render_order import RenderOrder
from input_handlers import GameOverEventHandler
from equipment_types import EquipmentType
import color


class Test_Fighter(unittest.TestCase):
    def test_init(self):
        '''
        test that initializing a fighter component sets
        values correctly
        '''
        ft = Fighter(hp=10, base_defense=20, base_power=30)
        self.assertEqual(ft.max_hp, 10)
        self.assertEqual(ft._hp, 10)
        self.assertEqual(ft.base_defense, 20)
        self.assertEqual(ft.base_power, 30)

    def test_entity_set(self):
        '''
        test that an entity can be set without issues
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        act = Actor(ai_cls=HostileEnemy, equipment=Equipment(), fighter=ft,
                    inventory=Inventory(capacity=5),
                    level=Level())
        ft.entity = act
        self.assertEqual(act, ft.entity)

    def test_property_hp(self):
        '''
        test that calling hp will return the hp value
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        self.assertEqual(ft.hp, 10)

    def test_setter_hp_in_bounds(self):
        '''
        test that setting the hp works as expected
        when setting within expected range
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        ft.hp = 5
        self.assertEqual(ft.hp, 5)

    def test_setter_hp_too_low(self):
        '''
        test that setting the hp works as expected
        when setting below 0
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        act = Actor(ai_cls=HostileEnemy, equipment=Equipment(), fighter=ft,
                    inventory=Inventory(capacity=5),
                    level=Level())
        ft.entity = act

        eng = Engine(player=act)
        gm = GameMap(engine=eng, width=10, height=10)
        act.parent = gm
        eng.game_map = gm

        ft.hp = -5
        self.assertEqual(ft.hp, 0)

    def test_setter_hp_too_high(self):
        '''
        test that setting the hp works as expected
        when setting above the max
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        ft.hp = 15
        self.assertEqual(ft.hp, ft.max_hp)

    def test_setter_die(self):
        '''
        test that setting hp to 0 will cause the entity to die
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        # this will set the ai to HostileEnemy
        act = Actor(ai_cls=HostileEnemy, equipment=Equipment(), fighter=ft,
                    inventory=Inventory(capacity=5),
                    level=Level())
        ft.parent = act

        eng = Engine(player=act)
        gm = GameMap(engine=eng, width=10, height=10)
        act.parent = gm
        eng.game_map = gm

        ft.hp = 0
        # triggering 'die' should remove the ai component
        self.assertIsNone(ft.parent.ai)

    def test_property_defense(self):
        '''
        def that that the property will return the defense of fighter plus equipment
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        act = Actor(
            ai_cls=HostileEnemy,
            equipment=Equipment(weapon=Item(equippable=Equippable(
                equipment_type=EquipmentType.WEAPON, power_bonus=2, defense_bonus=3))),
            fighter=ft,
            inventory=Inventory(capacity=5),
            level=Level()
        )
        ft.parent = act
        self.assertEqual(ft.defense, 13)

    def test_property_power(self):
        '''
        def that that the property will return the power of fighter plus equipment
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        act = Actor(
            ai_cls=HostileEnemy,
            equipment=Equipment(weapon=Item(equippable=Equippable(
                equipment_type=EquipmentType.WEAPON, power_bonus=2, defense_bonus=3))),
            fighter=ft,
            inventory=Inventory(capacity=5),
            level=Level()
        )
        ft.parent = act
        self.assertEqual(ft.power, 12)

    def test_property_defense_bonus(self):
        '''
        def that that the property will return the defense of equipment
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        act = Actor(
            ai_cls=HostileEnemy,
            equipment=Equipment(weapon=Item(equippable=Equippable(
                equipment_type=EquipmentType.WEAPON, power_bonus=2, defense_bonus=3))),
            fighter=ft,
            inventory=Inventory(capacity=5),
            level=Level()
        )
        ft.parent = act
        self.assertEqual(ft.defense_bonus, 3)

    def test_property_defense_bonus_none(self):
        '''
        def that that the property will return 0 if the parent has no equipment
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        act = Actor(
            ai_cls=HostileEnemy,
            equipment=Equipment(weapon=Item()),
            fighter=ft,
            inventory=Inventory(capacity=5),
            level=Level()
        )
        ft.parent = act
        self.assertEqual(ft.defense_bonus, 0)

    def test_property_power_bonus(self):
        '''
        def that that the property will return the defense of equipment
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        act = Actor(
            ai_cls=HostileEnemy,
            equipment=Equipment(weapon=Item(equippable=Equippable(
                equipment_type=EquipmentType.WEAPON, power_bonus=2, defense_bonus=3))),
            fighter=ft,
            inventory=Inventory(capacity=5),
            level=Level()
        )
        ft.parent = act
        self.assertEqual(ft.power_bonus, 2)

    def test_property_power_bonus_none(self):
        '''
        def that that the property will return 0 if the parent has no equipment
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        act = Actor(
            ai_cls=HostileEnemy,
            equipment=Equipment(weapon=Item()),
            fighter=ft,
            inventory=Inventory(capacity=5),
            level=Level()
        )
        ft.parent = act
        self.assertEqual(ft.power_bonus, 0)

    @patch('message_log.MessageLog.add_message')
    def test_die_player(self, mock_add_message):
        '''
        test that when a player dies, they get set well
        and a message of the correct color is added to the message log
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        # this will set the ai to HostileEnemy
        act = Actor(name="player", ai_cls=HostileEnemy, equipment=Equipment(),
                    fighter=ft, inventory=Inventory(capacity=5),
                    level=Level())
        ft.parent = act

        eng = Engine(player=act)
        gm = GameMap(engine=eng, width=10, height=10)
        act.parent = gm
        eng.game_map = gm

        ft.die()

        self.assertEqual(ft.parent.char, "%")
        self.assertEqual(ft.parent.color, (191, 0, 0))
        self.assertFalse(ft.parent.blocks_movement)
        self.assertIsNone(ft.parent.ai)
        self.assertEqual(ft.parent.name, "remains of player")
        self.assertEqual(ft.parent.render_order, RenderOrder.CORPSE)
        mock_add_message.assert_called_with("You died!", color.player_die)

    @patch('message_log.MessageLog.add_message')
    def test_die_other_actor(self, mock_add_message):
        '''
        test that when an actor (not player) dies, they get set well
        also verify that xp is given to the player
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        act = Actor(name="actor", ai_cls=HostileEnemy, equipment=Equipment(),
                    fighter=ft, inventory=Inventory(capacity=5),
                    level=Level(xp_given=150))
        ft.parent = act

        ft2 = Fighter(hp=10, base_defense=10, base_power=10)
        act2 = Actor(name="player", ai_cls=HostileEnemy, equipment=Equipment(),
                     fighter=ft2, inventory=Inventory(capacity=5),
                     level=Level(level_up_base=200))
        ft2.parent = act2

        eng = Engine(player=act2)
        gm = GameMap(engine=eng, width=10, height=10)
        act.parent = gm
        act2.parent = gm
        eng.game_map = gm

        ft.die()

        self.assertEqual(ft.parent.char, "%")
        self.assertEqual(ft.parent.color, (191, 0, 0))
        self.assertFalse(ft.parent.blocks_movement)
        self.assertIsNone(ft.parent.ai)
        self.assertEqual(ft.parent.name, "remains of actor")
        self.assertEqual(ft.parent.render_order, RenderOrder.CORPSE)
        mock_add_message.assert_any_call("actor is dead!", color.enemy_die)
        # verify xp is given to the player
        self.assertEqual(act2.level.current_xp, 150)

    def test_heal_max_hp(self):
        '''
        test that healing any amount while at max hp will heal 0
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        amount_recovered = ft.heal(10)
        self.assertEqual(amount_recovered, 0)

    def test_heal_up_to_max(self):
        '''
        test that healing more than necessary will cap at max hp
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        ft.hp = 5
        amount_recovered = ft.heal(10)
        self.assertEqual(amount_recovered, 5)
        self.assertEqual(ft.hp, ft.max_hp)

    def test_heal_some(self):
        '''
        test that healing some will increase the hp
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        ft.hp = 5
        amount_recovered = ft.heal(3)
        self.assertEqual(amount_recovered, 3)
        self.assertEqual(ft.hp, 8)

    def test_take_damage(self):
        '''
        test that taking damage will reduce the hp
        '''
        ft = Fighter(hp=10, base_defense=10, base_power=10)
        ft.take_damage(2)
        self.assertEqual(ft.hp, 8)
