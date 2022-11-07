import dataclasses
import datetime


@dataclasses.dataclass
class Address:
    street: str
    number:str
    city: str

admin = "5784227740"

@dataclasses.dataclass
class OrderSchema:
    client_name:str
    client_id:str
    product_name :str
    amount:str
    phone:str
    address:Address


    def prepare_saving(self):
        return {
            "product_name":self.product_name,
            "amount":self.amount,
            "phone":self.phone,
            "address":self.address.__dict__
        }

class OrderStatus:
    approved = 1
    canceled = 2
    pending = 3


@dataclasses.dataclass
class OrderDetailsProtocol:
    order_id:int
    status : int
    client_username:str
    client_id:str
    date:str
    admin_id:str
    admin_username:str
    product_name:str
    amount_of_product:str
    phone_number:str
    city:str
    street:str
    home_number:str




class OrderManager:
    def __init__(self):
        self.orders = {
            OrderStatus.pending: [],
            OrderStatus.canceled:[],
            OrderStatus.approved:[]
        }

    def order_notification(self,bot,order:OrderDetailsProtocol):

        bot.send_message(admin,f" id: {order.order_id}\nusername:  @{order.client_username} \n userid: {order.client_id}\n"
                          f"product: {order.product_name}\n amount: {order.amount_of_product}\n"
                          f"phone:{order.phone_number}\naddress:{order.street} {order.home_number} {order.city}")


    def create_order(self,order:OrderSchema):
        new_order = OrderDetailsProtocol(
            len(self.orders[OrderStatus.pending]),OrderStatus.pending,order.client_name,
            order.client_id, datetime.datetime.now().strftime("dd/mm/yyyy"),
            "some user","some user",order.product_name,order.amount,order.phone,
            order.address.city,order.address.street,order.address.number
        )
        self.orders[new_order.status].append(new_order)
        return new_order



