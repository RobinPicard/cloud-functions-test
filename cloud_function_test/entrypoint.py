from dotenv import load_dotenv
from test_classes import import_tests
from utils import print_centered_text, set_fd_nonblocking
import subprocess
import time


if __name__ == "__main__":

    load_dotenv()

    TEST_MODULE_NAME = 'test'
    LOCAL_URL = 'http://localhost:8080'

    tests = import_tests(TEST_MODULE_NAME)
    print_centered_text(f"Running {len(tests)} tests from the {TEST_MODULE_NAME} module...")

    process = subprocess.Popen(
        ['functions_framework', '--target=main'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        time.sleep(1)
        set_fd_nonblocking(process.stderr.fileno())

        from test_runner import TestRunner
        runner = TestRunner(process, LOCAL_URL)
        successes, failures = runner.run_tests(tests)

        print(f"*** {len(successes)} tests passed and {len(failures)} failed ***")

        if failures:
            print_centered_text("FAILED")
            for result in failures:
                print(result[1])

        if successes:
            print_centered_text("PASSED")
            for result in successes:
                print(result[1])

    finally:
        process.terminate()

