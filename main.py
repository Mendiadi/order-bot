import dataclasses
import os
import threading

from telegram.ext import *
from telegram import *

import json_func
from menu_models.bot_verify_manager_menu import VerifyManagerMenu
from menu_models.bot_verify_menu import VerifyMenu
from menu_models.bot_demo_menu import DemoMenu
from menu_models.bot_order_menu import OrderMenu
from menu_models.bot_delete_menu import DeleteMenu
from menu_models.bot_login_menu import LoginMenu
from menu_models.bot_order_manager_menu import AdminOrderManager
from menu_models import MainMenu, StockManager, StockEditor
from enums_schemas import MenuState, Status
from product_item import Stock
from menu_models.constant_messages import main_stage_msg


class Bot:
    ...

@dataclasses.dataclass
class Client:
    uid:str
    app:Bot
    is_verify:bool


class DemoBot(Bot):
    def __init__(self,stock,app):
        self.menu = DemoMenu(stock)
        self.stock = stock
        self.app = app



    def main_handler(self, update: Update, context):

        state = self.menu.handle(update.message, update.message.text, update.message.from_user,context)

        if state == MenuState.verify:

            self.menu = VerifyMenu(self.stock)
        elif state == Status.verify:
            ...

        elif state == "demo":
            user , userid = self.menu.username, self.menu.user_id
            self.app.waiting_for_approved.append((user,userid))
            self.menu = DemoMenu(self.stock,True)

        if state != Status.wait:
            update.message.reply_text(self.menu.show())




class MainBot(Bot):

    def __init__(self, stock,app):
        self.MENUS = {
            MenuState.main: MainMenu(stock),
            MenuState.login_menu: LoginMenu(stock),
            MenuState.delete_menu: DeleteMenu(stock),
            MenuState.stock_manager: StockManager(stock),
            MenuState.stock_editor: StockEditor(stock),
            MenuState.order_menu: OrderMenu(stock),
            MenuState.order_manage: AdminOrderManager(stock),
            MenuState.verify_manage:VerifyManagerMenu(stock,app.waiting_for_approved)
        }
        self.menu_state = MenuState.main
        self.menu = self.MENUS[self.menu_state]


    def updater(self, state):
        if state in self.MENUS:
            self.menu_state = state
        self.menu = self.MENUS[self.menu_state]

    def main_handler(self, update: Update, context):
        print(f"[LOG] {update.message}")
        print(f"[LOGMSG] {update.message} , ")
        state = self.menu.handle(update.message, update.message.text, update.message.from_user, context)
        self.updater(state)
        if state != Status.wait:
            update.message.reply_text(self.menu.show())


def help_command(update, context):
    return update.message.reply_text(
        "בוט זה מאפשר לך לבצע הזמנות ולנהל אותן, עקוב אחר ההוראות בכל תפריט ואם ראית באג דווח, שימוש מהנה")


class App:
    def __init__(self, updater: Updater):
        self.clients = {}
        self.stock = Stock("data.json")
        self.updater = updater
        self.verify_clients = {}
        self.waiting_for_approved = []
        self.approved_json_path="approved_clients.json"
        if self.approved_json_path in os.listdir():
            self.load_verify_clients()

    def load_verify_clients(self):
        clients = json_func.json_read(self.approved_json_path)
        for k,v in clients.items():

            self.verify_clients[int(k)] = Client(k,MainBot(self.stock,self),v)
            self.clients[int(k)] = Client(k,DemoBot(self.stock,self),v)
        print("client: ", self.clients, "approved: ", self.verify_clients)

    def update_verify_clients(self):
        data = {int(k):v.is_verify  for k,v in self.verify_clients.items()}
        json_func.write_to_json(data,self.approved_json_path,len(self.verify_clients))

    def client(self, update, context):
        print("client: ",self.clients,"approved: ", self.verify_clients)
        print( update.message.from_user.id)
        uid = update.message.from_user.id
        client = self.clients.get(uid,None)
        print("client",client)
        if not client:
            self.clients[uid] = Client(uid,DemoBot(self.stock,self),False)
        else:
            if client.is_verify and client.uid not in self.verify_clients:
                self.verify_clients[client.uid] = client
                client.app = MainBot(self.stock,self)
                self.update_verify_clients()

        thread_conv = threading.Thread(target=self.clients[uid].app.main_handler,
                                       args=(update, context))
        thread_conv.start()

    def listen(self):
        dp: Dispatcher = self.updater.dispatcher
        self.stock.load()
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(MessageHandler(Filters.text, self.client))
        dp.add_handler(MessageHandler(Filters.photo,self.client))
        self.updater.start_polling()
        self.updater.idle()


def main():
    api_key = "5743628298:AAH6gmGWyO4jGOr0vFxrlcMX8zic79_GCrc"
    app = App(Updater(api_key, use_context=True))
    app.listen()


if __name__ == '__main__':
    main()
