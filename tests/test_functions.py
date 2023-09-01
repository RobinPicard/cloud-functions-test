import pytest

from cloud_function_test.functions import create_tests
from cloud_function_test.functions import InvalidTestClassTypeError
from cloud_function_test.functions import HttpFunctionTest
from cloud_function_test.functions import EventFunctionTest


def test_create_tests():

    class DummyHttpClass:
        data = 0

    class DummyEventClass:
        event = 0

    # Test with http type
    classes = [DummyHttpClass, DummyHttpClass]
    tests = create_tests(classes)
    assert len(tests) == 2
    for test in tests:
        assert isinstance(test, HttpFunctionTest)

    # Test with event type
    classes = [DummyEventClass, DummyEventClass]
    tests = create_tests(classes)
    assert len(tests) == 2
    for test in tests:
        assert isinstance(test, EventFunctionTest)
