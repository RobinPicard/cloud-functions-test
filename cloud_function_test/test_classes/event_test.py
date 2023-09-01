from typing import Any, List, Union, Tuple, Type
import requests
from termcolor import colored, cprint
import json
from cloud_function_test.matching import partial_matching
from .base_test import BaseFunctionTest


class EventFunctionTest(BaseFunctionTest):
    """Class representing a test for an event-triggered function"""

    def __init__(self, *args) -> None:
        raise NotImplementedError("Event-triggered functions are not available yet, coming soon")
