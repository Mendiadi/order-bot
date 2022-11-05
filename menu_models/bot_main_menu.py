from menu_models import MenuProtocol
from enums_schemas import MenuState, Status
from .constant_messages import *


class MainMenu(MenuProtocol):
    actions = {
        "/start": Status.init,
        "1": Status.stock,
        "2": MenuState.order_menu,
        "3": MenuState.login_menu,
        "#": MenuState.main
    }

    def __init__(self,stock):
        super().__init__(stock)
        self.msg_stage = main_stage_msg

    def show(self) -> str:
        return self.msg_stage

    def handle(self, bot, message, sender):
        rep = super(MainMenu, self).handle(bot, message, sender)
        if rep == Status.error:
            bot.send_message(sender, ERROR_MSG)
            return rep
        elif rep == Status.stock:
            bot.send_message(sender, self.stock.get_stock())

        else:
            return rep
