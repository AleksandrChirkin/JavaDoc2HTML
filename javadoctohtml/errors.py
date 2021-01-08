class JDException(Exception):
    message = 'unknown error'


class JDDirException(JDException):
    def __init__(self, message):
        self.message = self.message.format(message)
        super().__init__(self.message)

    message = 'Directory: {} not exist'


class JDSyntaxError(JDException):
    def __init__(self):
        self.message = 'Syntax error'
        super().__init__(self.message)
