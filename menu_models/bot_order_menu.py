import datetime

from menu_models import MenuProtocol
from enums_schemas import Status, MenuState
from menu_models.constant_messages import *
from order import OrderSchema, Address, get_order_system


class OrderStates:
    product_state = 1
    amount_state = 2
    phone_state = 3
    address_state = 4
    note_state = 5
    add_product = 6
    cancel_order = Status.back_to_main_menu



class OrderMenu(MenuProtocol):

    def __init__(self, stock, app,me):
        super(OrderMenu, self).__init__(stock)
        self.order_manager = get_order_system()

        self.msg_stage: str = order_menu_stage_msg
        self.state = None
        self.stack = None
        self.cart = []
        self.reply_msg = ""
        self.state_callables = {
            OrderStates.product_state: self.on_product,
            OrderStates.amount_state: self.on_amount,
            OrderStates.phone_state: self.on_phone,
            OrderStates.address_state: self.on_address,
            OrderStates.note_state: self.on_notes,
            OrderStates.add_product: self.on_add_product_again,

        }
        self.me = me
        self.app = app




        self.order = OrderSchema(None, None, "", "", "", None)
        print(f"[LOG] state list -  {self.stack}")
        # todo constant message for each msg in state!!!!

        self.on_exit()




    def on_exit(self):
        print("on exit")
        self.stack = [OrderStates.note_state,
                      OrderStates.address_state,
                      OrderStates.phone_state,
                      OrderStates.add_product,
                      OrderStates.amount_state,
                      OrderStates.product_state

                      ]
        self.reply_msg = ""


    def show(self):
        return self.msg_stage + f"\n {self.stock.get_stock()}" + "הכנס שם מוצר:"

    def on_add_product_again(self, message, bot):
        if message == "1":
            self.on_exit()
        elif message == "2":
            self.reply_msg = "הכנס פאלפון:"
            return Status.wait
        else:
            bot.reply_text("משהו שגוי בבחירתך")
            self.stack.append(self.state)
            self.reply_msg = "רוצה לבחור מוצר נוסף? 1. כן 2. לא"
            return Status.wait

    def on_phone(self, message, bot):
        self.order.phone = message
        self.reply_msg = "הכנס כתובת:"
        # todo if phone is valid -> keep going
        return Status.wait

    def on_amount(self, message, bot):
        if int(self.cart[len(self.cart) - 1].ammount) < int(message):
            self.reply_msg = "הכנס כמות שוב:"
            self.stack.append(self.state)
            bot.reply_text("אין מספיק במלאי ")

        else:
            self.order.amount = str(len(self.cart))
            self.cart[-1].ammount = message
            self.reply_msg = "רוצה לבחור מוצר נוסף? 1. כן 2. לא"
            bot.reply_text(f"בחרת להוסיף  {message}")

        return Status.wait

    def on_notes(self, message, bot):
        self.order.products = self.cart
        order_ready = self.order_manager.create_order(self.order, message)
        self.order_manager.order_notification(bot.bot, order_ready)
        bot.reply_text(f"{self.order.prepare_saving()}")
        self.reply_msg = "ההזמנה נקלטה! מועבר לתפריט ראשי."
        self.cart = []
        self.on_restart()
        return MenuState.main

    def on_restart(self):
        self.on_exit()
        print("on restart")
        self.me.in_process = False
        self.me.time_process_start = None

        self.cart = []

    def on_address(self, message, bot):
        try:
            self.order.address = Address(*message.split(" "))
        except TypeError:
            self.order.address = Address(message, "", "")

        self.reply_msg = "זה הזמן לרשום הערה למנהל אם יש."
        return Status.wait

    def on_product(self, message, bot):
        if not self.order_manager.active:
            bot.reply_text("אין אפשרות להזמין כרגע.")
            self.on_restart()
            return MenuState.main
        if not self.me.time_process_start:
            self.me.in_process = True
            self.me.time_process_start = datetime.datetime.now()
            self.app.in_process_clients.append(self.me)
        product = self.stock.get_product(message)
        if product:
            self.reply_msg = f" נוסף לעגלה{message}"
            self.cart.append(product)

            self.reply_msg = "הכנס כמות"

        else:
            self.reply_msg = f"אין מוצר במלאי  הכנס מוצר תקין:"
            self.stack.append(self.state)
        return Status.wait

    def handle(self, bot, message, sender, context) -> str:
        if message == OrderStates.cancel_order:
            self.on_restart()
            return MenuState.main
        if self.stack:
            self.state = self.stack.pop()
        print(f"[LOG] state -  {self.state}")
        print(f"[LOG] data -  {message}")
        if not (self.order.client_id and self.order.client_name):
            self.order.client_id = sender.id
            self.order.client_name = sender.username
        callable = self.state_callables[self.state]
        state = callable(message, bot)
        if self.reply_msg:
            bot.reply_text(self.reply_msg)
        return state
