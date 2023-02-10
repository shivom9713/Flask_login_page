from flask import Flask, render_template, request, redirect, session, flash, url_for
from flask_mysqldb import MySQL
import os

# Creating connection with Database


app = Flask(__name__)
app.secret_key = os.urandom(24)

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'expense_app'
# app.config['MYSQL_PORT'] = 3306

app.config['MYSQL_HOST'] = 'mysql_db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'development_instance_root_password'
app.config['MYSQL_DB'] = 'warehouse_database'
app.config['MYSQL_PORT'] = 3306
mysql = MySQL(app)
# cur = mysql.connection.cursor()

@app.route("/")
def login():
    if "user_id" in session:
        return redirect(url_for("home"))
    else:
        return render_template("login.html")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/home")
def home():
    if "user_id" in session:
        return render_template("home.html")
    else:
        return redirect("/")


@app.route("/login_validation", methods=["GET", "POST"])
def login_validation():
    email = request.form.get("email")
    password = request.form.get("password")

    cur = mysql.connection.cursor()
    cur.execute(
        f"""SELECT * FROM users WHERE email = '{email}' AND password = '{password}'""")

    users = cur.fetchall()
    # returns in ((a,b,c),(a1,b1,c1),) format that is tuple of tuples

    if len(users) > 0:
        session["user_id"] = users[0][0]
        return redirect(url_for("home"))
    else:
        return redirect(url_for("login"))
    # return f"""SELECT * FROM users WHERE password = '{password}'"""


@app.route("/return_data")
def return_data():
    a = 1
    b = 2
    c = 3
    return render_template("abc.html", a_p=a, b_p=b, c_p=c)


@app.route("/logout_user", methods=["POST", "GET"])
def logout():
    if "user_id" in session:
        session.pop("user_id")
        flash("user logged out successfully")
        return redirect("/")
    return redirect("/")


@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")

    cur = mysql.connection.cursor()
    cur.execute(
        f"""SELECT * FROM users WHERE email = '{email}' AND password = '{password}'""")
    users = cur.fetchall()
    if len(users) > 0:
        return "User already registered"

    elif len(users) == 0:
        cur.execute(
            f"""INSERT INTO users (user_id, name, email, password) VALUES (NULL, '{username}', '{email}', '{password}');""")
        mysql.connection.commit()

        cur.execute(
            f"""SELECT * FROM users WHERE email = '{email}' """)
        user = cur.fetchall()
        session["user_id"] = user[0][0]
        # Adding user_id to session and pushing this to home
        return redirect("/home")


@app.route("/about")
def about():
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True,host="0.0.0.0",port=int("5000"))
