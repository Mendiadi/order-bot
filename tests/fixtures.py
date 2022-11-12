import os

import pytest

import json_func
from main import App, Client
from menu_models import LoginMenu
from menu_models.bot_delete_menu import DeleteMenu
from menu_models.bot_demo_menu import DemoMenu
from menu_models.bot_order_menu import OrderMenu
from order import OrderManager
from product_item import Stock,Product
from menu_models.bot_main_menu import MainMenu

class VirtualBotEnv:
    def __init__(self):
        self.message_chat_id = None
    def delete_message(self, msg, id_):
        self.message_chat_id = msg, id_

    def send_message(self,admin,order):...

class VirtualBotForTestEnv:

    def __init__(self):
        self.m_reply_text = None
        self.chat_id = 1
        self.message_id = 1

        self.bot = VirtualBotEnv()

    def reply_text(self,msg):
        self.m_reply_text = msg



@pytest.fixture
def virtual_bot():
    return VirtualBotForTestEnv()

@pytest.fixture
def create_virtual_stock():
    l = [Product("test",1).save_ready(),
         Product("test2",1).save_ready(),
         Product("test3",1).save_ready()]
    json_func.write_to_json({"Stock":l},"test_env.json" , 1)
    yield
    if "test_env.json" in os.listdir():
        os.remove("test_env.json")


@pytest.fixture
def stock_instant() -> Stock:
    stock = Stock("test_env.json")
    return stock


@pytest.fixture
def main_menu_instant(stock_instant) -> MainMenu:
    menu = MainMenu(stock_instant)
    return menu


@pytest.fixture
def login_menu_instant(stock_instant) -> LoginMenu:
    menu = LoginMenu(stock_instant)
    return menu

@pytest.fixture
def delete_menu_instant(stock_instant) -> DeleteMenu:
    menu = DeleteMenu(stock_instant)
    return menu

@pytest.fixture
def demo_menu_instant(stock_instant) -> DemoMenu:
    menu = DemoMenu(stock_instant)
    return menu

@pytest.fixture
def order_manager_instant() -> OrderManager:
    order_man = OrderManager()
    return order_man

@pytest.fixture
def app_instant():
    return App(None)

@pytest.fixture
def order_menu_instant(stock_instant,app_instant) -> OrderMenu:
    menu = OrderMenu(stock_instant,app_instant,None)
    return menu