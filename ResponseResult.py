from MasterData import ResponseStatus

class ResponseResult:
    def __init__(self, _data):
        self.status = ResponseStatus.PENDING
        self.error_message = ""
        self.data = _data
    
    def set_failure(self, error_message):
        self.status = ResponseStatus.FAIL
        self.error_message = error_message

    def set_success(self):
        self.status = ResponseStatus.SUCCESS

    def is_success(self):
        return self.status == ResponseStatus.SUCCESS
    
    def is_fail(self):
        return self.status == ResponseStatus.FAIL

    def is_loading(self):
        return self.status == ResponseStatus.PENDING

    def get_error_message(self):
        return self.error_message

    def get_data(self):
        return self.data