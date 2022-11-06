from menu_models import MenuProtocol
from enums_schemas import Status, MenuState
from menu_models.bot_active_talk import OrderObj
from menu_models.constant_messages import *
from product_item import Stock


class OrderStatus:
    approved = 1
    canceled = 2
    pending = 3


class OrderStates:
    product_state = 1
    amount_state = 2
    phone_state = 3
    address_state = 4


class OrderMenu(MenuProtocol):
    def __init__(self, stock):
        super(OrderMenu, self).__init__(stock)
        self.msg_stage: str = order_menu_stage_msg
        self.state = None
        self.queue = [OrderStates.address_state, OrderStates.phone_state,
                      OrderStates.amount_state,
                      OrderStates.product_state]
        self.cart = []
        self.reply_msg = ""
        self.order = OrderObj([],"","",None)
        print(f"[LOG] state list -  {self.queue}")
        # todo constant message for each msg in state!!!!

    def show(self):
        return self.msg_stage + f"\n {self.stock.get_stock()}" + "הכנס שם מוצר:"

    def handle(self, bot,message, sender) -> str:
        if self.queue:
            self.state = self.queue.pop()
        print(f"[LOG] state -  {self.state}")
        print(f"[LOG] data -  {message}")
        if self.state == OrderStates.product_state:
            product = self.stock.get_product(message)
            if product:
                self.reply_msg = f" נוסף לעגלה{message}"
                self.cart.append(product)
                self.order.cart = self.cart
                self.reply_msg = "הכנס כמות"

            else:
                self.reply_msg = f"אין מוצר במלאי  הכנס מוצר תקין:"
                self.queue.append(self.state)

        elif self.state == OrderStates.amount_state:
            if int(self.cart[0].ammount) < int(message):
                self.reply_msg = "הכנס כמות שוב:"
                self.queue.append(self.state)
                bot.reply_text("אין מספיק במלאי ")
            else:
                self.order.cart = {"p":self.cart[0].name,"amount": message}
                self.reply_msg = f"בחרת להוסיף  {message}"
                self.reply_msg = "הכנס פאלפון:"
        elif self.state == OrderStates.phone_state:

            self.reply_msg = "הכנס כתובת:"
            # todo if phone is valid -> keep going
            self.order.phone = message
        elif self.state == OrderStates.address_state:
            self.order.address = message
            print(self.order)

            return MenuState.main
        bot.reply_text(self.reply_msg)
        return Status.wait
