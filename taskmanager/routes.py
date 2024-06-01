from flask import render_template, request, redirect, url_for, flash
from taskmanager import app, db
from taskmanager.models import Category, Task, User
from werkzeug.security import generate_password_hash, check_password_hash

@app.route("/")
def home():
    tasks = list(Task.query.order_by(Task.due_date).all())
    return render_template("tasks.html", tasks=tasks)

@app.route("/register", methods=["GET", "POST"])
def register():
    users = list(User.query.all())
    if request.method == "POST":
        # Check if username already exists
        existing_user = db.session.query(User).filter(
            User.username == request.form.get("username").lower())
        if db.session.query(existing_user.exists()):
            flash("Username already taken")
            return redirect(url_for("register"))
        user = User(username=request.form.get("username").lower(), password=generate_password_hash(request.form.get("password")))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("home"))

    return render_template("register.html", users=users)

@app.route("/categories")
def categories():
    categories = list(Category.query.order_by(Category.category_name).all())
    return render_template("categories.html", categories=categories)

@app.route("/add_category", methods=["GET", "POST"])
def add_category():
    if request.method == "POST":
        category = Category(category_name=request.form.get("category_name"))
        db.session.add(category)
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("add_category.html")

@app.route("/edit_category/<int:category_id>", methods=["GET", "POST"])
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    if request.method == "POST":
        category.category_name = request.form.get("category_name")
        db.session.commit()
        return redirect(url_for("categories"))
    return render_template("edit_category.html", category=category)

@app.route("/delete_category/<int:category_id>")
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("categories"))

@app.route("/add_task", methods=["GET", "POST"])
def add_task():
    categories = list(Category.query.order_by(Category.category_name).all())
    if request.method == "POST":
        task = Task(
            task_name=request.form.get("task_name"),
            task_description=request.form.get("task_description"),
            is_urgent=bool(True if request.form.get("is_urgent") else False),
            due_date=request.form.get("due_date"),
            category_id=request.form.get("category_id")
            )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("add_task.html", categories=categories)

@app.route("/delete_task/<int:task_id>")
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/edit_task/<int:task_id>", methods=["GET", "POST"])
def edit_task(task_id):
    categories = list(Category.query.order_by(Category.category_name).all())
    task = Task.query.get_or_404(task_id)
    if request.method == "POST":
        task.task_name = request.form.get("task_name")
        task.task_description = request.form.get("task_description")
        task.due_date = request.form.get("due_date")
        task.is_urgent = bool(True if request.form.get("is_urgent") else False)
        task.category_id = request.form.get("category_id")
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit_task.html", task=task, categories=categories)