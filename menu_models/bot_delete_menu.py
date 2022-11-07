from menu_models import MenuProtocol
from enums_schemas import MenuState, Status
from .constant_messages import *


class DeleteMenu(MenuProtocol):

    def __init__(self,stock):
        super().__init__(stock)
        self.msg_stage = delete_menu_stage_msg
        self.msg = "הסתיים תהליך  המחיקה ."

    def handle(self, bot, message, sender,context):
        if message == Status.back_to_main_menu:
            return MenuState.main

        bot.reply_text(self.delete_product(message))
        bot.reply_text(self.msg)
        self.in_process = False
        return MenuState.stock_manager

    def show(self):
        return self.msg_stage

    def delete_product(self, name):

        res = self.stock.remove_product(name)
        if res:
            return f"נמחק בהצלחה בהצלחה{name}"
        else:
            return f"אין מוצר כזה במלאי - נא לבדוק את מה ששלחת{name}"
