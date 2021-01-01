from javadoctohtml import DocumentationItem
from pathlib import Path
from typing import List


class HTMLCreator:
    @staticmethod
    def create_html_file(output_folder: Path, file: str,
                         documentation: List[DocumentationItem]) -> None:
        file_name = file[:-5]
        with (output_folder / f'{file_name}.html') \
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
