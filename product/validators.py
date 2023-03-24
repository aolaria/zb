from utils import validator


class ProductValidator(validator.BaseValidator):
    schema = {
        "name": {
            "type": "string", 
            "nullable": False, 
            "empty": False, 
            "minlength": 1, 
            "maxlength": 100,
            "required": True,
        },
        "price": {
            "type": "float",
            "nullable": False,
            "empty": False,
            "min": 0.01,
            "required": True,
        },
        "brand": {
            "type": "string",
            "nullable": False,
            "empty": False,
            "min": 1,
            "max": 100,
            "required": True,
        }
    }


class ProductUpdateValidator(validator.BaseValidator):
    schema = {
        "name": {
            "type": "string", 
            "nullable": False, 
            "empty": False, 
            "minlength": 1, 
            "maxlength": 100,
        },
        "price": {
            "type": "float",
            "nullable": False,
            "empty": False,
            "min": 0.01,
        },
        "brand": {
            "type": "string",
            "nullable": False,
            "empty": False,
            "min": 1,
            "max": 100,
        }
    }


class BrandValidator(validator.BaseValidator):
    schema = {
        "name": {
            "type": "string", 
            "nullable": False, 
            "empty": False, 
            "minlength": 1, 
            "maxlength": 100,
            "required": True,
        }
    }