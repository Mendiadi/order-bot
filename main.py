import abc
import dataclasses
import datetime
import os
import threading
import time
import sys

from telegram.ext import *
from telegram import *

import json_func
from menu_models.bot_admin_menu import AdminMenu
from menu_models.bot_verify_manager_menu import VerifyManagerMenu
from menu_models.bot_verify_menu import VerifyMenu
from menu_models.bot_demo_menu import DemoMenu
from menu_models.bot_order_menu import OrderMenu
from menu_models.bot_delete_menu import DeleteMenu
from menu_models.bot_login_menu import LoginMenu
from menu_models.bot_order_manager_menu import AdminOrderManager
from menu_models import MainMenu, StockEditor, MenuProtocol
from enums_schemas import MenuState, Status
from product_item import Stock


@dataclasses.dataclass
class Client:
    uid: str
    app: Bot
    is_verify: bool
    time_process_start: datetime.datetime = None
    in_process: bool = False
    killed: bool = False
    is_admin: bool = False
    last_show_up: datetime.datetime = None


class Bot(metaclass=abc.ABCMeta):
    def __init__(self, stock, app, me: Client = None):
        self.this_user = me
        self.stock = stock
        self.app = app

    @abc.abstractmethod
    def main_handler(self, update: Update, context): ...


class DemoBot(Bot):
    def __init__(self, stock, app, me: Client = None):
        super(DemoBot, self).__init__(stock, app, me)
        self.MENUS = {
            MenuState.demo: DemoMenu(stock),

            MenuState.verify: VerifyMenu(self.stock),

        }
        self.menu = self.MENUS[MenuState.demo]

    def main_handler(self, update: Update, context):
        state = self.menu.handle(update.message,
                                 update.message.text,
                                 update.message.from_user,
                                 context
                                 )

        menu = self.MENUS.get(state, None)
        if menu: self.menu = menu
        if state == "demo":
            user, userid = self.menu.username, self.menu.user_id
            self.app.waiting_for_approved.append((user, userid))
            self.menu = DemoMenu(self.stock, True)
        if state != Status.wait:
            update.message.reply_text(self.menu.show())


class MemberBot(Bot):

    def __init__(self, stock, app, me: Client = None):
        super(MemberBot, self).__init__(stock, app, me)
        self.MENUS: dict[str, MenuProtocol] = {}
        self.restart_bot = False

    def updater(self, state):
        if state in self.MENUS:
            self.menu_state = state

        self.menu = self.MENUS[self.menu_state]
        if state == MenuState.verify_manage:
            self.menu.app = self.app

    def main_handler(self, update: Update, context):

        print(f"[LOG] {update.message}")
        print(f"[LOGMSG] {update.message} , ")

        if self.this_user.killed:
            self.this_user.killed = False
            self.menu.on_restart()
            state = MenuState.main
            self.restart_bot = True
        else:
            state = self.menu.handle(update.message,
                                     update.message.text,
                                     update.message.from_user,
                                     context
                                     )
        self.updater(state)
        if state != Status.wait:
            update.message.reply_text(self.menu.show())
        print(f"[USERLOG] {self.this_user}")


class ClientBot(MemberBot):

    def __init__(self, stock, app, me: Client = None):
        super(ClientBot, self).__init__(stock, app, me)
        self.MENUS = {
            MenuState.main: MainMenu(stock),
            MenuState.login_menu: LoginMenu(stock),
            MenuState.delete_menu: DeleteMenu(stock),
            MenuState.admin_man: AdminMenu(stock, self.app),
            MenuState.stock_editor: StockEditor(stock),
            MenuState.order_menu: OrderMenu(stock, app, me),
            MenuState.order_manage: AdminOrderManager(stock),
            MenuState.verify_manage: VerifyManagerMenu(self.stock, self.app)
        }
        self.menu_state = MenuState.main
        self.menu = self.MENUS[self.menu_state]


def help_command(update, context):
    update.message.reply_text(
        "בוט זה מאפשר לך לבצע הזמנות ולנהל אותן, עקוב אחר ההוראות בכל תפריט ואם ראית באג דווח, שימוש מהנה")


