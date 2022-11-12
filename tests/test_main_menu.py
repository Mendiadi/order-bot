import pytest

import product_item
from menu_models.constant_messages import main_stage_msg, ERROR_MSG
from enums_schemas import *

@pytest.mark.parametrize("msg,expected",[
    ("/start",Status.init),("1",None),("2",MenuState.order_menu),
    ("3",MenuState.login_menu),("#",MenuState.main)
])
def test_menu_init(main_menu_instant,virtual_bot,msg,expected,create_virtual_stock):
    main_menu_instant.stock.load()
    assert main_menu_instant.handle(virtual_bot,msg,None,None) == expected


def test_menu_error(main_menu_instant,virtual_bot):
    assert main_menu_instant.handle(virtual_bot,"d",None,None) == Status.error
    assert virtual_bot.m_reply_text == ERROR_MSG

def test_order_no_stock(main_menu_instant,stock_instant,virtual_bot):
    assert main_menu_instant.handle(virtual_bot, "2", None, None) == MenuState.main
    assert virtual_bot.m_reply_text == "אין מוצרים זמינים"

def test_get_stock(main_menu_instant,virtual_bot):
    main_menu_instant.handle(virtual_bot,"1",None,None)
    assert virtual_bot.m_reply_text is None
    main_menu_instant.stock.add_product(product_item.Product("test",10))
    main_menu_instant.handle(virtual_bot,"1",None,None)
    assert "test" in virtual_bot.m_reply_text


