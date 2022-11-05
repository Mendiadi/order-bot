from bot_telegram.menu_models import MenuProtocol
from bot_telegram.product_item import Product
from bot_telegram.enums_schemas import MenuState, Status
from .constant_messages import *


class StockEditor(MenuProtocol):

    def __init__(self):
        super().__init__()
        self.msg_stage = stock_editor_stage_msg
        self.temp_product = None
        self.msg = "הסתיים תהליך  עדכון / הוספה  של מוצר ."
        self.in_process = False

    def handle(self, bot, message, sender):
        if self.in_process:
            bot.send_message(sender, self.update_stock(message))
            self.in_process = False
            bot.send_message(sender, self.msg)
            return MenuState.stock_manager
        else:
            if message == Status.back_to_main_menu:
                return MenuState.main

            if self.stock.get_product(message):
                bot.send_message(sender, f"לכמה לעדכן את המלאי ל {message}?")
                self.temp_product = message
                self.in_process = True
            else:
                self.temp_product = message
                bot.send_message(sender, f"כמה לעדכן את המלאי ל {message}?")
                self.in_process = True
            return Status.wait

    def show(self):
        return self.msg_stage

    def update_stock(self, amount):
        if self.temp_product is None:
            self.temp_product = amount
            return (f"*ממתין לכמות*"
                    f"{self.temp_product}מוצר: ")
        else:
            product = self.stock.get_product(self.temp_product)
            if product:
                product.ammount = amount
            else:
                self.stock.products.append(Product(self.temp_product, amount))
            self.stock.commit()
            return (f"*הוסף / עודכן*"
                    f"{self.temp_product}מוצר: "
                    f"{amount}בכמות: ")
