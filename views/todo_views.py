from flask import request, render_template, redirect, url_for, jsonify

def todos():
    return render_template('todos.html')