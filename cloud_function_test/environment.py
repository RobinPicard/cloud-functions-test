import os
import re
from dotenv import load_dotenv

from .exceptions import InvalidTerraformFileError


def setup_environment(location: str) -> None:
    """Load environment variables from the file specified (.env by default)"""
    if location.split(".")[-1] == 'tf':
        load_terraform_env(location)
    else:
        load_dotenv(location)


def load_terraform_env(location: str) -> None:
    """Load the environment variables defined in the Terraform file provided"""
    env_vars_str = ""
    with open(location, 'r') as file:
        lines = file.readlines()
        reached_env_var = False
        open_braces_count = 0
        for line in lines:
            pattern = re.compile(r"environment_variables\s*=\s*(.*)")
            match = pattern.search(line)
            # if we've just encountered the beginning of the environment_variables, add everything after the match
            if match:
                reached_env_var = True
                open_braces_count += line.count('{')
                open_braces_count -= line.count('}')
                env_vars_str += match.group(1).strip()
            # if it's within the environment_variables, add the whole line
            elif reached_env_var:
                open_braces_count += line.count('{')
                open_braces_count -= line.count('}')
                env_vars_str += line.strip()
                # if we've reached the end of the def of the environment_variables
                if open_braces_count == 0:
                    break
    if env_vars_str:
        env_vars = parse_terraform_env_str(env_vars_str)
        # load the variables in the environment from the dict
        for key, value in env_vars.items():
            os.environ[key] = value


def parse_terraform_env_str(env_vars_str: str) -> dict:
    """
    Given a string containing the content of a Terraform environment_variables variable,
    return the content as a dict ENV_VAR:value
    """
    env_vars_str = env_vars_str.strip()[1:-1] # remove the brackets at the beginning and at the end
    env_vars = {}
    for line in env_vars_str.split(","):
        if not line.strip():
            continue
        try:
            var, val = line.strip().split('=')
            var = var.strip()
            val = val.strip().strip('"')
            # Replace any `${var.env}` with 'dev'
            val = re.sub(r'\${var.env}', 'dev', val)
            # Replace 'var.env' with 'dev'
            val = 'dev' if val == 'var.env' else val
            env_vars[var] = val
        except Exception:
            raise InvalidTerraformFileError("The Terraform file specified does not follow a syntax the package can read")
    if not env_vars:
        raise InvalidTerraformFileError("The Terraform file specified does not contain any env variables")
    return env_vars

