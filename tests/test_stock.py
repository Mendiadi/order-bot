import os

import json_func
from product_item import Stock,Product

smple_file = "test_env.json"

def test_product_class():
    obj = Product("sample",10)
    assert obj.name == "sample" and obj.ammount == 10
    assert obj.save_ready() == {"ammount":obj.ammount,"name":obj.name}

def test_stock_init(stock_instant):
    assert not stock_instant.stock
    assert not stock_instant.products
    assert stock_instant.out_put_file == smple_file

def test_load_valid_file(stock_instant):
    p = Product("test",10)
    json_func.write_to_json({"Stock": [p.save_ready()]}, smple_file, 1)
    stock_instant.load()
    assert stock_instant.products[0] == p
    assert stock_instant.stock == {"Stock":[p.save_ready()]}


def test_load_first_file(stock_instant):
    p = Product("test", 10)
    if smple_file in os.listdir():
        os.remove(smple_file)
    stock_instant.load()
    assert smple_file in os.listdir()
    assert stock_instant.stock == {"Stock": []}


def test_get_product(stock_instant,create_virtual_stock):
    stock_instant.load()
    a =stock_instant.get_product("test2")
    b = stock_instant.get_product("avi")
    assert b is None
    assert a.name == "test2" and a.ammount == 1

def test_add_product(stock_instant):

    p = Product("sample",10)
    stock_instant.add_product(p)
    assert p in stock_instant.products

def test_remove_product(stock_instant,create_virtual_stock):
    p = Product("sample1",10)
    stock_instant.load()
    stock_instant.add_product(p)
    stock_instant.commit()
    a = stock_instant.remove_product("sample1")
    b = stock_instant.remove_product("fail")
    stock_instant.load()
    assert a
    assert not b
    assert "sample1" not in stock_instant.products
