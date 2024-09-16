from app.signing_manager import load_signing_page
from app.home_page import load_home_page
from app.utils.db.user_db import userDB
from flask import Flask, redirect, session, render_template_string, g

"""Code"""
def init_session_cookies(user_db):
    if 'login_state' not in session or session['login_state'] is None:
        session.clear()
        session['login_state'] = False

    elif session['login_state'] is True:
        session['user_id'] = user_db.get_id_by_email(session['user_email'])
        session['username'] = user_db.get_username_by_id(session['user_id'])


"""Main flask_app"""
if __name__ == "__main__":
    # Flask and session cookies key init
    flask_app = Flask("sign.in.up - sqlite - flask")
    flask_app.secret_key = b'\xe5\xef\x92\x89\xc9v\x18\x14P\xbf\x88\xd7\x19\xff\x8b\x1aH\xd2\x15\xc7\xd0\x1cv\xf6'

    def get_user_db():
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = userDB("user_db")
        return db


    @flask_app.teardown_appcontext
    def close_user_db_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            print(f"Closing user_db : {exception}")
            db.quit_db()

    @flask_app.route("/", methods=["GET", "POST"])
    def route_index():
        # If there are no session cookies
        init_session_cookies(get_user_db())

        # Check if user is connected, redirect him to the right place
        if session['login_state'] is True:
            return redirect("/home")
        else:
            return redirect("/sign.in.up")


    @flask_app.route("/sign.in.up", methods=["GET", "POST"])
    def route_sign_in_or_up():
        # If there are no session cookies
        init_session_cookies(get_user_db())

        # Check if user is connected, redirect him to the right place
        if session['login_state'] is True:
            return redirect("/home")
        else:
            return load_signing_page(get_user_db())


    @flask_app.route("/home", methods=["GET", "POST"])
    def route_home():
        # If there are no session cookies
        init_session_cookies(get_user_db())

        # Check if user is connected, redirect him to the right place
        if session['login_state'] is True:
            return load_home_page()
        else:
            return redirect("sign.in.up")

    @flask_app.errorhandler(404)
    def handle_404(error):
        # Check if user is connected, redirect him to the right place
        if session['login_state'] is True:
            return render_template_string(f"<h1>{error}</h1>")
        else:
            return redirect("sign.in.up")

    flask_app.run(debug=True)