from .bot_base_menu import MenuProtocol
from .bot_admin_menu import AdminMenu
from order import OrderStatus

from .constant_messages import admin_order_man_stage
from order import get_order_system
from enums_schemas import Status, MenuState


class AdminOrderManagerStates:
    view_orders = 1
    choose_order = 2
    config_order = 3
    change_order = 4
    on_enter_order = 5
    on_msg_state = 6
    start_stop_sys = 7


class AdminOrderManager(MenuProtocol):
    actions = {
        "1": AdminOrderManagerStates.view_orders,
        "2": AdminOrderManagerStates.choose_order,
        "3":AdminOrderManagerStates.start_stop_sys,
        Status.back_to_main_menu: MenuState.admin_man
    }

    def __init__(self, stock):
        super(AdminOrderManager, self).__init__(stock)
        self.msg_stage = admin_order_man_stage

        self.state_callable = {
            AdminOrderManagerStates.view_orders: self.on_view_orders,
            AdminOrderManagerStates.choose_order: self.on_choose_order,
            AdminOrderManagerStates.change_order: self.on_change_order,
            AdminOrderManagerStates.on_enter_order: self.on_enter_order,
            AdminOrderManagerStates.on_msg_state: self.on_msg_for_updated_order_status,
            AdminOrderManagerStates.start_stop_sys:self.on_start_stop_sys
        }
        self.reply_msg = "חושב"
        self.order_manager = get_order_system()
        self.temp_status = None
        self.on_exit()

    def on_start_stop_sys(self,message,bot):
        if self.order_manager.active:
            self.reply_msg = "חסמת את האופציה לשלוח הזמנות. לביטול חסימה בחר 3 שוב"
        else:
            self.reply_msg = "אפשרת את האופציה לשלוח הזמנות. לחסימה בחר 3 שוב"
        self.order_manager.active = not self.order_manager.active

    def on_view_orders(self, message, bot):
        orders = self.order_manager.orders.items()
        if not orders:
            self.reply_msg = f"אין הזמנות ממתינות"
        else:
            self.reply_msg = f"{[f'orders: id: {order.order_id} products: {order.products} phone: {order.phone_number} address: {order.street}'for _, order in orders]}"
        self.on_exit()
        return MenuState.order_manage

    def on_enter_order(self, message, bot):
        if message.isdigit():
            self.order_number_temp = int(message)
            self.state = AdminOrderManagerStates.config_order
            self.reply_msg = "מספר נקלט"
            self.on_config_order(message, bot)
        else:
            self.reply_msg = "מספר הזמנה לא חוקי"
            self.state = AdminOrderManagerStates.choose_order
        return Status.wait

    def on_choose_order(self, message, bot):
        if not len(self.order_manager.orders):
            self.reply_msg = f"אין הזמנות ממתינות"
            return MenuState.stock_manager
        bot.reply_text("הכנס מספר הזמנה:\n")

        self.state = AdminOrderManagerStates.on_enter_order
        return Status.wait

    def on_exit(self):
        self.state = None
        self.order_temp = None
        self.order_number_temp = None
        self.temp_status = None

    def update_status(self, status):
        self.temp_status = self.order_manager.orders[self.order_temp.order_id].status = status
        self.order_manager.refresh()
        self.state = AdminOrderManagerStates.on_msg_state
        self.reply_msg = "הכנס סיבה:"
        return Status.wait

    def on_msg_for_updated_order_status(self, message, bot):
        status = self.temp_status
        print(f"[LOG CRITICAL] status is {status}")
        self.order_manager.notification_order(bot.bot, status, message)
        self.reply_msg = "תודה"
        self.on_exit()
        return MenuState.order_manage

    def on_change_order(self, message, bot):
        print(f"[LOG CRITICAL] {message} on change")
        if message == "1":

            return self.update_status(OrderStatus.approved)
        elif message == "2":
            return self.update_status(OrderStatus.canceled)
        else:
            self.reply_msg = "משהו שגוי בבחירתך"
            self.state = AdminOrderManagerStates.change_order

    def on_config_order(self, message, bot):
        pending = self.order_manager.orders

        self.reply_msg = "בחר אופציה"
        if self.order_number_temp in pending:
            self.order_temp = pending[self.order_number_temp]
            print("[LOG CRITICAL] ", type(self.order_temp))
            self.state = AdminOrderManagerStates.change_order
            bot.reply_text(f"{self.order_number_temp} ממתינה " + "לאישור הקש 1 .\n לביטול הקש 2")
        else:
            self.reply_msg = "הזמנה לא נמצאה"
            self.state = None

            return MenuState.stock_manager

    def handle(self, bot, message, sender, context) -> str:

        if message in self.actions and self.state != AdminOrderManagerStates.change_order and \
                self.state != AdminOrderManagerStates.on_msg_state:
            self.state = self.actions[message]
            if message == Status.back_to_main_menu:
                return self.actions[message]
        try:
            if int(self.state) not in self.state_callable:
                bot.reply_text("שגיאה קרתה מצטער..")
                return MenuState.order_manage
        except (TypeError, ValueError):

            bot.reply_text("שגיאה קרתה מצטער..")
            return MenuState.order_manage
        state = self.state_callable[int(self.state)](message, bot)
        bot.reply_text(self.reply_msg)
        return state

    def show(self):
        return self.msg_stage
