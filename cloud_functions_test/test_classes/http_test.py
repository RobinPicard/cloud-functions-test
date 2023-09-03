import json
import re
from typing import Any, List, Union, Tuple, Type

import requests
from termcolor import colored, cprint

from .base_test import BaseFunctionTest
from ..matching import partial_matching




class HttpFunctionTest(BaseFunctionTest):
    """Class representing a test for an http-triggered function"""

    def __init__(self, *args) -> None:
        super().__init__(*args)

    @property
    def attributes(self) -> dict:
        """
        Dict containing as keys each possible input attributes of the user-defined class for the given test type
        and as values the associated possible types for the attribute
        """
        attr = {
            "data": [dict, list],
            "headers": [dict],
            "status_code": [int],
            "output": [dict, list, str, re.Pattern],
        }
        return {
            **super().attributes,
            **attr
        }

    def make_post_request(self, url: str) -> None:
        """
        Make a post request to the url provided with self.headers and the self.data as parameters.
        Save the response in self.response
        """
        params = {'url': url}
        if self.headers is not None:
            params['headers'] = self.headers
        if self.data is not None:
            params['json'] = self.data
        self.response = requests.post(**params)

    def check_response_validity(self, error_logs: str, standard_logs: str) -> Tuple[str, str]:
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

        # assess general status (passed or failed) regardless of the type of success/failure
        if (
            ((response_output == Exception) != (self.error or False))
            or (self.status_code is not None and self.status_code != response_status)
            or (self.output is not None and not partial_matching(self.output, response_output))
        ):
            status = "failed"
            print(f"test {self.name} in {response_time}s: ", colored("FAILED", 'red'))
            display_message.append(colored(f"test {self.name}", "cyan"))
            if standard_logs: display_message.append(f"{standard_logs}")
        else:
            print(f"test {self.name} in {response_time}s: ", colored("PASSED", 'green'))         

        # add some detailled logs for different types of failure
        if (response_output == Exception) and not self.error:
            display_message.append(f"Function crashed")
            display_message.append(f"{error_logs}")
        elif (response_output != Exception) and self.error:
            display_message.append(f"Function did not crash while an error was expected")
            display_message.append(f"- received: {response_status}, {response_output}")
        else:
            if self.status_code is not None and self.status_code != response_status:
                display_message.append(f"Unexpected status code")
                display_message.append(f"- expected: {self.status_code}")
                display_message.append(f"- received: {response_status}")
            if self.output is not None and not partial_matching(self.output, response_output):
                display_message.append(f"Unexpected output")
                display_message.append(f"- expected: {self.output}")
                display_message.append(f"- received: {response_output}")

        # add the output to the logs in case of success if display_logs == True
        if status == "passed" and self.display_logs:
            display_message.append(colored(f"test {self.name}", "cyan"))
            if standard_logs: display_message.append(f"{standard_logs}")
            display_message.append("Output:")
            display_message.append(f"{response_output}, {response_status}")           

        return (status, "\n".join(display_message))      
