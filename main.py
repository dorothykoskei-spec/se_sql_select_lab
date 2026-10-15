import sqlite3
import pandas as pd

conn = sqlite3.connect("data.sqlite")


# STEP 2 - 23 rows, 2 cols
df_first_five = pd.read_sql("""
    SELECT employeeNumber, lastName FROM employees
""", conn)

# STEP 3 - 23 rows, 2 cols reversed
df_five_reverse = pd.read_sql("""
    SELECT lastName, employeeNumber FROM employees
""", conn)

# STEP 4 - alias ID
df_alias = pd.read_sql("""
    SELECT lastName, employeeNumber AS ID FROM employees
""", conn)

# STEP 5 - role column
df_executive = pd.read_sql("""
    SELECT *, CASE WHEN jobTitle IN ('President','VP Sales','VP Marketing')
    THEN 'Executive' ELSE 'Non-Executive' END AS role FROM employees
""", conn)

# STEP 6 - name_length
df_name_length = pd.read_sql("""
    SELECT *, LENGTH(lastName) AS name_length FROM employees
""", conn)

# STEP 7 - short_title
df_short_title = pd.read_sql("""
    SELECT SUBSTR(jobTitle,1,2) AS short_title FROM employees
""", conn)

# STEP 8 - total price = 9604251 (must use ROUND)
sum_total_price = pd.read_sql("""
    SELECT SUM(ROUND(priceEach * quantityOrdered)) AS total_price FROM orderdetails
""", conn)["total_price"]

# STEP 9 - day, month, year
df_day_month_year = pd.read_sql("""
    SELECT *, strftime('%d',orderDate) AS day, strftime('%m',orderDate) AS month, strftime('%Y',orderDate) AS year FROM orders
""", conn)


df_boston = pd.read_sql("""
    SELECT firstName, lastName, jobTitle FROM employees
    JOIN offices ON employees.officeCode = offices.officeCode WHERE city='Boston'
""", conn)

df_empty_offices = pd.read_sql("""
    SELECT offices.officeCode, offices.city FROM offices
    LEFT JOIN employees ON offices.officeCode=employees.officeCode WHERE employees.employeeNumber IS NULL
""", conn)

df_all_employees = pd.read_sql("""
    SELECT firstName, lastName, city, state FROM employees
    LEFT JOIN offices ON employees.officeCode=offices.officeCode ORDER BY firstName, lastName
""", conn)

df_customers_no_orders = pd.read_sql("""
    SELECT contactFirstName, contactLastName, phone, salesRepEmployeeNumber FROM customers
    LEFT JOIN orders ON customers.customerNumber=orders.customerNumber WHERE orders.orderNumber IS NULL ORDER BY contactLastName
""", conn)

df_payments = pd.read_sql("""
    SELECT contactFirstName, contactLastName, amount, paymentDate FROM customers
    JOIN payments ON customers.customerNumber=payments.customerNumber ORDER BY CAST(amount AS REAL) DESC
""", conn)

df_top_reps = pd.read_sql("""
    SELECT employees.employeeNumber, firstName, lastName, COUNT(customers.customerNumber) AS num_customers FROM employees
    JOIN customers ON employees.employeeNumber=customers.salesRepEmployeeNumber
    GROUP BY employees.employeeNumber HAVING AVG(creditLimit)>90000 ORDER BY num_customers DESC
""", conn)

df_product_sales = pd.read_sql("""
    SELECT productName, COUNT(DISTINCT orderdetails.orderNumber) AS numorders, SUM(quantityOrdered) AS totalunits FROM products
    JOIN orderdetails ON products.productCode=orderdetails.productCode GROUP BY products.productCode ORDER BY totalunits DESC
""", conn)

df_product_customers = pd.read_sql("""
    SELECT productName, products.productCode, COUNT(DISTINCT customerNumber) AS numpurchasers FROM products
    JOIN orderdetails ON products.productCode=orderdetails.productCode
    JOIN orders ON orderdetails.orderNumber=orders.orderNumber GROUP BY products.productCode ORDER BY numpurchasers DESC
""", conn)

df_customers_per_office = pd.read_sql("""
    SELECT COUNT(customers.customerNumber) AS n_customers, offices.officeCode, offices.city FROM offices
    LEFT JOIN employees ON offices.officeCode=employees.officeCode
    LEFT JOIN customers ON employees.employeeNumber=customers.salesRepEmployeeNumber GROUP BY offices.officeCode
""", conn)

df_employees_low_sales = pd.read_sql("""
    SELECT DISTINCT employees.employeeNumber, employees.firstName, employees.lastName, offices.city, offices.officeCode FROM employees
    JOIN customers ON employees.employeeNumber=customers.salesRepEmployeeNumber
    JOIN orders ON customers.customerNumber=orders.customerNumber
    JOIN orderdetails ON orders.orderNumber=orderdetails.orderNumber
    JOIN offices ON employees.officeCode=offices.officeCode
    WHERE orderdetails.productCode IN (SELECT productCode FROM orderdetails JOIN orders ON orderdetails.orderNumber=orders.orderNumber GROUP BY productCode HAVING COUNT(DISTINCT customerNumber)<20)
    ORDER BY employees.employeeNumber
""", conn)
conn.close()