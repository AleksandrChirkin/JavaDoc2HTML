import re
from typing import List, Optional

from javadoctohtml import JavaTemplate, \
    JavaField, JavaMethod, JavaFile, JavaComment


class JavaFileParser:
    pattern_class: re.Pattern = \
        re.compile(r'(\w+\s+)?(\w+\s+)?class\s+(\w+)\s*(.*)?.*\s?')
    pattern_interface: re.Pattern = \
        re.compile(r'(\w+\s+)?(\w+\s+)?interface\s+(\w+)\s*(.*)?.*\s?')
    pattern_method: re.Pattern = \
        re.compile(r'(\w+\s+)?(\w+\s+)?(.+\s+)?(\w+\s*)?\((.*?)\)')
    pattern_field: re.Pattern = \
        re.compile(r'(\w+\s+)?(\w+\s+)?(.+\s+)(\w+\s*)')

    def parser(self, strings: str) -> 'JavaFile':
        file = JavaFile()
        buf_comment = []
        template: JavaTemplate = JavaTemplate()
        brackets = 0
        it_template, it_method, it_comment = False, False, False
        for string in strings.split('\n'):
            string = string.strip()
            if string.count('}') or string.count('{'):
                brackets = brackets - string.count('}') + string.count('{')
                it_method = False if brackets == 1 else True
                if it_template and brackets == 0:
                    it_template = False
                    file.java_templates.append(template)
            elif string.startswith('/**'):
                it_comment = True
                continue
            elif not it_template and not it_comment:
                self._add_out_template(file, string)
            if it_comment:
                it_comment = self._add_buffer(
                    file, buf_comment, string, it_template)
                if not it_template and not it_comment:
                    buf_comment = []
            elif self.pattern_class.match(string):
                it_template = True
                template = self._create_template(
                    self.pattern_class.match(string), 'Class')
            elif self.pattern_interface.match(string):
                it_template = True
                template = self._create_template(
                    self.pattern_interface.match(string), 'Interface')
            elif self.pattern_method.match(string) \
                    and not string.count('=') and brackets == 1:
                self._add_method(
                    template, self._get_comment(buf_comment),
                    self.pattern_method.match(string))
                buf_comment = []
            elif it_template and not string.count('//') \
                    and not it_method:
                self._add_field(template,
                                self.pattern_field.match(
                                    re.split('[;|=]', string)[0]))
        return file

    @staticmethod
    def _add_out_template(file: JavaFile, string: str) -> None:
        if string.startswith('package'):
            file.packages.append(
                re.match(r'package ([\w|\\.]+);', string).group(1)
            )
        elif string.startswith('import'):
            file.imports.append(
                re.match(r'import ([\w|\\.]+);', string).group(1)
            )

    def _add_buffer(self,
                    file: JavaFile,
                    buffer: List[str],
                    string: str,
                    template: bool) -> Optional[bool]:
        if string.startswith('*/'):
            if not template:
                file.comments.append(
                    self._get_comment(buffer)
                )
            return False
        buffer.append(string)
        return True

    @staticmethod
    def _create_template(
            match: re.Match,
            template: str = 'Class') -> JavaTemplate:
        mod = match.group(1) if match.group(1) else 'package-private'
        template_ = f'{template}' \
                    f'{" - " + match.group(2) if match.group(2) else ""}'
        name = match.group(3)
        class_info = match.group(4)
        parent_list = re.findall(r'extends (\w+)', class_info)
        parent = parent_list[0] if len(parent_list) else ''
        inter_list = re.findall(r'implements (\w+)', class_info)
        interface = inter_list[0] if len(inter_list) else ''
        return JavaTemplate(
            template=template_.strip(),
            mod=mod.strip(),
            name=name.strip(),
            parent=parent.strip(),
            interface=interface.strip())

    @staticmethod
    def _create_interface(match: re.Match) -> 'JavaTemplate':
        return JavaTemplate(
            mod=match.group(1),
            name=match.group(2),
            template='Interface')

    @staticmethod
    def _add_method(template: JavaTemplate,
                    comment: JavaComment,
                    match_: re.Match) -> None:
        method = match_.group(0).split('(')[0]
        if re.match(r'(\w+\s+)(\w+\s+)(.+)\s+(.*)', method):
            match = re.match(r'(\w+\s+)(\w+\s+)(.+)\s+(.*)', method)
            mod = match.group(1)
            return_type = match.group(3)
            name = match.group(4)
        elif re.match(r'(\w+\s+)(.+)\s+(.*)', method):
            match = re.match(r'(\w+\s+)(.+)\s+(.*)', method)
            mod = match.group(1)
            if mod.strip() == 'abstract':
                mod = 'package-private'
            return_type = match.group(2)
            name = match.group(3)
        elif re.match(r'(.+)\s+(.*)', method):
            match = re.match(r'(.+)\s+(.*)', method)
            mod = 'package-private'
            return_type = match.group(1)
            name = match.group(2)
        else:
            mod = 'package-private'
            return_type = 'null'
            name = method
        template.methods.append(
            JavaMethod(all_name=match_.group(0),
                       mod=mod,
                       return_type=return_type
                       if return_type != 'void' else 'null',
                       name=name,
                       args=match_.group(5),
                       comment=comment)
        )

    @staticmethod
    def _add_field(template: JavaTemplate, match: re.Match) -> None:
        if match:
            value_type = match.group(2) if match.group(2) else ''
            value_type += match.group(3)
            mod = 'package-private'
            if match.group(1):
                mod = match.group(1)
            template.fields.append(
                JavaField(
                    name=match.group(4).strip(),
                    mod=mod.strip(),
                    value_type=value_type.strip()
                )
            )

    @staticmethod
    def _get_comment(buffer: List[str]) -> 'JavaComment':
        comment = JavaComment()
        for line in buffer:
            comment.parser(line.strip('*').strip())
        return comment
