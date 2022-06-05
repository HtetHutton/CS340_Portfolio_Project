# Citation for this file:
# Date: 06/04/2022
# Adapted from osu-cs340-ecampus/flask-starter-app
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app

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
        query = "SELECT customer_id AS 'Customer ID', first_name AS 'First Name', last_name AS 'Last Name', \
        email, customer_phone AS 'Phone' FROM Customers;"
        cur = mysql.connection.cursor()  # Open up connection
        cur.execute(query)
        results = cur.fetchall()

        # For customer id drop down. 
        query2 = "SELECT customer_id FROM `Customers` ORDER BY customer_id ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        all_customers_id = cur.fetchall()

        return render_template("customers.j2", Customers=results, Customers_id=all_customers_id)

    if request.method == "POST": # INSERT INTO table
        if request.form.get("addCustomer"): # Came from user clicking "Add Customer" button.
            first_name = request.form["cfname"]  
            last_name = request.form["clname"]
            email = request.form["cemail"]
            customer_phone = request.form["cphone"]   # These variables are names from j2 template. 

            # All fields must be filled by user. Creating a user also creates a new row in Orders to demonstrate M:M relationship. 
            query = "INSERT INTO `Customers` (first_name, last_name, email, customer_phone) VALUES (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()  
            cur.execute(query, (first_name, last_name, email, customer_phone))
            mysql.connection.commit()

            # Insert into child tables with some null values. Only customer ID has non-null value. 
            #query2 = "INSERT INTO `Orders` (customer_id) VALUES (SELECT max(customer_id) FROM `Customers`)"
            #query2 = "INSERT INTO `Orders` (customer_id) VALUES (last_insert_id())"
            #cur = mysql.connection.cursor()  
            #cur.execute(query2, (customer_id))
            #mysql.connection.commit()

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

        elif request.form.get("searchCustomer"):
            first_name = request.form["searchCustomerName"]
            last_name = request.form["searchCustomerName"]
            query = "SELECT * FROM `Customers` WHERE first_name LIKE %s Or last_name LIKE %s"
            cur = mysql.connection.cursor() 
            cur.execute(query, (first_name, last_name))
            search_results = cur.fetchall()
            query2 = "SELECT * FROM `Customers`;"
            cur = mysql.connection.cursor() 
            cur.execute(query2)
            results = cur.fetchall()
            mysql.connection.commit()
            return render_template("customers.j2", search_results=search_results, Customers=results)


@app.route('/pizzas', methods=["POST", "GET"])
def pizzas():
    if request.method == "GET": # Just displaying table contents
        query = "SELECT pizza_id AS 'Pizza ID', pizza_type AS 'Pizza Type', pizza_price AS 'Pizza Price' FROM Pizzas;"
        cur = mysql.connection.cursor()  
        cur.execute(query)
        results = cur.fetchall()

        query2 = "SELECT pizza_id FROM Pizzas ORDER BY pizza_id;"
        cur = mysql.connection.cursor()  
        cur.execute(query2)
        all_pizzas_id = cur.fetchall()
        return render_template("pizzas.j2", Pizzas=results, all_pizzas_id=all_pizzas_id)

    if request.method == 'POST':
        if request.form.get("addPizza"): # Came from user clicking "Add Pizza" button.
            pizza_type = request.form["ptype"]  
            pizza_price = request.form["pprice"]

            # All fields must be filled. 
            query = "INSERT INTO `Pizzas` (pizza_type, pizza_price) VALUES (%s, %s)"
            cur = mysql.connection.cursor()  
            cur.execute(query, (pizza_type, pizza_price))
            mysql.connection.commit()
            return redirect('/pizzas')

        elif request.form.get("updatePizza"): # Came from user clicking "Update Pizza" button.
            pizza_id = request.form["pid"]
            pizza_type = request.form["ptype"]  
            pizza_price = request.form["pprice"]

            # All fields must be filled. 
            query = "UPDATE `Pizzas` SET pizza_type=%s, pizza_price=%s WHERE pizza_id=%s"
            cur = mysql.connection.cursor()  
            cur.execute(query, (pizza_type, pizza_price, pizza_id))
            mysql.connection.commit()
            return redirect('/pizzas')


