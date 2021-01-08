from argparse import ArgumentParser, Namespace
from typing import List
import logging
import os
import re
import sys
logging.basicConfig(format=u'%(message)s', level=logging.INFO,
                    stream=sys.stdout)
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from javadoctohtml import JavaFileParser, JavaFile, ConvertHtml, FileManager,\
    errors  # noqa


def parse_args() -> Namespace:
    parser = ArgumentParser(prog="javadoc2html")
    parser.add_argument("project", nargs='+', type=str,
                        help="Input dir with java files or java files.")
    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    java_files: List[JavaFile] = []
    j_parser = JavaFileParser()
    convert = ConvertHtml()
    manager = FileManager()
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        for file in manager.open(args.project):
            j_file = j_parser.parser(manager.read(file))
            j_file.name = re.split(r'[\\/]', file)[-1]
            java_files.append(j_file)
        if len(java_files):
            manager.mkdir()
            for file in java_files:
                manager.write(
                    file.name.replace('.java', '.html'),
                    convert.convert(file)
                )
        else:
            logging.warning('Java files not found')
    except errors.JDException as exc:
        logging.error(exc.message)
        exit(1)
