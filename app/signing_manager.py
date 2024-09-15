"""IMPORTS"""
from flask import Flask, render_template, request, redirect, url_for, session
import app.sign_in as sign_in
import app.sign_up as sign_up
import re


"""Main func"""
def load_signing_page(user_db):
    default_input_values = [None, None, None, None]
    try:
        try:
            checked_user_email = email_getter_and_checker()
            email_existence = is_email_existing(user_db, checked_user_email)
            if email_existence is True:
                sign_in_or_sign_up = {"state": "sign_in", "phase": 0}
                sign_in.manage_sign_in(user_db)
            else:
                sign_in_or_sign_up = {"state": "sign_up", "phase": 0}
                sign_up.manage_sign_up(user_db, sign_in_or_sign_up, checked_user_email)

        except NoInput as noInput:
            sign_in_or_sign_up = {"state": "undetermined", "phase": 0}
    except MailNotValid as mailNotValid:
        sign_in_or_sign_up = {"state": "undetermined", "phase": 0}
    finally:
        return render_template("/signing.html", sign_in_or_sign_up="undetermined", default_input_values=default_input_values, error_message=NoInput)


"""
        sign_in_or_sign_up = is_email_existing(user_db, checked_user_email)
        if sign_in_or_sign_up["state"] == "sign_in":
            sign_in.manage_sign_in()
        else:
            sign_in_or_sign_up, default_input_values, is_account_created= sign_up.manage_sign_up(user_db, sign_in_or_sign_up, checked_user_email)

            else:
                if is_account_created:
                    return render_template("/signing.html", sign_in_or_sign_up=sign_in_or_sign_up, default_input_values=default_input_values, error_message=error)
                else:
                    print(f"from load_signin_page : {sign_in_or_sign_up}")
    else:
        error = "Invalid email"

    return render_template("/signing.html", sign_in_or_sign_up=sign_in_or_sign_up, default_input_values=default_input_values, error_message=error"""

"""CODE"""
def is_email_existing(user_db, user_email):
    email_found = False
    for email in user_db.fetch_all_emails():
        if email[0] == user_email:
            email_found = True
            break
    return email_found


def email_getter_and_checker():
    user_email = request.form.get("email_input")
    email_regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if user_email is not None:
        if not re.match(email_regex, user_email):
            raise MailNotValid("Please input a valid email")
        else:
            return True
    else:
        raise NoInput()


class MailNotValid(Exception):
    pass

class NoInput(Exception):
    pass