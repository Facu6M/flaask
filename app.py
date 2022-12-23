from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
import os


app = Flask(__name__)
app.config["MYSQL_HOST"]= "bofirw429yk1vjx5lqak-mysql.services.clever-cloud.com"
app.config["MYSQL_USER"]= "ugvo3vtnsufnbbuy"
app.config["MYSQL_PASSWORD"]= "7c2Lv6bY2tbn3zC4YuG2"
app.config["MYSQL_DB"]= "bofirw429yk1vjx5lqak"
mysql = MySQL(app)

app.secret_key = "facu22"

#Routa por defecto

@app.route("/")
def Index():
    return render_template("head.html")

#Ir a pagina de USUARIO y DATOS
@app.route("/add")
def add():
    return render_template("creacion_usuario.html")

#Añadir usuario y datos
@app.route("/add_user", methods=["POST"])
def add_contact():
        username = request.form["username"]
        name = request.form["name"]
        surname = request.form["surname"]
        email = request.form["email"]
        password = request.form["password"]
        phone = request.form["phone"]
        cur1 = mysql.connection.cursor()
        cur1.execute("SELECT email FROM user ")
        mail = cur1.fetchall()
        for i in mail:
            string = ' '.join(i)
            if email == string :
              return render_template("error_creacion_usuario.html")
            else:
              cur = mysql.connection.cursor()
              cur.execute("INSERT INTO user (username, name, surname, email, password, phone) VALUES (%s, %s, %s, %s, %s, %s)", (username, name, surname, email, password, phone))
              mysql.connection.commit()
              return redirect(url_for("Index"))


@app.route("/login")
def login():
    return render_template("iniciar_sesion.html")

@app.route("/iniciar", methods=["GET"])
def iniciar():
    email = request.args.get("email")
    password = request.args.get("password")
    conjunto = email + " " + password
    cur1 = mysql.connection.cursor()
    cur1.execute("SELECT email,password FROM user")
    datas = cur1.fetchall()
    for i in datas:
        str = ' '.join(i)
        print(str)
        if conjunto == str:
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM user WHERE email = %s", [email])
            datos = cur.fetchall()
            return render_template("main.html", usuarios = datos)
            print("es igual")

        else:
            print("noes igual")
    return render_template("iniciar_sesion.html")






@app.route("/delete/<string:id>")
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM gastos WHERE id = {0}".format(id))
    mysql.connection.commit()
    return redirect(url_for("Index"))


port = int(os.environ.get('PORT', 5000))

if __name__ == "__main__":
   app.run(host='0.0.0.0', port=port, debug=True)
