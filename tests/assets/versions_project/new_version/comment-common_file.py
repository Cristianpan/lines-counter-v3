class Common: #modificado

    def __init__(self, message): 
        self.message = message

    def print_message(self) -> None: #modificado
        print(self.message)

    def other(self) -> None: #agregado
        print("Hello world!") #agregado
