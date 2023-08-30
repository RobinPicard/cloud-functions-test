from importlib import import_module
from typing import Any, List, Union, Tuple, Type
import requests
from requests import Response
from termcolor import colored, cprint
import json


class Test:
    """
    A Test class for handling various testing attributes.
    """
    ATTRIBUTES = {
        "payload": (dict, list),
        "headers": (dict),
        "status_code": (int),
        "output": (dict, list, str, Exception),
        "display_output_success": (bool)
    }

    def __init__(self, user_defined_test_class: Type) -> None:
        """Initialize the Test object with attributes from a user-defined test class."""
        self.name = user_defined_test_class.__name__
        self.response = None
        self.initialize_attributes(user_defined_test_class)
        self.validate_attributes()

    @staticmethod
    def get_class_attr(obj: Type, attr: str) -> Any:
        """Get an attribute from a class if it exists, otherwise return None."""
        return getattr(obj, attr) if hasattr(obj, attr) else None

    def initialize_attributes(self, user_defined_test_class: Type) -> None:
        """Initialize attributes on the Test instance based on those of the user-defined class."""
        for attr, _ in self.ATTRIBUTES.items():
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
        for attr, expected_type in self.ATTRIBUTES.items():
            value = getattr(self, attr)
            if value is not None and not isinstance(value, expected_type):
                raise TypeError(f"Attribute {attr} must be of type {self.format_possible_types(expected_type)}")

    def make_post_request(self, url: str) -> None:
        """
        Make a post request to the url provided with self.headers and the self.payload as parameters.
        Save the response in self.response
        """
        headers = self.headers if self.headers else {}
        self.response = requests.post(
            url,
            headers=headers,
            json=self.payload
        )

    @staticmethod
    def extract_response_output(response: requests.Response) -> Union[Exception, str, dict]:
        """
        Get the output from a Reponse object.
        Return the Exception class is the output corresponds to the underlying function crashing.
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
        return response_output


    def check_response_validity(self, error_logs: str) -> Tuple[str, str]:
        """
        Check the validity of the request's response compared to the expected values.
        Print out whether the test passed or failed and returns the status and the detailled
        logs in case of failure or if the user asked for the output to be printed out.
        """
        response_status = self.response.status_code
        response_output = self.extract_response_output(self.response)
        response_time = self.response.elapsed.total_seconds()

        status = "passed"
        display_message = []

        # assess general status (passed or failed)
        if (
            (self.status_code and self.status_code != response_status)
            or (self.output and self.output != response_output)
            or (not self.output and response_output == Exception)
        ):
            status = "failed"
            print(f"test {self.name} in {response_time}s: ", colored("FAILED", 'red'))
            display_message.append(colored(f"test {self.name}", "cyan"))
        else:
            print(f"test {self.name} in {response_time}s: ", colored("PASSED", 'green'))         

        # add the detailled logs for different types of failure
        if self.status_code and self.status_code != response_status:
            display_message.append(f"Unexpected status code")
            display_message.append(f"- expected: {self.status_code}")
            display_message.append(f"- received: {response_status}")
        if self.output and self.output != response_output and response_output != Exception:
            display_message.append(f"Unexpected output")
            display_message.append(f"- expected: {self.output}")
            display_message.append(f"- received: {error_logs if error_logs else response_output}")
        if response_output == Exception and self.output != Exception:
            display_message.append(f"Function crashed")
            display_message.append(f"{error_logs}")
        # add the output to the logs in case of success if display_output_success == True
        if status == "passed" and self.display_output_success:
            display_message.append(colored(f"test {self.name}", "cyan"))
            display_message.append("Output:")
            display_message.append(f"{response_output}")           

        return (status, "\n".join(display_message))      


def import_tests(module_name: str) -> List[Test]:
    """Import user-defined test classes from a module and create Test instances."""
    module = import_module(module_name)
    user_defined_test_classes = [
        obj for _, obj
        in module.__dict__.items()
        if isinstance(obj, type)
    ]
    if not user_defined_test_classes:
        raise Exception(f"No class is defined in your {module_name}.py file")
    return [Test(cls) for cls in user_defined_test_classes]
