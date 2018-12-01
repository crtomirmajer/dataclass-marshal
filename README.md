# dataclass-marshal

Python package for marshalling (serializing) instances of classes decorated with `@dataclass`.

### Supported serialization types

* Simple types: `bool, int, float, complex, str, bytes, bytearray`
* Container types: `Tuple, List, Set, Dict`
* Other types: `Decimal, datetime, UUID`

## Usage

```python
from typing import Any, Dict
from dataclass_marshal import dataclass, marshal, unmarshal

@dataclass
class Product:
    id: int
    attributes: Dict[str, Any]


product = Product(1, {'weight': 10})

marshalled = marshal(product)
# {'id': 1, 'attributes': {'weight': 10}}
unmarshalled = unmarshal(marshalled, Product)
# Product(id=1, attributes={'weight': 10})
```

## Support for custom (un)marshallers

For custom types and non-`@dataclass` definitions it's possible to register custom marshaller/unmarshaller.

```python

from dataclass_marshal import register, marshal

class Dimensions:
    def __init__(self, height, width, depth):
        self.height = height
        self.width = width
        self.depth = depth


register(Dimensions, marshaller=lambda x: x.__dict__, unmarshaller=lambda x: Dimensions(**x))
marshalled = marshal(Dimensions(1,2,4))
# {'height': 1, 'width': 2, 'depth': 4}
```
