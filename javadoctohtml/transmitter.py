from javadoctohtml import DocumentationItem
from pathlib import Path
from typing import Any, Dict, List
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
                print(f'{full_route} was ignored because it does not exist')
                continue
            if file_extension != ".java":
                print(f'{full_route} '
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
        if not output_folder.exists():
            os.mkdir(output_folder)
        levels = file.split('/')
        for index in range(1, len(levels)):
            current_level = f'{output_folder}/{"/".join(levels[:index])}'
            if not os.path.exists(current_level):
                os.mkdir(current_level)
        self.create_html_file(output_folder, file, documentation)

    @staticmethod
    def create_html_file(output_folder: Path, file: str,
                         documentation: List[DocumentationItem]) -> None:
        file_name = file[:-5]
        with (output_folder / f'{file_name}.html')\
                .open('w', encoding='utf-8') as html_page:
            html_page.write('<!DOCTYPE html>\n'
                            '<html lang="en">\n'
                            '   <head>\n'
                            '       <meta charset="utf-8"/>\n')
            html_page.write(f'       <title>{file_name}</title>\n')
            html_page.write('   </head>\n'
                            '   <body>\n')
            for item in documentation:
                if item.type == 'class' or item.type == 'interface':
                    html_page.write(f'       <h1>{item.type.capitalize()} '
                                    f'{item.name}</h1>\n')
                    html_page.write(f'          <b>Author:</b> '
                                    f'{item.author}\n')
                    html_page.write(f'          <b>Version:</b> '
                                    f'{item.version}\n')
                else:
                    html_page.write(f'       <h2>{item.type.capitalize()} '
                                    f'{item.name}</h2>\n')
                    if item.type == 'method':
                        if len(item.params) > 0:
                            html_page.write('           <b>Parameters:</b>'
                                            '\n')
                            for param in item.params.keys():
                                html_page.write(f'              <b>{param}:'
                                                f'</b> {item.params[param]}'
                                                f'\n')
                        if len(item.exceptions) > 0:
                            html_page.write('           <b>Exceptions:</b>'
                                            '\n')
                            for exc in item.exceptions.keys():
                                html_page.write(f'              <b>{exc}:'
                                                f'</b> {item.exceptions[exc]}'
                                                f'\n')
                        if item.returning is not None:
                            html_page.write(f'          <b>Returns:</b>'
                                            f'{item.returning}\n')
            html_page.write('   </body>\n'
                            '</html>')
