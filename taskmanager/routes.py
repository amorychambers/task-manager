from flask import render_template, request, redirect, url_for, flash, session
from taskmanager import app, db
from taskmanager.models import Category, Task, Reader
from werkzeug.security import generate_password_hash, check_password_hash


@app.route("/")
def home():
    tasks = list(Task.query.order_by(Task.due_date).all())
    return render_template("tasks.html", tasks=tasks)


@app.route("/register", methods=["GET", "POST"])
def register():
    readers = list(Reader.query.all())
    if request.method == "POST":
        # Check if username already exists
        q = db.session.query(Reader.id).filter(Reader.username==request.form.get("username").lower())
        if db.session.query(q.exists()).scalar():
            flash("Username already taken")
            redirect(url_for("register"))
        else:
            reader = Reader(
                username=request.form.get("username").lower(),
                password=generate_password_hash(request.form.get("password")))
            db.session.add(reader)
            db.session.commit()
            flash("Registration successful!")
            return redirect(url_for("profile", username=session["user"]))

    return render_template("register.html", readers=readers)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Check that username exists
        q = db.session.query(Reader).filter(Reader.username==request.form.get("username").lower())
        if db.session.query(q.exists()).scalar():
            # Check password is correct
            if check_password_hash(q.first().password, request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("profile", username=session["user"]))
            else:
            # Password is not correct
                flash("Incorrect Username and/or Password")
                return redirect(url_for("login"))
        
        else:
            # Username does not exist
            flash("Incorrect Username and/or Password")
            return redirect(url_for("login"))
            
    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    # Find session user's username in the database
    username = db.session.query(Reader).filter(
    Reader.username == session["user"]).first().username
    if session["user"]:
        return render_template("profile.html", username=username)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out")
    return render_template("login.html")


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