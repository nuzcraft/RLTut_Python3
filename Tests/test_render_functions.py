import unittest
from unittest.mock import Mock, patch

import render_functions
import tcod
import color


class Test_Render_Functions(unittest.TestCase):
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
