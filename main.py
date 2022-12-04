from kivy.app import App
from kivy.app import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.image import Image
from datetime import datetime
from random import choice
from os import listdir
from os.path import getsize
from hoverable import HoverBehavior
import logging
import re
from requestHandler import RequestHandler
logging.basicConfig(level=logging.DEBUG,
                    format='%(name)s - %(levelname)s - %(message)s')
Builder.load_file("design.kv")

# Creating screen for login


class LoginScreen(Screen):
    # Changing the screen to sign up screen
    def sign_up(self):
        self.manager.transition.direction = "left"
        self.manager.current = "sign_up_screen"

    # Logging in
    def login(self, uname: str, pword: str):

        # Checking if password and username are correct
        handler = RequestHandler()

        if handler.login(uname, pword)["success"]:
            self.manager.transition.direction = "left"
            self.ids.wrong_login.text = ""
            self.ids.username.text = ""
            self.ids.password.text = ""
            self.manager.get_screen(
                "login_screen_success").ids.logged_as.text = uname
            self.manager.current = "login_screen_success"
        else:
            self.ids.wrong_login.text = "Wrong username or password. Try again"

    def forgot_pass(self):
        self.manager.transition.direction = "left"
        self.manager.current = "forgot_password_screen"

# Creating sign up screen


class SignUpScreen(Screen):

    # Methods for validating input
    def __validate_email(self, email):
        regex = r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+"
        return re.fullmatch(regex, email)

    def __validate_password(self, pword):
        regex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,40}$"
        return re.match(regex, pword)

    def __validate_username(self, uname: str):
        regex = r"^[A-Za-z0-9#$_&%!<>?-]{5,30}$"
        return re.match(regex, uname)

    def __email_and_user_exist(self, uname: str, email: str):
        handler = RequestHandler()
        return handler.check_user_exist(uname, email)

    # Method that adds user and validates password, email and username
    def add_user(self, uname: str, pword: str, email: str):

        # Validation
        check_email_exist, check_user_exist = self.__email_and_user_exist(
            uname, email).values()
        check_user = self.__validate_username(uname)
        check_email = self.__validate_email(email)
        check_pass = self.__validate_password(pword)

        if not check_user_exist and check_user and check_email and check_pass:
            handler = RequestHandler()
            handler.add_user(uname, pword, email,
                             datetime.now().strftime("%d-%m-%Y %H:%M"))
            self.ids.username.text = ""
            self.ids.password.text = ""
            self.ids.email.text = ""
            self.manager.current = "sign_up_screen_success"
        else:
            # Alert about wrong input
            wrong_input = ""
            if not check_pass:
                wrong_input = wrong_input + "Password is not strong. "
            if not check_email:
                wrong_input = wrong_input + "Wrong email. "
            if check_email_exist:
                wrong_input = wrong_input + "This email is used. "
            if check_user_exist and len(uname) > 0:
                wrong_input = wrong_input + "This user already exists "
            if check_user:
                wrong_input = wrong_input + "Wrong username"

            self.ids.wrong_sign_up.text = wrong_input

            logging.critical("INCORRECT SIGN UP")

    # Changing screen to login screen
    def back_to_login(self):
        self.ids.username.text = ""
        self.ids.password.text = ""
        self.ids.email.text = ""
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

# Creating sign up screen when signing up succeeds


class SignUpScreenSuccess(Screen):

    def go_back(self):
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"
    pass

# Creating screen that shows up when logging in succeeds


class LoginScreenSuccess(Screen):
    # Method for logging out
    def log_out(self):
        self.manager.transition.direction = "right"
        self.ids.logged_as.text = ""
        self.manager.current = "login_screen"

    def change_password(self):
        self.manager.transition.direction = "left"
        self.manager.current = "change_password_screen_1"

    # Getting quote from files
    def get_quote(self, feel: str):
        feel = feel.lower()
        feelings = [x[:-4] for x in listdir("./quotes")]
        if feel in feelings:

            with open(f"./quotes/{feel}.txt") as file:
                quotes = file.readlines()
            oldQuote = self.ids.quote.text
            newQuote = choice(quotes)

            while oldQuote == newQuote:
                newQuote = choice(quotes)

            self.ids.quote.text = newQuote
        else:
            self.ids.quote.text = "Please try another emotion"


class RootWidget(ScreenManager):
    pass

# Special class for image button


class ImageButton(ButtonBehavior, HoverBehavior, Image):
    pass


class ForgotPasswordScreen(Screen):
    def __email_and_user_exist(self, uname: str, email: str):
        handler = RequestHandler()
        return handler.check_user_exist(uname, email)

    def go_back(self):
        self.ids.username.text = ""
        self.ids.email.text = ""
        self.ids.wrong_data.text = ""
        self.manager.transition.direction = "right"
        self.manager.current = "login_screen"

    def change_password(self, uname: str, email: str):
        if self.__email_and_user_exist(uname, email).values():
            handler = RequestHandler()
            handler.send_mail(uname, email)
            self.manager.transition.direction = "left"
            self.manager.current = "token_screen"
        else:
            self.ids.wrong_data.text = "Username/email doesn't exist"


class TokenScreen(Screen):
    def __check_t(self, token: str):
        regex = r"^[0-9]{5}$"
        return re.match(regex, token)

    def check_token(self, token: str):
        handler = RequestHandler()
        uname = self.manager.get_screen(
            "forgot_password_screen").ids.username.text
        valid_token = self.__check_t(token)
        check_token = False
        if valid_token:
            check_token = handler.check_token(uname, token)["Success"]
        else:
            self.ids.wrong_code.text = "Wrong code"
        if check_token:
            self.manager.transition.direction = "left"
            self.manager.current = "change_password_screen_2"
            pass
        else:
            self.ids.wrong_code.text = "Wrong code"
    pass


class ChangePasswordScreen1(Screen):

    def __validate_password(self, pword):
        regex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,40}$"
        return re.match(regex, pword)

    def change_password(self, n_pass: str, o_pass: str):
        handler = RequestHandler()
        check_pass = self.__validate_password(n_pass)
        username = self.manager.get_screen(
            "login_screen_success").ids.logged_as.text
        pass_good = handler.change_password(
            username, n_pass, o_pass)["success"]
        if check_pass and pass_good:
            self.manager.current = "login_screen_success"
        else:
            wrong_input = ""
            if not pass_good:
                wrong_input += "Wrong password "
            if not check_pass:
                wrong_input += "Weak password"
            self.ids.wrong_pass.text = wrong_input


class ChangePasswordScreen2(Screen):

    def __validate_password(self, pword):
        regex = r"^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,40}$"
        return re.match(regex, pword)

    def update_password(self, n_pass: str):
        handler = RequestHandler()
        check_pass = self.__validate_password(n_pass)
        username = self.manager.get_screen(
            "forgot_password_screen").ids.username.text
        if check_pass:
            handler.update_password(username, n_pass)
            self.manager.transition.direction = "left"
            self.manager.current = "login_screen"
        else:
            wrong_input = ""
            if not check_pass:
                wrong_input += "Weak password"
            self.ids.wrong_pass.text = wrong_input


class MainApp(App):
    def build(self):
        return RootWidget()


# running the app
if __name__ == "__main__":
    MainApp().run()
