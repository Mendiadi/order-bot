from  .bot_base_menu import MenuProtocol
from enums_schemas import Status, MenuState
from .constant_messages import verify_menu_msg_stage




class DemoMenu(MenuProtocol):

    actions = {
        "1":Status.stock ,
        "2":1,
        Status.back_to_main_menu:2

    }

    def __init__(self,stock,is_finish_verify = False):
        super().__init__(stock)
        self.reply_msg = verify_menu_msg_stage
        self.is_finish_verify = is_finish_verify
    def show(self):
        return self.reply_msg

    def handle(self, bot, message,sender,context) -> str:
        rep = super(DemoMenu, self).handle(bot,message,sender,context)

        if rep == 1  and not self.is_finish_verify:
            self.reply_msg = "תהליך אימות מתחיל..."
            return MenuState.verify
        elif rep == 1 and self.is_finish_verify:
            bot.reply_text("אתה ממתין לאימות")

        elif rep == Status.stock:
            stock = self.stock.get_stock()
            if stock:
                bot.reply_text(stock)
        elif rep == 2:
            self.reply_msg = verify_menu_msg_stage

