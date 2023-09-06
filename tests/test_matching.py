import re
from typing import Any
from typing import Dict
from typing import List
from typing import Tuple
from typing import Type
from typing import Union
from typing import _SpecialForm

import pytest

from cloud_functions_test.matching import partial_matching


def test_partial_matching():
    # instance basic type
    assert partial_matching(int, 5) == True
    assert partial_matching(float, 5.5) == True
    assert partial_matching(str, "hello") == True
    assert partial_matching(str, 5) == False
    assert partial_matching(list, 5) == False
    assert partial_matching(list, [5]) == True
    assert partial_matching(dict, {"a": "b"}) == True
    assert partial_matching(set, {"a"}) == True
    # instance regex
    assert partial_matching(re.compile(r'^\d+$'), '123') == True
    assert partial_matching(re.compile(r'^\d+$'), '123a') == False
    assert partial_matching(re.compile(r'^\d+$'), 123) == False
    # instance list with Ellipsis
    assert partial_matching([1, 2, Ellipsis], [1, 2, 3, 4, 5]) == True
    assert partial_matching([1, 2, Ellipsis], [1, 2]) == True
    assert partial_matching([1, 2, Ellipsis], [2, 3, 4, 5]) == False
    # instance list without Ellipsis
    assert partial_matching([1, 2, 3], [1, 2, 3]) == True
    assert partial_matching([1, 2, 3], [1, 2]) == False
    assert partial_matching([1, 2, 3], [1, 2, 3, 4]) == False
    # instance dict with Ellipsis
    assert partial_matching({'a': 1, 'b': Ellipsis}, {'a': 1, 'b': 2}) == True
    assert partial_matching({'a': 1, Ellipsis: Ellipsis}, {'a': 1, 'b': 2}) == True
    assert partial_matching({'a': 1, 'b': Ellipsis}, {'a': 1}) == False
    # instance dict without Ellipsis
    assert partial_matching({'a': 1, 'b': 2}, {'a': 1, 'b': 2}) == True
    assert partial_matching({'a': 1, 'b': 2}, {'a': 1}) == False
    assert partial_matching({'a': 1, 'b': 2}, {'a': 1, 'b': 3}) == False
    assert partial_matching({'a': 1, 'b': 2}, {'a': 1, 'b': 2, 'c': 3}) == False
    # type basic
    assert partial_matching(int, 5) == True
    assert partial_matching(int, '5') == False
    assert partial_matching(str, 'hello') == True
    # typing.Any
    assert partial_matching(Any, 5) == True
    assert partial_matching(Any, "hello") == True
    assert partial_matching(Any, [1, 2, 3]) == True
    # typing.Union
    assert partial_matching(Union[int, str], 5) == True
    assert partial_matching(Union[int, str], "hello") == True
    assert partial_matching(Union[int, str], 5.5) == False
    # typing.List
    assert partial_matching(List[int], [1, 2, 3]) == True
    assert partial_matching(List[int], [1, "hello"]) == False
    assert partial_matching(List[int], "hello") == False
    # typing.Tuple
    assert partial_matching(Tuple[int, str], [1, "hello"]) == True
    assert partial_matching(Tuple[int, str], [1, 2]) == False
    assert partial_matching(Tuple[int, int], [1, 2, "hello"]) == False
    # typing.Dict
    assert partial_matching(Dict[str, int], {"key": 1, "foo": 2}) == True
    assert partial_matching(Dict[str, int], {1: "value"}) == False
    assert partial_matching(Dict[str, int], "not_a_dict") == False
    # various / mix of several things
    assert partial_matching(Union[List[int], str], [1, 2, 3]) == True
    assert partial_matching(Tuple[int, List[int]], [1, [2, 3]]) == True
    assert partial_matching(Tuple[int, List[int]], [1, [2, "hello"]]) == False
    assert partial_matching(Tuple[int, Dict[str, list]], [1, {"a": [1, 2]}]) == True
    assert partial_matching([1, {'a': Ellipsis, Ellipsis:Ellipsis}], [1, {'a': 1, 'b': 2}]) == True
    assert partial_matching({'a': [1, 2, Ellipsis]}, {'a': [1, 2, 3, 4]}) == True
    assert partial_matching(re.compile(r'^\d+$'), '123') == True
    assert partial_matching(Tuple[dict, List[int]], [{"a": 1}, [1, 2]]) == True
    assert partial_matching(Tuple[dict, List[int]], [{"a": 1}, [1, "b"]]) == False
    assert partial_matching({"a": Tuple[List[int], Dict[str, Tuple[int, int]]]}, {"a": [[1, 2], {"a": [1, 2]}]}) == True
    assert partial_matching({"a": Tuple[dict, List[int]], "b": Any, Ellipsis:Ellipsis}, {"a": [{"a": 1}, [1, 2]], "b": 1, "c": 1}) == True
    assert partial_matching({"a": Tuple[dict, List[int]], "b": 1, Ellipsis:Ellipsis}, {"a": [{"a": 1}, [1, "a"]], "b": Any, "c": 1}) == False
    assert partial_matching(Dict[str, str], [1, 2, 3]) == False
    assert partial_matching(Tuple[int, int], [1, 2, 3]) == False
    assert partial_matching(Tuple[int, int], [1, 2]) == True