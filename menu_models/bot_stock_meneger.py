from menu_models import Base_Menu


class Stock_meneger(Base_Menu):

    def __init__(self):
        super().__init__()
        self.temp_product = None

    def heandler(self, message):
        action = message
        if action == "1":
            self.state = "s_e"

        elif action == "2":
            self.state = "d_m"

        elif action == "3":
            self.state = "stock_m"

        elif action == "#":
            self.state = "m"

    def show(self):
        return ("ברוכים הבאים לתפריט מנהל \n"
                "1. לעדכון / הוספת של מוצר למלאי .\n"
                "2. למחיקת מוצר מהמלאי .\n"
                "3. לקבלת מצב מלאי .\n"
                "אנא בחר מספר .\n"
                "לחזרה לתפריט הראשי שלח # .\n")
