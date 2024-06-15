from dataclasses import dataclass

@dataclass
class ResponseMessage:
    message: str
    status_code: int
    data: dict

class ResponseBuilder:
    def __init__(self):
        self._message = ""
        self._status_code = 0
        self._data = {}

    def add_message(self, message: str):
        self._message = message
        return self
    
    def add_status_code(self, status_code: int):
        self._status_code = status_code
        return self
    
    def add_data(self, data: dict):
        self._data = data
        return self
    
    def build(self):
        return ResponseMessage(
            message=self._message,
            status_code=self._status_code,
            data=self._data
        )
