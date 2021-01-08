import os
from typing import Optional, List
from javadoctohtml import errors


class FileManager:
    _path: str = ''

    def open(self, paths: List[str]) -> Optional[List[str]]:
        files = []
        for path in paths:
            if not os.path.exists(path):
                raise errors.JDDirException(path)
            if os.path.isfile(path):
                self._add_file(files, path)
            elif os.path.isdir(path):
                self._path = path
                for file in os.listdir(path):
                    self._add_file(files, file)
        return files

    def read(self, path) -> Optional[str]:
        with open(os.path.join(self._path, path)) as file:
            return file.read()

    def mkdir(self):
        self._path = f'{self._path if self._path else "result"}_html'
        if not os.path.exists(self._path):
            os.mkdir(self._path)

    def write(self, file: str, inform: str):
        with open(os.path.join(self._path, file), "w") as f:
            f.write(inform)

    @staticmethod
    def _add_file(files: List[str], file: str):
        if file.endswith('.java'):
            files.append(file)
