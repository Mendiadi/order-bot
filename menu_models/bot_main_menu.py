from menu_models import Base_Menu


class Main_Menu(Base_Menu):
    def __init__(self):
        super().__init__()

    def heandler(self, message):
        action = message
        print(action)
        if action == "/start":
            self.state = "init"
        elif action == "1":
            self.state = "stock"
        elif action == "2":
            pass  # todo : make order
        elif action == "3":
            self.state = "l_m"
        else:
            self.state = "error"

    def show(self):
        return ("ברוכים הבאים לXXX \n"
                "בוט זה מפאשר הזמנה / צפיה במלאי: \n"
                "1. לתפריט .\n"
                '2. לביצוע הזמנה .\n'
                '3. לתפריט מנהל .\n'
                "אנא בחר מספר .\n")