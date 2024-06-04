from taskmanager import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(25), unique=True, nullable=False)
    tasks = db.relationship("Task", backref="category", cascade="all, delete", lazy=True)
    category_owner = db.Column(db.String(15), db.ForeignKey("reader.username"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.category_name



class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(50), unique=True, nullable=False)
    task_description = db.Column(db.Text, nullable=False)
    is_urgent = db.Column(db.Boolean, default=False, nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.id", ondelete="CASCADE"), nullable=False)
    task_owner = db.Column(db.String(15), db.ForeignKey("reader.username"), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return f"#{self.id} - Task: {self.task_name} | Urgent: {self.is_urgent}"
    
class Reader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        # __repr__ to represent itself in the form of a string
        return self.username