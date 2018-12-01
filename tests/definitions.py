import datetime
from typing import Any, Dict, List, Optional, Tuple, Union
import uuid

from dataclass_marshal.core import dataclass, register


# Test Classes

class Dimensions:
    def __init__(self, height, width, depth):
        self.height = height
        self.width = width
        self.depth = depth


@dataclass
class Product:
    id: int
    attributes: Dict[str, Any]


@dataclass
class CartItem:
    product: Product
    quantity: Union[int, float, Dict[str, Union[int, float, Tuple[Union[int, float]]]]]


@dataclass
class User:
    id: int
    email: Optional[str]
    cart: Optional[Dict[int, CartItem]]


@dataclass
class Shop:
    created: datetime.datetime
    sid: uuid.UUID
    users: Optional[List[User]]
    products: Optional[List[Product]]


# Test Objects


dt = datetime.datetime(year=2018, month=11, day=17, hour=13, minute=37)
uid = uuid.uuid4()

# Product 1

product_1 = Product(1, {})
product_1_marshalled = {'id': 1, 'attributes': {}}

# Product 2

product_2 = Product(2, {'age': 5, 'created': dt})
product_2_marshalled = {
    'id': 2,
    'attributes': {'age': 5, 'created': dt.timestamp()}
}

# Product 3

product_3 = Product(3, {'lifetime': {'idle': 10, 'browsing': 7, 'programming': 5}})
product_3_marshalled = {
    'id': 3,
    'attributes': {'lifetime': {'idle': 10, 'browsing': 7, 'programming': 5}}
}

# Product 4

product_4 = Product(4, {'sizes': {'S', 'M', 'L'}})
product_4_marshalled = {
    'id': 4,
    'attributes': {'sizes': ['L', 'M', 'S']}
}

# Product 5

product_5 = Product(5, {'models': ['LS', 'GS'], 'serial': uid})
product_5_marshalled = {
    'id': 5,
    'attributes': {'models': ['LS', 'GS'], 'serial': uid.hex}
}

# Product 6

product_6 = Product(6, {'dimensions': Dimensions(5, 4, 3)})
product_6_marshalled = {
    'id': 6,
    'attributes': {'dimensions': {'height': 5, 'width': 4, 'depth': 3}}
}

# Cart Item 1

cart_item_1 = CartItem(product_1, 1)
cart_item_1_marshalled = {'product': product_1_marshalled, 'quantity': 1}

# Cart Item 2

cart_item_2 = CartItem(product_2, 2.2)
cart_item_2_marshalled = {'product': product_2_marshalled, 'quantity': 2.2}

# Cart Item 3

cart_item_3 = CartItem(product_3, 33.333)
cart_item_3_marshalled = {'product': product_3_marshalled, 'quantity': 33.333}

# Cart Item 4

cart_item_4 = CartItem(product_4, {'oo': (1, 3.33)})
cart_item_4_marshalled = {
    'product': product_4_marshalled,
    'quantity': {'oo': [1, 3.33]}
}

# Cart Item 5

cart_item_5 = CartItem(product_5, {'kilogram': 1, 'pound': 2.20462})
cart_item_5_marshalled = {
    'product': product_5_marshalled,
    'quantity': {'kilogram': 1, 'pound': 2.20462}
}

# Cart Item 6

cart_item_6 = CartItem(product_6, 6.6)
cart_item_6_marshalled = {'product': product_6_marshalled, 'quantity': 6.6}

# User 1

user_1 = User(1, None, None)
user_1_marshalled = {'id': 1, 'email': None, 'cart': None}

# User 2

user_2 = User(2, 'master@disaster.com', None)
user_2_marshalled = {'id': 2, 'email': 'master@disaster.com', 'cart': None}

# User 3

user_3 = User(3, None, {1: cart_item_1})
user_3_marshalled = {
    'id': 3,
    'email': None,
    'cart': {1: cart_item_1_marshalled}
}

# User 4

user_4 = User(4, None, {2: cart_item_2, 3: cart_item_3, 4: cart_item_4})
user_4_marshalled = {
    'id': 4,
    'email': None,
    'cart': {2: cart_item_2_marshalled, 3: cart_item_3_marshalled, 4: cart_item_4_marshalled}
}

# User 5

user_5 = User(5, 'pro@disaster.com', {5: cart_item_5, 6: cart_item_6})
user_5_marshalled = {
    'id': 5,
    'email': 'pro@disaster.com',
    'cart': {5: cart_item_5_marshalled, 6: cart_item_6_marshalled}
}

# Shop 1

shop_1 = Shop(
    created=dt,
    sid=uuid.uuid4(),
    users=None,
    products=None
)
shop_1_marshalled = {
    'created': dt.timestamp(),
    'sid': shop_1.sid.hex,
    'users': None,
    'products': None
}

# Shop 2

shop_2 = Shop(
    created=dt,
    sid=uuid.uuid4(),
    users=[user_1, user_2],
    products=None
)
shop_2_marshalled = {
    'created': dt.timestamp(),
    'sid': shop_2.sid.hex,
    'users': [user_1_marshalled, user_2_marshalled],
    'products': None
}

# Shop 3

shop_3 = Shop(
    created=dt,
    sid=uuid.uuid4(),
    users=[user_3, user_4, user_5],
    products=[product_1, product_2, product_3, product_4, product_5, product_6]
)
shop_3_marshalled = {
    'created': dt.timestamp(),
    'sid': shop_3.sid.hex,
    'users': [user_3_marshalled, user_4_marshalled, user_5_marshalled],
    'products': [
        product_1_marshalled, product_2_marshalled, product_3_marshalled,
        product_4_marshalled, product_5_marshalled, product_6_marshalled
    ]
}

# Registered custom (un)marshallers

register(Dimensions, lambda x: x.__dict__, lambda x: Dimensions(**x))
