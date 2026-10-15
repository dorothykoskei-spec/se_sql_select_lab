# STEP 1A
import sqlite3
import pandas as pd

# STEP 1B
conn = sqlite3.connect("data.sqlite")

# QUESTION 1: Employees working in Boston
df_boston = pd.read_sql("""
    SELECT employees.firstName, employees.lastName, employees.jobTitle
    FROM employees
    JOIN offices
        ON employees.officeCode = offices.officeCode
    WHERE offices.city = 'Boston'
""", conn)
print("Employees working in Boston:")
print(df_boston)


# QUESTION 2: Offices with zero employees
df_empty_offices = pd.read_sql("""
    SELECT offices.officeCode, offices.city
    FROM offices
    LEFT JOIN employees
        ON offices.officeCode = employees.officeCode
    WHERE employees.employeeNumber IS NULL
""", conn)
print("Offices with zero employees:")
print(df_empty_offices)


# QUESTION 3: All employees and their office locations
df_all_employees = pd.read_sql("""
    SELECT employees.firstName, employees.lastName,
           offices.city, offices.state
    FROM employees
    LEFT JOIN offices
        ON employees.officeCode = offices.officeCode
    ORDER BY employees.firstName, employees.lastName
""", conn)
print("All employees and office locations:")
print(df_all_employees)


# QUESTION 4: Customers who have not placed orders
df_customers_no_orders = pd.read_sql("""
    SELECT customers.contactFirstName,
           customers.contactLastName,
           customers.phone,
           customers.salesRepEmployeeNumber
    FROM customers
    LEFT JOIN orders
        ON customers.customerNumber = orders.customerNumber
    WHERE orders.orderNumber IS NULL
    ORDER BY customers.contactLastName
""", conn)
print("Customers who have not placed orders:")
print(df_customers_no_orders)


# QUESTION 5: Customer payments sorted by amount
df_payments = pd.read_sql("""
    SELECT customers.contactFirstName,
           customers.contactLastName,
           payments.amount,
           payments.paymentDate
    FROM customers
    JOIN payments
        ON customers.customerNumber = payments.customerNumber
    ORDER BY CAST(payments.amount AS REAL) DESC
""", conn)
print("Customer payments:")
print(df_payments)


# QUESTION 6: Employees whose customers have average credit limits over 90,000
df_top_reps = pd.read_sql("""
    SELECT employees.employeeNumber,
           employees.firstName,
           employees.lastName,
           COUNT(customers.customerNumber) AS num_customers
    FROM employees
    JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY employees.employeeNumber,
             employees.firstName,
             employees.lastName
    HAVING AVG(customers.creditLimit) > 90000
    ORDER BY num_customers DESC
""", conn)
print("Sales representatives with high-credit-limit customers:")
print(df_top_reps)


# QUESTION 7: Number of orders and total units sold per product
df_product_sales = pd.read_sql("""
    SELECT products.productName,
           COUNT(DISTINCT orderdetails.orderNumber) AS numorders,
           SUM(orderdetails.quantityOrdered) AS totalunits
    FROM products
    JOIN orderdetails
        ON products.productCode = orderdetails.productCode
    GROUP BY products.productCode, products.productName
    ORDER BY totalunits DESC
""", conn)
print("Product sales:")
print(df_product_sales)


# QUESTION 8: Number of different customers per product
df_product_customers = pd.read_sql("""
    SELECT products.productName,
           products.productCode,
           COUNT(DISTINCT orders.customerNumber) AS numpurchasers
    FROM products
    JOIN orderdetails
        ON products.productCode = orderdetails.productCode
    JOIN orders
        ON orderdetails.orderNumber = orders.orderNumber
    GROUP BY products.productCode, products.productName
    ORDER BY numpurchasers DESC
""", conn)
print("Number of customers per product:")
print(df_product_customers)


# QUESTION 9: Number of customers per office
df_customers_per_office = pd.read_sql("""
    SELECT COUNT(customers.customerNumber) AS n_customers,
           offices.officeCode,
           offices.city
    FROM offices
    LEFT JOIN employees
        ON offices.officeCode = employees.officeCode
    LEFT JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    GROUP BY offices.officeCode, offices.city
""", conn)
print("Number of customers per office:")
print(df_customers_per_office)


# QUESTION 10: Employees who sold products bought by fewer than 20 customers
df_employees_low_sales = pd.read_sql("""
    SELECT DISTINCT employees.employeeNumber,
           employees.firstName,
           employees.lastName,
           offices.city,
           offices.officeCode
    FROM employees
    JOIN customers
        ON employees.employeeNumber = customers.salesRepEmployeeNumber
    JOIN orders
        ON customers.customerNumber = orders.customerNumber
    JOIN orderdetails
        ON orders.orderNumber = orderdetails.orderNumber
    JOIN offices
        ON employees.officeCode = offices.officeCode
    WHERE orderdetails.productCode IN (
        SELECT orderdetails.productCode
        FROM orderdetails
        JOIN orders
            ON orderdetails.orderNumber = orders.orderNumber
        GROUP BY orderdetails.productCode
        HAVING COUNT(DISTINCT orders.customerNumber) < 20
    )
    ORDER BY employees.employeeNumber
""", conn)
print("Employees who sold products bought by fewer than 20 customers:")
print(df_employees_low_sales)


# STEP 2
df_first_five = pd.read_sql("""
    SELECT employeeNumber, lastName
    FROM employees
""", conn)


# STEP 3
df_five_reverse = pd.read_sql("""
    SELECT lastName, employeeNumber
    FROM employees
""", conn)


# STEP 4
df_alias = pd.read_sql("""
    SELECT lastName, employeeNumber AS ID
    FROM employees
""", conn)


# STEP 5
df_executive = pd.read_sql("""
    SELECT *,
           CASE
               WHEN jobTitle IN ('President', 'VP Sales', 'VP Marketing')
               THEN 'Executive'
               ELSE 'Non-Executive'
           END AS role
    FROM employees
""", conn)


# STEP 6
df_name_length = pd.read_sql("""
    SELECT *, LENGTH(lastName) AS name_length
    FROM employees
""", conn)


# STEP 7
df_short_title = pd.read_sql("""
    SELECT SUBSTR(jobTitle, 1, 2) AS short_title
    FROM employees
""", conn)

order_details = pd.read_sql("""
    SELECT * FROM orderDetails
""", conn)

print("Order Details Data:")
print(order_details)


# STEP 8
sum_total_price = pd.read_sql("""
    SELECT SUM(ROUND(priceEach * quantityOrdered)) AS total_price
    FROM orderDetails
""", conn)["total_price"]


# STEP 9
df_day_month_year = pd.read_sql("""
    SELECT *,
           strftime('%d', orderDate) AS day,
           strftime('%m', orderDate) AS month,
           strftime('%Y', orderDate) AS year
    FROM orders
""", conn)


# STEP 11
conn.close()
