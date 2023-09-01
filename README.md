# cloud-function-testing

Test GCP Cloud Functions locally


## Basic description

The objective of this package is to allow you to easily test your GCP Cloud Functions locally before deploying them. Its interface is intended to look similar to that of popular python unit-testing libraries. You can define different tests as classes in a python file, specifying the input and the expected output. You can then launch the tests from the cli and the results are printed unto your terminal.

Let's say your Cloud Function is defined in the following file `main.py` with an entrypoint function `main`
`main.py`
```python
def main(request):
    value = request.get_json()
    if "a" not in value:
        return ("Error", 400)
    return ({**value, "b": 2}, 200)
```

You can define your tests in a file called `cf_tests.py` in the same directory
`cf_tests.py`
```python
class CorrectInput:
    data = {"a": 1}
    headers = {'Content-Type': 'application/json'}
    status_code = 200
    output = {"a": 1, "b": 2}

class IncorrectInput:
    data = {1: 2}
    headers = {'Content-Type': 'application/json'}
    status_code = 400

class CrashInput:
    data = ["a"]
    headers = {'Content-Type': 'application/json'}
    error = True

class OopsUnintendedError:
    data = {"a": "1"}
    headers = {'Content-Type': 'application/json'}
    status_code = 200
    output = {"a": 1, "b": 2}
```

You can then launch the tests by entering in your terminal `cloud-function-test`

You would see the following output in your terminal (with colors):
```
================================================ Running 4 tests from the cf_tests module... =================================================
test CorrectInput in 0.009216s:  PASSED
test IncorrectInput in 0.002605s:  PASSED
test CrashInput in 0.007339s:  PASSED
test OopsUnintendedError in 0.002422s:  FAILED
*** 3 tests passed and 1 failed ***
=================================================================== FAILED ===================================================================
test OopsUnintendedError
Unexpected output
- expected: {'a': 1, 'b': 2}
- received: {'a': '1', 'b': 2}
```
