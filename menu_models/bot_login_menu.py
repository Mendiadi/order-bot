from menu_models import MenuProtocol
from .constant_messages import *
from enums_schemas import Status, MenuState


class LoginMenu(MenuProtocol):

    def __init__(self,stock):
        super(LoginMenu, self).__init__(stock)
        self.msg_stage = login_stage_msg
        self.secret_key = "pass"

    def handle(self, bot, message, sender):
        if message == self.secret_key:
            bot.send_message(sender, text="התחברות בוצעה בהצלחה")
            return MenuState.stock_manager
        elif message == Status.back_to_main_menu:
            return MenuState.main
        else:
            bot.send_message(sender, text="סיסמא שגויה , נסה שוב.")

    def show(self):
        return self.msg_stage
