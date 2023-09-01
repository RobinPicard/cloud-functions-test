from typing import Any, List, Union, Tuple, Type
import requests
from termcolor import colored, cprint
import json
from cloud_function_test.matching import partial_matching
from .base_test import BaseFunctionTest
import re


class HttpFunctionTest(BaseFunctionTest):
    """Class representing a test for an http-triggered function"""

    def __init__(self, *args) -> None:
        super().__init__(*args)

    @property
    def attributes(self) -> dict:
        return {
            "payload": (dict, list, str),
            "headers": (dict),
            "status_code": (int),
            "output": (dict, list, str, re.Pattern, Exception),
            "display_output_success": (bool)
        }

    def make_post_request(self, url: str) -> None:
        """
        Make a post request to the url provided with self.headers and the self.payload as parameters.
        Save the response in self.response
        """
        params = {'url': url}
        if self.headers:
            params['headers'] = self.headers
        if self.payload:
            params['json'] = self.payload
        self.response = requests.post(**params)

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
        if isinstance(response_output, int):
            response_output = str(response_output)
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
            or (self.output and not partial_matching(self.output, response_output))
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
