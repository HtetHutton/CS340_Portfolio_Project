from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'classmysql.engr.oregonstate.edu'
app.config['MYSQL_USER'] = 'cs340_huttonh'
app.config['MYSQL_PASSWORD'] = '7386'  # last 4 of onid
app.config['MYSQL_DB'] = 'cs340_huttonh'
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql = MySQL(app)


# Routes
@app.route('/')
def root():
    #query = "SELECT * FROM Customers;"
    #query4 = 'SELECT * FROM Customers;';
    #cur = mysql.connection.cursor()  # Open up connection
    #cur.execute(query4)
    #results = cur.fetchall()

    # return "<H1>My SQL Results:</H1>" + str(results[0])
    return render_template("main.j2")

@app.route('/customers', methods=["POST", "GET"])
def customers():
    if request.method == "GET": # Just displaying table contents
        query = "SELECT * FROM Customers;"
        cur = mysql.connection.cursor()  # Open up connection
        cur.execute(query)
        results = cur.fetchall()
        return render_template("customers.j2", Customers=results)

    if request.method == "POST": # INSERT INTO table
        if request.form.get("addCustomer"): # Came from user clicking "Add Customer" button.
            first_name = request.form["cfname"]  
            last_name = request.form["clname"]
            email = request.form["cemail"]
            customer_phone = request.form["cphone"]   # These variables are names from j2 template. 

            # All fields must be filled. 
            query = "INSERT INTO `Customers` (first_name, last_name, email, customer_phone) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()  # Open up connection
            cur.execute(query, (first_name, last_name, email, customer_phone))
            mysql.connection.commit()
            return redirect('/customers')
            # Need to implement CASCADE to Orders later. 

        elif request.form.get("deleteCustomer"): # Came from user clicking "Delete Customer" button.
            customer_id = request.form["cid"]
            query = "DELETE FROM `Customers` WHERE customer_id= %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (customer_id,))
            mysql.connection.commit()
            return redirect('/customers')

        elif request.form.get("updateCustomer"): # Came from user clicking "Update Customer" button. 
            customer_id = request.form["cid"]
            first_name = request.form["cfname"]  
            last_name = request.form["clname"]
            email = request.form["cemail"]
            customer_phone = request.form["cphone"]

            query = "UPDATE `Customers` SET first_name=%s, last_name=%s, email=%s, customer_phone=%s WHERE customer_id=%s"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, email, customer_phone, customer_id))
            mysql.connection.commit()
            return redirect('/customers')


@app.route('/pizzas', methods=["POST", "GET"])
def pizzas():
    if request.method == "GET": # Just displaying table contents
        query = "SELECT * FROM Pizzas;"
        cur = mysql.connection.cursor()  # Open up connection
        cur.execute(query)
        results = cur.fetchall()
        return render_template("pizzas.j2", Pizzas=results)

    if request.method == 'POST':
        if request.form.get("addPizza"): # Came from user clicking "Add Pizza" button.
            pizza_type = request.form["ptype"]  
            pizza_price = request.form["pprice"]

            # All fields must be filled. 
            query = "INSERT INTO `Pizzas` (pizza_type, pizza_price) VALUES (%s, %s)"
            cur = mysql.connection.cursor()  # Open up connection
            cur.execute(query, (pizza_type, pizza_price))
            mysql.connection.commit()
            return redirect('/pizzas')
            # Need to implement CASCADE to Orders later. 

        elif request.form.get("updatePizza"): # Came from user clicking "Update Pizza" button.
            pizza_id = request.form["pid"]
            pizza_type = request.form["ptype"]  
            pizza_price = request.form["pprice"]

            # All fields must be filled. 
            query = "UPDATE `Pizzas` SET pizza_type=%s, pizza_price=%s WHERE pizza_id=%s"
            cur = mysql.connection.cursor()  # Open up connection
            cur.execute(query, (pizza_type, pizza_price, pizza_id))
            mysql.connection.commit()
            return redirect('/pizzas')
            # Need to implement CASCADE to Orders later.

@app.route('/employees', methods=["POST", "GET"])
def employees():
    if request.method == "GET": # Just displaying table contents
        query = "SELECT * FROM Employees;"
        cur = mysql.connection.cursor()  # Open up connection
        cur.execute(query)
        results = cur.fetchall()
        return render_template("employees.j2", Employees=results)

    if request.method == "POST": # INSERT INTO table
        if request.form.get("addEmployee"):
            employee_first_name = request.form["efname"]
            employee_last_name = request.form["elname"]
            hourly_wage = request.form["hwage"]

            query = "INSERT INTO `Employees` (employee_first_name, employee_last_name, hourly_wage) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()  # Open up connection
            cur.execute(query, (employee_first_name, employee_last_name, hourly_wage))
            mysql.connection.commit()
            return redirect('/employees')


@app.route('/orders')
def orders():
    query = "SELECT * FROM Orders"
    cur = mysql.connection.cursor()  # Open up connection
    cur.execute(query)
    results = cur.fetchall()
    return render_template("orders.j2", Orders=results)

# Listener
if __name__ == "__main__":
    # Start the app on port 3000, it will be different once hosted
    app.run(port=7387, debug=True)