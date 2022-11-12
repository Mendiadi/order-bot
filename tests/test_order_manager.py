from order import OrderDetailsProtocol, OrderStatus


def test_order_manager_init(order_manager_instant):
    assert not order_manager_instant.orders
    assert not order_manager_instant.approved_orders
    assert not order_manager_instant.cancelled_orders
    assert order_manager_instant.active


def test_refresh(order_manager_instant):
    test_data = ("test","test","test","test","test",[],"test","test","test","test","test","test")
    orders = (OrderDetailsProtocol(1,OrderStatus.pending,*test_data),
              OrderDetailsProtocol(2, OrderStatus.pending, *test_data),
              OrderDetailsProtocol(3,OrderStatus.approved,*test_data),
              OrderDetailsProtocol(4,OrderStatus.canceled,*test_data),
              OrderDetailsProtocol(5,OrderStatus.canceled,*test_data),
              OrderDetailsProtocol(6,OrderStatus.pending,*test_data))
    for o in orders:
        order_manager_instant.orders[o.order_id] = o
    order_manager_instant.refresh()
    assert len(order_manager_instant.approved_orders) == 1 and order_manager_instant.approved_orders[0] ==orders[2]
    assert len(order_manager_instant.cancelled_orders) == 2 and orders[3] in order_manager_instant.cancelled_orders \
    and orders[4] in order_manager_instant.cancelled_orders
    for o in order_manager_instant.orders.values():
        assert o.status == OrderStatus.pending


