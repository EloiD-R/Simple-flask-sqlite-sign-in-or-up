"""IMPORTS"""
from flask import Flask, render_template, request, redirect, url_for, session
from utils.db import *

"""Main func"""
def load_signing_page(user_db):
    user_email = request.form.get("email_input")
    default_input_values = {'email': user_email, "username": None, "password": None, "password_confirmation": None}


    sign_in_or_sign_up = choose_between_sign_in_and_up(user_db, user_email)
    if sign_in_or_sign_up["state"] == "sign_in":
        manage_sign_in()
    else:
        sign_in_or_sign_up, default_input_values, is_account_created = manage_sign_up(user_db, sign_in_or_sign_up, user_email)
        if is_account_created:
            return render_template("/signing.html", sign_in_or_sign_up=sign_in_or_sign_up, default_input_values=default_input_values)
        else:
            print(f"from load_signin_page : {sign_in_or_sign_up}")


    return render_template("/signing.html", sign_in_or_sign_up=sign_in_or_sign_up, default_input_values=default_input_values)

"""CODE"""
def choose_between_sign_in_and_up(user_db, user_email):
    sign_in_or_sign_up = {"state": "undetermined", "phase": None}
    if user_email:
        email_found = False
        for email in user_db.fetch_all_emails():
            if email[0] == user_email:
                sign_in_or_sign_up["state"] = "sign_in"
                email_found = True
                break

        if not email_found:
            sign_in_or_sign_up["state"] = "sign_up"
            if sign_in_or_sign_up["phase"] == None:
                sign_in_or_sign_up["phase"] = 1

    else:
        pass

    return sign_in_or_sign_up


def manage_sign_in():
    print("SIGNIN")


def manage_sign_up(user_db, sign_in_or_sign_up, email):
    # Because some fields might not be available if phase is not the final one
    username, password, password_confirmation, user_created = None, None, None, None
    if sign_in_or_sign_up["state"] == "sign_up":
        if sign_in_or_sign_up["phase"] == 1:
            username = request.form.get("username_input")
            if username:
                sign_in_or_sign_up["phase"] = 2

        if sign_in_or_sign_up["phase"] == 2:
            password = request.form.get("password_input")
            if password:
                sign_in_or_sign_up["phase"] = 3

        if sign_in_or_sign_up["phase"] == 3:
            password_confirmation = request.form.get("password_confirmation_input")
            print(f"from manage_sign_up : {email}, {username}, {password}, {password_confirmation}")
            user_db.create_user(email, username, password)
            print(f"from manage_sign_up : user created")
            session["login_state"] = True
            session["user_email"] = email
            print(f"from manage_sign_up : {session["user_email"]}, {session["login_state"]}")
            user_created = True

    elif sign_in_or_sign_up["state"] == "sign_in":
        password = request.form.get("password_input")

    default_input_values = {'email' : email, "username" : username, "password" : password, "password_confirmation" : password_confirmation}

    return sign_in_or_sign_up, default_input_values, user_created
