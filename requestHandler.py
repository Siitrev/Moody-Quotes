import requests
from hashlib import sha256


class RequestHandler():
    def check_user_exist(self, uname: str, email: str):
        try:
            if len(uname) > 35:
                raise OverflowError("Nie istnieje taki uzytkownik")
            data = {'username': uname,
                    "email": email}
            res = requests.post(
                url="https://Sitrev.pythonanywhere.com/check_sign_up", json=data)
            return res.json()
        except requests.ConnectTimeout:
            return "Connection Timeout"
        except requests.RequestException:
            return "Request Exception"
        except OverflowError as e:
            return e.args[0]

    def add_user(self, uname: str, pword: str, email: str, created: str):
        try:
            data = {"username": uname,
                    "password": sha256(pword.encode()).hexdigest(),
                    "email": email,
                    "created": created}
            requests.post(
                url="https://Sitrev.pythonanywhere.com/sign_up", json=data)
        except requests.ConnectTimeout:
            return "Connection Timeout"
        except requests.RequestException:
            return "Request Exception"
    
    def login(self, uname:str,pword:str):
        try:
            data = {"username": uname,
                    "password": sha256(pword.encode()).hexdigest()}
            res = requests.post(
                    url="https://Sitrev.pythonanywhere.com/login", json=data)
            return res.json()
        except requests.ConnectTimeout:
            return "Connection Timeout"
        except requests.RequestException:
            return "Request Exception"

