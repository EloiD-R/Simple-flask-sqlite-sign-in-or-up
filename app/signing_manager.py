"""IMPORTS"""
from flask import render_template, request, session
import app.sign_in as sign_in
import app.sign_up as sign_up
import app.utils.signing_utils as signing_utils
from app.utils.signing_utils import email_checker

"""Main func"""
def load_signing_page(user_db):
    sign_in_or_sign_up = {"state": "sign_up", "phase": 0}
    default_input_values = [None, None, None, None]
    checked_user_email = None
    error = None

    try:
        try:
            user_email = request.form.get("email_input")
            print("email : {}".format(user_email))
            if user_email:
                session['user_email'] = user_email
                checked_user_email = email_checker(user_email)
            email_existence = signing_utils.is_email_existing(user_db, user_email)
            if email_existence is True:
                sign_in_or_sign_up["state"] = "sign_in"
                sign_in.manage_sign_in(user_db)
            else:
                sign_in_or_sign_up["phase"] = sign_up.manage_sign_up(user_db, sign_in_or_sign_up, user_email)

        except signing_utils.NoInput as noInput:
            sign_in_or_sign_up = {"state": "undetermined", "phase": 0}
    except signing_utils.EmailNotValid as emailNotValid:
        sign_in_or_sign_up = {"state": "undetermined", "phase": 0}
        error = emailNotValid
    finally:
        return render_template("/signing.html", sign_in_or_sign_up=sign_in_or_sign_up, error_message=error)
