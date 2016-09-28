import json
import logging
from cerberus import Validator, SchemaError
from converttool import *
from converttool.settings import BASE_DIR
from converttool.exceptions import SettingsNotFound

log = logging.getLogger('converttool.Validate')

class Validate:
    """Class to dynamically add new validations to the schema"""
    
    def __init__(self, data):
        """Initialize the Validator
        
        :param list data: List of dictionaries of tha actual data
        #TODO: Make the schema a parameter to the initializer rather 
        than keep it fixed to validate.json
        """
        self.data = data
        if not os.path.exists(os.path.join(os.path.expanduser('~/.config'), 'validate.json')):
            # Use validate.json from project root
            self.settings = os.path.join(BASE_DIR, 'validate.json')
        else: 
            # Use validate.json from ~/.config
            self.settings = os.path.join(os.path.expanduser('~/.config'), 'validate.json')
        try:
            # load the schema
            with open(self.settings) as f:
                self.schema = json.load(f)
        except IOError:
            raise SettingsNotFound("Please make sure that validate.json is present in the ~/.config or project root")


    def validate(self):
        """Method to validate the schema against the data
        
        rtype: int errors: Number of errors found. 
        
        """
        try:
            v = Validator(self.schema)
        except SchemaError:
            return InvalidValidationSchema("There is a problem with yoru scheme. Please check validate.json again")
        errors = 0
        for d in self.data:
            v.validate(d, self.schema)
        if v.errors:
            errors+=1
        return errors

    def __repr__(self):
        return "Validator"

    def __str__(self):  
        return "Validator"
