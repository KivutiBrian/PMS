from flask import Flask,render_template,request,redirect,url_for,flash,session
import pygal
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

# DB_URL = 'postgresql://postgres:Brian8053@@127.0.0.1:5432/projectManagementSystem'

DB_URL = 'postgresql://kgnjbgcdxvalcc:ad5883d755db80637caa2ae80c98d6d712aeaa80eaf2781b46eb01e8d09fe479@ec2-184-73-216-48.compute-1.amazonaws.com:5432/dfncka2a8m051s'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] ='some-secret-string'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)


from models import ProjectModel
from userModel import AuthenticationModel


@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/authentication')
def auth():
    session.clear()
    return render_template("authentication.html")

@app.route('/logout',methods=['POST'])
def logout():
    session.clear()
    return redirect(url_for('home'))


@app.route('/',methods=['GET'])
def home():
    # session.clear()
    if session:
        print(session['email'])
        #if session is set
        records = ProjectModel.fetch_all()
        status = [x.status for x in records]
        print(status)
        pie_chart = pygal.Pie()
        pie_chart.title = "Completed vs Pending projects"
        pie_chart.add("Pending projects",status.count("pending"))
        pie_chart.add("Completed projects",status.count("complete"))
        graph = pie_chart.render_data_uri()

        return render_template("index.html",records = records,graph=graph)
    else:
        return redirect(url_for('auth'))


@app.route('/register',methods=['POST'])
def addUser():
    fullName = request.form['fullName']
    email = request.form['email']
    password = request.form['password']
    confirmpass = request.form['confirmpass']

    # check if password and confirm password match
    if password != confirmpass:
        flash("Passwords dont match")
        return render_template('authentication.html')
    elif(AuthenticationModel.checkEmailExist(email)):
        # check if email already exist
        flash("User already exist")
        return render_template('authentication.html')
    else:
        # hassing the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # create User
        register = AuthenticationModel(fullName=fullName,email=email,password=hashed_password)
        register.createUser()

        # create session
        session['email'] =  email

        flash("SUCCESS")
        return redirect(url_for('home'))

# creating a login route
@app.route('/login',methods=['GET','POST'])
def loginIn():

    email = request.form ['email']
    password = request.form ['password']

    if AuthenticationModel.checkEmailExist(email=email):
        if AuthenticationModel.userpass(email=email,password=password):
            # create session
            session['email'] = email
            return redirect(url_for('home'))
        else:
            flash("password incorrect")
            return render_template('authentication.html')
    else:
        flash("email is uknown")
        return render_template('authentication.html')





@app.route('/project/create',methods=['POST'])
def addNewProject():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        startDate = request.form['startDate']
        endDate = request.form['endDate']
        cost = request.form['cost']
        status = request.form['status']
        project = ProjectModel(title=title,description=description,startDate=startDate,
                                      endDate=endDate,cost=cost,status=status)

        project.create_record()

        flash("SUCCESS")
        return redirect(url_for('home'))

@app.route('/project/edit/<int:id>',methods=['POST'])
def editProject(id):
    newTitle = request.form['title']
    newDescription = request.form['description']
    newStartDate = request.form['startDate']
    newEndDate = request.form['endDate']
    newCost = request.form['cost']
    newStatus = request.form['status']
    updated = ProjectModel.update_by_id(id=id,newTitle=newTitle,newDescription=newDescription
                                        ,newStartDate=newStartDate,newEndDate=newEndDate,
                                        newCost=newCost,newStatus=newStatus)

    if updated:
        flash("Updated Successfully")
        return redirect(url_for('home'))
    else:
        flash("No record found")
        return redirect(url_for('home'))

@app.route('/project/delete/<int:id>',methods=['POST'])
def deleteRecord(id):
    deleted = ProjectModel.delete_by_id(id)
    if deleted:
        flash("Deleted Succesfully")
        return redirect(url_for('home'))
    else:
        flash("Record not found")
        return redirect(url_for('home'))



if __name__=='__main__':

    app.run(port=5001,debug=True)

# Bootstrap
# Flask
# SQL-Alchemy

# project management system
 # C- R - U - D


