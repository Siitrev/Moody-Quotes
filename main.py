from kivy.app import App
from kivy.app import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from datetime import datetime
import logging

logging.basicConfig(level=logging.DEBUG,format='%(name)s - %(levelname)s - %(message)s')
Builder.load_file("design.kv")


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current =  "sign_up_screen"
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        u_exist = 1
        with open("users.json") as file:
            try:
                users = json.load(file)
            except json.decoder.JSONDecodeError:
                users = {}
            
        for v in users.values():
            if v["name"] == uname:
                u_exist = 0
                break
        if u_exist:users.setdefault("user"+str(len(users)+1),
                        {"name":uname,
                         "password":hash(pword),
                         "created": datetime.now().strftime("%d-%m-%Y %H:%M")})
        else:
            logging.critical("DANY UZYTKOWNIK ISTNIEJE")
        with open("users.json","w") as file:
            json.dump(users,file)
        

        

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()
    
if __name__ == "__main__":
    MainApp().run()