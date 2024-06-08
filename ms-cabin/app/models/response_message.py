from dataclasses import dataclass

@dataclass
class ResponseMessage:
    message: str
    status_code: int
    data: dict

@dataclass
class ResponseBuilder:
    add_message: str
    add_status_code: int
    add_data: dict

    def add_message(self, message: str):
        self.add_message = message
        return self
    
    def add_status_code(self, status_code: int):
        self.add_status_code = status_code
        return self
    
    def add_data(self, data: dict):
        self.add_data = data
        return self
    
    def build(self):
        return ResponseMessage(
            message=self.add_message,
            status_code=self.add_status_code,
            data=self.add_data
        )
