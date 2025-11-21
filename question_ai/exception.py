class ApiException(Exception):

    def __init__(self, error_code, status_code, status):
        self.error_code = error_code
        self.status_code = status_code
        self.status = status
