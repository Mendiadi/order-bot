import threading

from telegram.ext import *
from telegram import *

from menu_models.bot_order_menu import OrderMenu
from menu_models.bot_delete_menu import DeleteMenu
from menu_models.bot_login_menu import LoginMenu
from menu_models.bot_order_manager_menu import AdminOrderManager
from menu_models import MainMenu, StockManager, StockEditor
from enums_schemas import MenuState, Status
from product_item import Stock


class MainBot:

    def __init__(self, stock):

        self.MENUS = {
            MenuState.main: MainMenu(stock),
            MenuState.login_menu: LoginMenu(stock),
            MenuState.delete_menu: DeleteMenu(stock),
            MenuState.stock_manager: StockManager(stock),
            MenuState.stock_editor: StockEditor(stock),
            MenuState.order_menu: OrderMenu(stock),
            MenuState.order_manage:AdminOrderManager(stock)
        }
        self.menu_state = MenuState.main
        self.menu = self.MENUS[self.menu_state]

    def updater(self, state):
        if state in self.MENUS:
            self.menu_state = state
        self.menu = self.MENUS[self.menu_state]

    def main_handler(self, update: Update, context):

        print(f"[LOG] {update.message.text}")
        print(f"[LOGMSG] {update.message} , ")
        state = self.menu.handle(update.message, update.message.text, update.message.from_user, context)
        self.updater(state)
        if state != Status.wait:
            update.message.reply_text(self.menu.show())



class App:
    def __init__(self, updater: Updater):
        self.clients = {}
        self.stock = Stock("data.json")
        self.updater = updater

    def client(self, update, context):
        uid = update.message.from_user.id
        if uid not in self.clients:
            app = MainBot(self.stock)
            self.clients[uid] = app
        thread_conv = threading.Thread(target=self.clients[uid].main_handler,
                                       args=(update, context))
        thread_conv.start()

    def main_loop(self):
        dp: Dispatcher = self.updater.dispatcher
        self.stock.load()
        dp.add_handler(MessageHandler(Filters.text, self.client))

        self.updater.start_polling()
        self.updater.idle()


def main():
    api_key = "5743628298:AAH6gmGWyO4jGOr0vFxrlcMX8zic79_GCrc"
    app = App(Updater(api_key, use_context=True))
    app.main_loop()


if __name__ == '__main__':
    main()
