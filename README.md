# Inventory-Management

# Overview

This is an extremely basic Inventory Management with preset items, the User can delete and update an Item of their choice and thats all the input required. It uses important SQL functions such as JOIN and GROUPBY and SUM

The purpose was to show my knowledge of SQL relation databases with the connection of two tables and using them like they would be in a real store. I found SQL to be easy to learn but overall pretty Tedious with the constant menus, reminded me a lot of HTML and CSS but overall I think it was intutive for Tables.


[Software Demo Video](https://youtu.be/QC3PS5ANTe8)

# Relational Database

Uses SQL Lite

The database (inventory.db) has two tables linked by a foreign key.

**categories**
- category_id (INTEGER, primary key)
- name (TEXT, required, unique)

**products**
- product_id (INTEGER, primary key)
- name (TEXT, required)
- price (REAL, required)
- quantity (INTEGER, required, cannot be negative)
- category_id (INTEGER, foreign key to categories)

# Development Environment

SQL Lite
SQL Lite Viewer
Claude AI for bugtesting and learning
Python

# Useful Websites

- [Python](https://docs.python.org/3.8/library/sqlite3.html)

# Future Work

-User input to add additional products
-better UI
