import sqlite3

db = sqlite3.connect("shop.db")

db.execute('''CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    price REAL NOT NULL);''')

db.execute('''CREATE TABLE IF NOT EXISTS customers(
        customer_id INTEGER PRIMARY KEY,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE);''')

db.execute('''
        CREATE TABLE IF NOT EXISTS orders ( order_id INTEGER PRIMARY KEY, customer_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, order_date DATE NOT NULL, FOREIGN KEY (customer_id) REFERENCES customers(customer_id), FOREIGN KEY (product_id) REFERENCES products(product_id));''')


while True:
    print('''
Що ви хочете зробити?

1 - Додавання продуктів:
2 - Додавання клієнтів:
3 - Замовлення товарів:
4 - Сумарний обсяг продажів:
5 - Кількість замовлень на кожного клієнта:
6 - Середній чек замовлення:
7 - Найбільш популярна категорія товарів:
8 - Загальна кількість товарів кожної категорії:
9 - Оновлення цін категорії на 10% більші:
10 - Показати усіх користувачів
11 - Показати усі продукти
12 - Показати усі замовлення(Joined)
0 - Вийти:

    ''')
    command = int(input("Оберіть ваші дії: "))
    match command:
        case 0:
            break
        case 1:
            name = input("Name: ")
            category = input("Category: ")
            price = int(input("Price: "))
            db.execute(f'''INSERT INTO products (name, category, price)
                        VALUES {name, category, price};''')
            db.commit()
        case 2:
            first_name = input("Name: ")
            last_name = input("Last Name: ")
            email = input("Email: ")
            db.execute(f'''INSERT INTO customers (first_name, last_name, email)
                        VALUES {first_name, last_name, email};''')
            db.commit()
        case 3:
            customer_id = int(input("Custom_ID: "))
            product_id = int(input("Prod_ID: "))
            quantity = input("Quantity: ")
            db.execute('''INSERT INTO orders (customer_id,    product_id, quantity, order_date)
                    VALUES(?,?,?, CURRENT_TIMESTAMP)''',
                    (customer_id, product_id, quantity))
            db.commit()
        case 4:
            total_bill = db.execute('''SELECT SUM(products.price * orders.quantity) AS total_bill
                                    FROM orders
                                    INNER JOIN products ON orders.product_id = products.product_id''')
            print(total_bill.fetchone())
        case 5:
            order_customer = db.execute('''SELECT customers.first_name, COUNT(orders.order_id)
                                        FROM orders INNER JOIN customers ON customers.customer_id = orders.customer_id
                                        GROUP BY customers.first_name''')
            print(order_customer.fetchall())
        case 6:
            avg = db.execute('''SELECT AVG(products.price * orders.quantity) AS avg
                            FROM orders
                            INNER JOIN products ON orders.product_id = products.product_id''')
            print(avg.fetchone())
        case 9:
            db.execute('''UPDATE products SET price = price * 1.1
                    WHERE category = "Internet"''')
            db.commit()