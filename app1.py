from flask import Flask, render_template, request, redirect, session
from db import get_connection

app = Flask(__name__)
app.secret_key = "bhavna_secret_key"

# ---------- HOME PAGE ----------
@app.route("/")
def home():
    return render_template("home.html")


# ---------- SIGNUP ----------
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO Users (Name, Email, Password) VALUES (?, ?, ?)",
                       (name, email, password))

        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("signup.html")


# ---------- LOGIN ----------
@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Users WHERE Email=? AND Password=?", (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            session["user_name"] = user.Name
            session["user_email"] = user.Email
            return redirect("/dashboard")

        else:
            error = "Invalid email or password!"

    return render_template("login.html", error=error)


# ---------- DASHBOARD ----------
@app.route("/dashboard")
def dashboard():
    if "user_name" not in session:
        return redirect("/login")

    return render_template("dashboard.html", name=session["user_name"])

@app.route("/profile")
def profile():

    if "user_email" not in session:
        return redirect("/login")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT ID, Name, Email FROM Users WHERE Email = ?", (session["user_email"],))
    user = cursor.fetchone()

    conn.close()

    if user:
        return render_template(
            "profile.html",
            id=user[0],
            name=user[1],
            email=user[2]
        )
    else:
        return redirect("/login")


@app.route("/edit")
def edit_account():
    
    return render_template("edit_account.html")

# ---------- LOGOUT ----------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
