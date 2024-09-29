"""Imports"""
from flask import Flask, redirect, session, render_template_string, request, g, render_template

"""Loader"""
def load():
    return render_template("signing.html")