from dataclasses import field, dataclass
from typing import List

from javadoctohtml.java_object import JavaTemplate, JavaComment


@dataclass
class JavaFile:
    name: str = None
    imports: List[str] = field(default_factory=list)
    packages: List[str] = field(default_factory=list)
    java_templates: List[JavaTemplate] = field(default_factory=list)
    comments: List[JavaComment] = field(default_factory=list)
