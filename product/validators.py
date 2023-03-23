from utils import validator


class ProductValidator(validator.BaseValidator):
    schema = {
        "name": {
            "type": "string", 
            "nullable": False, 
            "empty": False, 
            "min": 1, 
            "max": 100
        },
        "price": {
            "type": "float",
            "nullable": False,
            "empty": False,
            "min": 0.01,
        },
        "brand": {
            "name": "string",
            "nullable": False,
            "empty": False,
            "min": 1,
            "max": 100
        }
    }
