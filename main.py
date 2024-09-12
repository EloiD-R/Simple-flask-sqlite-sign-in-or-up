from app.signing_manager import load_signing_page
from app.home_page import load_home_page
from utils.db.user_db import userDB
from flask import Flask, render_template, request, redirect, url_for, session, render_template_string

"""Code"""

def init_session_cookies():
    if 'login_state' not in session:
        session['login_state'] = False
        session['user_id'] = None
        session['username'] = None
        session['user_email'] = None

"""Main flask_app"""
if __name__ == "__main__":
    # Create a userDB object, so I can give it to other functions for them to use methods to read/write it
    user_db = userDB()

    # Flask and session cookies key init
    flask_app = Flask("sign.in.up - sqlite - flask")
    flask_app.secret_key = b'\xe5\xef\x92\x89\xc9v\x18\x14P\xbf\x88\xd7\x19\xff\x8b\x1aH\xd2\x15\xc7\xd0\x1cv\xf6'


    @flask_app.route("/", methods=["GET", "POST"])
    def route_index():
        # If there are no session cookies
        init_session_cookies()

        # Check if user is connected, redirect him to the right place
        if session['login_state'] is True:
            return redirect("/home")
        else:
            return redirect("/sign.in.up")


    @flask_app.route("/sign.in.up", methods=["GET", "POST"])
    def route_sign_in_or_up():
        # If there are no session cookies
        init_session_cookies()

        # Check if user is connected, redirect him to the right place
        if session['login_state'] is True:
            return redirect("/home")
        else:
            return load_signing_page(user_db)


    @flask_app.route("/home", methods=["GET", "POST"])
    def route_home():
        # If there are no session cookies
        init_session_cookies()

        # Check if user is connected, redirect him to the right place
        if session['login_state'] is True:
            return load_home_page()
        else:
            return redirect("sign.in.up")

    @flask_app.errorhandler(404)
    def handle_404(error):
        # Check if user is connected, redirect him to the right place
        if session['login_state'] is True:
            return render_template_string("<h1>Page was not found</h1>")
        else:
            return redirect("sign.in.up")

    flask_app.run(debug=True)