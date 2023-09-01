import os
import sys
import time
import subprocess
from importlib import import_module
from typing import List, Tuple, Type

from requests import ConnectionError

from .exceptions import MissingTestClassError
from .exceptions import InvalidTestClassTypeError
from .test_classes.base_test import BaseFunctionTest
from .test_classes.event_test import EventFunctionTest
from .test_classes.http_test import HttpFunctionTest
from .utils import log_reader
from .utils import print_centered_text


def import_user_classes(module_name: str) -> list:
    """Import and return user-defined test classes from module_name"""
    sys.path.insert(0, os.getcwd())
    try:
        module = import_module(module_name)
    except ModuleNotFoundError:
        error_message = (
            f"Could not find the module {module_name}\n"
            "Make sure your test classes are located in this module "
            "or modify the name of the module in which the package will look for test classes "
            "by settings the value of cloud_function_test.module or by using the --module argument in the cli."
        )
        raise ModuleNotFoundError(error_message)
    user_defined_test_classes = [
        obj for _, obj
        in module.__dict__.items()
        if isinstance(obj, type)
    ]
    if not user_defined_test_classes:
        raise MissingTestClassError(f"No class is defined in your module {module_name}")
    return user_defined_test_classes


def create_tests(user_defined_classes: object, test_type: str) -> List[BaseFunctionTest]:
    """Create and return BaseFunctionTest instances from user-defined classes"""
    if test_type == "http":
        return [HttpFunctionTest(cls) for cls in user_defined_classes]
    if test_type == "event":
        return [EventFunctionTest(cls) for cls in user_defined_classes]
    raise InvalidTestClassTypeError("The type parameter must be equal either to 'http' or to 'event'")


def start_server(entrypoint: str, port: int) -> object:
    """Use function-framework to launch a server with the user's cloud function locally"""
    try:
        process = subprocess.Popen(
            ['functions_framework', f'--target={entrypoint}', f'--port={port}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(1)
        return process
    except ConnectionError:
        error_message = (
            f"Could not start the local server. Make sure that the port {port} of localhost is not already used "
            f"and that the entrypoint function of your Cloud Function is called {entrypoint}. Otherwise, you can "
            "change both of those parameters in your test file or in the cli."
        )
        raise ConnectionError(error_message)


def run_tests(process: object, local_url: str, tests: Type[BaseFunctionTest]) -> Tuple[List, List]:
    """Run all tests, return lists with the failures and the successes"""
    results = []
    for test in tests:
        try:
            test.make_post_request(local_url)
        except ConnectionError:
            error_message = (
                f"Could not run your Cloud Function. Make sure that the entrypoint you provided "
                "(main by default) matches the name of your function."
            )
            raise Exception(error_message)
        error_logs = log_reader(process.stderr)
        validity_result = test.check_response_validity(error_logs)
        results.append(validity_result)
    failures = [item for item in results if item[0] == 'failed']
    successes = [item for item in results if item[0] == 'passed']
    return (failures, successes)


def display_detailed_results(failures: list, successes: list) -> None:
    """Given lists of failures and successes, print their results"""
    print(f"*** {len(successes)} tests passed and {len(failures)} failed ***")
    if failures:
        print_centered_text("FAILED")
        for result in failures:
            print(result[1])
    if successes:
        print_centered_text("PASSED")
        for result in successes:
            print(result[1])
