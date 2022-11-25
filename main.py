from kivy.app import App
from kivy.app import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from datetime import datetime
import logging
from hashlib import sha256

logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s')
Builder.load_file("design.kv")


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current =  "sign_up_screen"
        
    def login(self,uname:str,pword:str):
        print()
        with open("users.json") as file:
            try:
                users = json.load(file)
            except json.decoder.JSONDecodeError:
                users = {}
                
        if uname in users and users[uname]["password"] == sha256(pword.encode()).hexdigest():
            self.manager.current = "login_screen_success"
        else:
            self.ids.wrong_login.text = "Wrong username or password. Try again"
    pass

class SignUpScreen(Screen):
    def add_user(self, uname:str, pword:str):
        u_exist = 1
        uname = uname.strip()
        with open("users.json") as file:
            try:
                users = json.load(file)
            except json.decoder.JSONDecodeError:
                users = {}
            
        for v in users:
            if uname in v:
                u_exist = 0
                break
        if u_exist and len(uname):
            users.setdefault(uname,
            {"name":uname,
            "password":sha256(pword.encode()).hexdigest(),
            "created": datetime.now().strftime("%d-%m-%Y %H:%M")})
            self.manager.current = "sign_up_screen_success"
        else:
            logging.critical("DANY UZYTKOWNIK ISTNIEJE")
        with open("users.json","w") as file:
            json.dump(users,file)
        
        
class SignUpScreenSuccess(Screen):
    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current =  "login_screen"
    pass

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    pass

class RootWidget(ScreenManager):
    pass



class MainApp(App):
    def build(self):
        return RootWidget()
    
if __name__ == "__main__":
    MainApp().run()