from typing import Any, Dict, List


class CorrectInput:
    data = {"a": 1}
    headers = {'Content-Type': 'application/json'}
    status_code = 200
    output = {"a": 1, "b": 2}

class IncorrectInput:
    data = {1: 2}
    headers = {'Content-Type': 'application/json'}
    status_code = 400

class IncorrectInputTypingEllipsis:
    data = {"a": [{"a": 1}], "b": 1, "c": 1, "d": 1}
    headers = {'Content-Type': 'application/json'}
    status_code = 200
    output = {"a": List[Dict[str, int]], "b": Any, Ellipsis:Ellipsis}

class CrashInput:
    data = ["a"]
    headers = {'Content-Type': 'application/json'}
    error = True 

class OopsUnintendedError:
    data = {"a": "1"}
    headers = {'Content-Type': 'application/json'}
    status_code = 200
    output = {"a": 1, "b": 2}
