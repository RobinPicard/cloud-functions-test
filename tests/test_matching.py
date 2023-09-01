import re
from typing import Any, Union, List, Tuple, _SpecialForm

import pytest

from cloud_function_test.matching import is_instance_of_type, partial_matching


def test_partial_matching():
    # basic
    assert partial_matching(5, 5) == True
    assert partial_matching("hello", "hello") == True
    assert partial_matching(5, 4) == False
    assert partial_matching(5, "hello") == False
    assert partial_matching("hello", ["hello"]) == False
    # regex
    assert partial_matching(re.compile(r'^\d+$'), '123') == True
    assert partial_matching(re.compile(r'^\d+$'), '123a') == False
    assert partial_matching(re.compile(r'^\d+$'), 123) == False
    # list with Ellipsis
    assert partial_matching([1, 2, Ellipsis], [1, 2, 3, 4, 5]) == True
    assert partial_matching([1, 2, Ellipsis], [1, 2]) == True
    assert partial_matching([1, 2, Ellipsis], [2, 3, 4, 5]) == False
    # list without Ellipsis
    assert partial_matching([1, 2, 3], [1, 2, 3]) == True
    assert partial_matching([1, 2, 3], [1, 2]) == False
    assert partial_matching([1, 2, 3], [1, 2, 3, 4]) == False
    # dict with Ellipsis
    assert partial_matching({'a': 1, 'b': Ellipsis}, {'a': 1, 'b': 2}) == True
    assert partial_matching({'a': 1, Ellipsis: Ellipsis}, {'a': 1, 'b': 2}) == True
    assert partial_matching({'a': 1, 'b': Ellipsis}, {'a': 1}) == False
    # dict without Ellipsis
    assert partial_matching({'a': 1, 'b': 2}, {'a': 1, 'b': 2}) == True
    assert partial_matching({'a': 1, 'b': 2}, {'a': 1}) == False
    assert partial_matching({'a': 1, 'b': 2}, {'a': 1, 'b': 3}) == False
    assert partial_matching({'a': 1, 'b': 2}, {'a': 1, 'b': 2, 'c': 3}) == False
    # types
    assert partial_matching(int, 5) == True
    assert partial_matching(int, '5') == False
    assert partial_matching(str, 'hello') == True
    # more complex
    assert partial_matching([1, {'a': Ellipsis, Ellipsis:Ellipsis}], [1, {'a': 1, 'b': 2}]) == True
    assert partial_matching({'a': [1, 2, Ellipsis]}, {'a': [1, 2, 3, 4]}) == True
    assert partial_matching(re.compile(r'^\d+$'), '123') == True


def test_is_instance_of_type():
    # basic type
    assert is_instance_of_type(5, int) == True
    assert is_instance_of_type(5.5, float) == True
    assert is_instance_of_type("hello", str) == True
    assert is_instance_of_type(5, str) == False
    assert is_instance_of_type(5, list) == False
    assert is_instance_of_type([5], list) == True
    assert is_instance_of_type({"a": "b"}, dict) == True
    assert is_instance_of_type({"a"}, set) == True
    # any
    assert is_instance_of_type(5, Any) == True
    assert is_instance_of_type("hello", Any) == True
    assert is_instance_of_type([1, 2, 3], Any) == True
    # union
    assert is_instance_of_type(5, Union[int, str]) == True
    assert is_instance_of_type("hello", Union[int, str]) == True
    assert is_instance_of_type(5.5, Union[int, str]) == False
    # list
    assert is_instance_of_type([1, 2, 3], List[int]) == True
    assert is_instance_of_type([1, "hello"], List[int]) == False
    assert is_instance_of_type("hello", List[int]) == False
    # tuple
    assert is_instance_of_type((1, "hello"), Tuple[int, str]) == True
    assert is_instance_of_type((1, 2), Tuple[int, str]) == False
    assert is_instance_of_type([1, 2, "hello"], Tuple[int, int]) == False
    # more complex
    assert is_instance_of_type([1, 2, 3], Union[List[int], str]) == True
    assert is_instance_of_type((1, [2, 3]), Tuple[int, List[int]]) == True
    assert is_instance_of_type((1, [2, "hello"]), Tuple[int, List[int]]) == False
