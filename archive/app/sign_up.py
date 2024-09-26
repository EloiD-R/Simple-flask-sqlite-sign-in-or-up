"""IMPORTS"""
from flask import Flask, render_template, request, redirect, url_for, session
import App.utils.signing_utils as signing_utils
from App.utils.db import *
import re

sign_up_form_inputs = {"email" : None, "username" : None, "password" : None, "password_confirmation" : None}

"""CODE"""
def manage_sign_up(user_db, sign_in_or_sign_up, email):
    sign_up_form_inputs["email"] = email
    sign_up_form_inputs_getter_and_setter(sign_in_or_sign_up)

    sign_in_or_sign_up["phase"] = signing_utils.phase_setter(sign_in_or_sign_up)

    print(f"From manage_sign_up : \n\tusername : {sign_up_form_inputs['username']}, email : {sign_up_form_inputs['email']}, password : {sign_up_form_inputs['password']}, password_confirmation : {sign_up_form_inputs['password_confirmation']}")

    return sign_in_or_sign_up["phase"]


def sign_up_form_inputs_getter_and_setter(sign_in_or_sign_up):
    sign_up_form_inputs = {"username" : None, "password" : None, "password_confirmation" : None}
    if sign_in_or_sign_up["phase"] == 1:
        sign_up_form_inputs["username"] = request.form.get("username_input")
    elif sign_in_or_sign_up["phase"] == 2:
        sign_up_form_inputs["username"] = request.form.get("username_input")
        sign_up_form_inputs["password"] = request.form.get("password_input")
    elif sign_in_or_sign_up["phase"] == 3:
        sign_up_form_inputs["username"] = request.form.get("username_input")
        sign_up_form_inputs["password"] = request.form.get("password_input")
        sign_up_form_inputs["password_confirmation"] = request.form.get("password_confirmation_input")
