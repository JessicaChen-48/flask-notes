from flask import Flask, render_template, request, redirect, flash, session

from models import db, connect_db, User

from forms import RegisterForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///notes"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

@app.route("/")
def homepage():

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User.register(username, password, email, first_name, last_name)
        db.session.add(user)
        db.session.commit()

        session["username"] = user.username
        return redirect("/secret")

    else:
        return render_template("register.html", form=form)

@app.route("/users/<username>")
def show_secret_page(username):

    user = User.query.get(username)

    print(f"user: {user.username}")
    print(f"session: {session['username']}")

    if not (session["username"] == user.username):
        flash("You must be logged in to view!")
        return redirect("/")

    return render_template("user_info.html", user=user)


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(username, password)

        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Incorrect name/password"]

    return render_template("login.html", form=form)

# end-login

@app.route("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    session.pop("username", None)

    return redirect("/")


