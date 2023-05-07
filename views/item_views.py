from flask import request, render_template, redirect, url_for, jsonify

def items():
    return render_template('items.html')