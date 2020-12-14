from typing import List


class DocumentationItem:
    def __init__(self, item: str, doc_string: str) -> None:
        if item.find('class') != -1:
            self.type = 'class'
            item_fragments = item[:item.find('{')].strip().split(' ')
            last_index = self.get_extends_or_implements_index(item_fragments)
            self.name = item_fragments[last_index - 1]
        elif item.find('interface') != -1:
            self.type = 'interface'
            item_fragments = item[:item.find('{')].strip().split(' ')
            last_index = self.get_extends_or_implements_index(item_fragments)
            self.name = item_fragments[last_index - 1]
        elif item.find('(') != -1:
            self.type = 'method'
            self.name = item[:item.find('(')].strip().split(' ')[-1]
        else:
            self.type = 'field'
            if item.find('=') != -1:
                self.name = item[:item.find('=')-1].strip().split(' ')[-1]
            else:
                self.name = item[:item.find(';')].strip().split(' ')[-1]
        if doc_string.find('@author') != -1 and \
                (self.type == 'class' or self.type == 'interface'):
            author = doc_string[doc_string.find('@author')+8:]
            self.author = author[:author.find('\n')].strip()
        if doc_string.find('@version') != -1 and \
                (self.type == 'class' or self.type == 'interface'):
            version = doc_string[doc_string.find('@version')+9:]
            self.version = version[:version.find('\n')].strip()
        self.exceptions = {}
        if doc_string.find('@exception') != -1 and self.type == 'method':
            self.find_all_exceptions(doc_string, '@exception')
        if doc_string.find('@throws') != -1 and self.type == 'method':
            self.find_all_exceptions(doc_string, '@throws')
        self.params = {}
        if doc_string.find('@param') != -1 and self.type == 'method':
            params = doc_string.split('* @param')
            for param in params[1:]:
                param_content = param.strip().split(' ')
                self.params[param_content[0]] = ' '.join(param_content[2:])
        self.returning = None
        if doc_string.find('@return') != -1 and self.type == 'method':
            returning = doc_string[doc_string.find('@return'):]
            self.returning = returning[:returning.find('\n')].strip()

    def find_all_exceptions(self, doc_string: str, separator: str) -> None:
        exceptions = doc_string.split(f'* {separator}')
        for exception in exceptions[1:]:
            exception_content = exception.strip().split(' ')
            self.exceptions[exception_content[0]] = ' ' \
                .join(exception_content[2:])

    @staticmethod
    def get_extends_or_implements_index(fragments: List[str]) -> int:
        try:
            return fragments.index('extends')
        except ValueError:
            try:
                return fragments.index('implements')
            except ValueError:
                return 0
