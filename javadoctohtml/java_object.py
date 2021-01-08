import re
from dataclasses import dataclass, field
from typing import List, Dict, Optional


class JavaComment:
    _comment: Dict[str, List[str]] = None
    _description: List[str] = None

    def __init__(self):
        self._description = []
        self._comment = {
                "@author": [],
                "@version": [],
                "@since": [],
                "@deprecated": [],
                "@see": [],
                "@throws": [],
                "@exception": [],
                "@return": [],
                "@param": [],
                "@link": []
            }

    def parser(self, comment: str) -> None:
        match = re.match(r'(@\w+)', comment)
        key = match.group(1) if match else None
        if key:
            if self._comment.get(key, None) is not None:
                self._comment[key].append(comment.split(key)[1].strip())
        else:
            self._description.append(comment.replace("* ", '').strip())

    @property
    def description(self) -> Optional[str]:
        return '\n'.join(self._description)

    @property
    def author(self) -> Optional[str]:
        return ', '.join(self._comment.get("@author", None))

    @property
    def version(self) -> Optional[str]:
        return ', '.join(self._comment.get("@version", None))

    @property
    def since(self) -> Optional[str]:
        return ', '.join(self._comment.get("@since", None))

    @property
    def deprecated(self) -> Optional[str]:
        return ', '.join(self._comment.get("@deprecated", None))

    @property
    def see(self) -> Optional[str]:
        return ', '.join(self._comment.get("@see", None))

    @property
    def throws(self) -> Optional[str]:
        return ', '.join(self._comment.get("@throws", None))

    @property
    def exception(self) -> Optional[str]:
        return ', '.join(self._comment.get("@exception", None))

    @property
    def returns(self) -> Optional[str]:
        return ', '.join(self._comment.get("@return", None))

    @property
    def param(self) -> Optional[str]:
        return ', '.join(self._comment.get("@param", None))

    @property
    def link(self) -> Optional[str]:
        return ', '.join(self._comment.get("@link", None))


@dataclass
class JavaMethod:
    all_name: str = None
    mod: str = None
    return_type: str = None
    name: str = None
    args: str = None
    comment: JavaComment = None


@dataclass
class JavaField:
    mod: str = None
    name: str = None
    value_type: str = None


@dataclass
class JavaTemplate:
    name: str = None
    mod: str = None
    template: str = None
    interface: str = field(repr=False, default='')
    parent: str = field(repr=False, default='')
    methods: List[JavaMethod] = field(default_factory=list)
    fields: List[JavaField] = field(default_factory=list)
