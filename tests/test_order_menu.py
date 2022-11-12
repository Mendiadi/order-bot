import datetime

import order
from enums_schemas import MenuState, Status
from main import Client
from menu_models.bot_order_menu import OrderStates
from product_item import Product

def test_make_order(order_menu_instant,create_virtual_stock,virtual_bot):
    p_name = "test3"
    p_name2 = "test"
    p_amount = 1
    p_amount_2 = 2
    phone = "01234"
    address = "galim 12 metula"
    note = "im like it hot"
    order_ = order.OrderSchema("adi","1", [Product(p_name,p_amount),Product(p_name2,p_amount_2-1)],
                               "2", phone, order.Address(*address.split(" ")))
    actions = (p_name,p_amount,"1",p_name2,p_amount_2,p_amount_2-1,"3","2",phone,address,note)
    order_menu_instant.stock.load()
    order_menu_instant.me = Client("1",None,True,datetime.datetime.now(),True)
    order_menu_instant.order.client_id = "1"
    order_menu_instant.order.client_name = "adi"
    order_menu_instant.handle(virtual_bot,"fail",None,None)
    assert virtual_bot.m_reply_text == f"אין מוצר במלאי  הכנס מוצר תקין:"
    for msg in actions:
        a = order_menu_instant.handle(virtual_bot,msg,None,None)
        print(virtual_bot.m_reply_text)
    assert order_menu_instant.order == order_
    assert a == MenuState.main
    assert not order_menu_instant.cart
    assert not order_menu_instant.me.in_process and order_menu_instant.me.time_process_start is None

def test_order_menu_init(order_menu_instant):
    assert order_menu_instant.stack ==  [OrderStates.note_state,
                      OrderStates.address_state,
                      OrderStates.phone_state,
                      OrderStates.add_product,
                      OrderStates.amount_state,
                      OrderStates.product_state

                      ]
    assert order_menu_instant.state is None
    assert order_menu_instant.reply_msg == ""


def test_on_product_active(order_menu_instant, create_virtual_stock, virtual_bot):
    order_menu_instant.stock.load()
    order_menu_instant.me =  Client("123",None,True)
    assert order_menu_instant.on_product("test2",virtual_bot) == Status.wait
    p = order_menu_instant.stock.get_product("test2")
    assert p
    assert order_menu_instant.me.in_process and order_menu_instant.me.time_process_start \
    and order_menu_instant.me in  order_menu_instant.app.in_process_clients
    assert order_menu_instant.reply_msg == "הכנס כמות" and p in order_menu_instant.cart




def test_on_product_no_stock_active(order_menu_instant, create_virtual_stock, virtual_bot):
    order_menu_instant.stock.load()
    order_menu_instant.me =  Client("123",None,True)
    assert order_menu_instant.on_product("banana",virtual_bot) == Status.wait
    p = order_menu_instant.stock.get_product("banana")
    assert not p
    assert order_menu_instant.me.in_process and order_menu_instant.me.time_process_start \
    and order_menu_instant.me in  order_menu_instant.app.in_process_clients
    assert order_menu_instant.reply_msg ==  f"אין מוצר במלאי  הכנס מוצר תקין:" and p not in order_menu_instant.cart

def test_on_product_inactive(order_menu_instant,create_virtual_stock,virtual_bot):
    order_menu_instant.order_manager.active = False
    order_menu_instant.stock.load()
    order_menu_instant.me = Client("123",None,True)
    assert order_menu_instant.on_product("test",virtual_bot) == MenuState.main
    assert virtual_bot.m_reply_text == "אין אפשרות להזמין כרגע."



def test_on_amount_valid(order_menu_instant,virtual_bot,create_virtual_stock):
    order_menu_instant.stock.load()
    order_menu_instant.me =  Client("123",None,True)

    p = order_menu_instant.stock.get_product("test3")
    assert p
    order_menu_instant.cart.append(p)
    assert order_menu_instant.on_amount("1",virtual_bot) == Status.wait
    assert p.ammount >= "1"
    assert order_menu_instant.cart[0].ammount == "1"
    assert order_menu_instant.reply_msg == "רוצה לבחור מוצר נוסף? 1. כן 2. לא"
    assert virtual_bot.m_reply_text == f"בחרת להוסיף  {'1'}"

def test_on_amount_invalid(order_menu_instant,virtual_bot,create_virtual_stock):
    order_menu_instant.stock.load()
    order_menu_instant.me =  Client("123",None,True)

    p = order_menu_instant.stock.get_product("test3")
    assert p
    order_menu_instant.cart.append(p)
    assert p.ammount <= 5
    order_menu_instant.state = OrderStates.amount_state
    assert order_menu_instant.on_amount("5",virtual_bot) == Status.wait

    assert order_menu_instant.cart[0].ammount == p.ammount
    assert order_menu_instant.reply_msg == "הכנס כמות שוב:"
    assert virtual_bot.m_reply_text == "אין מספיק במלאי "
    print(order_menu_instant.stack)
    assert order_menu_instant.stack[-1] == OrderStates.amount_state


def test_add_product_yes(order_menu_instant,virtual_bot):

    assert  order_menu_instant.on_add_product_again("1",virtual_bot) is None
    assert order_menu_instant.stack == [OrderStates.note_state,
                                        OrderStates.address_state,
                                        OrderStates.phone_state,
                                        OrderStates.add_product,
                                        OrderStates.amount_state,
                                        OrderStates.product_state

                                        ]
    assert order_menu_instant.state is None
    assert order_menu_instant.reply_msg == ""

def test_add_product_no(order_menu_instant,virtual_bot):
    assert order_menu_instant.on_add_product_again("2", virtual_bot) == Status.wait
    assert order_menu_instant.reply_msg == "הכנס פאלפון:"

def test_add_product_invalid(order_menu_instant,virtual_bot):
    order_menu_instant.state = OrderStates.add_product
    assert order_menu_instant.on_add_product_again("fail", virtual_bot) == Status.wait
    assert virtual_bot.m_reply_text == "משהו שגוי בבחירתך"
    assert  order_menu_instant.stack[-1] == OrderStates.add_product
    assert order_menu_instant.reply_msg == "רוצה לבחור מוצר נוסף? 1. כן 2. לא"


def test_on_phone(order_menu_instant,virtual_bot):
    assert order_menu_instant.on_phone("01234",virtual_bot) == Status.wait
    assert order_menu_instant.reply_msg == "הכנס כתובת:"

def test_on_adress(order_menu_instant,virtual_bot):
    assert order_menu_instant.on_address("galim 12 metula",virtual_bot) == Status.wait
    assert order_menu_instant.reply_msg ==  "זה הזמן לרשום הערה למנהל אם יש."

def test_on_note(order_menu_instant,virtual_bot):
    ...