class AdminBot(MemberBot):
    def __init__(self, stock, app, me=None):
        super(AdminBot, self).__init__(stock, app, me)
        self.MENUS = {
            MenuState.admin_man: AdminMenu(self.stock, self.app),
            MenuState.delete_menu: DeleteMenu(self.stock),

            MenuState.stock_editor: StockEditor(self.stock),
            MenuState.order_menu: OrderMenu(self.stock, self.app, me),
            MenuState.order_manage: AdminOrderManager(self.stock),
            MenuState.verify_manage: VerifyManagerMenu(self.stock, self.app)
        }
        self.menu_state = MenuState.admin_man
        self.menu = self.MENUS[self.menu_state]


class App:
    def __init__(self, updater: Updater):
        self.clients = {}
        self.stock = Stock("data.json")
        self.updater = updater
        self.verify_clients = {}
        self.waiting_for_approved = []
        self.admins_members = {}
        self.approved_json_path = "approved_clients.json"
        self.in_process_clients = []
        if self.approved_json_path in os.listdir():
            self.load_verify_clients()
        self.kill_process_thread = threading.Thread(target=self.standalone_process_provider)
        self.run = False

    def load_verify_clients(self):
        clients = json_func.json_read(self.approved_json_path)
        for k, v in clients.items():
            self.verify_clients[int(k)] = Client(k, ClientBot(self.stock, self), v)
            self.clients[int(k)] = Client(k, DemoBot(self.stock, self), v)
        print("client: ", self.clients, "approved: ", self.verify_clients)

    def update_verify_clients(self):
        data = {int(k): v.is_verify for k, v in self.verify_clients.items()}
        json_func.write_to_json(data, self.approved_json_path, len(self.verify_clients))

    def client(self, update, context):
        print("[IN PROCESS CLINETS LOG]", self.in_process_clients)
        print(update.message.from_user.id)
        uid = update.message.from_user.id

        client = self.clients.get(uid, None)
        print("client", client)
        if not client:
            self.clients[uid] = Client(uid, DemoBot(self.stock, self), False)

        else:
            if client.is_verify and client.uid not in self.verify_clients:
                self.verify_clients[client.uid] = client
                client.app = ClientBot(self.stock, self, client)
                self.update_verify_clients()
        self.clients[uid].last_show_up = datetime.datetime.now()
        thread_conv = threading.Thread(target=self.clients[uid].app.main_handler,
                                       args=(update, context))
        thread_conv.start()

    def listen(self):
        self.run = True
        dp: Dispatcher = self.updater.dispatcher
        self.stock.load()
        dp.add_handler(CommandHandler("help", help_command))
        dp.add_handler(MessageHandler(Filters.text, self.client))
        dp.add_handler(MessageHandler(Filters.photo, self.client))
        self.kill_process_thread.start()
        self.updater.start_polling()
        self.updater.idle()

    def standalone_process_provider(self):

        job_rate = 5
        while True:
            time.sleep(job_rate)
            if self.in_process_clients:
                self.kill_client_process()
                continue
            if self.clients:
                self.clean_client_garbage()

    def broad_cast_message(self, message):
        for client in self.verify_clients.values():
            self.updater.bot.send_message(client.uid, message)

    def filter_clients(self, clt, curr_time, max_time):

        if clt.in_process \
                or not clt.last_show_up \
                or clt.is_verify \
                or clt.is_admin \
                or clt.uid not in self.waiting_for_approved:
            return True
        subtract = curr_time - clt.last_show_up
        if subtract.seconds > max_time:
            return False

    def clean_client_garbage(self):
        max_time = 259200
        curr_time = datetime.datetime.now()
        self.clients = dict(
            filter(
                lambda clt: self.filter_clients(
                    clt[1], curr_time, max_time), self.clients.items()
                )
            )

        print(f"[LOG DELETE] removed  {self.clients}")

    def kill_client_process(self):
        max_time = 1800
        curr_time = datetime.datetime.now()
        for client in self.in_process_clients:
            if client.time_process_start:
                subtract_times = curr_time - client.time_process_start
                if subtract_times.seconds >= max_time:
                    client.in_process = False
                    client.time_process_start = None
                    client.killed = True
                    self.updater.bot.send_message(client.uid,
                                                  "נראה שעזבת בזמן תהליך הזמנה, ביטלתי אותה לבינתיים. הכנס כל דבר כדי להמשיך")
        self.in_process_clients = list(filter(lambda client: client.in_process, self.in_process_clients))


def main():
    api_key = "5743628298:AAH6gmGWyO4jGOr0vFxrlcMX8zic79_GCrc"
    app = App(Updater(api_key, use_context=True))
    app.listen()


if __name__ == '__main__':
    from tests import start_testing
    start_testing()

    # main()
