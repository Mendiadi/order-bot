from bot_telegram.menu_models import MenuProtocol
from bot_telegram.enums_schemas import MenuState, Status
from .constant_messages import *


class MainMenu(MenuProtocol):
    actions = {
        "/start": Status.init,
        "1": Status.stock,
        "2": Status.make_order,
        "3": MenuState.login_menu,
        "#": MenuState.main
    }

    def __init__(self):
        super().__init__()
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
        elif rep == Status.make_order:
            bot.send_message(sender, "מצטער אך הפיצר עוד לא קיים.")
        else:
            return rep
