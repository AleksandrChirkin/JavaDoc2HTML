import unittest
from javadoctohtml import ConvertHtml, \
    JavaMethod, JavaField, JavaTemplate, JavaComment  # noqa


class TestConvert(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.converter = ConvertHtml()

    def test_table_methods(self):
        method = JavaMethod(
            name='abc',
            mod='public',
            return_type='null')
        buffer = [
            '<table border="3" width="100%" cellpadding="5">',
            '<caption><h3>Class contains methods:</h3></caption>',
            '<tr><th>Method name</th><th>Modifier</th><th>Return type</th>'
            '<th>Args</th><th>Comment</th></tr>',
            f'<tr><td>{method.name}</td>'
            f'<td>{method.mod}</td>'
            f'<td>{method.return_type}</td>'
            f'<td>-</td>'
            f'<td>-</td></tr>',
            '</table>']
        self.assertEqual('\n'.join(buffer),
                         self.converter.add_table_methods(
                             [method], 'Class')
                         )

    def test_table_fields(self):
        field = JavaField(
            name='abc',
            mod='public',
            value_type='null')
        buffer = [
            '<table border="3" width="100%" cellpadding="5">',
            '<caption><h3>Class contains fields:</h3></caption>',
            '<tr><th>Field name</th><th>Modifier</th><th>Type</th></tr>',
            f'<tr><td>{field.name}</td>'
            f'<td>{field.mod}</td>'
            f'<td>{field.value_type}</td></tr>',
            '</table>']
        self.assertEqual('\n'.join(buffer),
                         self.converter.add_table_fields(
                             [field], 'Class')
                         )

    def test_imports(self):
        imports = ['java', 'test']
        self.assertEqual(
            '\n'.join([
                '<h3>Imported modules and packages:</h3>',
                '<ul>',
                *[f'<li>{line}</li>' for line in imports],
                '</ul>'
            ]),
            self.converter.add_imports(imports)
        )

    def test_add_template(self):
        template = JavaTemplate(mod='public',
                                interface='IClass',
                                parent='Parent',
                                template='Class')
        self.assertEqual(
            '\n'.join([
                f'<h2>Class {template.name}</h2>'
                '<ul>',
                f'<li>Modifier: {template.mod}</li>',
                f'<li>Interface: {template.interface}</li>',
                f'<li>Parent: {template.parent}</li>',
                '</ul>'
            ]),
            self.converter.add_template(template)
        )

    def test_get_comment(self):
        comment = JavaComment()
        array = 'Class Constructor\n' \
                '@param value boolean\n' \
                '@see See\n' \
                '@link Link\n' \
                '@exception IOException\n' \
                'Link {@link Test}\n' \
                'Link {@link Test1} {@link Test2}\n' \
                '@throws ParseException'.split('\n')
        for line in array:
            comment.parser(line)
        self.assertEqual(
            '<br>'.join([
                'Param: value boolean',
                'Throws: ParseException',
                'Exception: IOException',
                'See: <a href="See.html">See</a>',
                'Link: <a href="Link.html">Link</a>',
                'Description:',
                'Class Constructor',
                'Link { <a href="Test.html">Test</a>}',
                'Link { <a href="Test1.html">Test1</a>} '
                '{ <a href="Test2.html">Test2</a>}'
            ]),
            self.converter.get_comment(comment)
        )


if __name__ == '__main__':
    unittest.main()
