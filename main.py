from kivy.app import App
from kivy.app import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from datetime import datetime
from hashlib import sha256
from random import choice
from os import listdir
from hoverable import HoverBehavior
import logging, json


logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s')
Builder.load_file("design.kv")


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.transition.direction = "left"
        self.manager.current =  "sign_up_screen"
        
    def login(self,uname:str,pword:str):

        with open("users.json") as file:
            try:
                users = json.load(file)
            except json.decoder.JSONDecodeError:
                users = {}
                
        if uname in users and users[uname]["password"] == sha256(pword.encode()).hexdigest():
            self.manager.transition.direction = "left"
            self.ids.wrong_login.text = ""
            self.manager.current = "login_screen_success"
        else:
            self.ids.wrong_login.text = "Wrong username or password. Try again"

class SignUpScreen(Screen):
    def add_user(self, uname:str, pword:str, email:str):
        u_exist = 1
        uname = uname.strip()
        with open("users.json") as file:
            try:
                users = json.load(file)
            except json.decoder.JSONDecodeError:
                users = {}
            
        for v,v2 in users.items():
            if uname in v:
                u_exist = 0
                break
            if v2["email"] == email:
                u_exist = 0
                break
        if u_exist and len(uname) and len(email):
            users.setdefault(uname,
            {"name":uname,
            "password":sha256(pword.encode()).hexdigest(),
            "email": email, 
            "created": datetime.now().strftime("%d-%m-%Y %H:%M")})
            self.ids.username.text = ""
            self.ids.password.text = ""
            self.ids.email.text = ""
            self.manager.current = "sign_up_screen_success"
        else:
            logging.critical("DANY UZYTKOWNIK ISTNIEJE")
        with open("users.json","w") as file:
            json.dump(users,file)
    
    def back_to_login(self):
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.ids.email.text = ""
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        
class SignUpScreenSuccess(Screen):
    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current =  "login_screen"
    pass

class LoginScreenSuccess(Screen):
    def log_out(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
        
    def get_quote(self, feel:str):
        feel = feel.lower()
        feelings = [x[:-4] for x in listdir("./quotes")]
        if feel in feelings:
            
            with open(f"./quotes/{feel}.txt") as file:
                quotes = file.readlines()
            oldQuote = self.ids.quote.text
            newQuote =  choice(quotes)
            
            while oldQuote == newQuote:
                newQuote = choice(quotes)
                
            self.ids.quote.text = newQuote
        else:
            self.ids.quote.text = "Please try another emotion"
        

class RootWidget(ScreenManager):
    pass

class ImageButton(ButtonBehavior,HoverBehavior, Image):
    pass
class MainApp(App):
    def build(self):
        return RootWidget()
    
if __name__ == "__main__":
    MainApp().run()