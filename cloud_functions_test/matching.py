import re
from typing import Any
from typing import List
from typing import Tuple
from typing import Type
from typing import Union
from typing import _SpecialForm


def partial_matching(expected: Any, actual: Any) -> bool:
    """
    Return whether the actual object matches the expected object
    The function is recursive to be able to treat lists and dicts
    Supports the use of regex patterns
    Supports the use of Ellipsis in the expected object for partial matching
    Supports the use of types (either native or typing) in the expected object
    """

    # modify instance tuples as expected into lists because tuple is not json serializable
    if isinstance(expected, tuple):
        expected = list(expected)

    # basic types
    try:
        if isinstance(actual, expected):
            return True
    except TypeError:
        pass

    # typing.Any
    if isinstance(expected, _SpecialForm) and expected._name == "Any":
        return True

    # typing.Union
    if hasattr(expected, '__origin__') and expected.__origin__ is Union:
        return any(partial_matching(t, actual) for t in expected.__args__)

    # typing.List
    if hasattr(expected, '__origin__') and expected.__origin__ is list:
        if not isinstance(actual, list):
            return False
        element_type = expected.__args__[0]
        return all(partial_matching(element_type, a) for a in actual)

    # typing.Tuple
    if hasattr(expected, '__origin__') and expected.__origin__ is tuple:
        # tuple is not json-serializable so it's transformed into a list
        if not isinstance(actual, list):
            return False
        element_types = expected.__args__
        if len(element_types) != len(actual):
            return False
        return all(
            partial_matching(element_type, a)
            for a, element_type in zip(actual, element_types)
        )

    # typing.Dict
    if hasattr(expected, '__origin__') and expected.__origin__ is dict:
        if not isinstance(actual, dict):
            return False
        key_type, value_type = expected.__args__
        return all(
            partial_matching(key_type, k) and partial_matching(value_type, v)
            for k, v in actual.items()
        )

    # instance regex
    if isinstance(expected, re.Pattern) and isinstance(actual, str):
        return bool(expected.match(actual))

    # instance list
    elif isinstance(expected, list):
        if Ellipsis in expected:
            expected = [item for item in expected if item != Ellipsis]
            actual = actual[:len(expected)]
        if len(expected) != len(actual):
            return False
        return all(partial_matching(e, a) for e, a in zip(expected, actual))

    # instance dict
    elif isinstance(expected, dict):
        if not Ellipsis in expected and not expected.keys() == actual.keys():
            return False
        else:
            return all(partial_matching(expected[key], actual[key]) for key in expected if not expected[key] == Ellipsis)

    # for all other types
    return expected == actual
