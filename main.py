import telebot
from menu_models.bot_delete_menu import Delete_Menu
from menu_models.bot_login_menu import Login_Menu
from menu_models import Main_Menu, Stock_meneger, Stock_Editor

Key = "5743628298:AAH6gmGWyO4jGOr0vFxrlcMX8zic79_GCrc"
bot = telebot.TeleBot(Key)


class Main_Bot():
    def __init__(self):
        self.menu = Main_Menu()

    def greet(self, message):
        print(f"start, {bot} here")
        bot.reply_to(message, self.menu.show())

    def text_worker(self, message):
        action = str(message.json["text"])
        self.menu.heandler(action)
        #
        # if self.menu.state == "m_m":
        #     self.menu = Meneger_Menu()
        #     bot.reply_to(message, self.menu.show())

        if self.menu.state == "m":
            self.menu = Main_Menu()


        elif self.menu.state == "s_m":
            self.menu = Stock_meneger()


        elif self.menu.state == "s_e":
            self.menu = Stock_Editor()


        elif self.menu.state == "l_m":
            self.menu = Login_Menu()


        elif self.menu.state == "s_e":
            self.menu = Stock_Editor()

        if self.menu.state == "stock":
            stock = self.menu.get_stock()
            bot.reply_to(message, stock)
            self.menu.state = "init"

        elif self.menu.state == "d_m":
            self.menu = Delete_Menu()
        elif self.menu.state == "stock_m":
            bot.reply_to(message, self.menu.stock.get_stock_admin())
            self.menu.state = "init"




        elif self.menu.state == "pass_validation":
            self.menu = Stock_meneger()
            bot.reply_to(message, "התחברות בוצעה בהצלחה")


        elif self.menu.state == "error":
            bot.reply_to(message, "משהו שגוי בבחירה ששלחת , אנא נסה שוב")
            self.menu.state = "init"

        elif self.menu.state == "wrong_password":
            bot.reply_to(message, "סיסמא שגויה , נסה שוב.")
            self.menu.state = "init"

        if self.menu.state == "waiting_ammount" or self.menu.state == "updating":
            msg = self.menu.update_stock(action)
            bot.reply_to(message, msg)

        if self.menu.state == "waiting_delete":
            msg = self.menu.delete_product(action)
            bot.reply_to(message, msg)

        if self.menu.state == "deleted":
            bot.send_message(message.chat.id, "תרצה למחוק מוצר נוסף ?"
                                              "1. כן"
                                              "2. לא")
        if self.menu.state == "updated":
            self.menu.temp_product = None
            bot.send_message(message.chat.id, "תרצה לעדכן / להוסיף מוצר נוסף ?"
                                              "1. כן"
                                              "2. לא")
        elif self.menu.state == "yes":
            self.menu.state = "init"

        elif self.menu.state == "no":
            bot.send_message(message.chat.id, self.menu.msg)
            self.menu = Stock_meneger()

        if self.menu.state == "init":
            bot.reply_to(message, self.menu.show())

        # if action.isdigit():
        #     if action == "1":
        #         stock = a.get_stock()
        #         bot.reply_to(message, stock)
        #     elif action == "3":
        #         bot.reply_to(message, "enter password")
        # else:
        #     bot.reply_to(message, "make sure to send a valid action")
        # who_send_msg(message)

    def main_loop(self):

        bot.message_handler(func=self.greet, commands=["start"])
        while True:
            try:
                bot.polling()
            except:
                pass


def main():
    app = Main_Bot()
    print(f"start, {bot} ")

    @bot.message_handler(func=app.text_worker)
    def kengeroo(message): ...

    bot.polling()


if __name__ == '__main__':
    main()


def who_send_msg(message):
    first_name = message.json["chat"]["first_name"] if message.json["chat"].get("first_name") else None
    last_name = message.json["chat"]["last_name"] if message.json["chat"].get("last_name") else None
    text = message.json["text"]
    print(f"Message form :\nfirst name : {first_name} \nlast name : {last_name} \nMessage : {text}")
