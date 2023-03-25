from utils.validator import BaseValidator


class LoginValidator(BaseValidator):
    """
    Login's Validator
    """
    schema = {
        "username": {
            "type": "string", 
            "nullable": False, 
            "empty": False, 
            "minlength": 1, 
            "maxlength": 100,
            "required": True,
        },
        "password": {
             "type": "string", 
            "nullable": False, 
            "empty": False, 
            "minlength": 1, 
            "maxlength": 100,
            "required": True,
        },
    }


class AdminValidator(BaseValidator):
    """
    Admin's Validator
    """
    schema = {
        "username": {
            "type": "string", 
            "nullable": False, 
            "empty": False, 
            "minlength": 1, 
            "maxlength": 100,
            "required": True,
        },
        "email": {
            "type": "string", 
            "minlength": 8,
            "maxlength": 255,
            "required": True,
            "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
        },
        "password": {
             "type": "string", 
            "nullable": False, 
            "empty": False, 
            "minlength": 1, 
            "maxlength": 100,
            "required": True,
        },
    }

class AdminValidatorUpdate(BaseValidator):
    """
    Admin's Validator
    """
    schema = {
        "username": {
            "type": "string", 
            "nullable": False, 
            "empty": False, 
            "minlength": 1, 
            "maxlength": 100,
        },
        "email": {
            "type": "string", 
            "minlength": 8,
            "maxlength": 255,
            "regex": "^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$"
        },
        "password": {
             "type": "string", 
            "nullable": False, 
            "empty": False, 
            "minlength": 1, 
            "maxlength": 100,
        },
    }
