from argparse import ArgumentParser
from pathlib import Path
from typing import Any, Dict
import logging
import os
import sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from javadoctohtml import Transmitter  # noqa
logging.basicConfig(format=u'%(message)s', level=logging.INFO,
                    stream=sys.stdout)


def parse_args() -> Dict[str, Any]:
    parser = ArgumentParser(description='JavaDoc2HTMLTransmission')
    parser.add_argument("-directory", metavar='d', default=Path.cwd(),
                        help='Working directory')
    parser.add_argument("-target", default=Path.cwd(), metavar='t',
                        help='Place where HTML documentation will be stored')
    parser.add_argument("files", nargs="+", help='Java files')
    return parser.parse_args().__dict__


if __name__ == '__main__':
    Transmitter(parse_args()).run()
