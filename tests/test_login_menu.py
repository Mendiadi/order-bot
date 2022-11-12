from enums_schemas import MenuState


def test_login_menu_init(login_menu_instant):
    assert login_menu_instant.secret_key == "pass"


def test_wrong_pass(login_menu_instant,virtual_bot):
    assert login_menu_instant.handle(virtual_bot,"somthing",None,None) is None
    assert virtual_bot.m_reply_text == "סיסמא שגויה , נסה שוב."

def test_back_main_menu(login_menu_instant,virtual_bot):
    assert login_menu_instant.handle(virtual_bot,"#",None,None) == MenuState.main

def test_pass_good(login_menu_instant,virtual_bot):
    assert login_menu_instant.handle(virtual_bot, "pass", None, None)  == MenuState.admin_man
    assert virtual_bot.m_reply_text == "התחברות בוצעה בהצלחה"
    assert virtual_bot.bot.message_chat_id == (1, 1)