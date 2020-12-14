from pathlib import Path
import os
import sys
import unittest
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from javadoctohtml import Transmitter # noqa


class DocumentationTest(unittest.TestCase):
    def test_documentation(self) -> None:
        Transmitter({'directory': Path.cwd(),
                     'files': ['samples/TelegramBot.java'],
                     'target': Path.cwd()}).run()
        self.assertTrue((Path.cwd() / 'output' / 'samples' /
                         'TelegramBot.html').exists())


if __name__ == '__main__':
    unittest.main()
