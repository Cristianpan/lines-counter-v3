class UnchangedFile:
    def __init__(self, message):
        self.message = message

    def print_message(self) -> None:
        print(self.message)

    def other(self) -> None:
        print("Hello world!")