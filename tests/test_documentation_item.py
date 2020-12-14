from pathlib import Path
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from javadoctohtml import Transmitter # noqa


class MyTestCase(unittest.TestCase):
    def test_doc_item_for_extended_class(self):
        items = Transmitter.get_documentation(Path.cwd() / 'samples' /
                                              'TelegramBot.java')
        self.assertEqual(items[0].type, 'class')
        self.assertEqual(items[0].name, 'TelegramBot')
        self.assertEqual(items[1].type, 'field')
        self.assertEqual(items[1].name, 'bot')
        for item in items[2:]:
            self.assertEqual(item.type, 'method')

    def test_doc_item_for_unextended_class(self):
        items = Transmitter.get_documentation(Path.cwd() / 'samples' /
                                              'Bot.java')
        self.assertEqual(items[0].type, 'class')
        self.assertEqual(items[0].name, 'Bot')
        for item in items[1:4]:
            self.assertEqual(item.type, 'field')
        for item in items[4:]:
            self.assertEqual(item.type, 'method')


if __name__ == '__main__':
    unittest.main()
