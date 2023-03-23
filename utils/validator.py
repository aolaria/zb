from cerberus import Validator


class BaseValidator:
    """
    Base Validator
    """
    schema = {}

    def __init__(self, data):
        self.validator = Validator()
        self.data = data
        self.schema = self.__class__.schema

    def errors(self) -> dict:
        """
        stores all errors related to invalid payload
        :return: (dict)
        """
        return self.validator.errors

    @classmethod
    def validate(cls, data:dict):
        """
        validates payload
        :param data: (data) payload
        """
        if not data:
            raise ValueError("empty payload")

        v = cls(data)
        if v.validator.validate(data, cls.schema):
            return True
        raise ValueError(v.errors())
