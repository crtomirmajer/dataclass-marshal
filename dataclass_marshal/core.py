import datetime
import decimal
import json
from typing import Any, Callable, Dict, Iterable, List, Set, Tuple, TypeVar, Union, get_type_hints
import uuid

import dataclasses

MarshalledPayload = Union[Dict, List, str, float, int, None]
Marshaller = Callable[[Any], MarshalledPayload]
Unmarshaller = Callable[[MarshalledPayload], Any]

NONE_TYPE = type(None)
UNION_TYPE = type(Union)
T = TypeVar('T')

_json_encoder = json.JSONEncoder()
_registered_dataclasses = set()
_registered_type_marshallers = {}
_registered_type_unmarshallers = {}


def dataclass(cls: T) -> T:
    dataclasses.dataclass(cls)
    _registered_dataclasses.add(cls)
    cls.__marshallable_schema__ = _get_schema(cls)
    return cls


def register(typ: type, marshaller: Marshaller, unmarshaller: Unmarshaller) -> None:
    _registered_type_marshallers[typ] = marshaller
    _registered_type_unmarshallers[typ] = unmarshaller


def marshal(obj: Any) -> MarshalledPayload:
    typ = type(obj)
    if typ in _registered_type_marshallers:
        return _registered_type_marshallers[typ](obj)
    elif obj is None:
        return None
    elif isinstance(obj, (bool, int, float, complex, str)):
        return obj
    elif isinstance(obj, (list, tuple)):
        return [marshal(val) for val in obj]
    elif isinstance(obj, set):
        return sorted(marshal(val) for val in obj)
    elif isinstance(obj, dict):
        return {key: marshal(val) for key, val in obj.items()}
    elif isinstance(obj, (bytearray, bytes)):
        return obj.hex()
    elif typ in _registered_dataclasses:
        return {field: marshal(getattr(obj, field))
                for field in typ.__marshallable_schema__}
    return _json_encoder.encode(obj)


def unmarshal(data: MarshalledPayload, typs: Union[type, Iterable[type]]) -> Any:
    if not isinstance(typs, Iterable):
        typs = (typs,)

    if data is None and NONE_TYPE in typs:
        return data

    for typ in typs:
        if typ in _registered_type_unmarshallers:
            return _registered_type_unmarshallers[typ](data)
        elif typ in _registered_dataclasses:
            kwargs = {
                field: unmarshal(data.get(field), types)
                for field, types in typ.__marshallable_schema__.items()
            }
            return typ(**kwargs)
        elif typ in {bool, int, float, complex, str}:
            if isinstance(data, (bool, int, float, complex, str)):
                return data
            continue
        elif typ is Any:
            return data
        elif _issubclass_safe(typ, bytes) or _issubclass_safe(typ, bytearray):
            bs = bytearray.fromhex(data)
            return typ(bs)

        args = typ.__args__
        if isinstance(typ, UNION_TYPE):
            return unmarshal(data, args)
        elif _issubclass_safe(typ, Dict):
            return {
                unmarshal(key, args[0]): unmarshal(val, args[1])
                for key, val in data.items()
            }
        elif _issubclass_safe(typ, List):
            return [unmarshal(val, args) for val in data]
        elif _issubclass_safe(typ, Set):
            return {unmarshal(val, args) for val in data}
        elif _issubclass_safe(typ, Tuple):
            return tuple(unmarshal(val, args) for val in data)
    raise ValueError(f'Unable to unmarshall "{data}" as "{typs}"')


def _issubclass_safe(cls, typ: type):
    try:
        return issubclass(cls, typ)
    except Exception:
        return False


def _get_schema(cls: type) -> Dict[str, Union[type, Iterable[type]]]:
    types = {}
    for field, typ in get_type_hints(cls).items():
        if isinstance(typ, type(Union)):
            types[field] = typ.__args__
        else:
            types[field] = typ
    return types


register(uuid.UUID, lambda x: x.hex, lambda x: uuid.UUID(hex=x))
register(datetime.datetime, lambda x: x.timestamp(), lambda x: datetime.datetime.fromtimestamp(x))
register(decimal.Decimal, lambda x: str(x), lambda x: decimal.Decimal(x))
