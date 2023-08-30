from utils import log_reader
from typing import List, Tuple

class TestRunner:

    def __init__(self, process, local_url: str):
        self.process = process
        self.local_url = local_url

    def run_tests(self, tests: List) -> Tuple[List, List]:
        results = []

        for test in tests:
            test.make_post_request(self.local_url)
            error_logs = log_reader(self.process.stderr)
            validity_result = test.check_response_validity(error_logs)
            results.append(validity_result)

        failures = [item for item in results if item[0] == 'failed']
        successes = [item for item in results if item[0] == 'passed']

        return successes, failures
