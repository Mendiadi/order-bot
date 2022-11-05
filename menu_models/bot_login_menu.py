from menu_models import Base_Menu


class Login_Menu(Base_Menu):

    def heandler(self, message):
        action = message
        if self.state == "wating_for_password":
            if action == "pass":
                self.state = "pass_validation"
            else:
                self.state = "wrong_password"

    def show(self):
        self.state = "wating_for_password"
        return ("ברוכים הבאים לתפריט התחברות למסך מנהל \n"
                "אנא הקלד סיסמא \n"
                "לחזרה לתפריט הראשי שלח: # .\n")
