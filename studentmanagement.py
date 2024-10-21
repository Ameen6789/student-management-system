from flask import *
import sqlite3
app=Flask(__name__)
app.secret_key = 'abcdef'


@app.route("/",methods=["get","post"])
def logins():
    
    
    if request.method=="POST":
        USERNAME=request.form["username"]
        PASSWORD=request.form["password"]
        if USERNAME=="admin" and PASSWORD=="admin":
            
            return render_template("admin.html")
        con=sqlite3.connect("student_management.db")
        cursor=con.cursor()
        con.row_factory=sqlite3.Row
        cursor.execute("select id,username,password,usertype,is_approved from user where username=?",(USERNAME,))
        
        id,usern,passw,usertype,is_approved=cursor.fetchone()
       
        
        
        if (usertype=="student") and (USERNAME==usern and PASSWORD==passw) and is_approved:
            session["student_id"]=id
            return render_template("studenthome.html")
        elif usertype=="teacher" and (USERNAME==usern and PASSWORD==passw):
            session["teacher_id"]=id
            return render_template("teacherhome.html")
        
        else:
            return make_response("invalid login")
    else:
        return render_template("home.html")
    
@app.route("/logout")
def logouts():
    if "student_id" in session:
        del session["student_id"]
    if "teacher_id" in session:
        del session["teacher_id"]
    return render_template("home.html")

@app.route("/studentregister",methods=["get","post"])
def studentregister():
    if request.method=="POST":
        firstname=request.form["firstname"]
        lastname=request.form["lastname"]
        address=request.form["address"]
        email=request.form["email"]
        phone=request.form["phone_number"]
        guardian=request.form["guardian"]
        USERNAME=request.form["username"]
        PASSWORD=request.form["password"]
        con=sqlite3.connect("student_management.db")
        cursor=con.cursor()
        cursor.execute("insert into user(username,password,is_staff,is_approved,usertype) values(?,?,?,?,?)",(USERNAME,PASSWORD,0,0,"student"))
        con.commit()
        con.row_factory=sqlite3.Row
        cursor.execute("select max(id) from user")
        id=cursor.fetchone()[0]
        cursor.execute("insert into student(firstname,lastname,email,address,phone_number,guardian,id) values(?,?,?,?,?,?,?)",(firstname,lastname,email,address,phone,guardian,id))
        con.commit()
        return render_template("login.html")
        
    else:
        return render_template("studentregister.html")
    
@app.route("/addteacher",methods=["get","post"])
def addteacher():
    if request.method=="POST":
        firstname=request.form["firstname"]
        lastname=request.form["lastname"]
        address=request.form["address"]
        email=request.form["email"]
        phone=request.form["phone_number"]
        experience=request.form["experience"]
        salary=request.form["salary"]
        USERNAME=request.form["username"]
        PASSWORD=request.form["password"]
        con=sqlite3.connect("student_management.db")
        cursor=con.cursor()
        cursor.execute("insert into user(username,password,is_staff,is_approved,usertype) values(?,?,?,?,?)",(USERNAME,PASSWORD,1,1,"teacher"))
        con.commit()
        con.row_factory=sqlite3.Row
        cursor.execute("select max(id) from user")
        id=cursor.fetchone()[0]
        cursor.execute("insert into teacher(firstname,lastname,email,address,phone_number,experience,salary,id) values(?,?,?,?,?,?,?,?)",(firstname,lastname,email,address,phone,experience,salary,id))
        con.commit()
        return render_template("login.html")
        
    else:
        return render_template("addteacher.html")
    


@app.route("/adminviewstudent",methods=["get","post"])
def adminviewstudent():

    con=sqlite3.connect("student_management.db")
    cursor=con.cursor()
    con.row_factory=sqlite3.Row
    cursor.execute("select u.is_approved,s.firstname,s.lastname,s.email,s.address,s.phone_number,s.guardian,s.id from user u inner join student s where u.id=s.id")
    
    datas=cursor.fetchall()
    
  
    
    return render_template("adminviewstudent.html",data=datas)


