from cloud_function_test.utils import log_reader


def test_log_reader():

    class FakeLogLine:
        def __init__(self, value):
            self.value = value
        def decode(self, type):
            return self.value   
    class FakeProcessStderr:
        def __init__(self, logs):
            self.logs = iter(logs)
        def readline(self):
            try:
                return next(self.logs)
            except StopIteration:
                return None

    assert log_reader(FakeProcessStderr([FakeLogLine('hello\n'), FakeLogLine('there')])) == 'hello\nthere'
    assert log_reader(FakeProcessStderr([FakeLogLine('hello\n'), FakeLogLine('there\n')])) == 'hello\nthere'
    assert log_reader(FakeProcessStderr([])) == ''
