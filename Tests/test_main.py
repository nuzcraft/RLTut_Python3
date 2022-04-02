import unittest
from unittest.mock import Base, patch

import main
from input_handlers import (
    BaseEventHandler,
    EventHandler,
)
from engine import Engine
from entity import Entity

class TestMain(unittest.TestCase):
    def test_save_game_EventHandler(self):
        '''
        test that a game will be saved if
        the handler is an event handler
        '''
        eng = Engine(player=Entity())
        eh = EventHandler(engine=eng)
        with patch('engine.Engine.save_as') as patch_save_as:
            main.save_game(handler=eh, filename='save')

        patch_save_as.assert_called_once()

    def test_save_game_BaseEventHandler(self):
        '''
        test that a game will not be saved if
        the handler is a base event handler
        '''
        eh = BaseEventHandler()
        with patch('engine.Engine.save_as') as patch_save_as:
            main.save_game(handler=eh, filename='save')

        patch_save_as.assert_not_called()