from turtle import width
import unittest
from unittest.mock import patch

import render_functions
import tcod
import color
from game_map import GameMap
from engine import Engine
from entity import Entity


class Test_Render_Functions(unittest.TestCase):
    def test_get_names_at_location_out_of_bounds(self):
        '''
        test that get_names_at_location will return a blank string
        when searching out of bounds
        '''
        ent = Entity()
        ent1 = Entity(x=12, y=13, name="entity1")
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.visible[:] = True
        gm.entities = {ent1}
        names = render_functions.get_names_at_location(12, 13, gm)
        self.assertEqual(names, "")

    def test_get_names_at_location_not_visible(self):
        '''
        test that get_names_at_location will return a blank string
        when searching in bounds, but the tiles are not visible
        '''
        ent = Entity()
        ent1 = Entity(x=5, y=6, name="entity1")
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        # gm.visible[:] = True
        gm.entities = {ent1}
        names = render_functions.get_names_at_location(5, 6, gm)
        self.assertEqual(names, "")

    def test_get_names_at_location_multiple_entities(self):
        '''
        test that get_names_at_location will return the names of
        all entities at that location, comma delimited
        '''
        ent = Entity()
        ent1 = Entity(x=5, y=6, name="entity1")
        ent2 = Entity(x=5, y=6, name="entity2")
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        gm.visible[:] = True
        gm.entities = {ent1, ent2}
        names = render_functions.get_names_at_location(5, 6, gm)
        # notice that the first letter is capitalized
        self.assertEqual(names, "Entity1, entity2")

    def test_render_bar_value_0(self):
        '''
        verify that the hp bar is rendered with 2 rectangles
        when the value is greater than 0
        '''
        console = tcod.Console(width=10, height=10)

        with patch('tcod.Console.draw_rect') as patches:
            with patch('tcod.Console.print') as patch_print:
                render_functions.render_bar(
                    console=console, current_value=0, maximum_value=10, total_width=10
                )

        patches.assert_called_once_with(
            x=0, y=45, width=10, height=1, ch=1, bg=color.bar_empty)

        patch_print.assert_called_once()

    def test_render_bar_value_greater_than_0(self):
        '''
        verify that the hp bar is rendered with 2 rectangles
        when the value is greater than 0
        '''
        console = tcod.Console(width=10, height=10)

        with patch('tcod.Console.draw_rect') as patch_draw_rect:
            with patch('tcod.Console.print') as patch_print:

                render_functions.render_bar(
                    console=console, current_value=5, maximum_value=10, total_width=10
                )

        patch_draw_rect.assert_any_call(
            x=0, y=45, width=5, height=1, ch=1, bg=color.bar_filled)

        patch_draw_rect.assert_any_call(
            x=0, y=45, width=10, height=1, ch=1, bg=color.bar_empty)

        patch_print.assert_called_once()

    @patch("tcod.console.Console.print")
    def test_render_names_at_mouse_location(self, patch_print):
        '''
        tests that the function will render names returned by
        get_names_at_location. The called function has already been tested,
        so we'll just check that the functions were called okay
        '''
        console = tcod.Console(width=10, height=10)
        ent = Entity()
        eng = Engine(player=ent)
        gm = GameMap(engine=eng, width=10, height=10)
        eng.game_map = gm

        with patch('render_functions.get_names_at_location') as patch_get_names:
            patch_get_names.return_value = "entity1"

            render_functions.render_names_at_mouse_location(
                console=console, x=5, y=5, engine=eng)

        patch_get_names.assert_called()

        patch_print.assert_any_call(
            x=5, y=5, string="entity1"
        )
