import cloud_function_test


class CorrectInput:
    event = {"a": 1}
    context = {"a": 1}

class WrongInput:
    event = {"a": 1}
    context = {"b": 2}
    error = True
