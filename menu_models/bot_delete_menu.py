from bot_telegram.menu_models import MenuProtocol
from bot_telegram.enums_schemas import MenuState, Status
from .constant_messages import *


class DeleteMenu(MenuProtocol):

    def __init__(self):
        super().__init__()
        self.msg_stage = delete_menu_stage_msg
        self.msg = "הסתיים תהליך  המחיקה ."

    def handle(self, bot, message, sender):
        if message == Status.back_to_main_menu:
            return MenuState.main

        bot.send_message(sender, self.delete_product(message))
        bot.send_message(sender, self.msg)
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
