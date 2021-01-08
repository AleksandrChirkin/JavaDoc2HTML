import re
from typing import List, Optional

from javadoctohtml import JavaField, \
    JavaComment, JavaMethod, JavaFile, JavaTemplate


def converter(func):
    def wrapper(*args, **kwargs):
        return '\n'.join([
            '<html>',
            '<head>',
            '<meta http-equiv="Content-Type" '
            'content="text/html; charset=utf-8">',
            f'<title>{args[-1].name}</title>',
            '</head>',
            '<body>',
            func(*args, **kwargs),
            '</body>'
        ])
    return wrapper


class ConvertHtml:
    @converter
    def convert(self,
                file: JavaFile) -> Optional[str]:
        buffer = [
            f'<h1 align="center" '
            f'style="color:Black">Documentation : {file.name}</h1>',
            '<br>']
        if len(file.comments):
            buffer.append(
                f'<p  style="font-size: 20px">'
                f'{self.get_comment(file.comments[0])}</p>')
        if len(file.packages):
            buffer.append(f'<p  style="font-size: 23px">'
                          f'Package: {file.packages[0]}</p>')
        if len(file.imports):
            buffer.append(self.add_imports(file.imports))
        if len(file.java_templates):
            for template in file.java_templates:
                buffer.append(self.add_template(template))
        return '<br>\n'.join(buffer)

    def add_template(self, template: JavaTemplate) -> Optional[str]:
        buffer = [
            f'<h2>{template.template} {template.name}</h2>'
            '<ul>',
            f'<li>Modifier: {template.mod}</li>',
            f'<li>Interface: '
            f'{template.interface if template.interface else "-"}</li>',
            f'<li>Parent: '
            f'{template.parent if template.parent else "-"}</li>',
            '</ul>'
        ]
        if len(template.fields):
            buffer.append(
                self.add_table_fields(
                    template.fields,
                    template.template)
            )
        if len(template.methods):
            buffer.append(
                self.add_table_methods(
                    template.methods,
                    template.template)
            )
        return '\n'.join(buffer)

    @staticmethod
    def add_imports(imports: List[str]) -> Optional[str]:
        return '\n'.join([
            '<h3>Imported modules and packages:</h3>',
            '<ul>',
            *[f'<li>{line}</li>' for line in imports],
            '</ul>'
        ])

    @staticmethod
    def add_table_fields(
            fields: List[JavaField],
            template: str) -> Optional[str]:
        buffer: List[str] = [
            '<table border="3" width="100%" cellpadding="5">',
            f'<caption><h3>{template} contains fields:</h3></caption>',
            '<tr><th>Field name</th><th>Modifier</th><th>Type</th></tr>'
        ]
        for field in fields:
            buffer.append(f'<tr><td>{field.name}</td>'
                          f'<td>{field.mod}</td>'
                          f'<td>{field.value_type}</td></tr>')
        buffer.append('</table>')
        return '\n'.join(buffer)

    def add_table_methods(self,
                          methods: List[JavaMethod],
                          template: str) -> Optional[str]:
        buffer: List[str] = [
            '<table border="3" width="100%" cellpadding="5">',
            f'<caption><h3>{template} contains methods:</h3></caption>',
            '<tr><th>Method name</th><th>Modifier</th><th>Return type</th>'
            '<th>Args</th><th>Comment</th></tr>'
        ]
        for method in methods:
            buffer.append(f'<tr><td>{method.name}</td>'
                          f'<td>{method.mod}</td>'
                          f'<td>{method.return_type}</td>'
                          f'<td>{method.args if method.args else "-"}</td>'
                          f'<td>'
                          f'{self.get_comment(method.comment)}</td></tr>')
        buffer.append('</table>')
        return '\n'.join(buffer)

    def get_comment(self, comment: JavaComment) -> Optional[str]:
        if not comment:
            return '-'
        buffer = []
        attrs = ['author', 'version', 'since',
                 'deprecated', 'param',
                 'throws', 'exception', 'returns']
        for attr in attrs:
            if getattr(comment, attr):
                buffer.append(f'{attr.title()}: {getattr(comment, attr)}')
        for attr in ['see', 'link']:
            if len(getattr(comment, attr)):
                links = [f'<a href="{link.strip()}.html">{link.strip()}</a>'
                         for link in getattr(comment, attr).split(',')]
                buffer.append(f"{attr.title()}: {', '.join(links)}")
        if len(comment.description):
            buffer.append(self.add_description(comment.description))
        return '<br>'.join(buffer if len(buffer) else ['-'])

    @staticmethod
    def add_description(string: str) -> Optional[str]:
        description = 'Description:'
        for line in string.split('\n'):
            for link in re.findall(r'{(.*?)}', line):
                if link.count('@link'):
                    link = re.sub('@link', '', link).strip()
                    line = re.sub(link, f'<a href="{link.strip()}.html">'
                                        f'{link.strip()}</a>',
                                  re.sub('@link', '', line, count=1))
            description = f'{description}<br>{line}'
        return description
