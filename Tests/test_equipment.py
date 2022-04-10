import unittest
from unittest.mock import patch

from components.ai import BaseAI
from components.equipment import Equipment
from components.equippable import Equippable
from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from engine import Engine
from entity import Actor, Item
from equipment_types import EquipmentType
from game_map import GameMap


class TestEquipment(unittest.TestCase):
    def test_init(self):
        '''
        test that equipment can be initialized without issues
        '''
        wp = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, power_bonus=2))
        ar = Item(equippable=Equippable(
            equipment_type=EquipmentType.ARMOR, defense_bonus=3))
        eq = Equipment(weapon=wp, armor=ar)
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eq.parent = actor
        self.assertEqual(eq.weapon, wp)
        self.assertEqual(eq.armor, ar)
        self.assertEqual(eq.parent, actor)

    def test_property_defense_bonus_only_armor(self):
        '''
        test that the defense bonus will come through without issues
        if only armor has a defense stat
        '''
        wp = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, power_bonus=2))
        ar = Item(equippable=Equippable(
            equipment_type=EquipmentType.ARMOR, defense_bonus=3))
        eq = Equipment(weapon=wp, armor=ar)
        self.assertEqual(eq.defense_bonus, 3)

    def test_property_defense_bonus_both(self):
        '''
        test that the defense bonus will come through without issues
        when both weapon and armor boost defense
        '''
        wp = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, defense_bonus=2))
        ar = Item(equippable=Equippable(
            equipment_type=EquipmentType.ARMOR, defense_bonus=3))
        eq = Equipment(weapon=wp, armor=ar)
        self.assertEqual(eq.defense_bonus, 5)

    def test_property_defense_bonus_no_boost(self):
        '''
        test that the defense bonus will come through without issues
        when weapon and armor aren't equippable or don't boost
        '''
        wp = Item()
        ar = Item(equippable=Equippable(
            equipment_type=EquipmentType.ARMOR, power_bonus=3))
        eq = Equipment(weapon=wp, armor=ar)
        self.assertEqual(eq.defense_bonus, 0)

    def test_property_power_bonus_only_weapon(self):
        '''
        test that the defense bonus will come through without issues
        if only weapon has a power stat
        '''
        wp = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, power_bonus=2))
        ar = Item(equippable=Equippable(
            equipment_type=EquipmentType.ARMOR, defense_bonus=3))
        eq = Equipment(weapon=wp, armor=ar)
        self.assertEqual(eq.power_bonus, 2)

    def test_property_power_bonus_both(self):
        '''
        test that the defense bonus will come through without issues
        when both weapon and armor boost defense
        '''
        wp = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, power_bonus=2))
        ar = Item(equippable=Equippable(
            equipment_type=EquipmentType.ARMOR, power_bonus=3))
        eq = Equipment(weapon=wp, armor=ar)
        self.assertEqual(eq.power_bonus, 5)

    def test_property_power_bonus_no_boost(self):
        '''
        test that the defense bonus will come through without issues
        when weapon and armor aren't equippable or don't boost
        '''
        ar = Item()
        wp = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, defense_bonus=3))
        eq = Equipment(weapon=wp, armor=ar)
        self.assertEqual(eq.power_bonus, 0)

    def test_item_is_equipped_weapon_only(self):
        '''
        test that the function will return true when only a weapon is equipped
        '''
        wp = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, power_bonus=2))
        eq = Equipment(weapon=wp)
        self.assertTrue(eq.item_is_equipped(item=wp))

    def test_item_is_equipped_armor_only(self):
        '''
        test that the function will return true when only armor is equipped
        '''
        wp = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, power_bonus=2))
        eq = Equipment(armor=wp)
        self.assertTrue(eq.item_is_equipped(item=wp))

    def test_item_is_equipped_both(self):
        '''
        test that the function will return true when the same item is both weapon and armor
        '''
        wp = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, power_bonus=2))
        eq = Equipment(weapon=wp, armor=wp)
        self.assertTrue(eq.item_is_equipped(item=wp))

    def test_item_is_equipped_not_equipped(self):
        '''
        test that the function will return false a different item is equipped
        '''
        wp = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, power_bonus=2))
        wp2 = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, power_bonus=2))
        eq = Equipment(weapon=wp)
        self.assertFalse(eq.item_is_equipped(item=wp2))

    def test_item_is_equipped_none_equipped(self):
        '''
        test that the function will return false when no items are equipped
        '''
        wp = Item(equippable=Equippable(
            equipment_type=EquipmentType.WEAPON, power_bonus=2))
        eq = Equipment()
        self.assertFalse(eq.item_is_equipped(item=wp))

    def test_unequip_message(self):
        '''
        test that the unequip message is formatted as expected
        '''
        eq = Equipment()
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        actor.parent = gm
        eq.parent = actor
        with patch('message_log.MessageLog.add_message') as patch_add_message:
            eq.unequip_message(item_name="coffee mug")
        patch_add_message.assert_called_once_with("You remove the coffee mug.")

    def test_equip_message(self):
        '''
        test that the equip message is formatted as expected
        '''
        eq = Equipment()
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        actor.parent = gm
        eq.parent = actor
        with patch('message_log.MessageLog.add_message') as patch_add_message:
            eq.equip_message(item_name="coffee mug")
        patch_add_message.assert_called_once_with("You equip the coffee mug.")

    def test_equip_to_slot_with_current_item(self):
        '''
        test that equipping a new item will remove the old one
        '''
        item = Item()
        item2 = Item()
        eq = Equipment(weapon=item)
        eq.equip_to_slot("weapon", item2, False)
        self.assertEqual(eq.weapon, item2)

    def test_equip_to_slot_no_current_item(self):
        '''
        test that equipping a new item will not try to remove
        an old one if it does not exist
        '''
        item = Item()
        eq = Equipment()
        eq.equip_to_slot("weapon", item, False)
        self.assertEqual(eq.weapon, item)

    def test_equip_to_slot_with_message(self):
        '''
        test that equipping a new item with add_message set to true
        will send an equip message
        '''
        item = Item(name="item")
        eq = Equipment()
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        actor.parent = gm
        eq.parent = actor
        with patch("components.equipment.Equipment.equip_message") as patch_equip_message:
            eq.equip_to_slot(slot="weapon", item=item, add_message=True)

        self.assertEqual(eq.weapon, item)
        patch_equip_message.assert_called_once()

    def test_unequip_from_slot_with_current_item(self):
        '''
        test that unequipping will remove the old item
        '''
        item = Item()
        eq = Equipment(weapon=item)
        eq.unequip_from_slot("weapon", False)
        self.assertIsNone(eq.weapon)

    def test_unequip_from_slot_with_message(self):
        '''
        test that unequipping an item with add_message set to true
        will send an unequip message
        '''
        item = Item(name="item")
        eq = Equipment(weapon=item)
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        actor.parent = gm
        eq.parent = actor
        with patch("components.equipment.Equipment.unequip_message") as patch_equip_message:
            eq.unequip_from_slot(slot="weapon", add_message=True)

        self.assertIsNone(eq.weapon)
        patch_equip_message.assert_called_once()

    def test_toggle_equip_weapon_equip(self):
        '''
        test that the toggle_equip function can equip a weapon
        '''
        item = Item(equippable=Equippable(equipment_type=EquipmentType.WEAPON))
        eq = Equipment()
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        actor.parent = gm
        eq.parent = actor
        eq.toggle_equip(equippable_item=item, add_message=False)
        self.assertEqual(eq.weapon, item)

    def test_toggle_equip_armor_equip(self):
        '''
        test that the toggle_equip function can equip armor
        '''
        item = Item(equippable=Equippable(equipment_type=EquipmentType.ARMOR))
        eq = Equipment()
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        actor.parent = gm
        eq.parent = actor
        eq.toggle_equip(equippable_item=item, add_message=False)
        self.assertEqual(eq.armor, item)

    def test_toggle_equip_weapon_unequip(self):
        '''
        test that the toggle_equip function can unequip a weapon
        '''
        item = Item(equippable=Equippable(equipment_type=EquipmentType.WEAPON))
        eq = Equipment(weapon=item)
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        actor.parent = gm
        eq.parent = actor
        eq.toggle_equip(equippable_item=item, add_message=False)
        self.assertIsNone(eq.weapon)

    def test_toggle_equip_armor_unequip(self):
        '''
        test that the toggle_equip function can unequip armor
        '''
        item = Item(equippable=Equippable(equipment_type=EquipmentType.ARMOR))
        eq = Equipment(armor=item)
        actor = Actor(
            ai_cls=BaseAI,
            fighter=Fighter(hp=10, defense=10, power=10),
            inventory=Inventory(capacity=5),
            level=Level()
        )
        eng = Engine(player=actor)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm
        actor.parent = gm
        eq.parent = actor
        eq.toggle_equip(equippable_item=item, add_message=False)
        self.assertIsNone(eq.armor)
