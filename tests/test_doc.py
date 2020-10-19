from argparse import Namespace
from domain import Transmitter
import os
import unittest


class DocumentationTest(unittest.TestCase):
    def test_documentation(self):
        Transmitter().run(Namespace(directory=os.getcwd(),
                                    files=['samples/TelegramBot.java'],
                                    target=os.getcwd()))
        self.assertTrue(os.path.exists('{}/output/samples/TelegramBot.html'
                                       .format(os.getcwd())))


if __name__ == '__main__':
    unittest.main()
