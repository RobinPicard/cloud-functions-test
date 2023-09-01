class MissingTestClassError(Exception):
    """Used when no user-defined function test class is found in the module"""
    pass


class InvalidTestClassTypeError(Exception):
    """Used when no user-defined function test class is found in the module"""
    pass


class InvalidAttributeTypeError(Exception):
    """Used when no user-defined class contains an attribute of the wrong type"""
    pass