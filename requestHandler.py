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
                    "created": created,
                    "token": ""}
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
    
    def change_password(self,uname:str, n_pass: str, o_pass: str):
        try:
            data = {"username":uname,
                    "n_pass": sha256(n_pass.encode()).hexdigest(),
                    "o_pass": sha256(o_pass.encode()).hexdigest()}
            res = requests.post(
                    url="https://Sitrev.pythonanywhere.com/change_password", json=data)
            return res.json()
        except requests.ConnectTimeout:
            return "Connection Timeout"
        except requests.RequestException:
            return "Request Exception"
    def send_mail(self, uname: str, email: str):
        try:
            data = {"username": uname,
                    "email": email}
            requests.post(
                url="https://Sitrev.pythonanywhere.com/send_mail", json=data)
        except requests.ConnectTimeout:
            return "Connection Timeout"
        except requests.RequestException:
            return "Request Exception"
    def check_token(self, uname: str, token: str):
        try:
            data = {"username": uname,
                    "code": token}
            res = requests.post(
                url="https://Sitrev.pythonanywhere.com/check_token", json=data)
            print(res)
            return res.json()
        except requests.ConnectTimeout:
            return "Connection Timeout"
        except requests.RequestException:
            return "Request Exception"
    def update_password(self,uname:str, n_pass: str):
        try:
            data = {"username":uname,
                    "n_pass": sha256(n_pass.encode()).hexdigest()}
            requests.post(
                    url="https://Sitrev.pythonanywhere.com/update_password", json=data)
        except requests.ConnectTimeout:
            return "Connection Timeout"
        except requests.RequestException:
            return "Request Exception"
