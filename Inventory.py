import sqlite3
#I also personally used SQL lite viewer extension better for physically seeing the table


conn = None   # start with no connection

#Instead of the basic just connecting it it requires a try to allow for some error handling if it cannot connect
try:
    conn = sqlite3.connect("inventory.db")
    conn.execute("PRAGMA foreign_keys = ON") #allows connection of tables
    print("Connected!")

    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS products")
    cur.execute("DROP TABLE IF EXISTS categories")

    #thisll make the categories table, I did this so we can have two tables much like many 
    #stores actually would do

    #name and ID are unique and there can't be two of the same (why would there be?)
    cur.execute("""
        CREATE TABLE categories (
            category_id INTEGER PRIMARY KEY,
            name        TEXT NOT NULL UNIQUE
        )
    """)

    cur.executemany(
        "INSERT INTO categories (name) VALUES (?)",
        #our categories added
        [("Electronics",), ("Office",), ("Food",)]
    )
    conn.commit()

    print("\nCategories:")
    print("category_id | name")
    cur.execute("SELECT * FROM categories")
    for row in cur.fetchall():
        print(row)

    #Product ID must be a number and can't have 2 that are the same
    #Name is text, cannot be empty
    #Price is Decimal, cannot be empty
    # Also added quantity, does not allow negative quantity, dont sell what you don't have
    cur.execute("""
        CREATE TABLE products (
            product_id  INTEGER PRIMARY KEY,
            name        TEXT NOT NULL,
            price       REAL NOT NULL,
            quantity    INTEGER NOT NULL DEFAULT 0 CHECK (quantity >= 0),
            category_id INTEGER NOT NULL,
            FOREIGN KEY (category_id) REFERENCES categories(category_id)
        )
    """)

    #Uses Tuples to add many products just to have a baseline
    #Will auto assign a ID
    #connects itself to a category
    cur.executemany(
        "INSERT INTO products (name, price, quantity, category_id) VALUES (?, ?, ?, ?)",
        [("Keyboard", 24.50, 47, 1), ("Pencils", 6.25, 160, 2), ("12 Pack of Barqs", 9.99, 75, 3)]
    )

    cur.execute(
        "INSERT INTO products (name, price, quantity, category_id) VALUES (?, ?, ?, ?)",
        ("Monitor", 79.99, 8, 1)
    )

    conn.commit()

    #Joining for each product, find the category with the matching ID and attach its name
    print("\nProducts with their category:")
    print("name | price | category")
    cur.execute("""
        SELECT products.name, products.price, categories.name AS category
        FROM products
        JOIN categories ON categories.category_id = products.category_id
    """)
    
    for row in cur.fetchall():
        print(row)


    #Group by function use, bundle products by category, then count and total each bundle
    print("\nSummary per category:")
    print("category | num_products | total_price")
    cur.execute("""
        SELECT categories.name,
        COUNT(*)            AS num_products,
        SUM(products.price) AS total_price
        FROM products
        JOIN categories ON categories.category_id = products.category_id
        GROUP BY categories.name
    """)
    for row in cur.fetchall():
        print(row)

    #Inventory value: quantity * price for each product
    print("\nInventory value per product:")
    print("name | quantity | price | stock_value")
    cur.execute("""
        SELECT name, quantity, price, ROUND(quantity * price, 2) AS stock_value
        FROM products
        ORDER BY stock_value DESC
    """)
    for row in cur.fetchall():
        print(row)

    #Inventory value per category: SUM + GROUP BY + JOIN together
    print("\nInventory value per category:")
    print("category | total_units | total_value")
    cur.execute("""
        SELECT categories.name,
        SUM(products.quantity) AS total_units,
        ROUND(SUM(products.quantity * products.price), 2) AS total_value
        FROM products
        JOIN categories ON categories.category_id = products.category_id
        GROUP BY categories.name
        ORDER BY total_value DESC
    """)
    for row in cur.fetchall():
        print(row)

    #shows rows, all prices, average price, min price, max price
    print("\nSummary:")
    print("count | sum | average | min | max")
    cur.execute("""
        SELECT COUNT(*), SUM(price), AVG(price), MIN(price), MAX(price)
        FROM products
    """)
    print(cur.fetchone())

    #UPDATE with user input
    print("\nUpdate a product")
    name = input("Which product? ")

    try:
        new_price = float(input("New price: "))
        sold = int(input("How many sold? "))
    except ValueError:
        print("Please enter numbers only.")
    else:
        cur.execute(
            "UPDATE products SET price = ?, quantity = quantity - ? WHERE name = ?",
            (new_price, sold, name)
        )
        conn.commit()

        if cur.rowcount == 0:
            print("No product with that name.")
        else:
            print("Updated!")
            cur.execute("SELECT name, price, quantity FROM products WHERE name = ?", (name,))
            print(cur.fetchone())


    #DELETE with user input
    print("\nDelete a product")
    name = input("Which product do you want to delete? ")

    #Look it up first so we can show the user what theyre about to delete
    cur.execute("SELECT name, price, quantity FROM products WHERE name = ?", (name,))
    product = cur.fetchone()

    if product is None:
        print("No product with that name.")
    else:
        print(f"Found: {product}")
        confirm = input("Type 'yes' to delete it: ")

        if confirm.lower() == "yes":
            cur.execute("DELETE FROM products WHERE name = ?", (name,))
            conn.commit()
            print("Deleted!")
        else:
            print("Cancelled.")

    #Show what's left
    print("\nProducts remaining:")
    print("name | price | quantity")
    cur.execute("SELECT name, price, quantity FROM products")
    for row in cur.fetchall():
        print(row)
    
    
except sqlite3.Error as e:
    print(f"Database error: {e}")
    
finally:
    if conn:
        conn.execute("DROP TABLE IF EXISTS products") #deletes at end for testing.
        conn.execute("DROP TABLE IF EXISTS categories")
        conn.commit()
        conn.close()
        print("Connection closed.")