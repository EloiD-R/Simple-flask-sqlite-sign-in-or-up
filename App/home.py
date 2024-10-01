"""Imports"""
from flask import Flask, redirect, session, render_template_string, request, g, render_template

"""Loader"""
def load():
    logout_input = request.form.get("logout")
    if logout_input is not None:
        session.clear()
        return redirect("/sign.in.up")

    return render_template("home.html")