

from flask import Flask, request, render_template, redirect
import mysql.connector

app = Flask(__name__)

my_db = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Admin@1",
  database="mydatabase"
)

mycursor = my_db.cursor()
mycursor.execute("CREATE TABLE IF NOT EXISTS todos (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), dueDate VARCHAR(255))")

@app.route('/')
def home():
    sql = "SELECT id,name,dueDate,status FROM todos"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    if len(myresult) == 0:
        list =""
    else:
        list=myresult

    return render_template("home.html", user='', list=list)

@app.route("/add", methods=['POST', 'GET'])
def add():
  if request.method == 'POST':
    name = request.form.get('name')
    dueDate = request.form.get('duedate')
    status = "Not Done"
    
    sql = "INSERT INTO todos(name,dueDate,status) VALUES (%s, %s, %s)"
    values =[name,dueDate,status]
    mycursor.execute(sql, values)

    my_db.commit()

    return redirect("/")

@app.route('/delete/<int:id>')
def delete(id):
    
    sql = "DELETE FROM todos WHERE id= %s"
    value = (id,)

    mycursor.execute(sql, value)
    my_db.commit()

    return redirect('/')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
  
  if request.method == 'POST':
    name = request.form.get('name')
    dueDate = request.form.get('duedate')
    status = request.form.get('status')
    
    sql = "UPDATE todos SET name= %s, dueDate= %s, status= %s WHERE id= %s"
    values = (name, dueDate, status, id)
    mycursor.execute(sql, values)

    my_db.commit()

    return redirect("/")
  else:
    sql = "SELECT id,name,dueDate,status FROM todos WHERE id= %s"
    value = (id,)
    mycursor.execute(sql, value)
    myresult = mycursor.fetchone()

    return render_template('edit.html', user='', task=myresult)

if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
