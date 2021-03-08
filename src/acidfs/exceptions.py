class InvalidPathException(Exception):
    # Store the cause of the exception (e.g. dot-files, invalid-character, ...)
    reason: str
    # User facing error message
    message: str

    def __init__(self, reason, message):
        super().__init__(reason, message)
        self.reason = reason
        self.message = message
