import datetime

from flask import Flask, request, jsonify, render_template, redirect
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "pass"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orders.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)


def get_time() -> str:
    day_name, mouth, day, time_, year = datetime.datetime.now().ctime().replace("  ", " ").split(" ")
    return f"{day_name}  {day}/{mouth}/{year} {time_}"


class Schemas:
    def to_json(self):
        return {k: v for k, v in self.__dict__.items()}


class CreateOrder(Schemas):
    def __init__(self,
                 status,
                 client_username=None,
                 client_id=None,
                 products=None,
                 phone_number=None
                 ):
        self.status = status
        self.client_username = client_username
        self.client_id = client_id
        self.products = products
        self.phone_number = phone_number



class OrderView(Schemas):
    def __init__(self, order_id,
                 status,
                 client_username=None,
                 client_id=None,
                 date=None,
                 products=None,
                 phone_number=None
                 ):
        self.order_id = order_id
        self.status = status
        self.client_username = client_username
        self.client_id = client_id
        self.date = date
        self.products = products
        self.phone_number = phone_number


    @staticmethod
    def create(obj):
        return OrderView(obj.order_id,
                         obj.status,
                         obj.client_username, obj.client_id, obj.date, obj.phone_number
                         )


class CreateProduct(Schemas):
    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class ProductView(Schemas):
    def __init__(self, id, name, amount):
        self.id = id
        self.name = name
        self.amount = amount


class Error(Schemas):
    def __init__(self, msg, code):
        self.msg = msg
        self.code = code

    def pack(self) -> tuple[str, int]:
        return self.msg, self.code


class clients(db.Model):
    uid = db.Column(db.String(100),primary_key=True)
    status = db.Column(db.String(10))

    def __init__(self,uid,status="pending"):
        self.uid = uid
        self.status = status

class products(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    amount = db.Column(db.Integer)

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount


class orders(db.Model):
    order_id = db.Column("order_id", db.Integer, primary_key=True)
    status = db.Column("status", db.Integer)
    client_username = db.Column("client_username", db.String(100))
    client_id = db.Column("client_id", db.String(100))
    date = db.Column("date", db.String(100))
    products = db.Column("products",db.PickleType)
    phone_number = db.Column("phone_number", db.String(100))


    def __init__(self,
                 status,
                 client_username=None,
                 client_id=None,
                 date=None,
                 products=None,
                 phone_number=None,

                 ):
        self.status = status
        self.client_username = client_username
        self.client_id = client_id
        self.date = date
        self.products = products
        self.phone_number = phone_number




@app.route("/")
def init_app():
    return "helo"

@app.route("/client",methods=["POST"])
def add_client():

    client = clients(request.json['uid'])
    if clients.query.filter_by(uid=client.uid).first():
        return "client already in", 400
    db.session.add(client)
    db.session.commit()
    return {"uid":client.uid,"status":client.status}

@app.route("/client",methods=["GET"])
def get_clients():
    clients_ = clients.query.filter_by().all()
    if not clients_:
        return []
    res = []
    for p in clients_:
        res.append({"uid":p.uid,"status":p.status})
    return res

@app.route("/product", methods=["POST"])
def add_product():
    new_product = products(request.json['name'], request.json['amount'])
    db.session.add(new_product)
    db.session.commit()
    return {"id": new_product._id, "name": new_product.name, "amount": new_product.amount}, 201

@app.route("/client/<uid>", methods=["GET"])
def get_client(uid):
    c = clients.query.filter_by(uid=uid).first()
    if not c:
        return "client not found", 404
    return {"uid":c.uid,"status":c.status}

@app.route("/client/<uid>",methods=["DELETE"])
def delete_client(uid):
    c_found = products.query.filter_by(uid=uid).first()
    if c_found:
        db.session.delete(c_found)
        db.session.commit()
        return "deleted", 204
    else:
        return Error("client not found", 404).pack()

@app.route("/client/getbystatus/<status>",methods=["GET"])
def get_clients_by_status(status):
    clients_ = clients.query.filter_by(status = status).all()
    if not clients_:
        return []
    res = []
    for p in clients_:
        res.append({"uid":p.uid,"status":p.status})
    return res


@app.route("/client/<uid>",methods=["PUT"])
def update_client(uid):
    c = clients.query.filter_by(uid=uid).first()
    if not c:
        return "client not found", 404
    c.status = request.json.get("status",None)

    db.session.add(c)
    db.session.commit()
    return {"uid":c.uid,"status":c.status}

@app.route("/product", methods=["GET"])
def get_products():
    products_ = products.query.filter_by().all()
    if not products_:
        return []
    res = []
    for p in products_:
        res.append({"id": p._id, "name": p.name, "amount": p.amount})
    return res


@app.route("/product/<name>", methods=["GET"])
def get_product(name):
    p = products.query.filter_by(name=name).first()
    if not p:
        return "product not found", 404
    return {"id": p._id, "name": p.name, "amount": p.amount}




@app.route("/product/<name>", methods=["PUT"])
def update_product(name):
    p = products.query.filter_by(name=name).first()
    if not p:
        return Error("product not found", 404).pack()
    p.name = request.json["name"]
    p.amount = request.json["amount"]
    db.session.add(p)
    db.session.commit()
    return {"id": p._id, "name": p.name, "amount": p.amount}


@app.route("/product/<name>", methods=["DELETE"])
def delete_product(name):
    p_found = products.query.filter_by(name=name).first()
    if p_found:
        db.session.delete(p_found)
        db.session.commit()
        return "deleted", 204
    else:
        return Error("product not found", 404).pack()


@app.route("/order", methods=["GET"])
def get_orders():
    orders_found = orders.query.filter_by().all()
    if not orders_found:
        return []
    res = []
    for order in orders_found:
        res.append(OrderView.create(order).to_json())
    return res


@app.route("/order/<order_id>", methods=['GET'])
def get_order(order_id):
    order_found = orders.query.filter_by(order_id=order_id).first()
    if order_found:
        return OrderView.create(order_found).to_json()
    else:
        return Error("order not found", 404).pack()


@app.route("/order", methods=['POST'])
def post_order():
    order_created = CreateOrder(**request.json)
    new_order = orders(order_created.status, order_created.client_username
                       , order_created.client_id, get_time(), order_created.phone_number
                       )
    db.session.add(new_order)
    db.session.commit()
    return OrderView.create(new_order).to_json(), 201


@app.route("/order/<order_id>", methods=["DELETE"])
def delete_order(order_id):
    order_found = orders.query.filter_by(order_id=order_id).first()
    if order_found:
        db.session.delete(order_found)
        db.session.commit()
        return "deleted", 204
    else:
        return Error("order not found", 404).pack()


@app.route("/order/<order_id>", methods=["PUT"])
def update_order(order_id):
    order_ = orders.query.filter_by(order_id=order_id).first()
    if not order_:
        return Error("order not found", 404).pack()
    order_.status = request.json["status"]
    db.session.add(order_)
    db.session.commit()
    return {"order_id": order_.order_id, "status": order_.status}, 204


if __name__ == '__main__':
    with app.app_context() as a:
        db.create_all()
        a.app.run(debug=True)
