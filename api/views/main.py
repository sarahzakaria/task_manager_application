from flask import Blueprint, request, make_response, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta, timezone
from functools import wraps
import jwt
from api.models import Users, Tasks, db
from api.mongodb import mongodb
from api.config import config
from api.worker import celery


main = Blueprint("main", __name__, template_folder='/templates') 

def log_event(event_type, user_id, action_details):
    doc = {
        'event_type': event_type,
        'user_id': user_id,
        'timestamp': datetime.now(timezone.utc),
        'action_details': action_details
    }
    mongodb.insert_one("logs", doc)

def send_email(recipient: str, subject: str, body: str) -> str:
    try:
        celery.send_task('tasks.send_email', args=[recipient, subject, body], kwargs={})
        return
    except Exception as e:
        print("send_email", e)

@main.route("/")
def index():
    return redirect(url_for('main.login'))


@main.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        data = request.form
        email = data.get("email")
        firstName = data.get("firstName")
        lastName = data.get("lastName")
        password = data.get("password")
        is_admin = False  # Default to False unless checkbox is checked

        if firstName and lastName and email and password:
            user = Users.query.filter_by(email=email).first()
            if user:
                flash("Please Sign In", "warning")
                return redirect(url_for('main.login'))
            user = Users(
                email=email,
                password=generate_password_hash(password),
                firstName=firstName,
                lastName=lastName,
                is_admin=is_admin
            )
            db.session.add(user)
            db.session.commit()
            flash("User Created", "success")
            return redirect(url_for('main.login'))

        flash("Unable to create User", "danger")
        return redirect(url_for('main.signup'))

    return render_template("signup.html")


@main.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        auth = request.form
        if not auth or not auth.get("email") or not auth.get("password"):
            flash("Proper Credentials were not provided", "danger")
            return redirect(url_for('main.login'))

        user = Users.query.filter_by(email=auth.get("email")).first()
        if not user:
            flash("Please create an account", "warning")
            return redirect(url_for('main.signup'))

        if check_password_hash(user.password, auth.get("password")):
            try:
                token = jwt.encode(
                    {
                        'id': user.id,
                        'exp': datetime.utcnow() + timedelta(minutes=30)
                    },
                    config.secret_key,
                    algorithm="HS256"
                )
                response = make_response(redirect(url_for('main.tasks')))
                response.set_cookie('token', token)
                log_event('login', auth.get("email"), f"Login event using id = {user.id}")
                send_email(user.email , 'Login', datetime.now(timezone.utc))
                return response
            except Exception as e:
                flash("Internal Server Error", "danger")
                return redirect(url_for('main.login'))

        flash("Please check your credentials", "danger")
        return redirect(url_for('main.login'))

    return render_template("login.html")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')

        if not token:
            return make_response(({"message": "Token is missing"}), 401)

        try:
            data = jwt.decode(token, config.secret_key, algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data["id"]).first()
        except jwt.ExpiredSignatureError:
            return make_response(make_response({"message": "Token has expired"}), 401)
        except jwt.InvalidTokenError:
            return make_response(make_response({"message": "Invalid token"}), 401)
        except Exception as e:
            print(e)
            return make_response(make_response({"message": "Token validation error"}), 401)

        return f(current_user, *args, **kwargs)

    return decorated


@main.route("/tasks", methods=["GET"])
@token_required
def tasks(current_user):
    if current_user.is_admin:
        tasks = Tasks.query.all()
    else:
        tasks = Tasks.query.filter_by(user_id=current_user.id).all()
    return render_template("tasks.html", tasks=tasks)


@main.route("/task/new", methods=["GET", "POST"])
@token_required
def new_task(current_user):
    if request.method == "POST":
        data = request.form
        name = data.get("name")
        description = data.get("description")
        priority = data.get("priority")
        due_date_str = data.get("due_date")

        if not all([name, priority, due_date_str]):
            flash("Missing required fields", "danger")
            return redirect(url_for("main.new_task"))

        try:
            if len(due_date_str) == 16:
                due_date_str += ":00"
            input_format = "%Y-%m-%dT%H:%M:%S"
            due_date = datetime.strptime(due_date_str, input_format)
        except ValueError:
            flash("Invalid due_date format, use ISO format: YYYY-MM-DDTHH:MM:SS", "danger")
            return redirect(url_for("main.new_task"))
        try:
            task = Tasks(
                name=name,
                description=description,
                priority=priority,
                due_date=due_date,
                user_id=current_user.id
            )
            db.session.add(task)
            db.session.commit()
            flash("Task Created", "success")
            log_event('task_created', data.get("name"), f"Create task event using id = {current_user.id}")
            send_email(data.get("name"), 'Create Task', datetime.now(timezone.utc))

            return redirect(url_for("main.tasks"))
        except Exception as e:
            db.session.rollback()
            flash("Internal Server Error", "danger")
            return redirect(url_for("main.new_task"))

    return render_template("task_form.html", form_title="New Task", form_action=url_for("main.new_task"), task=None)


@main.route("/task/<int:task_id>/edit", methods=["GET", "POST"])
@token_required
def edit_task(current_user, task_id):
    task = Tasks.query.get(task_id)
    if not task or (current_user.id != task.user_id and not current_user.is_admin):
        return redirect(url_for("main.tasks"))

    if request.method == "POST":
        data = request.form
        name = data.get("name")
        description = data.get("description")
        priority = data.get("priority")
        due_date_str = data.get("due_date")

        if not all([name, priority, due_date_str]):
            flash("Missing required fields", "danger")
            return redirect(url_for("main.edit_task", task_id=task_id))

        try:
            if len(due_date_str) == 16:
                due_date_str += ":00"
            input_format = "%Y-%m-%dT%H:%M:%S"
            due_date = datetime.strptime(due_date_str, input_format)
        except ValueError:
            flash("Invalid due_date format, use ISO format: YYYY-MM-DDTHH:MM:SS", "danger")

        try:
            task.name = name
            task.description = description
            task.priority = priority
            task.due_date = due_date
            db.session.commit()
            flash("Task Updated", "success")
            log_event('task_updated', task.name, f"Update task event using id = {current_user.id}")
            send_email(task.name, 'Update Task', datetime.now(timezone.utc))

            return redirect(url_for("main.tasks"))
        except Exception as e:
            db.session.rollback()
            flash("Internal Server Error", "danger")
            return redirect(url_for("main.edit_task", task_id=task_id))

    return render_template("task_form.html", form_title="Edit Task", form_action=url_for("main.edit_task", task_id=task_id),
                           task=task)


@main.route("/task/<int:task_id>/delete", methods=["POST"])
@token_required
def delete_task(current_user, task_id):
    task = Tasks.query.get(task_id)

    if not task:
        flash("Task not found", "danger")
        return redirect(url_for("main.tasks"))

    if current_user.id != task.user_id and not current_user.is_admin:
        flash("Unauthorized to delete this task", "danger")
        return redirect(url_for("main.tasks"))

    db.session.delete(task)
    db.session.commit()
    flash("Task deleted successfully", "success")
    return redirect(url_for("main.tasks"))


@main.route("/admin/tasks", methods=["GET"])
@token_required
def get_all_tasks_for_admin(current_user):
    if not current_user.is_admin:
        flash("Unauthorized, admin access required", "danger")
        return redirect(url_for("maintasks"))

    tasks = Tasks.query.all()
    return render_template("tasks.html", tasks=tasks)
