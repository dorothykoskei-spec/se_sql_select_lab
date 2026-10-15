import sqlite3
import pandas as pd
conn = sqlite3.connect("data.sqlite")


df_first_five = pd.read_sql("SELECT employeeNumber, lastName FROM employees", conn)
df_five_reverse = pd.read_sql("SELECT lastName, employeeNumber FROM employees", conn)
df_alias = pd.read_sql("SELECT lastName, employeeNumber AS ID FROM employees", conn)
df_executive = pd.read_sql("SELECT *, CASE WHEN jobTitle IN ('President','VP Sales','VP Marketing') THEN 'Executive' ELSE 'Non-Executive' END AS role FROM employees", conn)
df_name_length = pd.read_sql("SELECT *, LENGTH(lastName) AS name_length FROM employees", conn)
df_short_title = pd.read_sql("SELECT SUBSTR(jobTitle,1,2) AS short_title FROM employees", conn)
sum_total_price = pd.read_sql("SELECT SUM(ROUND(priceEach * quantityOrdered)) AS total_price FROM orderdetails", conn)["total_price"]
df_day_month_year = pd.read_sql("SELECT *, strftime('%d',orderDate) AS day, strftime('%m',orderDate) AS month, strftime('%Y',orderDate) AS year FROM orders", conn)

# --- Part 1: Join and Filter ---
df_join_and_filter = pd.read_sql("SELECT employees.firstName, employees.lastName FROM employees JOIN offices ON employees.officeCode=offices.officeCode WHERE city='Boston'", conn)
df_boston = df_join_and_filter
df_zero_emp = pd.read_sql("SELECT offices.officeCode, offices.city FROM offices LEFT JOIN employees ON offices.officeCode=employees.officeCode WHERE employees.employeeNumber IS NULL", conn)
df_empty_offices = df_zero_emp

# --- Part 2: Type of Join ---
df_employee = pd.read_sql("SELECT employees.firstName, employees.lastName, offices.city, offices.state FROM employees LEFT JOIN offices ON employees.officeCode=offices.officeCode ORDER BY employees.firstName, employees.lastName", conn)
df_contacts = pd.read_sql("SELECT customers.contactFirstName, customers.contactLastName, customers.phone, customers.salesRepEmployeeNumber FROM customers LEFT JOIN orders ON customers.customerNumber=orders.customerNumber WHERE orders.orderNumber IS NULL ORDER BY customers.contactLastName", conn)
df_customers_no_orders = df_contacts
df_no_orders = df_contacts

# --- Part 3: Built-in Function ---
df_payment = pd.read_sql("SELECT customers.contactFirstName, customers.contactLastName, payments.amount, payments.paymentDate FROM customers JOIN payments ON customers.customerNumber=payments.customerNumber ORDER BY CAST(amount AS REAL) DESC", conn)
df_payments = df_payment

# --- Part 4: Joining and Grouping ---
df_credit = pd.read_sql("SELECT employees.employeeNumber, employees.firstName, employees.lastName, COUNT(customerNumber) AS num_customers FROM employees JOIN customers ON employeeNumber=salesRepEmployeeNumber GROUP BY employeeNumber HAVING AVG(creditLimit)>90000 ORDER BY num_customers DESC", conn)
df_product_sold = pd.read_sql("SELECT products.productName, COUNT(DISTINCT orderNumber) AS numorders, SUM(quantityOrdered) AS totalunits FROM products JOIN orderdetails ON products.productCode=orderdetails.productCode GROUP BY products.productCode ORDER BY totalunits DESC", conn)
df_product_sales = df_product_sold

# --- Part 5: Multiple Joins -> expects 109 rows ---
df_total_customers = pd.read_sql("SELECT products.productName, products.productCode, COUNT(DISTINCT customerNumber) AS numpurchasers FROM products JOIN orderdetails ON products.productCode=orderdetails.productCode JOIN orders ON orderdetails.orderNumber=orders.orderNumber GROUP BY products.productCode ORDER BY numpurchasers DESC", conn)
df_product_customers = df_total_customers
df_customers_per_office = pd.read_sql("SELECT COUNT(customers.customerNumber) AS n_customers, offices.officeCode, offices.city FROM offices LEFT JOIN employees ON offices.officeCode=employees.officeCode LEFT JOIN customers ON employees.employeeNumber=customers.salesRepEmployeeNumber GROUP BY offices.officeCode", conn)

# --- Part 6: Subquery -> expects Loui first ---
df_under_20 = pd.read_sql("""
    SELECT DISTINCT employees.employeeNumber, employees.firstName, employees.lastName, offices.city, offices.officeCode
    FROM employees
    JOIN offices ON employees.officeCode=offices.officeCode
    JOIN customers ON employees.employeeNumber=customers.salesRepEmployeeNumber
    JOIN orders ON customers.customerNumber=orders.customerNumber
    JOIN orderdetails ON orders.orderNumber=orderdetails.orderNumber
    WHERE orderdetails.productCode IN (
        SELECT productCode FROM orderdetails 
        JOIN orders ON orderdetails.orderNumber=orders.orderNumber 
        GROUP BY productCode HAVING COUNT(DISTINCT customerNumber) < 20
    )
    ORDER BY employees.firstName, employees.lastName
""", conn)

conn.close()