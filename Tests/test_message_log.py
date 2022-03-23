from cgitb import text
import unittest
from unittest.mock import patch

from message_log import Message, MessageLog
from tcod import Console


class Test_Message(unittest.TestCase):
    def test_init(self):
        '''
        test that a message can be initialized properly
        '''
        text = 'Hello'
        fg = [100, 101, 102]
        ms = Message(text=text, fg=fg)
        self.assertEqual(ms.plain_text, text)
        self.assertEqual(ms.fg, fg)
        self.assertEqual(ms.count, 1)

    def test_property_full_text_count_equals_one(self):
        '''
        test that the full_text property returns the plain_text
        when the count=1
        '''
        text = 'Hello'
        ms = Message(text=text, fg=[0, 0, 0])
        self.assertEqual(ms.count, 1)
        self.assertEqual(ms.full_text, ms.plain_text)

    def test_property_full_text_count_greaterthan_one(self):
        '''
        test that the full_text property returns a new string
        with the new count when the count is creater than one
        '''
        text = 'Hello'
        ms = Message(text=text, fg=[0, 0, 0])
        ms.count = 5
        expected_text = "Hello (x5)"
        self.assertEqual(ms.count, 5)
        self.assertNotEqual(ms.full_text, ms.plain_text)
        self.assertEqual(ms.full_text, expected_text)


class Test_MessageLog(unittest.TestCase):
    def test_init(self):
        '''
        test that a new MessageLog will start with an empty list
        '''
        ml = MessageLog()
        self.assertEqual(ml.messages, [])

    def test_add_message_stack_False(self):
        '''
        test that adding a message to the MessageLog with stack=False
        will append it to the end of the messages
        '''
        ml = MessageLog()
        text = 'Hello'
        ml.add_message(text=text, stack=False)
        # add the message a second time
        ml.add_message(text=text, stack=False)
        self.assertEqual(len(ml.messages), 2)  # 2 messages
        # both have matching text
        self.assertEqual(ml.messages[0].full_text, text)
        self.assertEqual(ml.messages[1].full_text, text)

    def test_add_message_stack_True(self):
        '''
        test that adding a message to the MessageLog with stack=True
        will stack the message into the same one
        '''
        ml = MessageLog()
        text = 'Hello'
        expected_text = "Hello (x2)"
        ml.add_message(text=text, stack=True)
        # add the message a second time
        ml.add_message(text=text, stack=True)
        self.assertEqual(len(ml.messages), 1)  # 2 messages
        self.assertEqual(ml.messages[0].full_text, expected_text)

    def test_add_message_stack_True_different_text(self):
        '''
        test that adding a message to the MessageLog with stack=True
        but the text is different will append it to the end of the messages
        '''
        ml = MessageLog()
        text = 'Hello'
        text_2 = 'World'
        ml.add_message(text=text, stack=True)
        # add the message a second time
        ml.add_message(text=text_2, stack=True)
        self.assertEqual(len(ml.messages), 2)  # 2 messages
        # both have matching text
        self.assertEqual(ml.messages[0].full_text, text)
        self.assertEqual(ml.messages[1].full_text, text_2)

    def test_add_message_right_order(self):
        '''
        test that adding a message to the MessageLog with stack=False
        will append them in the correct order
        '''
        ml = MessageLog()
        text = 'Hello'
        text_2 = 'World'
        ml.add_message(text=text, stack=False)
        # add the message a second time
        ml.add_message(text=text_2, stack=False)
        self.assertEqual(len(ml.messages), 2)  # 2 messages
        # both have matching text
        self.assertEqual(ml.messages[0].full_text, text)
        self.assertEqual(ml.messages[1].full_text, text_2)

    def test_render(self):
        '''
        test that calling render will call render_messages
        '''
        ml = MessageLog()
        console = Console(width=10, height=10, order='F')
        with patch('message_log.MessageLog.render_messages') as patch_render_messages:
            ml.render(
                console=console,
                x=10,
                y=10,
                width=10,
                height=10,
            )

        patch_render_messages.assert_called()

    def test_render_messages(self):
        '''
        test that console.print will be called to render the messages
        we could probably figure out a way to test that the text wrap works
        as expected and that the messages go in reverse and that only the right
        number of messages make it onto the screen...but I don't want to deal
        with replacing the console.print with some sort of standard output that
        I can check easily
        '''
        ml = MessageLog()
        ml.add_message(text='Hello')
        console = Console(width=10, height=10, order='F')
        with patch('tcod.console.Console.print') as patch_print:
            ml.render_messages(
                console=console,
                x=10,
                y=10,
                width=10,
                height=10,
                messages=ml.messages,
            )
        patch_print.assert_called()
