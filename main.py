from kivy.app import App
from kivy.app import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from collections import defaultdict
from datetime import datetime

Builder.load_file("design.kv")


class LoginScreen(Screen):
    def sign_up(self):
        self.manager.current =  "sign_up_screen"
    pass

class SignUpScreen(Screen):
    def add_user(self, uname, pword):
        def default_key():
            return 0
        with open("users.json") as file:
            try:
                users = defaultdict(default_key,json.load(file))
            except json.decoder.JSONDecodeError:
                users = {}
                
        if len(users.keys()) == 0:
                users.setdefault("user1",{"name":uname,"password":hash(pword),"created": str(datetime.now())})
                pass
        else:
            print("bruh")
        print(users)
        print("tal")
        

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()
    
if __name__ == "__main__":
    MainApp().run()