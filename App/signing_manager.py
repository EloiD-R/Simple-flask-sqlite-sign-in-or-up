"""Imports"""
from flask import Flask, redirect, session, render_template_string, request, g, render_template
import re

"""Loader"""
def load(user_db):
    # Allows the html to render the submit button for the email, if the email's correct it will be changed later anyway
    session["signing_phase"] = 0

    feedback_messages = {
        "email_field" : None,
        "username_field" : None,
        "password_field" : None
    }

    # Get email (see the readme for the long explanation)
    if request.form.get('email') is None:
        email = session.get('email')
    else:
        email = request.form.get('email')
        session['email'] = email

    is_email_valid = check_email(email)
    if is_email_valid is True:
        feedback_messages["email_field"] = "Email valid"

        signing_state = determine_signing_state(user_db, email)
        session['signing_state'] = signing_state
        signing_phase = determine_signing_phase(signing_state)
        session['signing_phase'] = signing_phase

    elif is_email_valid is False:
        session['signing_state'] = None
        feedback_messages["email_field"] = "Please enter a valid email address"
    else: # If it's None (no query (first launch or clear cookies))
        pass

    return render_template("signing.html", feedback_messages=feedback_messages)

"""Code"""
def determine_signing_phase(signing_state):
    if signing_state is "sign_in":
        return 1
    elif signing_state is "sign_up":
        if request.form.get('username'):
            return 2
        else:
            return 1

"""Email related"""
# If email exists -> sign in, else -> sign up
def determine_signing_state(user_db, user_email):
    all_emails = user_db.fetch_all_emails()
    is_email_existing = "sign_up" # default value
    for email in all_emails:
        if email[0] == user_email:
            is_email_existing = "sign_in"
            break

    return is_email_existing


def check_email(email):
    email_regex = "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if email is not None:
        if re.match(email_regex, email):
            return True
        else:
            return False
    else:
        return None
