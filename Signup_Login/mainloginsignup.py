import sys
import json
import os
from PyQt5 import QtWidgets

DATA_FILE = "user_data.json"

# --- Utilities ---
def load_user_data():
    if not os.path.exists(DATA_FILE):
        return {"users": []}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_user_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def find_user(username):
    data = load_user_data()
    for user in data["users"]:
        if user["username"] == username:
            return user
    return None

# --- Login Window ---
class LoginWindow(QtWidgets.QMainWindow, Ui_Login):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        if hasattr(self, "signupButton"):
            self.signupButton.clicked.connect(self.open_signup)

        if hasattr(self, "loginButton"):
            self.loginButton.clicked.connect(self.login_user)

    def login_user(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        user = find_user(username)
        if user and user["password"] == password:
            QtWidgets.QMessageBox.information(self, "Success", "Login successful!")
        else:
            QtWidgets.QMessageBox.warning(self, "Failed", "Invalid username or password.")

    def open_signup(self):
        self.signup_window = SignupWindow()
        self.signup_window.show()
        self.close()

# --- Signup Window ---
class SignupWindow(QtWidgets.QMainWindow, Ui_Signup):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        if hasattr(self, "backButton"):
            self.backButton.clicked.connect(self.open_login)

        if hasattr(self, "registerButton"):
            self.registerButton.clicked.connect(self.register_user)

    def register_user(self):
        username = self.usernameInput.text()
        password = self.passwordInput.text()

        if not username or not password:
            QtWidgets.QMessageBox.warning(self, "Error", "Please fill in all fields.")
            return

        if find_user(username):
            QtWidgets.QMessageBox.warning(self, "Error", "Username already exists.")
            return

        data = load_user_data()
        data["users"].append({"username": username, "password": password})
        save_user_data(data)

        QtWidgets.QMessageBox.information(self, "Success", "Account created!")
        self.open_login()

    def open_login(self):
        self.login_window = LoginWindow()
        self.login_window.show()
        self.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

