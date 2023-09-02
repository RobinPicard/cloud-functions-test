import re
from typing import Any
from typing import Tuple
from typing import Type
from typing import Union
from typing import List
from typing import _SpecialForm


def partial_matching(expected: Any, actual: Any) -> bool:
    """
    Return whether the actual object matches the expected object
    The function is recursive to be able to treat lists and dicts
    Supports the use of regex patterns
    Supports the use of Ellipsis in the expected object for partial matching
    Supports the use of types (either native or typing) in the expected object
    """

    # in case of a type
    if (
        isinstance(expected, type)
        or hasattr(expected, '__origin__')
        or (
            hasattr(expected, '__module__')
            and expected.__module__ == 'typing'
        )
    ):
        return is_instance_of_type(actual, expected)

    # in case of a regex
    if isinstance(expected, re.Pattern) and isinstance(actual, str):
        return bool(expected.match(actual))

    # after having checked the 2 above, if the objects have different types they are necessarily not matching
    elif type(expected) != type(actual):
        return False

    # in case of a list
    elif isinstance(expected, list):
        if Ellipsis in expected:
            expected = {item for item in expected if item != Ellipsis}
            for item in expected:
                return any(partial_matching(item, element) for element in actual)
        else:
            if len(expected) != len(actual):
                return False
            return all(partial_matching(a, b) for a, b in zip(expected, actual))

    # in case of a dict
    elif isinstance(expected, dict):
        if not Ellipsis in expected and not expected.keys() == actual.keys():
            return False
        else:
            return all(partial_matching(expected[key], actual[key]) for key in expected if not expected[key] == Ellipsis)

    # for all other types
    return expected == actual



def is_instance_of_type(value: Any, type_hint: Any) -> bool:
    """
    Return whether the value is an instance of the type_hint
    Supports both basic types and types from the typing package
    The function is recursive to support more complex typing types (Union, List...)
    May not work for the most complex cases
    """

    # in case type_hint is a basic type
    try:
        if isinstance(value, type_hint):
            return True
    except TypeError:
        pass

    # in case type_hint = Any
    if isinstance(type_hint, _SpecialForm):
        if type_hint._name == "Any":
            return True

    # in case type_hint = Union
    if hasattr(type_hint, '__origin__') and type_hint.__origin__ is Union:
        return any(is_instance_of_type(value, t) for t in type_hint.__args__)

    # in case type_hint = List
    if hasattr(type_hint, '__origin__') and type_hint.__origin__ is list:
        if not isinstance(value, list):
            return False
        element_type = type_hint.__args__[0]
        return all(is_instance_of_type(element, element_type) for element in value)

    # in case type_hint = Dict
    if hasattr(type_hint, '__origin__') and type_hint.__origin__ is dict:
        if not isinstance(value, dict):
            return False
        key_type, value_type = type_hint.__args__
        return all(
            is_instance_of_type(k, key_type) and is_instance_of_type(v, value_type)
            for k, v in value.items()
        )

    # in case type_hint = Tuple
    if hasattr(type_hint, '__origin__') and type_hint.__origin__ is tuple:
        if not isinstance(value, tuple):
            return False
        element_types = type_hint.__args__
        if len(element_types) != len(value):
            return False
        return all(
            is_instance_of_type(element, element_type)
            for element, element_type in zip(value, element_types)
        )

    # cases not treated
    return False
