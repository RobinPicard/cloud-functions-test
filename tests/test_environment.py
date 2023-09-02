import pytest

from cloud_function_test.exceptions import InvalidTerraformFileError
from cloud_function_test.environment import parse_terraform_env_str


def test_parse_terraform_env_str():
    # normal input
    input_str = '{VAR1="value1", VAR2="value2"}'
    expected_output = {'VAR1': 'value1', 'VAR2': 'value2'}
    assert parse_terraform_env_str(input_str) == expected_output
    # extra spaces
    input_str = ' { VAR1 = "value1" , VAR2 = "value2" } '
    expected_output = {'VAR1': 'value1', 'VAR2': 'value2'}
    assert parse_terraform_env_str(input_str) == expected_output
    # with variable interpolation
    input_str = '{VAR1="${var.env}", VAR2="var.env"}'
    expected_output = {'VAR1': 'dev', 'VAR2': 'dev'}
    assert parse_terraform_env_str(input_str) == expected_output
    # malformed input (missing '=')
    input_str = '{VAR1 "value1"}'
    with pytest.raises(InvalidTerraformFileError):
        parse_terraform_env_str(input_str)
    # malformed input (extra characters)
    input_str = '{VAR1="value1"! VAR2="value2"}'
    with pytest.raises(InvalidTerraformFileError):
        parse_terraform_env_str(input_str)
    # empty input
    input_str = '{}'
    with pytest.raises(InvalidTerraformFileError):
        parse_terraform_env_str(input_str)
