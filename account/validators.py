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
            "min": 1, 
            "max": 100,
            "required": True,
        },
        "password": {
             "type": "string", 
            "nullable": False, 
            "empty": False, 
            "min": 1, 
            "max": 100,
            "required": True,
        },
    }