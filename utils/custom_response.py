from rest_framework.response import Response


class ErrorResponse(Response):
    """
    Costum Response for Error messages
    """
    def __init__(self, data, status):
        """
        :param data: (dict) error message
        :param status: (int) HTML error code
        """
        super().__init__(data, status)
        self._data = data
        self.status = status

    @property
    def data(self) -> dict:
        """
        builds error message
        """
        return {"error": {"msg": self._data}}

    @data.setter
    def data(self, value):
        self._data = value
        