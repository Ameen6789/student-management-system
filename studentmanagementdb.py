import sqlite3
con=sqlite3.connect("student_management.db")
print("database created")
con.execute("create table user(id integer primary key autoincrement,username text unique,password text ,is_staff boolean ,is_approved boolean default false,usertype text)")
con.execute("create table student(student_id integer primary key autoincrement,firstname text, lastname text,email text,address text,phone_number int,guardian text,id int,foreign key (id) references user(id) on delete cascade)")
con.execute("create table teacher(teacher_id integer primary key autoincrement,firstname text, lastname text,email text,address text,phone_number int,experience int,salary int,id int,foreign key (id) references user(id) on delete cascade)")

print("table created")