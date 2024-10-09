"""Imports"""
import requests
from flask import Flask, redirect, session, render_template_string, request, g, send_from_directory, render_template
from App import index, home, signing_manager
from App.utils.db.user_db import *

global request_counter
globals()['request_counter'] = 0

if __name__ == "__main__":
    # Flask and session cookies secret key init
    flask_app = Flask("sign.in.up - sqlite - flask")
    print("Flask_app created")
    flask_app.secret_key = b'\xe5\xef\x92\x89\xc9v\x18\x14P\xbf\x88\xd7\x19\xff\x8b\x1aH\xd2\x15\xc7\xd0\x1cv\xf6' # os.urandom(24)
    print("Flask_app secret key for session cookies added")

    """DB MANAGEMENT"""
    # Open db when needed
    def get_user_db():
        db = getattr(g, "_database", None)
        if db is None:
            db = g._database = userDB("user_db")
            print("Database initialized in 'g'")
        print("Database opened and returned via get_user_db()")
        return db

    # Close db at each teardown (end of request, exception, ...)
    @flask_app.teardown_appcontext
    def close_user_db_connection(exception):
        db = getattr(g, '_database', None)
        if db is not None:
            print(f"Closing user_db after teardown context : {exception}")
            db.quit_db()


    @flask_app.before_request
    def requests_counter():
        globals()["request_counter"] += 1
        print(f"Request n°{globals()['request_counter']} since server was launched (made by IP: '{request.remote_addr}').")


    @flask_app.before_request
    def check_if_user_is_connected():
        EXCLUDED_ROUTES = ["route_sign_in_or_up", "route_index"]  # add routes as needed
        route_to_load = request.endpoint  # To make the code more readable
        print(f"IP:'{request.remote_addr}' wants to access {route_to_load}, beginning auth verification")
        if route_to_load == "static":
            print(f"User with IP : '{request.remote_addr}' wants to access a static file, bypassing authentication.")
            return # Just go one so we do't need to put every static file in the excluded route list
        if route_to_load not in EXCLUDED_ROUTES:
            if route_to_load is not None:
                if session.get('login_state') is None or 'login_state' not in session:
                    print(f"IP : {request.remote_addr} with no login_state cookie wants to access {route_to_load}, redirecting him to signing page")
                    return redirect("/sign.in.up")
                elif session['login_state'] is True:
                    print(f"authenticated user with IP : '{request.remote_addr}' with a 'True' login_state cookie that wants to access {route_to_load}, letting him go by.")
                else:
                    print(f"IP : '{request.remote_addr}' with a 'False' login_state cookie that wants to access {route_to_load}, redirecting him to signing page")
                    return redirect("/sign.in.up")

            # Typically occurs when an error is triggered ex : 404
            if route_to_load is None and session.get("login_state") != True:
                print(f"Unauthenticated IP: '{request.remote_addr}' triggered an error or something unexpected, redirecting him to signing page")
                return redirect("/sign.in.up")
            else:
                print(f"IP: '{request.remote_addr}' wants to access an EXCLUDED_ROUTE, bypassing authentication")
                # Else, continue and load request (from EXCLUDED_ROUTES)
        else:
            print(f"IP: '{request.remote_addr}' wants to access an EXCLUDED_ROUTE, bypassing authentication")

    @flask_app.route("/", methods=["GET", "POST"])
    def route_index():
        print(f"IP : '{request.remote_addr}' is accessing '/' index")
        return index.load()

    @flask_app.route("/home", methods=["GET", "POST"])
    def route_home():
        print(f"IP : '{request.remote_addr}' is accessing home page '/home'")
        return home.load()

    @flask_app.route("/sign.in.up", methods=["GET", "POST"])
    def route_sign_in_or_up():
        print(f"IP : '{request.remote_addr}' is accessing the sign in or up page '/sign.in.up'")
        return signing_manager.load(get_user_db(), request.remote_addr)

    @flask_app.errorhandler(404)
    def handle_404(error):
        print(f"IP : '{request.remote_addr}' generated a 404 error")
        return render_template("404.html")


    flask_app.run(debug=True, host="0.0.0.0", port=5000)
