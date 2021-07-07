from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import random

app=Flask(__name__)
MySQLdb.connect(host="185.28.21.1", user="u320202036_coordinator", password="Conzura9346@", database="u320202036_coordinator", port=3306)
app.secret_key='success'
app.config['MYSQL_HOST']='185.28.21.1'
app.config['MYSQL_USER']='u320202036_coordinator'
app.config['MYSQL_PORT']=3306
app.config['MYSQL_PASSWORD']='Conzura9346@'
app.config['MYSQL_DB']='u320202036_coordinator'
mysql=MySQL(app)

@app.route('/')
@app.route('/login',methods=['GET','POST'])
def login():
    msg=''
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username=request.form['username']


        password=request.form['password']
        cursor= mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from accounts where username='{}' and password='{}'".format(username,password))

        account=cursor.fetchone()
        if account:

            session['username'] = request.form['username']
            return render_template('homepage.html')
        else:
            msg='incorrect username or password'



    return render_template('log.html',msg=msg)

@app.route('/home')
def homepage():
    return render_template('homepage.html')


@app.route('/homepage/team_view')
def team_view():
    database =MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
    c = database.cursor()


    c.execute("select teamname,project , mentor,marks,link from team_manage")
    data = c.fetchall()
    c.execute("select teamname from team_manage")
    teams=c.fetchall()
    print(data)

    return render_template('team_table.html',table=data,project='nothing',teamcode='nothing',teams=teams)


@app.route('/home/delete',methods=['POST','GET'])
def delete():
    if request.method=='POST':
        team=request.form['formteam']

        database =MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
        cursor = database.cursor()


        db = MySQLdb.connect(host="185.28.21.1", user="u320202036_mentor", password="Conzura9346@", database="u320202036_mentor", port=3306)

        c =db.cursor()
        cursor.execute("select team_members from {}".format(team))
        team_members=cursor.fetchall()
        print(team_members)


        c.execute("update accounts set project=null where teamname='{}'".format(team))
        c.execute("update accounts set teamname=null where teamname='{}'".format(team))
        c.execute("delete from project_files where teamname='{}'".format(team))
        database.commit()
        db.commit()

        cursor.execute("select team_members from {}".format(team))
        team_members = cursor.fetchall()
        le = len(team_members)

        cursor.execute("update accounts set team=null where teamname='{}'".format(team))
        cursor.execute("update accounts set teamname=null where teamname='{}'".format(team))

        cursor.execute("drop table {}".format(team))
        cursor.execute("delete from team_manage where teamname='{}'".format(team))
        database.commit()
        db.commit()

    return team_view()


@app.route('/account')
def account():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select  email ,password from accounts where username='{}'".format(session['username']))
    data=cursor.fetchone()
    return render_template('account.html',username=session['username'].split('@')[0],email=data['email'],password=data['password'])

@app.route('/change_password',methods=['POST','GET'])
def change_password():

    cursor=mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    password=request.form['new_psd']
    cursor.execute("update accounts set password='{}' where username='{}'".format(password,session['username']))
    mysql.connection.commit()
    return account()

@app.route('/logout',methods=['POST','GET'])
def logout():


    session.pop('username',None)
    session.pop('loggedin',None)
    session.pop('teamname',None)
    return render_template('log.html')
@app.route('/homepage/view',methods=["POST","GET"])
def view():
    if request.method=='POST':
        team=request.form['team']
        database = MySQLdb.connect(host="185.28.21.1", user="u320202036_student", password="Conzura9346@", database="u320202036_student", port=3306)
        cursor = database.cursor()
        cursor.execute("select team_members,roll_no,branch ,project from {}".format(team))
        data=cursor.fetchall()
        print(data)


        return render_template('team_view.html',data=data)


if __name__ == '__main__':
    app.secret_key='success'
    app.debug=True
    app.run()
