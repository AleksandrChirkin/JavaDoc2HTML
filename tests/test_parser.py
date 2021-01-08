from tests import TestManager
from typing import List, Dict
import unittest
from javadoctohtml import JavaFileParser, \
    JavaField, JavaTemplate, JavaMethod, JavaComment, JavaFile  # noqa


class TestParser(unittest.TestCase):
    parser: JavaFileParser = None
    path_class: str = 'TestClass.java'
    path_interface: str = 'TestInterface.java'
    str_class: str = None
    str_interface: str = None
    fields: List[Dict[str, str]] = [
        {
            'mod': 'private',
            'value_type': 'Map<Integer, String>',
            'name': 'values'
        },
        {
            'mod': 'package-private',
            'value_type': 'boolean',
            'name': 'value'
        }
    ]

    methods: List[Dict] = [
        {
            'all_name': 'TestClass(boolean value)',
            'mod': 'package-private',
            'return_type': 'null',
            'name': 'TestClass',
            'args': 'boolean value',
            'comment': None
        },
        {
            'all_name': 'Map<Integer, String> getValues()',
            'mod': 'package-private',
            'return_type': 'Map<Integer, String>',
            'name': 'getValues',
            'args': '',
            'comment': None
        },
        {
            'all_name': 'String getString(Integer index)',
            'mod': 'package-private',
            'return_type': 'String',
            'name': 'getString',
            'args': 'Integer index',
            'comment': None
        },
        {
            'all_name': 'boolean getValue()',
            'mod': 'package-private',
            'return_type': 'boolean',
            'name': 'getValue',
            'args': '',
            'comment': None
        },
        {
            'all_name': 'void addString(Integer '
                        'index, String string)',
            'mod': 'package-private',
            'return_type': 'null',
            'name': 'addString',
            'args': 'Integer index, String string',
            'comment': None
        },
    ]

    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        cls.parser = JavaFileParser()
        cls.path_class = TestManager.create_path(cls.path_class)
        cls.path_interface = TestManager.create_path(
            cls.path_interface
        )
        with open(cls.path_class) as f:
            cls.str_class = f.read()
        with open(cls.path_interface) as f:
            cls.str_interface = f.read()

    def test_imports(self):
        file = self.parser.parser(self.str_class)
        self.assertEqual(
            ['javadoc2html.tests.TestInterface'],
            file.imports)

    def test_packages(self):
        file = self.parser.parser(self.str_class)
        self.assertEqual(['javadoc2html.tests'], file.packages)

    def test_file_comment(self):
        file = self.parser.parser(self.str_class)
        comment = file.comments[0]
        self.assertEqual(comment.author, 'UserName')
        self.assertEqual(comment.version, '1.1')
        self.assertEqual(comment.since, '1.0')
        self.assertEqual(comment.see, 'TestInterface')
        self.assertEqual(comment.description,
                         'Class created for unittest')

    def test_get_comment(self):
        array = '* Class Constructor\n' \
               '* @param value boolean\n' \
               '* @exception IOException\n' \
               '* @throws ParseException'.split('\n')
        comment = JavaFileParser._get_comment(array)
        self.assertEqual(comment.description,
                         'Class Constructor')
        self.assertEqual(comment.param, 'value boolean')
        self.assertEqual(comment.exception, 'IOException')
        self.assertEqual(comment.throws, 'ParseException')

    def check_fields(self, first: JavaField, second: JavaField):
        self.assertEqual(first.name, second.name)
        self.assertEqual(first.value_type, second.value_type)
        self.assertEqual(first.mod, second.mod)

    def test_add_field(self):
        template = JavaTemplate()
        JavaFileParser._add_field(
            template,
            JavaFileParser.pattern_field.match(
                'private Map<Integer, String> values'
            ))
        JavaFileParser._add_field(
            template,
            JavaFileParser.pattern_field.match('boolean value'))
        for index in range(len(template.fields)):
            self.check_fields(
                JavaField(**self.fields[index]),
                template.fields[index])

    def check_methods(self, first: JavaMethod, second: JavaMethod):
        self.assertEqual(first.all_name, second.all_name)
        self.assertEqual(first.mod, second.mod)
        self.assertEqual(first.name, second.name)
        self.assertEqual(first.args, second.args)
        self.assertEqual(first.return_type, second.return_type)

    def test_add_method(self):
        template = JavaTemplate()
        for method in self.methods:
            JavaFileParser._add_method(
                template,
                JavaComment(),
                JavaFileParser.pattern_method.match(
                    method.get('all_name')))
        for index in range(len(template.methods)):
            self.check_methods(
                JavaMethod(**self.methods[index]), template.methods[index])

    def test_add_buffer(self):
        buffer = []
        string = 'abcde'
        self.assertTrue(
            JavaFileParser()._add_buffer(
                JavaFile(), buffer, string, True))
        self.assertEqual(string, *buffer)
        self.assertFalse(
            JavaFileParser()._add_buffer(
                JavaFile(), buffer, '*/', True))

    def test_create_template(self):
        cl = JavaFileParser._create_template(
            JavaFileParser.pattern_class.match('public class Child'))
        self.assertEqual('public', cl.mod)
        self.assertEqual('Child', cl.name)
        cl = JavaFileParser._create_template(
            JavaFileParser.pattern_class.match(
                'public class Child extends Parent implements IParent'))
        self.assertEqual('Parent', cl.parent)
        self.assertEqual('IParent', cl.interface)
        interf = JavaFileParser._create_template(
            JavaFileParser.pattern_interface.match(
                'public interface IParent'), 'Interface')
        self.assertEqual('IParent', interf.name)
        self.assertEqual('public', interf.mod)
        interf = JavaFileParser._create_template(
            JavaFileParser.pattern_interface.match(
                'interface IParent'), 'Interface')
        self.assertEqual('package-private', interf.mod)

    def test_class(self):
        file = self.parser.parser(self.str_class)
        cl = file.java_templates[0]
        self.assertEqual(cl.name, 'TestClass')
        self.assertEqual(cl.mod.strip(), 'public')
        self.assertEqual(cl.template, 'Class')
        self.assertEqual(cl.interface, 'TestInterface')
        self.assertEqual(cl.parent, '')
        for index in range(len(cl.fields)):
            self.check_fields(
                JavaField(**self.fields[index]), cl.fields[index])
        for index in range(len(cl.methods)):
            self.check_methods(
                JavaMethod(**self.methods[index]), cl.methods[index])


if __name__ == '__main__':
    unittest.main()
