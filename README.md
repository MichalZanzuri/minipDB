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


### [SelectQueries](Stage2/SelectQueries.sql)
>#### ❶ מספר ההזמנות לכל ספק בכל שנה לפי סטטוס:
>  שאילתה זו מציגה את מספר ההזמנות שבוצעו לכל ספק, בכל שנה, כשהנתונים מחולקים לפי סטטוס ההזמנה (למשל: הוזמנה, סופקה, בוטלה וכו').
> מטרת השאילתה היא לספק מבט כולל על רמת הפעילות של כל ספק לאורך השנים.
>לאחר הרצה הטבלה תראה כך:
![image](https://github.com/user-attachments/assets/77ce3cdd-618c-440a-91c0-649796f46ed8)

>#### ❷ ממוצע כמות הזמנות לכל מוצר:
> שאילתה זו מחשבת את ממוצע הכמות שהוזמנה לכל מוצר, יחד עם שמו וקטגוריית המוצר.  
> מטרתה לבדוק אילו מוצרים נמכרים בכמויות גבוהות יותר בממוצע, כדי לנתח פופולריות.
>לאחר הרצה הטבלה תראה כך:
>![image](https://github.com/user-attachments/assets/bffd52ba-cce2-482a-abf9-aebe58b427ba)

>#### ❸ ממוצע מחיר מוצר לפי קטגוריה וחודש הוספה:
> שאילתה זו מחשבת את ממוצע המחיר של מוצרים, לפי קטגוריה ולפי החודש שבו נוספו למערכת.  
> מטרת השאילתה היא לזהות מגמות במחירים לאורך חודשי השנה ולפי סוגי המוצרים.
>לאחר הרצה הטבלה תראה כך:

>![image](https://github.com/user-attachments/assets/52207e8c-625e-4a0c-bb78-dd9e356d4748)

> #### ❹ הצעות מחיר שפגו החודש: 
> שאילתה זו מחפשת הצעות מחיר שתוקפן פג במהלך החודש הנוכחי.  
> המידע כולל את שם הספק, מספר ההצעה, המחיר, ותאריך התפוגה של כל הצעה.
> לאחר הרצה הטבלה תראה כך:

> ![image](https://github.com/user-attachments/assets/635b7463-e2aa-4779-bf4e-a1d1487fe978)

>#### ❺ עובדים שביצעו יותר מ־3 הזמנות בסכום כולל של מעל 1000 ש"ח: 
> שאילתה זו מציגה את שמות העובדים שביצעו יותר משלוש הזמנות, ובסך כולל של מעל 1000 ש"ח.  
> מטרת השאילתה היא לאתר עובדים פעילים במיוחד בהזמנת מוצרים.
>לאחר הרצה הטבלה תראה כך:

>![image](https://github.com/user-attachments/assets/139333bc-8c8c-486c-a888-54a1de260929)


>#### ❻ כל ההחזרות מהשנה האחרונה כולל פרטי ספק:
> שאילתה זו מציגה את כל ההחזרות שבוצעו במהלך השנה האחרונה, כולל תאריך ההחזרה, סטטוס ההחזרה, סיבת ההחזרה ושם הספק הקשור להחזרה.
>לאחר הרצה הטבלה תראה כך:

>![image](https://github.com/user-attachments/assets/604cb3ab-13fa-48d2-be30-19c94aeb67ad)


>#### ❼ כמות ההזמנות שסופקו בזמן לעומת כמות ההזמנות שאיחרו: 
> שאילתה זו בודקת כמה מההזמנות סופקו במועד שהובטח, וכמה מהן הגיעו באיחור.  
> כך ניתן לנתח את רמת הדיוק והאמינות בזמני האספקה.
>לאחר הרצה הטבלה תראה כך:

>![image](https://github.com/user-attachments/assets/4caab307-a9cb-42dd-89f5-d873db82472e)

 
>#### ❽ כמות מוצרים לפי צבע ומין, מחולקת לפי חודש הוספה:  
> שאילתה זו מציגה את כמות המוצרים שבמאגר, מחולקת לפי צבע המוצר ומיועד למין (זכר/נקבה), ולפי החודש שבו המוצר נוסף למערכת.  
> מטרתה לבחון את פריסת המוצרים לפי מאפיינים וטרנדים חודשיים.
>לאחר הרצה הטבלה תראה כך:

>![image](https://github.com/user-attachments/assets/804bb708-851c-4428-8a71-1af59cebca29)

### [DeleteQueries](Stage2/DeleteQueries.sql)

>#### ❶ מחיקת הצעות מחיר שתוקפן פג בחודש נבחר (דצמבר 2024):
> שאילתה זו מוחקת את כל הצעות המחיר (Quotation) שפגו בדצמבר 2024.  
> המטרה היא לנקות מהמערכת הצעות שאינן בתוקף ואינן רלוונטיות.
> לפני הרצת השאילתא הטבלה נראתה כך:
> 
> ![image](https://github.com/user-attachments/assets/14474991-75d3-4ef1-a5c1-8da24b6460d6)
> 
> ![image](https://github.com/user-attachments/assets/42e92ada-6e76-47a4-af29-94715088c473)
>
> אחרי הרצת השאילתא כאשר month=6 year=2024 הטבלה תראה כך
>
> ![image](https://github.com/user-attachments/assets/69138c80-89ef-4b65-a099-fdb1b570734d)

> #### ❷ מחיקת מוצרים שלא הוזמנו מעולם:
> שאילתה זו מוחקת מהמלאי מוצרים שמעולם לא הוזמנו, על פי הצלבה עם טבלת ProductOrder.  
> כך ניתן לנקות את בסיס הנתונים ממוצרים שאינם פעילים או שאינם מבוקשים.
> לפני הרצת השאילתא הטבלה נראתה כך:
> 
>![image](https://github.com/user-attachments/assets/6b7c3a89-947c-42cc-a0bf-63fced3bba1b)
>
>  ![image](https://github.com/user-attachments/assets/de70e522-81ea-4a43-b664-82a13e0c4511)

> אחרי הרצת השאילתא לאחר סינון המוצרים, הטבלה תראה כך:
> 
> ![image](https://github.com/user-attachments/assets/90344e62-d6fe-461c-a3c4-0134682f04b5)


> #### ❸ מחיקת הצעות מחיר שלא הובילו להזמנה:
> שאילתה זו מוחקת את כל הצעות המחיר שלא שויכו להזמנה בפועל (order_id IS NULL).  
> המטרה היא לנקות הצעות שלא מומשו ואינן בשימוש.
> 
> ![image](https://github.com/user-attachments/assets/54151f2a-6dde-4a96-afd3-bbcfa8555d9b)

> 
> ![image](https://github.com/user-attachments/assets/03a34b2d-ab3e-406b-9132-f00fe2285c90)
> 

> אחרי הרצת השאילתא לאחר סינון הצעות המחיר, הטבלה תראה כך:(במקרה הנ"ל לא התקיים התנאי בנתונים הנוכחיים ולכן הטבלה נשארה אותו דבר לאחר הפעלת השאילתא)
> 
> ![image](https://github.com/user-attachments/assets/df57b057-8d1f-431e-a29f-14cffab7eb4a)


### [UpdateQueries](Stage2/UpdateQueries.sql)

> #### ❶ עדכון מחירים – עלייה של 10% למוצרים שנמכרו ביותר מ־100 פעמים:
> עדכון זה מעלה את המחיר ב־10% לכל המוצרים שנמכרו ביותר מ־100 פעמים.  
> המטרה היא להתאים את המחיר בהתאם לביקוש הגבוה.
> לפני הרצת השאילתא הטבלה תראה כך:
> 
> ![image](https://github.com/user-attachments/assets/423eb612-2877-4aa1-bf81-286940595604)

> 
> ![image](https://github.com/user-attachments/assets/a87d4c77-78fb-4057-afe5-3145a4860809)
> 

> לאחר הרצת השאילתא ועדכון המחירים :
> 
> ![image](https://github.com/user-attachments/assets/c6c202ae-1281-4eb6-b912-032be69d52e6)


> #### ❷ עדכון תפקיד לעובדים עם ותק של 3 שנים – שינוי ל־"Senior":
> עדכון זה משנה את שם התפקיד של כל עובד שהתקבל לעבודה לפני שלוש שנים או יותר ל־"Senior".  
> המטרה היא לשקף את הוותק והניסיון של העובדים במערכת.
> לפני הרצת השאילתא הטבלה תראה כך:
> 
> ![image](https://github.com/user-attachments/assets/e6de4859-d1c7-450b-a8c8-99ceed16b8a6)

> 
> ![image](https://github.com/user-attachments/assets/22c6a255-3880-4f0f-b8cd-723e97b58d3a)
> 
> לאחר הרצת השאילתא ועדכון שם התפקיד לעובדים, הטבלה תראה כך:
> 
> ![image](https://github.com/user-attachments/assets/5304a98b-ead6-47a7-a0fb-ff0e6e94c666)
> 


> #### ❸ עדכון מחיר – הנחה של 20% לכל המוצרים בקטגוריה מסוימת:
> עדכון זה מוריד את המחיר ב־20% לכל המוצרים ששייכים לקטגוריה מסוימת (במקרה הזה 'test').  
> המטרה היא להפעיל מבצע או לקדם מוצרים מקטגוריה ספציפית.
> לפני הרצת השאילתא הטבלה תראה כך:
> 
> ![image](https://github.com/user-attachments/assets/c9fd10ca-8df8-43eb-99be-899cfdfd740f)

> 
> ![image](https://github.com/user-attachments/assets/2bacfaae-2a33-42e3-a951-a9c54d7d4f67)


> לאחר הרצת השאילתא ועדכון המחירים למוצרים, הטבלה תראה כך:
> 
> ![image](https://github.com/user-attachments/assets/56129732-24e5-4fe2-a1fb-4abd3ace479a)

> 

### [Constraints](Stage2/Constraints.sql)

> ####  -אילוץ CHECK על טבלת Product – המחיר חייב להיות חיובי  
> באמצעות הפקודה `ALTER TABLE` הוסף אילוץ מסוג `CHECK` לעמודה `price`, אשר מוודא שכל ערך שמוזן בעמודה זו יהיה **גדול מ־0**.  
> המטרה של האילוץ היא למנוע הזנת מחירים שליליים למוצרים.
> 
> ![image](https://github.com/user-attachments/assets/104d2657-3cef-4894-b4d3-c125f763a058)

> ####  -אילוץ DEFAULT על טבלת Order_d – ערך ברירת מחדל לסטטוס ההזמנה  
> באמצעות הפקודה `ALTER TABLE` הוגדר ערך ברירת מחדל (`DEFAULT`) לעמודה `status`, כך שאם בעת יצירת הזמנה חדשה לא מצוין סטטוס – המערכת תשלים אוטומטית את הערך `'Pending'`.  
> המטרה היא לחסוך צורך בהזנה ידנית של ערך ברוב המקרים ולהבטיח עקביות בנתונים.
> 
> ![image](https://github.com/user-attachments/assets/e61628d5-c7d4-47e1-8fae-48be62e97ada)

> ####  -אילוץ NOT NULL על טבלת Supplier – שם החברה הוא שדה חובה  
> באמצעות הפקודה `ALTER TABLE` הוגדר אילוץ מסוג `NOT NULL` לעמודה `company_name`, כך שאי אפשר להזין ערך ריק (NULL) לשדה זה.  
> המטרה היא להבטיח שלכל ספק שמוזן למערכת יהיה שם חברה מוגדר.
> 
> ![image](https://github.com/user-attachments/assets/d7d7f135-fed9-4943-9958-6c6e517da9fe)


## Backup
**[Backups](Stage2/Backups)**


# Stage 3: Integration and Views
המטרה בשלב זה היתה למזג בין 2 בסיסי נתונים
בסיס הנתונים שלנו הוא mydatabase לו היו מספר טבלאות מלאות בערכים, ובסיס נתונים נוסף בשם LHDB בו היו חלק מהטבלאות שונות והערכים שונים
>#### ERD LHDB
>![ERD_LHDB](https://github.com/user-attachments/assets/1f4569a9-4574-4e2a-80ad-c70abbe26fa0)
>
>#### DSD LHDB
>![DSD_LHDB](https://github.com/user-attachments/assets/d4359059-2423-4b3f-b0eb-765470afc054)


>
>[Integrate](Stage3/Integrate)
לצורך ביצוע האינטגרציה בין שני בסיסי הנתונים, ביצענו את הצעדים הבאים:
- טענו את קובצי הגיבוי של שני האגפים אל תוך בסיס נתונים חדש, כך שכל טבלה קיימת קיבלה שם חדש עם הסיומת _X_temp – לדוגמה: Product_X_temp, Customer_X_temp.
- יצרנו טבלאות חדשות בשם הקלאסי של כל ישות מתוך תרשימי ה־ERD, והעברנו אליהן את העמודות שנבחרו מבין שתי הגרסאות של הטבלאות, תוך שמירה על שמות עקביים ומבנה נורמלי. הנתונים המתאימים לכל עמודה הועתקו גם כן בעזרת שאילתות INSERT INTO ... SELECT.
- מאחר שלשתי טבלאות – Employee ו־Customer – היו עמודות משותפות כמו FullName, יצרנו טבלת־אב בשם Person. טבלאות הבת מכילות מפתח זר (PersonId) שמצביע על הרשומה המתאימה בטבלת־האב. כך נמנעה כפילות והושגה אחידות מבנית.
- טבלאות שהיו קיימות רק באגף שלנו (למשל ReturnProduct, Order_d) נותרו ללא שינוי. טבלאות חדשות מהאגף השני (למשל Store, Discount, StoreSale) נבנו מחדש והוזנו אליהן נתונים רלוונטיים מהמקורות הקיימים.
- לצורך שליפת מידע מבסיס הנתונים השני-LHDB, נעשה שימוש בפקודת dblink, שאפשרה שליפת נתונים ממסד LHDB, והשוואתם לרשומות הקיימות כדי למנוע כפילויות. הנתונים הוזנו אל טבלאות כמו Product תוך המרה והתאמה לעמודות החדשות.
  
תרשימי בסיס הנתונים הסופי שיצרנו:
  >#### ERD Merged_DB
>![Merged_DB](https://github.com/user-attachments/assets/d837ba84-b6ea-4513-9a80-907baded9229)

>#### DSD Merged_DB
>![Merged_DB DSD](https://github.com/user-attachments/assets/52f81e3b-5639-48aa-9092-bc15bb572db3)


>
>### Views
>####  View 1:supplier_orders_with_employee
>מציג את כל ההזמנות שבוצעו על ידי עובדים, כולל פרטי ההזמנה, שם העובד ושם הספק.
הוא משלב בין שלוש טבלאות: Order_d, supplier, ו־employee
>![image](https://github.com/user-attachments/assets/a6709b8e-4a8b-4823-b474-8ac6c656cbdc)

>שאילתה 1 על המבט מציגה את כל ההזמנות שביצע העובד לפי שם העובד.
>קוד:
>
>![צילום מסך 2025-06-03 192928](https://github.com/user-attachments/assets/ac0680b3-43fa-473c-a13a-ff437d02496a)

>
>פלט:
>
>![image](https://github.com/user-attachments/assets/c38e482f-da2f-4d0d-a467-b001d5717073)


>שאילתה 2 על המבט מציגה כמה הזמנות ביצע כל עובד – סופרת לפי שם העובד.
>קוד:
>
>![image](https://github.com/user-attachments/assets/c256edb5-1029-4143-989a-d5b1fe05fdc3)

>פלט:
>
>![image](https://github.com/user-attachments/assets/5d8f4a62-ab45-4526-a8f1-f9d75a089656)


>#### View 2: customer_sales_view
>המבט הזה מציג את כל הלקוחות ואת המכירות שהם ביצעו (אם בכלל).
אם לקוח לא ביצע מכירה – הוא עדיין יופיע (בזכות LEFT JOIN)
>
>![image](https://github.com/user-attachments/assets/80f779a4-ba3a-49ff-87a7-f884017beba6)

>שאילתה 1 על המבט מציגה את כמות הלקוחות שקנו מעל סכום מסוים.
>
>קוד:
>
>![image](https://github.com/user-attachments/assets/784e3e04-46f7-4f0c-a048-da43bf95aa7c)


>פלט:
>
>![image](https://github.com/user-attachments/assets/d25a1e14-f510-41a8-862b-6793c875f83b)




>שאילתה 2 על המבט מציגה מי מהלקוחות ביצע רכישה לי תאריך לפי הפורמט YYYY-MM-DD.
>
>קוד:
>
>![image](https://github.com/user-attachments/assets/ecd5efdb-19d2-4a0a-8e51-f46c0ad58b3a)

>פלט:
>
>![image](https://github.com/user-attachments/assets/9f8337e9-0743-4779-9939-913544f13df4)


>

# Stage 4: Programming
בשלב זה יצרנו תוכניות לא טריוויאליות בשפת PL/pgSQL אשר כוללות פונקציות, פרוצדורות, טריגרים ותוכניות ראשיות. כל תוכנית עושה שימוש ברכיבי תכנות מתקדמים כמו לולאות, תנאים, חריגות, רשומות ופקודות DML. בנוסף, ביצענו שינויים בטבלאות בסיס הנתונים לפי הצורך, ותיעדנו אותם בקובץ ALTER.

>### Function
>>#### [get_low_stock_products.sql](Stage4/Function/get_low_stock_products.sql)
>> הפונקציה מחזירה את כל המוצרים שיש להם פחות מ־10 יחידות במלאי.
>>הפונקציה נועדה לעקוב אחרי מלאי חסר.
>>
>>![image](https://github.com/user-attachments/assets/e7f3ec83-81a4-475d-b1ab-13499c66812a)
>>


>>
>>#### [get_total_sales_for_customer.sql](Stage4/Function/get_total_sales_for_customer.sql)
>>הפונקציה מחזירה את סכום המכירות הכולל של לקוח מסוים
>>הפונקציה שימושית לניתוח פעילות לקוחות
>>
>>![image](https://github.com/user-attachments/assets/123c2c9e-fc08-4f4e-9b8e-310a4ce13b2d)
>>
>>
>>![image](https://github.com/user-attachments/assets/1702954c-41e7-4c98-8b67-c9814ec3849f)
>
>### Procedure
>
>>#### [get_active_discounts_by_store.sql](Stage4/Procedure/get_active_discounts_by_store.sql)
>>מחזירה את ההנחות הפעילות נכון לעכשיו בחנות מסוימת.
>>הפרוצדורה נועדה למעקב אחרי מבצעים.
>>
>>![image](https://github.com/user-attachments/assets/6b180494-db6d-47b4-a632-be493ab08cd2)
>>
>>
>>![image](https://github.com/user-attachments/assets/8b3f9bca-f212-4815-8e08-b06dc28c924b)
>>
>>#### [update_product_stock.sql](Stage4/Procedure/update_product_stock.sql)
>>הפרוצדורה מעדכנת את כמות המלאי של מוצר מסוים, וזורקת חריגה אם המוצר לא קיים.
>>לפני עדכון:
>>
>>![image](https://github.com/user-attachments/assets/aa99fba1-98ac-4ca4-af6d-82be22bba774)
>>
>>אחרי עדכון:
>>
>>![image](https://github.com/user-attachments/assets/913c773a-911d-41b1-af82-d0a97700bf37)
>
>### Trigger
>
>#### [trigger_check_price.sql](Stage4/Trigger/trigger_check_price.sql)
>הטריגר מונע הכנסת מוצר עם מחיר שהוא 0 או פחות.
>![image](https://github.com/user-attachments/assets/883ffd63-bf5b-49ba-a19e-d44e334c639a)
>
>במקרה של עדכון מחיר חיובי-תקין ההרצה עובדת תקין
>![image](https://github.com/user-attachments/assets/865d2a34-b9d7-4da4-ac20-ba1fa1aef00f)
>
>#### [update_last_updated_column.sql](Stage4/Trigger/update_last_updated_column.sql)
>הטריגר בכל עדכון למוצר, מעדכן את שדה last_updated עם התאריך הנוכחי.
>
>![image](https://github.com/user-attachments/assets/5f6f405d-590d-43bd-a1af-412a8d8ce132)
>
>### Main Program
>
>#### [main_update_customer_sale.sql](Stage4/Main_Program/main_update_customer_sale.sql)
>התוכנית מציגה את כל המכירות של לקוח לפני ואחרי עדכון מחיר מכירה.
>התוכנית משלבת בין פונקציה לפרוצדורה.
>
>![image](https://github.com/user-attachments/assets/f92d1e91-fe07-4016-b08e-fb554d3a877d)
>
>#### [program_apply_discount_top_selling_product.sql](Stage4/Main_Program/program_apply_discount_top_selling_product.sql)
>התוכנית מאתרת את המוצר הכי נמכר, ומוסיפה לו הנחה.
>
>![image](https://github.com/user-attachments/assets/9536da07-bf63-4b10-b22e-12224f012362)
>
>![image](https://github.com/user-attachments/assets/a910a5f4-2369-4296-90c6-d60f3e02aa1a)
>
>###  ALTER TABLE
>#### [ALTER TABLE.sql](Stage4/ALTER_TABLE.sql)
>הוספת העמודה last_updated לטבלת product לצורך כתיבת הטריגר update_last_updated_column
>הסרת העמודה discountid והוספתה מחדש כ־IDENTITY PRIMARY KEY לצורך כתיבת התוכנית program_apply_discount_top_selling_product
>
>###  backup
>#### [backup4](Stage4/Stage4/backup4)
>
># Stage 5: Creating a User-Friendly GUI for Database Management
>#### סקירה כללית על המערכת:
>מערכת ניהול החנות היא אפליקציית ממשק גרפי מקצועית שפותחה בשפת Python באמצעות ספריית Tkinter. המערכת מיועדת לניהול כל היבטי החנות: מוצרים, מכירות, הנחות וסטטיסטיקות מפורטות.
>#### הוראות הפעלה של האפליקציה:
>התקנת Python 3.7+
>שימוש בספריות pip install tkinter
pip install mysql-connector-python
# או
pip install psycopg2
שימוש במערכת
- מסך הבית: מציג ברכת פתיחה וניווט למודולים השונים
- ניהול מוצרים: הוספה, צפייה וניהול מלאי + יצוא לאקסל
- ניהול מכירות: רישום מכירות חדשות וצפייה בהיסטוריה + יצוא לאקסל
- סטטיסטיקות: דשבורד עם נתונים ויזואליים
- ניהול הנחות: יצירה וניהול הנחות לתקופות שונות + יצוא לאקסל
- שאילתות: הפעלת שאילתות מותאמות אישית + יצוא תוצאות לאקסל
#### כלים וטכנולוגיות שימושיות:
#### Python & Tkinter
Python: שפה ידידותית ועם ספריות עשירות
Tkinter: ספרייה מובנית לממשק גרפי, קלה לפיתוח  
#### עיצוב ממשק המשתמש (UI/UX)
צבעוניות עקבית: מפת צבעים מוגדרת לכל מודול
אייקונים ויזואליים: שיפור חווית המשתמש
Responsive Design: ממשק מותאם לגדלי מסך שונים
#### ניהול מסד נתונים
Connection Pooling: חיבורים יעילים למסד הנתונים
Error Handling: טיפול מקיף בשגיאות
SQL Injection Prevention: שימוש ב-prepared statements
#### אינטראקטיביות ומשוב למשתמש
Hover Effects: אפקטי העברת עכבר על כפתורים
Real-time Updates: עדכון תאריך ושעה בזמן אמת
Loading States: הצגת סטטוס טעינה
Error Messages: הודעות שגיאה
#### ויזואליזציה של נתונים
גרפי עמודות פשוטים למכירות שבועיות
כרטיסי סטטיסטיקה אינטראקטיביים
צבעי סטטוס (ירוק לפעיל, אדום ללא פעיל)

#### דוחות אקסל מקצועיים:
מבנה הדוח: כותרת, מטא-דטה, כותרות עמודות, נתונים
עיצוב מקצועי: צבעים, גבולות, פונטים
נוסחאות אוטומטיות: חישובים במקרה הצורך

### 📊 תכונות מרכזיות של המערכת
#### ניהול מוצרים עם יצוא
הוספת מוצרים חדשים עם ולידציה
מעקב אחר מלאי ואזהרות מלאי נמוך
חישוב שווי מלאי אוטומטי
יצוא כל המוצרים לאקסל
יצוא מוצרים עם מלאי נמוך לטיפול מיידי

#### ניהול מכירות עם דוחות
רישום מכירות בזמן אמת
מעקב אחר הכנסות יומיות
ניתוח לקוחות ייחודיים
יצוא כל המכירות לאקסל
אפשרות סינון לפי תאריכים ביצוא

#### מערכת הנחות מתקדמת עם דוחות
הנחות מותנות תאריך
ניהול הנחות לפי מוצר וסניף
מעקב אחר סטטוס הנחות (פעיל/לא פעיל)
יצוא רשימת הנחות עם סטטוס
צבעים מותאמים לסטטוס בקובץ האקסל

#### דשבורד סטטיסטיקות
כרטיסי מידע אינטראקטיביים
גרפי מכירות שבועיים
חלונות פרטים למידע מורחב

#### מערכת שאילתות גמישה עם יצוא
שאילתות מוגדרות מראש
תמיכה בפרמטרים דינמיים
הצגת תוצאות בטבלה מסודרת
יצוא תוצאות שאילתות לאקסל
שמירת תוצאות עם כותרת השאילתה

#### מערכת יצוא אקסל מקצועית
תכונות יצוא עיקריות:
יצוא עם עיצוב מקצועי: כותרות צבעוניות, גבולות, פונטים
מטא-דטה אוטומטית: תאריך יצירה, שם מערכת, כותרת דוח
שמות קבצים חכמים: רשימת_מוצרים_20241225_143022.xlsx
בחירת מיקום שמירה: דיאלוג ידידותי למשתמש
פתיחה אוטומטית: של התיקייה אחרי שמירה מוצלחת

סוגי דוחות זמינים:
דוח מוצרים מלא - כל המוצרים במערכת
דוח מלאי נמוך - מוצרים הדורשים טיפול מיידי
דוח מכירות - כל המכירות עם פרטים מלאים
דוח הנחות - הנחות עם סטטוס פעיל/לא פעיל
דוחות שאילתות מותאמים - תוצאות שאילתות ספציפיות

### -המערכת מוכנה לשימוש מסחרי ויכולה לשרת עסקים קטנים ובינוניים ברמת יעילות גבוהה-


