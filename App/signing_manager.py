"""Imports"""
from flask import Flask, redirect, session, render_template_string, request, g, render_template
import bcrypt
import re

"""Loader"""
def load(user_db):
    # Allows the html to render the submit button for the email, if the email's correct it will be changed later anyway
    session["signing_phase"] = 0

    # Messages to display for each input
    feedback_messages = {
        "email_field" : None,
        "username_field" : None,
        "password_field" : None
    }


    # Email :
    # Get input and remove whitespaces, lowercase it
    email = get_input("email")
    if email:
        email = email.replace(" ", "").lower()

    # Check email, if it's all good determine state and phase.
    is_email_valid = check_email(email)
    if is_email_valid is True:
        feedback_messages["email_field"] = "Email valid"
        session['signing_state'] = determine_signing_state(user_db, email)
        session['signing_phase'] = determine_signing_phase(session.get("signing_state"))
    elif is_email_valid is False:
        session["signing_state"] = None
        feedback_messages["email_field"] = "Please enter a valid email address"
    else: # If it's None (no query (first launch or clear cookies))
        pass

    # Sign_up :
    # If a state was determined watch for username, password. If both input are filled and ok -> create user, connect
    if session.get("signing_state") == "sign_up":
        if session.get("signing_phase"):
            if session.get("signing_phase") > 0:
                username = get_input("username")
                is_username_valid = check_username(username)
                if is_username_valid is True:
                    feedback_messages["username_field"] = "username valid"
                else:
                    if is_username_valid == "username must be at least 3 characters" or is_username_valid == "username must be at most 20 characters":
                        feedback_messages["username_field"] = is_username_valid
            if session.get("signing_phase") > 1:
                password = get_input("password")
                is_password_valid = check_password(password)
                if is_password_valid is not None:
                    if is_password_valid == "password must be at least 8 characters":
                        feedback_messages["password_field"] = is_password_valid
                    if is_password_valid == True:
                        feedback_messages["password_field"] = "Password valid"
                        password = hash_password(password)
                        user_db.create_user(email, username, password)
                        session.clear()
                        session["email"], session["username"], session["login_state"] = email, username, True
                        return redirect("/home")

    # Sign_in :
    # If a state was determined, look for password, compare it to the hash, if it's all right -> connect
    elif session.get("signing_state") == "sign_in":
        if session.get("signing_phase") > 0:
            password = get_input("password")
            if password:
                password = password.encode("utf-8")
                if bcrypt.checkpw(password, user_db.get_password_hash_by_email(email)):
                    feedback_messages["password_field"] = "Password valid"
                    session.clear()
                    session["email"], session["username"], session["login_state"] = email, user_db.get_username_by_email(email), True
                    return redirect("/home")
                else:
                    feedback_messages["password_field"] = "Password invalid"


    return render_template("signing.html", feedback_messages=feedback_messages)


"""Code"""
def determine_signing_phase(signing_state):
    if signing_state == "sign_in":
        return 1
    elif signing_state == "sign_up":
        if get_input("username"):
            return 2
        else:
            return 1

def get_input(field):
    # See the readme to know why i read from form or cookies
    if request.form.get(field) is None:
        user_input = session.get(field)
    else:
        user_input = request.form.get(field)
        session[field] = user_input

    return user_input


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

def check_username(username):
    if username is not None:
        if len(username) < 3:
            return "username must be at least 3 characters"
        elif len(username) > 20:
            return "username must be at most 20 characters"
        else:
            return True
    else:
            return None

def check_password(password):
    # password_regex = "" # usable but i'm not gonna
    if password is not None:
        if len(password) < 8:
            return "password must be at least 8 characters"
        else:
            return True
    else:
        return None


def hash_password(password):
    # str -> bstr
    password_bytes = password.encode('utf-8')
    # generating the salt
    salt = bcrypt.gensalt()
    # hashing the password
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password
