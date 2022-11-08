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

    def handle(self, bot, message, sender,context):
        if message == "2":
            if len(self.stock.products) == 0:
                bot.reply_text("אין מוצרים זמינים")
                return MenuState.main
        rep = super(MainMenu, self).handle(bot, message, sender,context)
        if rep == Status.error:
            bot.reply_text( ERROR_MSG)
            return rep
        elif rep == Status.stock:
            stock = self.stock.get_stock()
            if stock:
                bot.reply_text(stock)


        else:
            return rep
