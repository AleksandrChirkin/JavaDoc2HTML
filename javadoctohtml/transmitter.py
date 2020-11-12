from argparse import Namespace
from javadoctohtml import DocumentationItem
from pathlib import Path
from typing import List
import os


class Transmitter:
    def run(self, arguments: Namespace) -> None:
        for file in arguments.files:
            full_route = '{0}/{1}'.format(arguments.directory, file)
            if not os.path.exists(full_route):
                print('{} was ignored because it does not exist'
                      .format(full_route))
                continue
            if file[-5:] != ".java":
                print('{} was ignored because it is not a java file'
                      .format(full_route))
                continue
            documentation = self.get_documentation(full_route)
            self.create_output(file, arguments, documentation)

    @staticmethod
    def get_documentation(full_route: str) -> List[DocumentationItem]:
        with open(Path(full_route), encoding='utf-8') as source:
            content = ''.join(source.readlines())
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

    def create_output(self, file: str, arguments: Namespace,
                      documentation: List[DocumentationItem]) -> None:
        output_folder = '{}/output'.format(arguments.target)
        if not os.path.exists(output_folder):
            os.mkdir(output_folder)
        levels = file.split('/')
        for index in range(1, len(levels)):
            current_level = '{}/{}'.format(output_folder,
                                           '/'.join(levels[:index]))
            if not os.path.exists(current_level):
                os.mkdir(current_level)
        self.create_html_file(output_folder, file, documentation)

    @staticmethod
    def create_html_file(output_folder: str, file: str,
                         documentation: List[DocumentationItem]) -> None:
        with open(Path('{}/{}.html').format(output_folder,
                                            file[:-5]), 'w',
                  encoding='utf-8') as html_page:
            html_page.write('<!DOCTYPE html>\n'
                            '<html lang="en">\n'
                            '   <head>\n'
                            '       <meta charset="utf-8"/>\n')
            html_page.write('       <title>{}</title>\n'.format(file[:-5]))
            html_page.write('   </head>\n'
                            '   <body>\n')
            for item in documentation:
                if item.type == 'class' or item.type == 'interface':
                    html_page.write('       <h1>{} {}</h1>\n'
                                    .format(item.type.capitalize(),
                                            item.name))
                    html_page.write('       <b>Author:</b> {}\n'
                                    .format(item.author))
                    html_page.write('       <b>Version:</b> {}\n'
                                    .format(item.version))
                else:
                    html_page.write('       <h2>{} {}</h2>\n'
                                    .format(item.type.capitalize(),
                                            item.name))
                    if item.type == 'method':
                        if len(item.params) > 0:
                            html_page.write('       <b>Parameters:</b>\n')
                            for param in item.params.keys():
                                html_page.write('           <b>{}:</b> {}\n'
                                                .format(param,
                                                        item.params[param]))
                        if len(item.exceptions) > 0:
                            html_page.write('       <b>Exceptions:</b>\n')
                            for exc in item.exceptions.keys():
                                html_page.write('           <b>{}:</b> {}\n'
                                                .format(exc,
                                                        item.exceptions[exc]))
                        if item.returning is not None:
                            html_page.write('       <b>Returns:</b>{}\n'
                                            .format(item.returning))
            html_page.write('   </body>\n'
                            '</html>')
