import unittest
from unittest.mock import Mock

import render_functions

class Test_Render_Functions(unittest.TestCase):
    def test_render_bar_value_greaterthan_0(self):
        '''
        verify that the hp bar is rendered with 2 rectangles
        when the value is greater than 0
        TODO: figure out how to mock the draw_rect calls in here
        '''
        console = Mock()
        render_functions.render_bar(
            console=console, current_value=0, maximum_value=10, total_width=10
        )
        