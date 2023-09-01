import subprocess
import time

import requests

from .environment import setup_environment
from .functions import display_detailed_results
from .functions import create_tests
from .functions import import_user_classes
from .functions import run_tests
from .functions import start_server
from .utils import print_centered_text
from .utils import set_fd_nonblocking


LOCAL_URL_BASE = 'http://localhost'
TEST_MODULE = "cf_tests"


def main(cli_test_type: str, cli_test_module: str, cli_port: int, cli_env: str, cli_entrypoint: str) -> None:

    test_module = cli_test_module or TEST_MODULE

    user_defined_classes = import_user_classes(test_module)

    # other settings variables, variables are imported after importing user-defined classes
    # so that their value can be modified in the test_module by the user
    from . import entrypoint as settings_entrypoint
    from . import type as settings_test_type
    from . import port as settings_port
    from . import env as settings_env
    test_type = cli_test_type or settings_test_type
    port = cli_port or settings_port
    env = cli_env or settings_env
    entrypoint = cli_entrypoint or settings_entrypoint
    local_url = ":".join([LOCAL_URL_BASE, str(port)])

    setup_environment(env)

    # create BaseFunctionTest objects from the user-defined classes
    tests = create_tests(user_defined_classes, test_type)
    print_centered_text(f"Running {len(tests)} tests from the {test_module} module...")

    process = start_server(entrypoint, port)
    try:
        set_fd_nonblocking(process.stderr.fileno())
        failures, successes = run_tests(process, local_url, tests)
        display_detailed_results(failures, successes)
    finally:
        process.terminate()

