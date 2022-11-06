import threading
import time
import asyncio

from telegram.ext import *
from telegram import *

from menu_models.bot_active_talk import OrdersMeneger
from menu_models.bot_order_menu import OrderMenu
from menu_models.bot_delete_menu import DeleteMenu
from menu_models.bot_login_menu import LoginMenu
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
            MenuState.order_menu: OrderMenu(stock)
        }
        self.menu_state = MenuState.main
        self.menu = self.MENUS[self.menu_state]
        self.order_meneger = OrdersMeneger("/talk_json.json")

    def greet(self,update,context):...

    def updater(self, state):
        if state in self.MENUS:
            self.menu_state = state
        self.menu = self.MENUS[self.menu_state]


    def main_handler(self, update:Update, context):
        # def wrapper(update:Update, context):
        print(f"[LOG] {update.message.text}")

        print(f"[LOGMSG] {update.message} , ")
        state = self.menu.handle(update.message,update.message.text,update.message.chat_id)
        self.updater(state)
        if state != Status.wait:
            update.message.reply_text( self.menu.show())
        print(threading.active_count())


clients = {}
stock = Stock("./data_json.json")

def client(update,context):
    uid = update.message.from_user.id
    if uid not in clients:
        app = MainBot(stock)
        clients[uid] = app
        thread_conv = threading.Thread(target=clients[uid].main_handler,
                                       args=(update, context))
        thread_conv.start()
        print(clients," chat_id")
    else:
        thread_conv = threading.Thread(target=clients[uid].main_handler,
                                       args=(update, context))
        thread_conv.start()

def main():

    key = "5743628298:AAH6gmGWyO4jGOr0vFxrlcMX8zic79_GCrc"

    updater = Updater(key, use_context=True)
    a:Dispatcher = updater.dispatcher

    stock.load()
    a.add_handler(MessageHandler(Filters.text,client))
    updater.start_polling()
    updater.idle()




if __name__ == '__main__':
    main()
