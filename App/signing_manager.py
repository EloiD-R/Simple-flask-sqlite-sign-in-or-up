"""Imports"""
from flask import Flask, redirect, session, render_template_string, request, g, render_template
import re

"""Loader"""
def load(user_db):
    feedback_messages = {
        "email_field" : None,
        "username_field" : None,
        "password_field" : None,
    }

    # Check email
    email = request.form.get('email')
    session['email'] = email
    is_email_valid = check_email(email)
    if is_email_valid is True:
        print("a")
        signin_state = determine_signing_state(user_db, email)
        print(signin_state)
        feedback_messages["email_field"] = "Email valid"
    elif is_email_valid is False:
        print("b")
        feedback_messages["email_field"] = "Please enter a valid email address"
    else:
        print("c")
        feedback_messages["email_field"] = "Please enter an email address"

    print("d")
    return render_template("signing.html", feedback_messages=feedback_messages)

"""Code"""


"""Email related"""
# If email exists -> sign in, else -> sign up
def determine_signing_state(user_db, email):
    all_emails = user_db.fetch_all_emails()
    is_email_existing = "sign_up" # default value
    for email in all_emails:
        if email[0] == email:
            is_email_existing = "sign_in"
            break

    return is_email_existing


def check_email(email):
    email_regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if email is not None:
        if not re.match(email_regex, email):
            return False
        else:
            return True
    else:
        return None
