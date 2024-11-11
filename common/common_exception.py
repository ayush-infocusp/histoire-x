class CommonAppException(Exception):
    def __init__(self, message, status_code=400):
        super().__init__(message)
        self.message = message
        self.status_code = status_code

    def to_dict(self):
        """convert data to doc"""
        return {
            'message': self.message,
            'message_code': self.status_code,
            'data': ''
        }
