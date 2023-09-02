# cloud-function-test

Test GCP Cloud Functions locally

<br>

## Basic Description

The objective of this package is to allow you to easily test your GCP Cloud Functions locally before deploying them. The package relies on Google's functions-framework to launch a local server that receives requests triggering your Cloud Function. Even though the functions are triggered through a request in the package's testing mechanism, event-triggered Cloud Functions are also supported.
The package's interface is intended to look similar to that of popular python unit-testing libraries. You can define different tests as classes in a python file, specifying the input and the expected output. You can then launch the tests from the cli and the results are printed unto your terminal.

Let's say your Cloud Function is defined in the following file `main.py` with an entrypoint function `main`
```python
def main(request):
    value = request.get_json()
    if "a" not in value:
        return ("Error", 400)
    return ({**value, "b": 2}, 200)
```

You can define your tests in a file called `cf_tests.py` in the same directory
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

<br>

## Detailed description


### General Functioning

In your test module, `cf_tests.py` by default, you need to create a basic class for each of your test.

Each class can have a set of attributes that work as parameters for the test. All of those attributes are optional. If none are specified, the test will return "PASSED" if the Cloud Function ran without crashing.

If you do specifiy some of those attributes, you need to make sure their value is of a supported type.

There are 2 possible attributes that are common to both http-triggered and event-triggerd functions:
* error (bool): indicates whether the test is expected to raise an Exception. The test will succeed if the function crashes while it will fail if it runs without error
* display_logs (bool): indicates whether the logs and the return value should be displayed even in case of success (they are always displayed in case of failure of the test)


### Http-triggered Functions

This package has primarily been made for http-triggered Cloud Function so your test classes will be considered to be for this kind of function by default.

You can specify 4 additional attributes for those:
* data (dict, list): the payload that will be included in the request triggering your function
* headers (dict): the headers that will be included in the request triggering your function
* status_code (dict, list): the status code your function is expected to return giving the parameters provided
* output (dict, list): the output your function is expected to return giving the parameters provided. Details on the specific structure the value of this attribute can take are specified below


### Wildcards for Expected Content

It's quite common to want to check the validity of the output of an http-triggered Cloud Function without knowing the exact value of the expected output. This happens for instance if you Cloud Function is calling an external service or if your output includes an "updated_at" timestamp. In that case, you may want to test that the structure of the output is correct rather than the exact content.

There are 2 types of wildcards your can use for that purpose:
* Ellipsis
    * If you include this object in a list, the test will only check that the other elements of the list are found in the actual output
    ```
    A:
        output = ["a", Ellipsis]
    ```
    This will match with `actual_output = ["a", "b", "c"]`
    * If you pass this object as a key in a dict, the test will only check that all other key/value pairs are found in the actual output
    ```
    A:
        output = {"a": 1, "b": Ellipsis}
    ```
    This will match with `actual_output = {"a": 1, "b": 2, "c": 3}`
* Types

    You can include both basic types (int, str...) and types from the typing package (Union, Tuple...) in the expected output.
    * Rather simple case
        ```
        A:
            output = List[int]
        ```
        This will match with `actual_output = [1, 2]`
    * More complex example
        ```
        A:
            output = Tuple[dict, List[int]]
        ```
        This will match with `actual_output = ({"a": 1}, [1, 2])`
    
    We cannot ensure you that the most complex cases are covered unfortunately

### Event-triggered Functions

Testing event-triggered functions is not as straightforward as for http-triggered ones. Since we cannot fully simulate the underlying event for which GCP would trigger the function, we make a request to it as a workaround. In the definition of your test class, you can specify the event and the context you want your function to receive as dictionaries. The package will then pass them on your function.

You can specify 2 additional attributes for those:
* event (dict): the event that your function will receive
* context (dict): the context that you function will receive


### Settings

There are 5 options you can modify for running your tests. Those can typically be modified either in your test module or in the cli

* module: defaults to "cf_tests.py", name of the module in which your test classes are defined

   * cli: `cloud-function-test --module <name_test_module>`


* source: defaults to "main.py", path to the file in which your Cloud Function is defined

   * cli: `cloud-function-test --source <path_to_file>`
   * in test module:
   ```
   import cloud_function_framework
   cloud_function_framework.source = "<path_to_file>"
   ```

* entrypoint: defaults to "main", name of the Cloud Function entrypoint in the file in which your Cloud Function is defined

   * cli: `cloud-function-test --entrypoint <entrypoint>`
   * in test module:
   ```
   import cloud_function_framework
   cloud_function_framework.entrypoint = "<entrypoint>"
   ```

* env: defaults to ".env", path to the file in which your environment variables are defined (nothing happens if the file does not exist)

   * cli: `cloud-function-test --env <env_file_path>`
   * in test module:
   ```
   import cloud_function_framework
   cloud_function_framework.env = "<env_file_path>"
   ```
   This file can either be a bash file organized as such:
   ```bash
   ENV=dev
   FOO=bar
   ```
   Or a Terraform file. In this case, the package will do its best to infer the env variables from the structure of the file. Example of supported structure:
   ```terraform
    module "test_module" {
      env         = var.env
      environment_variables = {
        ENV               = var.env,
        LOCATION_ID       = "europe-west1",
        NAME = "test_${var.env}",
      }
      memory_mb   = 512
    }
   ```

* port: defaults to 8080, port of localhost that will be used by functions-framework to launch the local server receiving the requests that will trigger the Cloud Functions

   * cli: `cloud-function-test --port <port>`
   * in test module:
   ```
   import cloud_function_framework
   cloud_function_framework.port = <port>
