from colorama import Fore


class ResponseData:
    def __init__(self,
                 message,
                 status_code=200,
                 success=True):
        self.message = message
        self.status_code = status_code
        self.success = success
        print(Fore.LIGHTGREEN_EX + self.message + Fore.RESET)


class BadRequest:
    def __init__(self, message, status_code=400):
        self.message = message
        self.status_code = status_code
        print(Fore.LIGHTRED_EX + self.message + Fore.RESET)
