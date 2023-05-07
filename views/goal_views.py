from flask import request, render_template, redirect, url_for, jsonify

def goals():
    return render_template('goals.html')