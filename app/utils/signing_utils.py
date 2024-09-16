from flask import request, session
import re

"""Managing the phase of connection for each client"""
def phase_setter(sign_in_or_sign_up):
    print("a")
    if sign_in_or_sign_up["state"] == "sign_up":
        if sign_in_or_sign_up["phase"] == 1:
            if request.form["username_input"]:
                sign_in_or_sign_up["phase"] = 2
        elif sign_in_or_sign_up["phase"] == 2:
            if request.form["password_input"]:
                sign_in_or_sign_up["phase"] = 3

    elif sign_in_or_sign_up["state"] == "sign_in":
        if sign_in_or_sign_up["phase"] == 0:
            if request.form["password_input"]:
                sign_in_or_sign_up["phase"] = 1

    return sign_in_or_sign_up["phase"]



"""Email part"""
def is_email_existing(user_db, user_email):
    email_found = False
    for email in user_db.fetch_all_emails():
        if email[0] == user_email:
            email_found = True
            break
    return email_found


def email_checker(user_email):
    email_regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if user_email is not None:
        if not re.match(email_regex, user_email):
            raise EmailNotValid("Please input a valid email")
        else:
            return True
    else:
        raise NoInput()


class EmailNotValid(Exception):
    pass

class NoInput(Exception):
    pass