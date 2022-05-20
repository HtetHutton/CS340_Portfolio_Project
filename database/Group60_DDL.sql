-- CS340 Group 60 [Htet Hutton, Marisela Vasquez]
-- Project Step 2 Draft: Normalized Schema + DDL with Sample Data
-- Data Definition Query 

SET FOREIGN_KEY_CHECKS=0;
SET AUTOCOMMIT = 0;

-- Create entity tables
-- Customers table
CREATE OR REPLACE TABLE Customers (
	customer_id INT(10) NOT NULL AUTO_INCREMENT,
	first_name VARCHAR(45) NOT NULL,
	last_name VARCHAR(45) NOT NULL,
	email VARCHAR(45) NOT NULL UNIQUE,
	customer_phone VARCHAR(20),
	PRIMARY KEY (customer_id)
);

-- Employees table
CREATE OR REPLACE TABLE Employees (
	employee_id INT(10) NOT NULL AUTO_INCREMENT,
	employee_first_name VARCHAR(45) NOT NULL,
	employee_last_name VARCHAR(45) NOT NULL,
	hourly_wage DECIMAL(5,2),
	PRIMARY KEY (employee_id)
);

-- Orders table
-- Updated employee_id to default Null from project step 3 feedback
-- CASCADE tested and woring. Deleting Customer also deletes Order with matching customer_id. 
CREATE OR REPLACE TABLE Orders (
	order_id INT(10) NOT NULL AUTO_INCREMENT,
	order_date DATE DEFAULT NULL,
	customer_id INT(10),
	employee_id INT(10) DEFAULT NULL,
    pizza_id INT(10) DEFAULT NULL,
    quantity INT(10) DEFAULT 0,
	order_total DECIMAL(10,2) DEFAULT 0,
	PRIMARY KEY (order_id),
	FOREIGN KEY (customer_id) REFERENCES Customers(customer_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
	FOREIGN KEY (employee_id) REFERENCES Employees(employee_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
    FOREIGN KEY (pizza_id) REFERENCES Pizzas(pizza_id)
    ON DELETE CASCADE
    ON UPDATE CASCADE
);

-- Pizzas table
CREATE OR REPLACE TABLE Pizzas (
	pizza_id INT(10) NOT NULL AUTO_INCREMENT,
	pizza_type VARCHAR(45) NOT NULL UNIQUE,
	pizza_price DECIMAL(10,2) NOT NULL,
	PRIMARY KEY (pizza_id)
);

-- OrderDetails table [Table deleted and attributes combined into Orders table]
/* 
CREATE OR REPLACE TABLE OrderDetails (
	line_number INT(10) NOT NULL AUTO_INCREMENT,
	order_id INT(10),
	pizza_id INT(10),
	quantity INT(10),
	PRIMARY KEY (line_number),
	FOREIGN KEY (order_id) REFERENCES Orders(order_id),
	FOREIGN KEY (pizza_id) REFERENCES Pizzas(pizza_id)
); 
*/

-- Insert sample data into tables
-- Insert data to Customers table
INSERT INTO Customers (first_name, last_name, email, customer_phone)
VALUES ('Miguel','Davis','mdavis@gmail.com','555-555-5555'),
('Sam','Smith','ssmith@yahoo.com','555-555-5556'),
('Ana','Rodriguez','anar@gmail.com','555-555-5557');

-- Insert data to Employees table
INSERT INTO Employees (employee_first_name, employee_last_name, hourly_wage)
VALUES ('Dan','Anderson',23.50),
('Mila','Gantes',16.20),
('Val','Obeso',24.00);
 
-- Insert data to Orders table
-- Used subquery for customer_id and employee_id like in Intermediate SQL Assignment
INSERT INTO Orders (order_date, order_total, customer_id, employee_id, pizza_id, quantity)
VALUES ('2022-04-27',52.24, (SELECT customer_id FROM Customers WHERE first_name='Ana' AND last_name='Rodriguez'), 
(SELECT employee_id FROM Employees WHERE employee_first_name='Dan' AND employee_last_name='Anderson'), 1, 2),
('2022-04-28',25.22,(SELECT customer_id FROM Customers WHERE first_name='Sam' AND last_name='Smith'), 
(SELECT employee_id FROM Employees WHERE employee_first_name='Val' AND employee_last_name='Obeso'), 4, 1),
('2022-04-29',23.22,(SELECT customer_id FROM Customers WHERE first_name='Miguel' AND last_name='Davis'), 
(SELECT employee_id FROM Employees WHERE employee_first_name='Mila' AND employee_last_name='Gantes'), 3, 1);

-- Insert data to Pizzas table
INSERT INTO Pizzas (pizza_type, pizza_price)
VALUES ('Meat Lovers',26.12),
('Cheese',20.00),
('Pepperoni',23.22),
('Vegetarian',25.22); 

-- Insert data to OrderDetails table [Table deleted]
/*
INSERT INTO OrderDetails (order_id, pizza_id, quantity)
VALUES (1,(SELECT pizza_id FROM Pizzas WHERE pizza_type='Meat Lovers'),2),
(2,(SELECT pizza_id FROM Pizzas WHERE pizza_type='Vegetarian'),1),
(3,(SELECT pizza_id FROM Pizzas WHERE pizza_type='Pepperoni'),1);
*/

SET FOREIGN_KEY_CHECKS=1;
COMMIT;