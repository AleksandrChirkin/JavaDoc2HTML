from argparse import Namespace
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from javadoctohtml import Transmitter # noqa


class DocumentationTest(unittest.TestCase):
    def test_documentation(self) -> None:
        Transmitter().run(Namespace(directory=os.getcwd(),
                                    files=['samples/TelegramBot.java'],
                                    target=os.getcwd()))
        self.assertTrue(os.path.exists('{}/output/samples/TelegramBot.html'
                                       .format(os.getcwd())))


if __name__ == '__main__':
    unittest.main()
