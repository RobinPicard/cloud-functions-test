import json
from abc import abstractmethod
from typing import Any, Tuple, Type, Union

from requests import Response

from ..exceptions import InvalidAttributeTypeError


class BaseFunctionTest:
    """
    Base class for the function test classes
    Initialized with a user-defined test class
    """

    def __init__(self, user_defined_test_class: Type) -> None:
        """Initialize the Test object with attributes from a user-defined test class."""
        self.name = user_defined_test_class.__name__
        self.response = None
        self.initialize_attributes(user_defined_test_class)
        self.validate_attributes()

    @property
    def attributes(self) -> dict:
        """
        Dict containing as keys each possible input attributes of the user-defined class for the given test type
        and as values the associated possible types for the attribute
        """
        return {
            "error": [bool],
            "display_logs": [bool]
        }

    @staticmethod
    def get_class_attr(obj: Type, attr: str) -> Any:
        """Get an attribute from a class if it exists, otherwise return None."""
        return getattr(obj, attr) if hasattr(obj, attr) else None

    def initialize_attributes(self, user_defined_test_class: Type) -> None:
        """Initialize attributes on the Test instance based on those of the user-defined class."""
        for attr, _ in self.attributes.items():
            setattr(self, attr, self.get_class_attr(user_defined_test_class, attr))

    @staticmethod
    def format_possible_types(types: list) -> str:
        """Turn a tuple of type names into a human-readable string."""
        number_types = len(types)
        output = ""
        for index, item in enumerate(types):
            if index == number_types - 1 and index != 0:
                output += ' or '
            elif index != 0:
                output += ', '
            output += item.__name__
        return output

    def validate_attributes(self) -> None:
        """Check the validity of the attributes provided."""
        for attr, expected_types in self.attributes.items():
            value = getattr(self, attr)
            if (
                value is not None
                and not any(isinstance(value, expected_type) for expected_type in expected_types)
                and value not in expected_types
            ):
                error_message = f"In class {self.name}, attribute '{attr}' must be of type {self.format_possible_types(expected_types)}"
                raise InvalidAttributeTypeError(error_message)

    @abstractmethod
    def make_post_request(self, url: str) -> None:
        """Make a post request to the url provided. Save the response in self.response"""
        pass

    @staticmethod
    def extract_response_output(response: Response) -> Union[Type[Exception], dict, Any]:
        """
        Get the output from a Reponse object.
        Return the Exception class as the output if the function crashed.
        Otherwise, return a dict if the output was a json and a str in all other cases.
        """
        response_output = response.text
        if response_output.startswith("500 Internal Server Error"):
            response_output = Exception
        else:
            try:
                response_output = response.json()
            except json.JSONDecodeError:
                pass
        if isinstance(response_output, int):
            response_output = str(response_output)
        return response_output

    @abstractmethod
    def check_response_validity(self, error_logs: str, standard_logs: str) -> Tuple[str, str]:
        """
        Check the validity of the request's response compared to the expected values.
        Return the status of the test and the detailed message that should be printed out
        """
        pass
