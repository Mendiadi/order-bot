import telebot

from menu_models.bot_order_menu import OrderMenu
from menu_models.bot_delete_menu import DeleteMenu
from menu_models.bot_login_menu import LoginMenu
from menu_models import MainMenu, StockManager, StockEditor
from enums_schemas import MenuState, Status
from product_item import Stock

class MainBot:

    def __init__(self, bot,stock):

        self.MENUS =  {
        MenuState.main: MainMenu(stock),
        MenuState.login_menu: LoginMenu(stock),
        MenuState.delete_menu: DeleteMenu(stock),
        MenuState.stock_manager: StockManager(stock),
        MenuState.stock_editor: StockEditor(stock),
        MenuState.order_menu:OrderMenu(stock)
        }
        self.menu_state = MenuState.main
        self.menu = self.MENUS[self.menu_state]
        self.bot = bot


    def updater(self, state):
        if state in self.MENUS:
            self.menu_state = state
        self.menu = self.MENUS[self.menu_state]

    def main_handler(self, message):
        print(f"[LOG] {message}")
        action = str(message.json["text"])
        state = self.menu.handle(self.bot, action, message.json['chat']['id'])
        self.updater(state)
        if state != Status.wait:
            self.bot.send_message(message.json['chat']['id'], self.menu.show())

    def run(self):
        @self.bot.message_handler(func=self.main_handler)
        def wrapper(message): ...
        self.bot.polling()

def main():
    Key = "5743628298:AAH6gmGWyO4jGOr0vFxrlcMX8zic79_GCrc"
    bot = telebot.TeleBot(Key)
    bot.message_handlers.clear()
    stock = Stock("./data_json.json")
    stock.load()
    app = MainBot(bot,stock)
    app.run()





    bot.polling()


if __name__ == '__main__':
    main()
