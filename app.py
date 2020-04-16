from flask import Flask, redirect, render_template, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cr_users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key = True)
    first_name = db.Column(db.String(45))
    last_name = db.Column(db.String(45))
    email = db.Column(db.String(45))
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default = func.now())
    updated_at = db.Column(db.DateTime, server_default = func.now(), onupdate = func.now())

@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users = users)

@app.route("/create", methods=['POST'])
def create():
    new_user = User(first_name = request.form['first_name'], last_name = request.form['last_name'], email = request.form['email'], age = request.form['age'])
    db.session.add(new_user)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)