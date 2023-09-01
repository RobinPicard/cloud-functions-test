import json
from typing import Any, List, Union, Tuple, Type

import requests
from termcolor import colored, cprint

from .base_test import BaseFunctionTest
from ..matching import partial_matching


class EventFunctionTest(BaseFunctionTest):
    """Class representing a test for an event-triggered function"""

    def __init__(self, *args) -> None:
        super().__init__(*args)

    @property
    def attributes(self) -> dict:
        return {
            "event": [dict],
            "context": [dict],
            "error": [bool],
        }

    def make_post_request(self, url: str) -> None:
        """
        Make a post request to the url provided with self.event and self.context as data
        Save the response in self.response
        """
        params = {'url': url, 'headers': {'Content-Type': 'application/json'}}
        data = {}
        if self.event:
            data['event'] = self.event
        if self.context:
            data['context'] = self.context
        if data:
            params['json'] = data
        self.response = requests.post(**params)

    def check_response_validity(self, error_logs: str) -> Tuple[str, str]:
        """
        Check whether the function created error logs and compare it to the value of self.error
        Print out whether the test passed or failed and returns the detailled logs in case of failure.
        """
        response_time = self.response.elapsed.total_seconds()
        status = "passed"
        display_message = []

        if (
            (not error_logs and self.error)
            or (error_logs and not self.error)
        ):
            status = "failed"
            print(f"test {self.name} in {response_time}s: ", colored("FAILED", 'red'))
            display_message.append(colored(f"test {self.name}", "cyan"))
            if error_logs:
                display_message.append(f"Function crashed")
                display_message.append(f"{error_logs}")
            else:
                display_message.append(f"Function did not crash while an error was expected")
        else:
            print(f"test {self.name} in {response_time}s: ", colored("PASSED", 'green'))

        return (status, "\n".join(display_message))
