from javadoctohtml import DocumentationItem, HTMLCreator
from pathlib import Path
from typing import Any, Dict, List
import logging
import os


class Transmitter:
    def __init__(self, arguments: Dict[str, Any]) -> None:
        self.files = arguments['files']
        self.directory = Path(arguments['directory'])
        self.target = Path(arguments['target'])

    def run(self) -> None:
        for file in self.files:
            file_extension = file[-5:]
            full_route = self.directory / file
            if not full_route.exists():
                logging.info(f'{full_route} '
                             f'was ignored because it does not exist')
                continue
            if file_extension != ".java":
                logging.info(f'{full_route} '
                             f'was ignored because it is not a java file')
                continue
            documentation = self.get_documentation(full_route)
            self.create_output(file, documentation)

    @staticmethod
    def get_documentation(full_route: Path) -> List[DocumentationItem]:
        with full_route.open(encoding='utf-8') as source:
            content = source.read()
        documentation_pieces = content.split('/**')
        documentation = {}
        for doc_piece in documentation_pieces[1:]:
            item = doc_piece[doc_piece.find('*/') + 2:].split('\n')
            current_line = item[0]
            index = 0
            while current_line == '':
                index += 1
                current_line = item[index]
            documentation[current_line.strip()] =\
                doc_piece[:doc_piece.find('*/')]
        doc_items = []
        for key in documentation.keys():
            doc_items.append(DocumentationItem(key, documentation[key]))
        return doc_items

    def create_output(self, file: str,
                      documentation: List[DocumentationItem]) -> None:
        output_folder = self.target / 'output'
        full_route = output_folder / file
        for parent in reversed(full_route.parents):
            if not parent.exists():
                os.mkdir(parent)
        HTMLCreator.create_html_file(output_folder, file, documentation)
        logging.info(f'{file} documentation was transformed into HTML')
