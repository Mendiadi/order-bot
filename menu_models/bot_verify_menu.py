from enums_schemas import Status, MenuState
from .bot_base_menu import MenuProtocol


class VerifyLevel:
    id_pic = 1
    phone = 2
    end = 3

class VerifyMenu(MenuProtocol):
    def __init__(self,stock):
        super(VerifyMenu, self).__init__(stock)
        self.reply_msg = "שלח צילום תז/רישיון/דרכון"
        self.stack = [VerifyLevel.end,VerifyLevel.phone,VerifyLevel.id_pic]
        self.data_from_levels = []
        self.username = None
        self.user_id = None

    def show(self):
        return self.reply_msg


    def send_details(self,message,bot):
        for msg in self.data_from_levels:
            bot.bot.forward_message(bot.chat_id, bot.chat_id,msg)
        self.data_from_levels.clear()


    def handle(self, bot, message,sender,context) -> str:
        self.level = self.stack.pop()
        if self.level == VerifyLevel.id_pic:
            if not bot.photo:
               self.reply_msg = "תמונה בלבד"
               self.stack.append(self.level)
            else:
                self.data_from_levels.append(bot.message_id)
                self.reply_msg = "הכנס טלפון: "

        if self.level == VerifyLevel.phone and not bot.photo:
            self.data_from_levels.append(bot.message_id)
            self.send_details(message, bot)
            self.username = sender.username
            self.user_id = sender.id
            self.reply_msg = "ממתין לאימות"
            return "demo"



        return Status.verify
