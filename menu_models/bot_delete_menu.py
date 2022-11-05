from menu_models import Base_Menu


class Delete_Menu(Base_Menu):
    def __init__(self):
        super().__init__()
        self.msg = "הסתיים תהליך  המחיקה ."

    def heandler(self, message):
        action = message
        if self.state == "waiting_delete":
            pass
        elif action == "#":
            self.state = "m"
        elif action == "1":
            self.state = "yes"
        elif action == "2":
            self.state = "no"

    def show(self):
        self.state = "waiting_delete"
        return ("ברוכים הבאים למחיקת מוצר מהמלאי \n"
                "כדי למחוק מוצר  מהמלאי יש לשלוח את שם המוצר .\n"
                "לחזרה לתפריט הראשי שלח # .\n")

    def delete_product(self, action):
        res = self.stock.remove_product(action)
        self.state = "deleted"
        if res:
            return f"נמחק בהצלחה בהצלחה{action}"
        else:
            return f"אין מוצר כזה במלאי - נא לבדוק את מה ששלחת{action}"
