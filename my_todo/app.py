from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.String(300))
    priority = db.Column(db.String(20), nullable=False)
    is_completed = db.Column(db.Boolean, default=False)
    due_date = db.Column(db.Date, nullable=False)


@app.route("/")
def home():
    pending_tasks = Task.query.filter_by(is_completed=False).all()
    completed_tasks = Task.query.filter_by(is_completed=True).all()

    return render_template(
        "home.html",
        pending_tasks=pending_tasks,
        completed_tasks=completed_tasks
    )
@app.route("/add", methods=["POST"])
def add():
    title = request.form["title"]
    description = request.form["description"]
    priority = request.form["priority"]
    due_date = datetime.strptime(
        request.form["due_date"], "%Y-%m-%d"
    ).date()

    task = Task(
        title=title,
        description=description,
        priority=priority,
        due_date=due_date
    )

    db.session.add(task)
    db.session.commit()

    return redirect(url_for("home"))

@app.route("/toggle/<int:id>")
def toggle(id):
    task = Task.query.get_or_404(id)

    task.is_completed = not task.is_completed

    db.session.commit()

    return redirect(url_for("home"))



@app.route("/update/<int:id>", methods=["POST"])
def update(id):
    task = Task.query.get_or_404(id)

    task.title = request.form["title"]
    task.description = request.form["description"]
    task.priority = request.form["priority"]

    task.due_date = datetime.strptime(
        request.form["due_date"], "%Y-%m-%d"
    ).date()

    db.session.commit()

    return redirect(url_for("home"))

@app.route("/delete/<int:id>", methods=["POST"])
def delete(id):
    task = Task.query.get_or_404(id)

    db.session.delete(task)
    db.session.commit()

    return redirect(url_for("home"))

with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(debug=True)