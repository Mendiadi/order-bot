from enums_schemas import MenuState
from menu_models.constant_messages import verify_menu_msg_stage

def test_demo_menu_init(demo_menu_instant):
    assert demo_menu_instant.is_finish_verify is False

def test_back_to_main(demo_menu_instant,virtual_bot):
    demo_menu_instant.handle(virtual_bot,"#",None,None)
    assert demo_menu_instant.reply_msg == verify_menu_msg_stage


def test_show_stock(virtual_bot,demo_menu_instant,create_virtual_stock):
    demo_menu_instant.stock.load()
    demo_menu_instant.handle(virtual_bot,"1",None,None)
    assert virtual_bot.m_reply_text == demo_menu_instant.stock.get_stock()


def test_show_stock_empty(virtual_bot, demo_menu_instant):
    demo_menu_instant.handle(virtual_bot, "1", None, None)
    assert virtual_bot.m_reply_text is None

def test_start_verify_process(virtual_bot,demo_menu_instant):
    assert demo_menu_instant.handle(virtual_bot,"2",None,None) == MenuState.verify
    assert demo_menu_instant.reply_msg == "תהליך אימות מתחיל..."


def test_start_verify_process_after_finish_one(virtual_bot,demo_menu_instant):
    demo_menu_instant.is_finish_verify = True
    assert demo_menu_instant.handle(virtual_bot,"2",None,None) is None
    assert virtual_bot.m_reply_text ==     "אתה ממתין לאימות"