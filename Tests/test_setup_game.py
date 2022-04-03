import unittest
from unittest.mock import patch

import tcod
from input_handlers import MainGameEventHandler

import setup_game
from engine import Engine
from game_map import GameMap
from entity import Actor


class TestSetupGame(unittest.TestCase):
    def test_new_game(self):
        '''
        test that new_game will return an engine that has
        a player and a game map
        '''
        eng = setup_game.new_game()
        self.assertIsInstance(eng, Engine)
        self.assertIsInstance(eng.game_map, GameMap)
        self.assertIsInstance(eng.player, Actor)


class TestMainMenu(unittest.TestCase):
    def test_on_render(self):
        '''
        test that the main menu:
        draws the background, prints some text
        '''
        mm = setup_game.MainMenu()
        console = tcod.console.Console(width=10, height=10, order='F')

        with patch('tcod.console.Console.draw_semigraphics') as patch_draw_semigraphics:
            with patch('tcod.console.Console.print') as patch_print:
                mm.on_render(console=console)

        patch_draw_semigraphics.assert_called_once()
        patch_print.assert_called()

    def test_ev_keydown_q(self):
        '''
        test that pressing q will raises a system exit
        '''
        mm = setup_game.MainMenu()
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.Q,
            sym=tcod.event.K_q,
            mod=tcod.event.Modifier.NONE
        )
        with self.assertRaises(SystemExit):
            mm.ev_keydown(event=event)

    def test_ev_keydown_escape(self):
        '''
        test that pressing escape will raises a system exit
        '''
        mm = setup_game.MainMenu()
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.ESCAPE,
            sym=tcod.event.K_ESCAPE,
            mod=tcod.event.Modifier.NONE
        )
        with self.assertRaises(SystemExit):
            mm.ev_keydown(event=event)

    def test_ev_keydown_n(self):
        '''
        test that pressing n will return a main game event handler
        '''
        mm = setup_game.MainMenu()
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.N,
            sym=tcod.event.K_n,
            mod=tcod.event.Modifier.NONE
        )
        ret = mm.ev_keydown(event=event)
        self.assertIsInstance(ret, MainGameEventHandler)

    # def test_ev_keydown_c(self):
    #     '''
    #     test that pressing c will return None since we've not
    #     implemented saving and continuing yet
    #     '''
    #     mm = setup_game.MainMenu()
    #     event = tcod.event.KeyDown(
    #         scancode=tcod.event.Scancode.C,
    #         sym=tcod.event.K_c,
    #         mod=tcod.event.Modifier.NONE
    #     )
    #     ret = mm.ev_keydown(event=event)
    #     self.assertIsNone(ret)

    def test_ev_keydown_other(self):
        '''
        test that pressing a non-assigned key will return None
        '''
        mm = setup_game.MainMenu()
        event = tcod.event.KeyDown(
            scancode=tcod.event.Scancode.G,
            sym=tcod.event.K_g,
            mod=tcod.event.Modifier.NONE
        )
        ret = mm.ev_keydown(event=event)
        self.assertIsNone(ret)
