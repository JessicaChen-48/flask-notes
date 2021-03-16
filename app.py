from flask import Flask, render_template, redirect, flash

from models import db, connect_db, User

from forms import 

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///[ADDDBNAME]"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

connect_db(app)
db.create_all()

@app.route("/")
def homepage():

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register():

    form = RegisterForm()

    

    else:
        return render_template("register.html", form=form)

