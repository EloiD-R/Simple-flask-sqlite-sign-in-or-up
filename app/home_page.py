from flask import Flask, render_template, request, redirect, url_for, session

def load_home_page():
    return render_template("/home.html", user_id=session['user_id'], username=session['username'], user_email=session['user_email'])