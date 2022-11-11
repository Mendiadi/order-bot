import dataclasses
import datetime
import random


def generate_id_order(orders) -> int:
    number = random.randint(1000, 9999)
    while number in orders:
        number = random.randint(1000, 9999)
    return number


def get_time() -> str:
    day_name, mouth, day, time_, year = datetime.datetime.now().ctime().replace("  ", " ").split(" ")
    return f"{day_name}  {day}/{mouth}/{year} {time_}"


@dataclasses.dataclass
class Address:
    street: str
    number: str
    city: str


admin = "458614153"


@dataclasses.dataclass
class OrderSchema:
    client_name: str
    client_id: str
    products: list
    amount: str
    phone: str
    address: Address

    def prepare_saving(self):
        return {
            "product_name": self.products,
            "amount": self.amount,
            "phone": self.phone,
            "address": self.address.__dict__
        }


class OrderStatus:
    approved = 1
    canceled = 2
    pending = 3


@dataclasses.dataclass
class OrderDetailsProtocol:
    order_id: int
    status: int
    client_username: str
    client_id: str
    date: str
    admin_id: str
    admin_username: str
    products: list
    amount_of_product: str
    phone_number: str
    city: str
    street: str
    home_number: str
    notes: str


class OrderManager:
    def __init__(self):
        self.orders = {}
        self.approved_orders = []
        self.cancelled_orders = []

    def refresh(self):
        print(f"[LOG CRITICAL] {self.orders}")
        for order in self.orders.values():
            if order.status == OrderStatus.approved:
                self.approved_orders.append(order)

            elif order.status == OrderStatus.canceled:
                self.cancelled_orders.append(order)

        self.orders = dict(filter(lambda order: order[1] == OrderStatus.pending, self.orders.items()))

        print(self.orders)
        print(self.approved_orders)

    async def notification_order(self, bot, status,reason):
        if status == OrderStatus.approved:
            for order in self.approved_orders:
                bot.send_message(order.client_id, f" {reason} {order.order_id}" + "ההזמנה שלך אושרה לפרטים מספר הזמנה הוא:")
        else:
            for order in self.cancelled_orders:
                bot.send_message(order.client_id, f"{reason} {order.order_id}" + "ההזמנה שלך בוטלה")


    def order_notification(self, bot, order: OrderDetailsProtocol):

        bot.send_message(admin,
                         f" date: {order.date}\nid: {order.order_id}\nusername:  @{order.client_username} \n userid: {order.client_id}\n"
                         f"product: {order.products}\n amount: {order.amount_of_product}\n"
                         f"phone:{order.phone_number}\naddress:{order.street} {order.home_number} {order.city},\n note for manager/driver: {order.notes}")
        self.approved_orders.clear()

    def create_order(self, order: OrderSchema, notes):
        new_order = OrderDetailsProtocol(
            generate_id_order(self.orders), OrderStatus.pending, order.client_name,
            order.client_id, get_time(),

            "some user", "some user", order.products, str(len(order.products)), order.phone,
            order.address.city, order.address.street, order.address.number, notes
        )
        self.orders[new_order.order_id] = new_order
        print(new_order)
        return new_order


order_manager_golobal = OrderManager()


def get_order_system() -> OrderManager:
    return order_manager_golobal
