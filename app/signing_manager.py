from flask import Flask, render_template, request, redirect, url_for, session
from utils.db import *

def load_signing_page(user_db):
    sign_in_or_sign_up = "undetermined"
    user_email = request.form.get("email_input")
    default_input_values = {'email' : user_email}

    if user_email:
        email_found = False
        for email in user_db.fetch_all_emails():
            if email[0] == user_email:
                sign_in_or_sign_up = "sign_in"
                print("email found")
                email_found = True
                break

        if not email_found:
            sign_in_or_sign_up = "sign_up"
            print("email not found")
    else:
        pass

    print(sign_in_or_sign_up)




    return render_template("/signing.html", sign_in_or_sign_up=sign_in_or_sign_up, default_input_values=default_input_values)
