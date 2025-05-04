class Common:

    """
        Commentario de Bloque
    """

    def __init__(self, message): #nuevo comentario innecesario
        self.message = message

    def print_message(self) -> None:
        print(self.message)

    def other(self) -> None:
        print("Hello world!")