from flask import Flask,request,jsonify,render_template,redirect
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = "pass"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///orders.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes=5)

db = SQLAlchemy(app)

class Schemas:
    ...

class CreateOrder(Schemas):
    def __init__(self,status):
        self.status = status

class OrderView(Schemas):
    def __init__(self,order_id,status):
        self.order_id = order_id
        self.status = status

class CreateProduct(Schemas):
    def __init__(self,name,amount):
        self.name = name
        self.amount = amount

class ProductView(Schemas):
    def __init__(self,id,name,amount):
        self.id = id
        self.name = name
        self.amount = amount

class Error(Schemas):
    def __init__(self,msg,code):
        self.msg = msg
        self.code = code

    def pack(self) -> tuple[str,int]:
        return self.msg, self.code

class products(db.Model):
    _id = db.Column("id",db.Integer,primary_key=True)
    name = db.Column(db.String(100))
    amount = db.Column(db.Integer)
    def __init__(self,name,amount):
        self.name = name
        self.amount = amount

class orders(db.Model):
    order_id = db.Column("order_id",db.Integer,primary_key=True)
    status = db.Column("status",db.Integer)
    # client_username = db.Column("client_username",db.String(50))
    # client_id = db.Column("client_id",db.String)
    # date = db.Column("date",db.String)
    # admin_id = db.Column("admin_id",db.String)
    # admin_username = db.Column("admin_username",db.String)
    # products: list
    # amount_of_product: str
    # phone_number= db.Column("phone_number",db.String)
    # city: str
    # street: str
    # home_number: str
    # notes: str
    def __init__(self,
                 status,

                ):
        self.status = status
        # self.client_username = client_username
        # self.client_id =client_id
        # self.date =date
        # self.admin_id = admin_id
        # self.admin_username = admin_username
        # self.phone_number =phone_number



@app.route("/")
def init_app():
    return "helo"

@app.route("/product",methods=["POST"])
def add_product():
    new_product = products(request.json['name'],request.json['amount'])
    db.session.add( new_product)
    db.session.commit()
    return {"id": new_product._id,"name": new_product.name,"amount": new_product.amount}, 201


@app.route("/product",methods=["GET"])
def get_products():
    products_ = products.query.filter_by().all()
    if not products_:
        return []
    res = []
    for p in products_:
        res.append({"id":p._id,"name": p.name, "amount": p.amount})
    return res


@app.route("/product/<name>",methods=["GET"])
def get_product(name):
    p = products.query.filter_by(name=name).first()
    if not p:
        return "product not found",404
    return {"id":p._id,"name": p.name, "amount": p.amount}

@app.route("/product/<name>",methods=["PUT"])
def update_product(name):
    p = products.query.filter_by(name=name).first()
    if not p:
        return Error("product not found", 404).pack()
    p.name = request.json["name"]
    p.amount = request.json["amount"]
    db.session.add(p)
    db.session.commit()
    return {"id": p._id, "name": p.name, "amount": p.amount}

@app.route("/product/<name>",methods=["DELETE"])
def delete_product(name):
    p_found = products.query.filter_by(name = name).first()
    if p_found:
        db.session.delete(p_found)
        db.session.commit()
        return "deleted", 204
    else:
        return Error("product not found", 404).pack()

@app.route("/order",methods=["GET"])
def get_orders():
    orders_found = orders.query.filter_by().all()
    if not orders_found:
        return []
    res = []
    for order in orders_found:
        res.append({"order_id": order.order_id, "status": order.status})
    return res

@app.route("/order/<order_id>",methods=['GET'])
def get_order(order_id):

    order_found = orders.query.filter_by(order_id=order_id).first()
    if order_found:
        return {"order_id":order_found.order_id,"status":order_found.status}
    else: return Error("order not found", 404).pack()


@app.route("/order",methods=['POST'])
def post_order():

    new_order = orders(request.json['status'])
    db.session.add(new_order)
    db.session.commit()
    return {"order_id":new_order.order_id,"status":new_order.status}, 201


@app.route("/order/<order_id>",methods=["DELETE"])
def delete_order(order_id):
    order_found = orders.query.filter_by(order_id = order_id).first()
    if order_found:
        db.session.delete(order_found)
        db.session.commit()
        return "deleted", 204
    else:
        return Error("order not found", 404).pack()

@app.route("/order/<order_id>",methods=["PUT"])
def update_order(order_id):
    order_ = orders.query.filter_by(order_id=order_id).first()
    if not order_:
        return Error("order not found", 404).pack()
    order_.status = request.json["status"]
    db.session.add(order_)
    db.session.commit()
    return {"order_id":order_.order_id,"status":order_.status}, 204



if __name__ == '__main__':
    with app.app_context() as a:
        db.create_all()
        a.app.run(debug=True)

