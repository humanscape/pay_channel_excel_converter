class NotWantToSaveException(BaseException):
    def __init__(self, text: str = None):
        self.error_message = f"Expected Exception : {text[:40]}"

    def __repr__(self):
        return self.error_message
