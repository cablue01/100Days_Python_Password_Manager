from password_manager import PasswordManager

# constants
DEFAULT_EMAIL = "NotReal@NotEmail.com"
DATA_FILE_NAME = "data.csv"

pwd = PasswordManager("data.csv", DEFAULT_EMAIL)
pwd.open_form()

