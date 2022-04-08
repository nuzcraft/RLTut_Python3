import unittest

from equipment_types import EquipmentType
from entity import Item
from components.consumable import Consumable
import components.equippable as equippable


class TestEquippable(unittest.TestCase):
    def test_init(self):
        '''
        test that initializing the equippalbe component works as expected
        '''
        item = Item(
            consumable=Consumable()
        )
        eq = equippable.Equippable(
            EquipmentType.ARMOR,
            power_bonus=5,
            defense_bonus=6
        )
        eq.parent = item

        self.assertEqual(eq.equipment_type, EquipmentType.ARMOR)
        self.assertEqual(eq.power_bonus, 5)
        self.assertEqual(eq.defense_bonus, 6)
        self.assertEqual(eq.parent, item)


class TestDagger(unittest.TestCase):
    def test_init(self):
        '''
        test that the dagger is initialized with the correct inputs
        '''
        dagger = equippable.Dagger()
        self.assertEqual(dagger.equipment_type, EquipmentType.WEAPON)
        self.assertEqual(dagger.power_bonus, 2)


class TestSword(unittest.TestCase):
    def test_init(self):
        '''
        test that the sword is initialized with the correct inputs
        '''
        sword = equippable.Sword()
        self.assertEqual(sword.equipment_type, EquipmentType.WEAPON)
        self.assertEqual(sword.power_bonus, 4)


class TestLeatherArmor(unittest.TestCase):
    def test_init(self):
        '''
        test that the leather armor is initialized with the correct inputs
        '''
        leather_armor = equippable.LeatherArmor()
        self.assertEqual(leather_armor.equipment_type, EquipmentType.ARMOR)
        self.assertEqual(leather_armor.defense_bonus, 1)


class TestChainMail(unittest.TestCase):
    def test_init(self):
        '''
        test that the chainmail is initialized with the correct inputs
        '''
        chainmail = equippable.ChainMail()
        self.assertEqual(chainmail.equipment_type, EquipmentType.ARMOR)
        self.assertEqual(chainmail.defense_bonus, 3)
