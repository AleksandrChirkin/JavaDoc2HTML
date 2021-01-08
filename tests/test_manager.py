from typing import Optional
import os
import unittest
from javadoctohtml import FileManager, errors  # noqa


class TestManager(unittest.TestCase):
    files = ['TestClass.java', 'TestInterface.java']

    @classmethod
    def setUpClass(cls) -> None:
        cls.manager = FileManager()

    @staticmethod
    def create_path(file: str) -> Optional[str]:
        for path in ['java', 'tests']:
            if os.path.exists(file):
                return file
            if file != path:
                file = os.path.join(path, file)
        return file

    def test(self):
        with self.assertRaises(errors.JDDirException):
            self.manager.open(['random_dir'])
        files = []
        self.manager._add_file(files, 'random_file.doc')
        self.manager._add_file(files, 'JavaClass.java')
        self.assertEqual(['JavaClass.java'], files)

    def test_open(self):
        files = [self.create_path(file) for file in self.files]
        self.assertEqual(files, self.manager.open(files))
        self.assertEqual(
            self.files,
            self.manager.open(
                [self.create_path('java')]
            )
        )


if __name__ == '__main__':
    unittest.main()
