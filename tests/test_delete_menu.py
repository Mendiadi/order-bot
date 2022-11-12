from enums_schemas import MenuState


def test_back_to_main_menu(delete_menu_instant,virtual_bot):
    assert delete_menu_instant.handle(virtual_bot,"#",None,None) == MenuState.admin_man


def test_delete_product(delete_menu_instant,create_virtual_stock):
    delete_menu_instant.stock.load()
    name = "fail"
    name_valid = "test"
    assert delete_menu_instant.stock.get_product(name) is None
    assert delete_menu_instant.delete_product(name) == f"אין מוצר כזה במלאי - נא לבדוק את מה ששלחת{name}"
    assert delete_menu_instant.delete_product(name_valid) ==  f"נמחק בהצלחה בהצלחה{name_valid}"
    assert delete_menu_instant.stock.get_product(name_valid) is None


def test_delete_product_handle(delete_menu_instant,create_virtual_stock,virtual_bot):
    delete_menu_instant.stock.load()

    name_valid = "test"

    assert delete_menu_instant.handle(virtual_bot,name_valid,None,None) == MenuState.admin_man
    assert virtual_bot.m_reply_text ==  delete_menu_instant.msg


def test_delete_product_handle_invalid(delete_menu_instant,virtual_bot):
    name = "fail"
    assert delete_menu_instant.stock.get_product(name) is None
    assert delete_menu_instant.handle(virtual_bot, name, None, None) == MenuState.admin_man
