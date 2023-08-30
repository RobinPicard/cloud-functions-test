class CodeErrorExceptoin:
    payload = ["q"]
    headers = {}
    #output = Exception
    status_code = 200

class WrongStatusCode:
    payload = {"value": 1}
    headers = {}
    output = "SOMETHING"
    status_code = 200

class WrongOutput:
    payload = {"value": 1}
    headers = {}
    output = "SOMETHING"
    status_code = 200

class GoodOne:
    payload = {"value": 1}
    headers = {}
    output = "YAY"
    status_code = 200
    display_output_success = True
