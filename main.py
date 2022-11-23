from kivy.app import App
from kivy.app import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
import json
from collections import defaultdict

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
            users = defaultdict(default_key,json.loads(file))
        if users[uname] == 0:
            print("Mozna stworzyc konto")
        else:
            print("Nie mozna stworzyc konta")
        

class RootWidget(ScreenManager):
    pass

class MainApp(App):
    def build(self):
        return RootWidget()
    
if __name__ == "__main__":
    MainApp().run()