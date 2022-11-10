from enums_schemas import MenuState, Status
from .bot_base_menu import MenuProtocol


class VerifyManagerMenu(MenuProtocol):
    def __init__(self,stock,app):
        super(VerifyManagerMenu, self).__init__(stock)
        self.app = app

        self.state = 0
        self.reply_msg =  " \nהכנס מספר משתמש "+ str(self.app.waiting_for_approved)
        self.user_id_temp = None

    def show(self):
        return self.reply_msg

    def handle(self, bot, message,sender,context) -> str:
         if self.state == 0:
            for username,userid in self.app.waiting_for_approved:
                if message == str(userid):

                    self.user_id_temp = message
            if self.user_id_temp:
                self.state = 1
            else:
                bot.reply_text("הכנס מספר קיים")
         elif message == Status.back_to_main_menu:
             return MenuState.stock_manager
         elif self.state == 1:
             if message == "1":
                 self.app.clients[int(self.user_id_temp)].is_verify = True
                 bot.reply_text("עודכן")
                 # self.app.waiting_for_approved.remove()
                 self.app.update_verify_clients()
                 return MenuState.stock_manager


