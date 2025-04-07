# Store Managment
Michal Zanzuri and Yael Bouskila-Ditchi
## Table of Contents
[Stage 1: Design and Build the Database](#stage-1:-design-and-build-the-database)
[Introduction](#introduction)
[System Purpose](#System-Purpose)
[ERD and DSD Diagrams](#ERD-and-DSD-Diagrams)
[SQL Scripts](#SQL-Scripts)
[Data Insertion](#Data-Insertion)
[Backup and Restoration](#Backup-and-Restoration)


# Stage 1: Design and Build the Database

### Introduction
The system is designed for inventory management of a store, including managing supplier details, orders, and products. It allows tracking of product inventory, suppliers, orders, and invoices. The system is meant to provide store managers with an organized and convenient way to manage the inventory and coordinate with suppliers.

#### System Purpose
The system aims to ensure effective management of the store's inventory, suppliers, and orders, while maintaining an organized flow of information. Using the system, actions such as the following can be performed:
Managing supplier details and establishing contact with suppliers.
Managing orders with suppliers, including dates, quantities, and prices.
Tracking inventory and product status in the store.
Handling returns and processing canceled orders.

### ERD and DSD Diagrams
#### ERD (Entity-Relationship Diagram):
The ERD diagram represents the entities within the system and the relationships between them. Each entity is represented by a table in the database.

View ERD Diagram

#### DSD (Data Structure Diagram):
The DSD diagram shows the data structure and how data is stored in the database, including tables, primary and foreign keys, and relationships between fields.

View DSD Diagram

### SQL Scripts
The system includes the following SQL files:

**createTables.sql:** This file contains all SQL commands to create the tables in the database.

View createTables.sql

**insertTables.sql:** This file contains all SQL commands to insert data into the tables.

View insertTables.sql

**dropTables.sql:** This file contains the SQL commands to drop all the tables.

View dropTables.sql

**selectAll_tables.sql:** This file contains SQL commands to select all data from all tables.

View selectAll_tables.sql

### Data Insertion
Data insertion was performed using three different tools:

**1. Mockaroo:** We used Mockaroo to generate a CSV file for the Supplier and Employee tables. The file contains data inserted within specific ranges for each table.

View Mockaroo Data CSV

**2. Generatedata:** We used Generatedata to create CSV files for the Supplier table. The files were generated with predefined ranges for each table.

View Generatedata CSV Files

**3. Python Script:** A Python script was used to create CSV files for the following tables: Supplier, Employee, Product, Order_d, Quotation, ReturnProduct, and ProductOrder. The script automatically generated data for each table based on the defined attributes, allowing for quick and structured data insertion.

View Python Script

### Backup and Restoration
The backup is saved in a file named backup_YYYYMMDD_HHMM.sql. To restore, simply run the backup file in your database management system.
