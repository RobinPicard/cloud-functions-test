import os
import socket
import shutil
import sys
import time
import subprocess
from importlib import import_module
from typing import List, Tuple, Type

from requests import ConnectionError

from .exceptions import DifferentClassTypesError
from .exceptions import MissingTestClassError
from .exceptions import PortUnavailableError
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
            "by settings the value of cloud_functions_test.module or by using the --module argument in the cli."
        )
        raise ModuleNotFoundError(error_message)
    user_defined_classes = [
        obj for _, obj
        in module.__dict__.items()
        if isinstance(obj, type)
    ]
    if not user_defined_classes:
        raise MissingTestClassError(f"No class is defined in your module {module_name}")
    return user_defined_classes


def create_tests(user_defined_classes: List[object]) -> Tuple[List[BaseFunctionTest], Type[BaseFunctionTest]]:
    """Create and return BaseFunctionTest instances from user-defined classes + the type of the classes"""
    test_classes = []
    for c in user_defined_classes:
        if hasattr(c, "event"):
            test_classes.append(EventFunctionTest(c))
        else:
            test_classes.append(HttpFunctionTest(c))
    types = set([type(c) for c in test_classes])
    if len(types) > 1:
        raise DifferentClassTypesError
    return test_classes, types.pop()


def start_server(port: int, entrypoint: str, temp_file_path) -> object:
    """Use function-framework to launch a server with the user's cloud function locally"""
    check_port_availability(port)
    try:
        process = subprocess.Popen(
            ['functions_framework', f'--target={entrypoint}', f'--port={port}', f'--source={temp_file_path}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        time.sleep(1) # to make sure the server has time to be running
        return process
    except ConnectionError:
        error_message = (
            f"Could not start the local server. Make sure that the entrypoint function of your Cloud Function "
            "is called {entrypoint}. Otherwise, you can change this parameters in your test file or in the cli."
        )
        raise ConnectionError(error_message)


def check_port_availability(port: int) -> None:
    """Check whether the port chosen is available, raise Exception if not"""
    host = "localhost"
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)
    result = s.connect_ex((host, port))
    if result == 0:
        PortUnavailableError(f"Port {port} is already used by another process")
    else:
        pass


def create_temp_file_event(tempfile: object, source: str, entrypoint: str, event_func_entrypoint: str) -> Tuple[str, str]:
    """
    Create a temporary file with the content of the source
    Add a event_func_entrypoint function that will receive the request in the server and redirect it
    to the user'd original entrypoint after having transformed the request param into event/context
    """
    temp_file_path = tempfile.name
    with open(source, 'r') as src_file:
        with open(temp_file_path, 'w') as dest_file:
            shutil.copyfileobj(src_file, dest_file)
    with open(temp_file_path, 'a') as temp_file:
        temp_file.write(
            "\n\n"
            f"def {event_func_entrypoint}(request):\n"
            "    payload = request.get_json()\n"
            "    event = payload.get('event')\n"
            "    context = payload.get('context')\n"
            f"    {entrypoint}(event, context)\n"
            "    return('DUMMY', 200)\n"
        )
    return temp_file_path, event_func_entrypoint


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
        error_logs, standard_logs = log_reader(process)
        validity_result = test.check_response_validity(error_logs, standard_logs)
        results.append(validity_result)
    failures = [item[1] for item in results if item[0] == 'failed']
    successes = [item[1] for item in results if item[0] == 'passed']
    return (failures, successes)


def display_detailed_results(failures: list, successes: list) -> None:
    """Given lists of failures and successes, print their results"""
    print(f"*** {len(successes)} tests passed and {len(failures)} failed ***")
    if failures:
        print_centered_text("FAILED")
        for result in failures:
            print(result)
    if any(result for result in successes):
        print_centered_text("PASSED")
        for result in successes:
            if result:
                print(result)
