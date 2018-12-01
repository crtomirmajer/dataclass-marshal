import pytest

from dataclass_marshal.core import marshal, unmarshal
import tests.definitions as defs


@pytest.mark.parametrize('input, expected', [
    (defs.product_1_marshalled, defs.product_1),
    (defs.product_2_marshalled, defs.product_2),
    (defs.product_3_marshalled, defs.product_3),
    (defs.product_4_marshalled, defs.product_4),
    (defs.product_5_marshalled, defs.product_5),
    (defs.product_6_marshalled, defs.product_6),
])
def test_unmarshal_simple(input, expected):
    obj = unmarshal(input, defs.Product)
    data = marshal(obj)
    assert data == input
    assert data == marshal(expected)


@pytest.mark.parametrize('input, expected', [
    (defs.cart_item_1_marshalled, defs.cart_item_1),
    (defs.cart_item_2_marshalled, defs.cart_item_2),
    (defs.cart_item_3_marshalled, defs.cart_item_3),
    (defs.cart_item_4_marshalled, defs.cart_item_4),
    (defs.cart_item_5_marshalled, defs.cart_item_5),
    (defs.cart_item_6_marshalled, defs.cart_item_6),
])
def test_unmarshal_union(input, expected):
    obj = unmarshal(input, defs.CartItem)
    data = marshal(obj)
    assert data == input
    assert data == marshal(expected)


@pytest.mark.parametrize('input, expected', [
    (defs.user_1_marshalled, defs.user_1),
    (defs.user_2_marshalled, defs.user_2),
    (defs.user_3_marshalled, defs.user_3),
    (defs.user_4_marshalled, defs.user_4),
    (defs.user_5_marshalled, defs.user_5),
])
def test_unmarshal_optional(input, expected):
    obj = unmarshal(input, defs.User)
    data = marshal(obj)
    assert data == input
    assert data == marshal(expected)


@pytest.mark.parametrize('input, expected', [
    (defs.shop_1_marshalled, defs.shop_1),
    (defs.shop_2_marshalled, defs.shop_2),
    (defs.shop_3_marshalled, defs.shop_3),
])
def test_unmarshal_complex(input, expected):
    obj = unmarshal(input, defs.Shop)
    data = marshal(obj)
    assert data == input
    assert data == marshal(expected)