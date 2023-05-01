from flask import Flask, render_template, redirect, url_for, request
from models import db
from flask_sqlalchemy import SQLAlchemy
from views.main_views import index
from views.task_views import add_task, toggle_task
from views.grocery_views import add_grocery_item, toggle_grocery

# Initialize Flask web app instance
app = Flask(__name__)
# Set the database URI to use a SQLite database named 'tasks.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

db.init_app(app)

with app.app_context():
    db.create_all()

app.add_url_rule("/", view_func=index)
app.add_url_rule("/add", view_func=add_task, methods=["POST"])
app.add_url_rule("/toggle-task/<int:task_id>", view_func=toggle_task, methods=["POST"])
app.add_url_rule("/add-grocery", view_func=add_grocery_item, methods=["POST"])
app.add_url_rule("/toggle-grocery/<int:grocery_id>", view_func=toggle_grocery, methods=["POST"])


if __name__ == '__main__':
    app.run(debug=True)
