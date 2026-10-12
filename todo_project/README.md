DB Lab 2 - Login & ToDo Application
Student
Ahmed Ashraf

ID
2204003

Technology
Backend: Flask

Frontend: HTML / CSS

Database: MySQL

Features
Register
Login
Logout
Session Management
Password Hashing (bcrypt)
Add ToDo
Edit ToDo
Delete ToDo
Mark Done / Undone
Open Tasks Counter
How To Run
Install Python.

Install packages:

pip install flask mysql-connector-python bcrypt

Run schema.sql in MySQL Workbench.

Update database password in app.py.

Run:

py app.py

Open:
http://127.0.0.1:5000

Answers
A
Why do UPDATE and DELETE contain AND user_id = ?

To prevent users from editing or deleting todos that do not belong to them.

B
What happens if a todo is inserted with a user_id that does not exist?

MySQL raises a foreign key constraint error.

C
Why do you store a hash instead of the password?

To protect user passwords if the database is compromised.

D
Why did you check for an empty name although the column is NOT NULL?

Because NOT NULL only prevents NULL values. Empty strings are still accepted.