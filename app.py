from flask import Flask, request, render_template, redirect, url_for, abort, flash, Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "g3nt!"

app.config["MYSQL_HOST"] = "LOCALHOST"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Ambra11erla"
app.config["MYSQL_DB"] = "blog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

#Show
@app.route("/")
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close

    return render_template("index.html", students=data)

#insert
@app.route("/register", methods=['GET'])
def register_get():
    return render_template("insert.html")


@app.route("/register", methods=["POST"])
def register_post():
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone,))
        mysql.connection.commit()
        return redirect(url_for('index'))


#delete
@app.route("/<int:id>/delete", methods=["POST"])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM students WHERE id=%s", (id,))
    mysql.connection.commit()
    return redirect(url_for("index"))


#update
@app.route("/<int:id>/update", methods=["POST", "GET"])
def update(id):
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        phone = request.form["phone"]

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE students
        set name=%s, email=%s, phone=%s
        WHERE id=%s
        """, (name, email, phone, id,))
        mysql.connection.commit()
        return render_template("update.html",id=id)

app.run(debug=True)
