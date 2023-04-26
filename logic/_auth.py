import hashlib


class Auth:

    def __init__(self):
        ...

    def authorize(self, login: str, password: str):
        password_hashed = self.__password_hash(password=password)

    @staticmethod
    def __password_hash(password: str):
        result = password.encode("utf-8").hex()
        for i in range(1000):
            result = hashlib.sha512(result).hexdigest()
        return result
