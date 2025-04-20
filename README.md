# Store Managment
Michal Zanzuri and Yael Bouskila-Ditchi
## Table of Contents
-[Stage 1: Design and Build the Database](#stage-1:-design-and-build-the-database)
- [Introduction](#introduction)
- [System Purpose](#System-Purpose)
- [ERD and DSD Diagrams](#ERD-and-DSD-Diagrams)
- [SQL Scripts](#SQL-Scripts)
- [Data Insertion](#Data-Insertion)
- [Backup and Restoration](#Backup-and-Restoration)


# Stage 1: Design and Build the Database

## Introduction
The system is designed for inventory management of a store, including managing supplier details, orders, and products. It allows tracking of product inventory, suppliers, orders, and invoices. The system is meant to provide store managers with an organized and convenient way to manage the inventory and coordinate with suppliers.

#### System Purpose
The system aims to ensure effective management of the store's inventory, suppliers, and orders, while maintaining an organized flow of information. Using the system, actions such as the following can be performed:
Managing supplier details and establishing contact with suppliers.
Managing orders with suppliers, including dates, quantities, and prices.
Tracking inventory and product status in the store.
Handling returns and processing canceled orders.

## ERD and DSD Diagrams
#### ERD (Entity-Relationship Diagram):
The ERD diagram represents the entities within the system and the relationships between them. Each entity is represented by a table in the database.
![ERD](https://github.com/user-attachments/assets/fa613e91-3ceb-4cbe-a41a-73fc2d0a15cb)


#### DSD (Data Structure Diagram):
The DSD diagram shows the data structure and how data is stored in the database, including tables, primary and foreign keys, and relationships between fields.
![DSD](https://github.com/user-attachments/assets/3f6f33f6-a07a-4697-bc61-0f9622c94742)


## SQL Scripts
The system includes the following SQL files:

**createTables.sql:** This file contains all SQL commands to create the tables in the database.

**[View createTables.sql](Stage1/Scripts/CreateTable)**


**insertTables.sql:** This file contains all SQL commands to insert data into the tables.

**[View insertTables.sql](Stage1/Scripts/InsertTable)**


**dropTables.sql:** This file contains the SQL commands to drop all the tables.

**[View dropTables.sql](Stage1/Scripts/DropTable)**

**selectAll_tables.sql:** This file contains SQL commands to select all data from all tables.

**[View selectAll_tables.sql](Stage1/Scripts/SelectAll)**

## Data Insertion
Data insertion was performed using three different tools:

**1. Mockaroo:** We used Mockaroo to generate a CSV file for the Supplier and Employee tables. The file contains data inserted within specific ranges for each table.
![image](https://github.com/user-attachments/assets/4f198e7b-ef74-423d-b3c1-3ca72c21014e)


[View Mockaroo Data CSV](Stage1/MockData)

**2. Generatedata:** We used Generatedata to create CSV files for the Supplier table. The files were generated with predefined ranges for each table.
![צילום מסך 2025-04-06 173425](https://github.com/user-attachments/assets/79cbcea5-0b47-4b24-b412-727ef6eee95b)


[View Generatedata CSV Files](Stage1/Generatedata)

**3. Python Script:** A Python script was used to create CSV files for the following tables: Supplier, Employee, Product, Order_d, Quotation, ReturnProduct, and ProductOrder. The script automatically generated data for each table based on the defined attributes, allowing for quick and structured data insertion.
![image](https://github.com/user-attachments/assets/769db7ad-15e7-4cf1-802b-8f7d0c536be0)

[View Python Script](Stage1/PythonScripts/InsertData)

## Backup and Restoration
The backup is saved in a file named backup_YYYYMMDD_HHMM.sql. To restore, simply run the backup file in your database management system.

**[Backups](Stage1/Backups)**
![image](https://github.com/user-attachments/assets/d93b987c-ebce-4368-9aa8-cad8e7a4fe8f)


# Stage 2: Queries

#### Select
-[How many orders each supplier had each year by status](#How_Many_Orders_Each_Upplier_Had_Each_Year_By_Status)
> שאילתה זו מציגה את מספר ההזמנות שבוצעו לכל ספק, בכל שנה, כשהנתונים מחולקים לפי סטטוס ההזמנה (למשל: הוזמנה, סופקה, בוטלה וכו').
> מטרת השאילתה היא לספק מבט כולל על רמת הפעילות של כל ספק לאורך השנים.
- [Introduction](#introduction)
- [System Purpose](#System-Purpose)
- [ERD and DSD Diagrams](#ERD-and-DSD-Diagrams)
- [SQL Scripts](#SQL-Scripts)
- [Data Insertion](#Data-Insertion)
- [Backup and Restoration](#Backup-and-Restoration)
