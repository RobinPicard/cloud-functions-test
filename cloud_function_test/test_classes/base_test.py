from abc import abstractmethod
from typing import Any, Tuple, Type

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
    @abstractmethod
    def attributes(self) -> dict:
        """
        Dict containing as keys each possible input attributes of the user-defined class for the given test type
        and as values the associated possible types for the attribute
        """
        pass

    @staticmethod
    def get_class_attr(obj: Type, attr: str) -> Any:
        """Get an attribute from a class if it exists, otherwise return None."""
        return getattr(obj, attr) if hasattr(obj, attr) else None

    def initialize_attributes(self, user_defined_test_class: Type) -> None:
        """Initialize attributes on the Test instance based on those of the user-defined class."""
        for attr, _ in self.attributes.items():
            setattr(self, attr, self.get_class_attr(user_defined_test_class, attr))

    @staticmethod
    def format_possible_types(types: Tuple) -> str:
        """Turn a tuple of type names into a human-readable string."""
        number_types = len(types)
        output = ""
        for index, item in enumerate(types):
            if index == number_types - 1:
                output += ' or '
            elif index != 0:
                output += ', '
            output += item.__name__
        return output

    def validate_attributes(self) -> None:
        """Check the validity of the attributes provided."""
        for attr, expected_type in self.attributes.items():
            value = getattr(self, attr)
            if value is not None and not isinstance(value, expected_type) and value not in expected_type:
                error_message = f"In class {self.name}, attribute '{attr}' must be of type {self.format_possible_types(expected_type)}"
                raise InvalidAttributeTypeError(error_message)

    @abstractmethod
    def make_post_request(self, url: str) -> None:
        """Make a post request to the url provided. Save the response in self.response"""
        pass

    @abstractmethod
    def check_response_validity(self, error_logs: str) -> Tuple[str, str]:
        """
        Check the validity of the request's response compared to the expected values.
        Return the status of the test and the detailed message that should be printed out
        """
        pass
