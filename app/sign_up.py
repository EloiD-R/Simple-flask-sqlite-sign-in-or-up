"""IMPORTS"""
from http.client import error

from flask import Flask, render_template, request, redirect, url_for, session
from utils.db import *
import re

"""CODE"""
def manage_sign_up(user_db, sign_in_or_sign_up, email):
    # Because some fields might not be available if phase is not the final one
    username, password, password_confirmation, is_user_created = None, None, None, None
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
            is_user_created = True

    elif sign_in_or_sign_up["state"] == "sign_in":
        password = request.form.get("password_input")

    default_input_values = {'email' : email, "username" : username, "password" : password, "password_confirmation" : password_confirmation}

    return sign_in_or_sign_up, default_input_values, is_user_created
