import subprocess
import tempfile

import requests

from .environment import setup_environment
from .functions import create_temp_file_event
from .functions import create_tests
from .functions import display_detailed_results
from .functions import import_user_classes
from .functions import run_tests
from .functions import start_server
from .utils import print_centered_text
from .utils import set_fd_nonblocking
from .test_classes.event_test import EventFunctionTest
from .test_classes.http_test import HttpFunctionTest


LOCAL_URL_BASE = 'http://localhost'
TEST_MODULE = "cf_tests"
EVENT_FUNC_ENTRYPOINT = "cloud_functions_test_entrypoint"


def main(cli_test_module: str, cli_source: str, cli_entrypoint: str, cli_env: str, cli_port: int) -> None:

    test_module = cli_test_module or TEST_MODULE

    user_defined_classes = import_user_classes(test_module)

    # other settings variables, variables are imported after importing user-defined classes
    # so that their value can be modified in the test_module by the user
    from . import source as settings_source
    from . import entrypoint as settings_entrypoint
    from . import port as settings_port
    from . import env as settings_env
    source = cli_source or settings_source
    entrypoint = cli_entrypoint or settings_entrypoint
    env = cli_env or settings_env
    port = cli_port or settings_port
    local_url = ":".join([LOCAL_URL_BASE, str(port)])

    setup_environment(env)

    # create BaseFunctionTest objects from the user-defined classes
    tests, test_type = create_tests(user_defined_classes)
    print_centered_text(f"Running {len(tests)} tests from the {test_module} module...")

    # if it's for an event function, create temp file to turn the http request into an event/context pair
    if test_type == EventFunctionTest:
        with tempfile.NamedTemporaryFile(suffix='.py') as temp_file:
            temp_source, temp_entrypoint = create_temp_file_event(temp_file, source, entrypoint, EVENT_FUNC_ENTRYPOINT)
            process = start_server(port, temp_entrypoint, temp_source)
    else:
        process = start_server(port, entrypoint, source)

    try:
        set_fd_nonblocking(process.stderr.fileno())
        set_fd_nonblocking(process.stdout.fileno())
        failures, successes = run_tests(process, local_url, tests)
        display_detailed_results(failures, successes)
    finally:
        process.terminate()
