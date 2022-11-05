from menu_models import MenuProtocol
from product_item import Product
from enums_schemas import MenuState, Status
from .constant_messages import *

class StockEditorStates:
    name = 1
    amount = 2

class StockEditor(MenuProtocol):



    def __init__(self,stock):
        super().__init__(stock)
        self.msg_stage = stock_editor_stage_msg
        self.temp_product = None
        self.msg = "הסתיים תהליך  עדכון / הוספה  של מוצר ."
        self.in_state = StockEditorStates.name

    def handle(self, bot, message, sender):
        if self.in_state == StockEditorStates.amount:
            bot.send_message(sender, self.update_stock(message))
            self.in_state = StockEditorStates.name
            bot.send_message(sender, self.msg)
            return MenuState.stock_manager
        else:
            if message == Status.back_to_main_menu:
                return MenuState.main

            if self.stock.get_product(message):
                bot.send_message(sender, f"לכמה לעדכן את המלאי ל {message}?")
                self.temp_product = message
            else:
                self.temp_product = message
                bot.send_message(sender, f"כמה לעדכן את המלאי ל {message}?")
            self.in_state = StockEditorStates.amount
            return Status.wait

    def show(self):
        return self.msg_stage

    def update_stock(self, amount):
        product = self.stock.get_product(self.temp_product)
        if product:
            product.ammount = amount
        else:
            self.stock.add_product(Product(self.temp_product, amount))
        self.stock.commit()
        return (f"*הוסף / עודכן*"
                f"{self.temp_product}מוצר: "
                f"{amount}בכמות: ")
