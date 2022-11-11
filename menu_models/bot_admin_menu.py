
from .bot_base_menu import MenuProtocol

from .constant_messages import *
from enums_schemas import MenuState, Status

class AdminMenu(MenuProtocol):
    actions = {
        "1": MenuState.stock_editor,
        "2": MenuState.delete_menu,
        "3": Status.stock,
        "4": MenuState.order_manage,
        "5": MenuState.verify_manage,
        Status.back_to_main_menu: MenuState.main

    }

    def show(self) -> str:
        return self.msg_stage

    def __init__(self, stock):
        super().__init__(stock)
        self.msg_stage = stock_manager_stage_msg
        self.temp_product = None

    def handle(self, bot, message, sender, context):
        rep = super(AdminMenu, self).handle(bot, message, sender, context)
        if rep == Status.stock:
            print(f"stock = {self.stock.get_stock_admin()}")
            bot.reply_text(self.stock.get_stock_admin())

        return rep


