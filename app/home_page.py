from flask import Flask, render_template, request, redirect, url_for, session

def load_home_page():
    logout_input = request.form.get("logout")
    if logout_input is not None:
        session["login_state"] = False
        session["user_id"] = None
        session["username"] = None
        session["user_email"] = None
        return redirect("/sign.in.up")

    return render_template("/home.html", user_id=session['user_id'], username=session['username'], user_email=session['user_email'])