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


df_join_and_filter = pd.read_sql("""
    SELECT employees.firstName, employees.lastName 
    FROM employees 
    JOIN offices ON employees.officeCode = offices.officeCode 
    WHERE offices.city = 'Boston'
""", conn)


df_boston = df_join_and_filter

# Part 2: Type of Join - 
df_employee = pd.read_sql("""
    SELECT employees.firstName, employees.lastName, offices.city, offices.state
    FROM employees
    LEFT JOIN offices ON employees.officeCode = offices.officeCode
    ORDER BY employees.firstName, employees.lastName
""", conn)

# Part 3: Built-in Function - payments sorted DESC
df_payment = pd.read_sql("""
    SELECT customers.contactFirstName, customers.contactLastName, payments.amount, payments.paymentDate
    FROM customers
    JOIN payments ON customers.customerNumber = payments.customerNumber
    ORDER BY CAST(payments.amount AS REAL) DESC
""", conn)

# Part 4: Joining and Grouping - 4 reps avg credit > 90k
df_credit = pd.read_sql("""
    SELECT employees.employeeNumber, employees.firstName, employees.lastName, COUNT(customers.customerNumber) AS num_customers
    FROM employees
    JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY employees.employeeNumber
    HAVING AVG(customers.creditLimit) > 90000
    ORDER BY num_customers DESC
""", conn)

# Part 5: Multiple Joins - customers per office
df_total_customers = pd.read_sql("""
    SELECT COUNT(customers.customerNumber) AS n_customers, offices.officeCode, offices.city
    FROM offices
    LEFT JOIN employees ON offices.officeCode = employees.officeCode
    LEFT JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY offices.officeCode
""", conn)

# Part 6: Subquery - employees who sold products with <20 customers
df_under_20 = pd.read_sql("""
    SELECT DISTINCT employees.employeeNumber, employees.firstName, employees.lastName, offices.city, offices.officeCode
    FROM employees
    JOIN offices ON employees.officeCode = offices.officeCode
    JOIN customers ON employees.employeeNumber = customers.salesRepEmployeeNumber
    JOIN orders ON customers.customerNumber = orders.customerNumber
    JOIN orderdetails ON orders.orderNumber = orderdetails.orderNumber
    WHERE orderdetails.productCode IN (
        SELECT productCode FROM orderdetails JOIN orders ON orderdetails.orderNumber = orders.orderNumber GROUP BY productCode HAVING COUNT(DISTINCT customerNumber) < 20
    )
    ORDER BY employees.employeeNumber
""", conn)

conn.close()