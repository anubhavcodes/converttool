class Error(Exception):
    """Base class for exceptions in converttool"""
    pass

class ValidationError(Error):
    """Exception raised when there is a validation error"""
    pass

class CSVNotFound(Error):
    """Exception raised when there is no csv file"""
    pass

class FormatterNotFound(Error):
    """Exception raised when the pluggable implementation formatter 
    class is not found
    """
    pass

class ConversionError(Error):
    """Exception raised when there is an error converting and 
    writing to output file"""
    pass

class SettingsNotFound(Error):
    """Exception raised when there is an error loading the settings 
    file for dynamic validation"""

class InvalidValidationSchema(Error):
    """Exception raised when validate.json is invalid"""
