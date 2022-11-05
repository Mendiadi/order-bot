from menu_models import Base_Menu

class Meneger_Menu(Base_Menu):
    def show(self):
        return ("ברוכים הבאים לתפריט מנהל \n"
                "1. ניהול מלאי .\n"
                '3. ניהול הזמנות .\n'
                "אנא בחר מספר .\n"
                "לחזרה לתפריט הראשי שלח # .\n")

    def heandler(self, message):
        action = message
        if action == "1":
            self.state = "s_e"
        elif action == "2":
            self.state = "order_maneger"
        elif action == "#":
            self.state = "init"