@app.route('/employees', methods=["POST", "GET"])
def employees():
    if request.method == "GET": # Just displaying table contents
        query = "SELECT employee_id AS 'Employee ID', employee_first_name AS 'First Name', \
        employee_last_name AS 'Last Name', hourly_wage AS 'Hourly Wage' FROM Employees;"
        cur = mysql.connection.cursor()  
        cur.execute(query)
        results = cur.fetchall()
        return render_template("employees.j2", Employees=results)

    if request.method == "POST": # INSERT INTO table
        if request.form.get("addEmployee"):
            employee_first_name = request.form["efname"]
            employee_last_name = request.form["elname"]
            hourly_wage = request.form["hwage"]

            query = "INSERT INTO `Employees` (employee_first_name, employee_last_name, hourly_wage) VALUES (%s, %s, %s)"
            cur = mysql.connection.cursor()  
            cur.execute(query, (employee_first_name, employee_last_name, hourly_wage))
            mysql.connection.commit()
            return redirect('/employees')


@app.route('/orders', methods=["POST", "GET"])
def orders():
    if request.method == "GET": # Just displaying table contents
        query = "SELECT order_id AS 'Order ID', order_date AS 'Order Date', CONCAT(Customers.first_name, ' ', \
        Customers.last_name) AS 'Customer Name', employee_id AS 'Employee ID', \
        Pizzas.pizza_type AS 'Pizza Type', quantity AS 'Quantity', quantity*Pizzas.pizza_price AS 'Order Total' FROM Orders \
        LEFT JOIN Pizzas ON Orders.pizza_id = Pizzas.pizza_id \
        LEFT JOIN Customers ON Customers.customer_id = Orders.customer_id \
        ORDER BY Order_id ASC;"
        cur = mysql.connection.cursor() 
        cur.execute(query)
        all_results = cur.fetchall()

        query2 = "SELECT * FROM Orders" 
        cur = mysql.connection.cursor()  
        cur.execute(query2)
        results = cur.fetchall()

        query3 = "SELECT customer_id FROM `Customers` ORDER BY customer_id ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query3)
        all_customers_id = cur.fetchall()

        query4 = "SELECT employee_id FROM `Employees` ORDER BY employee_id ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query4)
        all_employee_id = cur.fetchall()

        query5 = "SELECT pizza_id FROM `Pizzas` ORDER BY pizza_id ASC;"
        cur = mysql.connection.cursor()
        cur.execute(query5)
        all_pizzas_id = cur.fetchall()

        return render_template("orders.j2", Orders_table=all_results, Orders=results, Customers_id=all_customers_id, Employees_id=all_employee_id, Pizzas_id=all_pizzas_id)

    if request.method == "POST":
        if request.form.get("addOrder"):
            order_date = request.form["odate"]
            customer_id = request.form["cid"]
            employee_id = request.form["eid"]
            pizza_id = request.form["pid"]
            quantity = request.form["qty"] 

            # All fields must be filled. Inserting all data into Orders table except order_total.
            query = "INSERT INTO `Orders` (order_date, customer_id, employee_id, quantity, pizza_id) VALUES (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()  
            cur.execute(query, (order_date, customer_id, employee_id, quantity, pizza_id))
            mysql.connection.commit()

            # order_total is updated with the calculated amount (quantity*pizza_price.)
            query2 = "UPDATE `Orders` SET order_total=quantity*(SELECT Pizzas.pizza_price from Pizzas where Pizzas.pizza_id=Orders.pizza_id) \
            WHERE order_id=last_insert_id()"
            cur = mysql.connection.cursor()  
            cur.execute(query2)
            mysql.connection.commit()  # This is working before adding another query to UPDATE order. 

            return redirect('/orders')

        elif request.form.get("updateOrder"):  # User clicked Update Order button. 
            order_id = request.form["oid"]
            order_date = request.form["odate"]
            customer_id = request.form["cid"]
            employee_id = request.form["eid"]
            pizza_id = request.form["pid"]
            quantity = request.form["qty"] 

            # Query updates attributes in Orders except order_total which is calculated and updated in the next query. 
            query = "UPDATE `Orders` SET order_date=%s, customer_id=%s, employee_id=%s, pizza_id=%s, quantity=%s, \
            order_total=quantity*(SELECT Pizzas.pizza_price FROM Pizzas where Pizzas.pizza_id=Orders.pizza_id) WHERE order_id=%s"
            cur = mysql.connection.cursor()  
            cur.execute(query, (order_date, customer_id, employee_id, pizza_id, quantity, order_id))
            mysql.connection.commit() # Is it a problem if I have two commits?

            # A second query to update order_total column in Orders table - cannot make it work, so that went into query above as subquery. 
            return redirect('/orders')

        elif request.form.get("deleteOrder"): # Came from user clicking "Delete Order" button.
            order_id = request.form["oid"]
            query = "DELETE FROM `Orders` WHERE order_id= %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (order_id,)) # Why did delete break when that trailing comma is removed?
            mysql.connection.commit()
            return redirect('/orders')


# Listener
if __name__ == "__main__":
    # Start the app on port 3000, it will be different once hosted
    app.run(port=7387, debug=True)