class LoginError(Exception):
    def __init__(self):
        super().__init__("Token has not been set")
    