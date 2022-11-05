from menu_models import Base_Menu
from product_item import Product


class Stock_Editor(Base_Menu):

    def __init__(self):
        super().__init__()
        self.temp_product = None
        self.msg = "הסתיים תהליך  עדכון / הוספה  של מוצר ."

    def heandler(self, message):
        action = message
        if self.state == "waiting_ammount" or self.state == "updating":
            pass
        elif action == "#":
            self.state = "m"
        elif action == "1":
            self.state = "yes"
        elif action == "2":
            self.state = "no"


    def show(self):
        self.state = "updating"
        return ("ברוכים הבאים לעדכון מלאי \n"
                "כדי לעדכן מלאי יש לשלוח 2 הודעות נפרדות .\n"
                "הודעה 1. הנכס שם של מוצר .\n"
                "הודעה 2. הנכס כמות של המוצר .\n"
                "אנא בחר מספר .\n"
                "לחזרה לתפריט הראשי שלח # .\n")

    def update_stock(self, action) -> None:
        if self.temp_product is None:
            self.temp_product = action
            self.state = "waiting_ammount"
            return (f"*ממתין לכמות*"
                    f"{self.temp_product}מוצר: ")
        else:
            product = self.stock.get_product(self.temp_product)
            if product:
                product.ammount = action
            else:
                self.stock.products.append(Product(self.temp_product,action))
            self.stock.commit()
            self.state = "updated"
            return (f"*הוסף / עודכן*"
                    f"{self.temp_product}מוצר: "
                    f"{action}בכמות: ")
