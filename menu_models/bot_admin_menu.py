
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
        "6":Status.broadcast,
        Status.back_to_main_menu: MenuState.main

    }

    def show(self) -> str:
        return self.msg_stage

    def __init__(self, stock,app):
        super().__init__(stock)
        self.msg_stage = stock_manager_stage_msg
        self.temp_product = None
        self.app = app
        self.wait_for_broadcast = False

    def handle(self, bot, message, sender, context):
        if self.wait_for_broadcast:
            self.wait_for_broadcast = False
            self.app.broad_cast_message(message)
            bot.reply_text("שלחתי להם.")
            return MenuState.admin_man
        rep = super(AdminMenu, self).handle(bot, message, sender, context)
        if rep == Status.stock:
            print(f"stock = {self.stock.get_stock_admin()}")
            bot.reply_text(self.stock.get_stock_admin())
        if rep == Status.broadcast:
            bot.reply_text("מה לרשום לכולם? ")
            self.wait_for_broadcast = True
            return Status.wait
        return rep