@app.route("/approvestudent/<int:id>")
def approvestudent(id):
    con=sqlite3.connect("student_management.db")
    cursor=con.cursor()
    cursor.execute("update user set is_approved=1 where id=%d"%id)
    con.commit()
    return redirect(url_for("adminviewstudent"))



@app.route("/deletestudent/<int:id>")
def deletestudent(id):
    con=sqlite3.connect("student_management.db")
    con.execute("PRAGMA foreign_keys = ON")
    cursor=con.cursor()
    cursor.execute("delete from user where id=%d"%id)
    con.commit()
    return redirect(url_for("adminviewstudent"))

@app.route("/deleteteacher/<int:id>")
def deleteteacher(id):
    con=sqlite3.connect("student_management.db")
    con.execute("PRAGMA foreign_keys = ON")
    cursor=con.cursor()
    cursor.execute("delete from user where id=%d"%id)
    con.commit()
    return redirect(url_for("adminviewteacher"))




@app.route("/adminviewteacher",methods=["get","post"])
def adminviewteacher():

    con=sqlite3.connect("student_management.db")
    cursor=con.cursor()
    con.row_factory=sqlite3.Row
    cursor.execute("select firstname,lastname,email,address,phone_number,experience,salary,id from teacher")
    datas=cursor.fetchall()
    return render_template("adminviewteacher.html",data=datas)


@app.route("/studenteditprofile",methods=["get","post"])
def studenteditprofile():
    if request.method=="POST":
        id=session["student_id"]
        firstname=request.form["firstname"]
        lastname=request.form["lastname"]
        address=request.form["address"]
        email=request.form["email"]
        phone=request.form["phone_number"]
        guardian=request.form["guardian"]
        con=sqlite3.connect("student_management.db")
        cursor=con.cursor()
        cursor.execute("update student set firstname=?,lastname=?,email=?,address=?,phone_number=?,guardian=? where id=? ",(firstname,lastname,email,address,phone,guardian,id))

        con.commit()
        return render_template("studenthome.html")
    else:
        con=sqlite3.connect("student_management.db")
        cursor=con.cursor()
        con.row_factory=sqlite3.Row
        id=session["student_id"]
        cursor.execute("select firstname,lastname,address,email,phone_number,guardian,id from student where id=?",(id,))
        datas=cursor.fetchone()
        return render_template("studenteditprofile.html",data=datas)
    
@app.route("/studentviewteacher")
def studentviewteacher():
    con=sqlite3.connect("student_management.db")
    cursor=con.cursor()
    con.row_factory=sqlite3.Row
    cursor.execute("select firstname,lastname,email,address,phone_number,experience,salary from teacher")
    datas=cursor.fetchall()
    return render_template("studentviewteacher.html",data=datas)




@app.route("/teachereditprofile",methods=["get","post"])
def teachereditprofile():
    if request.method=="POST":
        id=session["teacher_id"]
        firstname=request.form["firstname"]
        lastname=request.form["lastname"]
        address=request.form["address"]
        email=request.form["email"]
        phone=request.form["phone_number"]
        experience=request.form["experience"]
        salary=request.form["salary"]
        con=sqlite3.connect("student_management.db")
        cursor=con.cursor()
        cursor.execute("update teacher set firstname=?,lastname=?,email=?,address=?,phone_number=?,experience=?,salary=? where id=? ",(firstname,lastname,email,address,phone,experience,salary,id))

        con.commit()
        return render_template("teacherhome.html")
    else:
        con=sqlite3.connect("student_management.db")
        cursor=con.cursor()
        con.row_factory=sqlite3.Row
        id=session["teacher_id"]
        cursor.execute("select firstname,lastname,address,email,phone_number,experience,salary,id from teacher where id=?",(id,))
        datas=cursor.fetchone()
        return render_template("teachereditprofile.html",data=datas)
    

@app.route("/teacherviewstudent")
def teacherviewstudent():
    con=sqlite3.connect("student_management.db")
    cursor=con.cursor()
    con.row_factory=sqlite3.Row
    cursor.execute("select firstname,lastname,email,address,phone_number,guardian from student")
    datas=cursor.fetchall()
    return render_template("teacherviewstudent.html",data=datas)
    
if __name__=="__main__":
    app.run(debug=True)

