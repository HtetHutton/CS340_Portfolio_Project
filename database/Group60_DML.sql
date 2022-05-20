-- Project Step 3 Draft Version: Data Manipulation Queries
-- Group 60 CS340

-- Pizzas page ---------------
-- Get all Pizzas for Pizzas table
SELECT pizza_id, pizza_type, pizza_price FROM Pizzas;

-- Add Pizza 
-- Removed pizza_id input - not needed because it's auto-incrementing.
INSERT INTO Pizzas (pizza_type, pizza_price)
VALUES (:ptypeInput, :ppriceInput);

-- Included UPDATE to demonstarte parent > child update funtionality.
UPDATE Pizzas SET pizza_type = :ptypeInput, pizza_price = :ppriceInput
WHERE pizza_id = :pidInput;
-- Pizzas page ends ----------------

-- Employees page ------------------
-- Get all employees for Employees table
SELECT employee_id, employee_first_name, employee_last_name, hourly_wage FROM Employees;

-- Add Employee
INSERT INTO Employees (employee_first_name, employee_last_name, hourly_wage)
VALUES (:efnameInput, :elnameInput, :hwageInput);
-- Employees page ends -------------

-- Customers page ------------------
-- Get all customers for Customers table
SELECT customer_id, customer_first_name, customer_last_name, email, phone FROM Customers;

-- Add Customer 
-- Added another query with subquery to INSERT INTO child table with default NULL values. 
INSERT INTO Customers (first_name, last_name, email, phone)
VALUES (:cfnameInput, :clnameInput, :cemailInput, :cphoneInput)
INSERT INTO Orders (customer_id)
VALUES ((SELECT Customers.customer_id FROM Customers WHERE first_name = :cfnameInput AND last_name = :clnameInput));

-- Customers page ends -------------

-- Orders page ---------------------
-- Get all Orders. pizza_id diskplays as pizza_type and customer_id displays as first name and last name.
-- LEFT JOIN is used here so that rows with NULL values will show up. 
SELECT order_id, order_date, CONCAT(Customers.first_name, ' ', Customers.last_name) AS 'customer_name', employee_id,  Pizzas.pizza_type, quantity, quantity*Pizzas.pizza_price FROM Orders
LEFT JOIN Pizzas ON Orders.pizza_id = Pizzas.pizza_id
LEFT JOIN Customers ON Customers.customer_id = Orders.customer_id
ORDER BY Order_id ASC;

-- Add order
-- Updated Orders with two more attributes (from deleted OrderDetails table.) Don't need to input order_total since it will be displayed
-- as multiplied result in above query. 
INSERT INTO Orders (order_date, customer_id, employee_id, pizza_id, quantity)
VALUES (:odateInput, :cidInput, :eidInput, :pidInput, :qtyInput); 

-- Update order - demonstrating parent > child UPDATE/DELETE funtionality. 
UPDATE Orders SET order_date = :odateInput, customer_id = :cidInput, employee_id = :eidInput, pizza_id = :pidInput, quantity = :qtyInput
WHERE order_id = :oidInput;

-- Delete order
DELETE FROM Orders WHERE order_id = :oidInput AND customer_id = :cidInput; 
-- Orders page ends ----------------

-- OrderDetails page ---------------
-- Page deleted and attributes combined into Orders. 
-- OrderDetails page ends ----------




