#!usr/bin/env python3
from argparse import ArgumentParser
from javadoctohtml import Transmitter
import os


def parse_args():
    parser = ArgumentParser(description='JavaDoc2HTMLTransmission')
    parser.add_argument("-directory", metavar='d', default=os.getcwd(),
                        help='Working directory')
    parser.add_argument("-target", default=os.getcwd(), metavar='t',
                        help='Place where HTML documentation will be stored')
    parser.add_argument("files", nargs="+", help='Java files')
    return parser.parse_args()


if __name__ == '__main__':
    Transmitter().run(parse_args())
