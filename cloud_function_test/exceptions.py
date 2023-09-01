class MissingTestClassError(Exception):
    """Used when no user-defined function test class is found in the module"""
    pass


class InvalidAttributeTypeError(Exception):
    """Used when no user-defined class contains an attribute of the wrong type"""
    pass


class InvalidTerraformFileError(Exception):
    """Used when the Terraform file provided for env variables cannot be read"""
    pass


class PortUnavailableError(Exception):
    """Used when the user tries to use a port of localhost that is already used by another process"""
    pass


class DifferentClassTypesError(Exception):
    """Used when the user included two different types of functions in the user-defined classes"""
    pass
