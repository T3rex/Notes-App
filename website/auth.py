from nis import cat
from flask import Blueprint, render_template, request,flash, redirect, url_for
from website.models import User,Note
from werkzeug.security import generate_password_hash,check_password_hash
from website import db
from flask_login import login_required,login_user,logout_user,current_user

auth = Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        email= request.form.get("email")  
        pswd = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        
        if user:
            if check_password_hash(user.password,pswd):
                flash('Logged in successfully',category='success')
                login_user(user,remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password try again',category='danger')
        else:
            flash("Email not registered",category='danger')        
                    
    return render_template('login.html', user=current_user)



@auth.route('/signup',methods=['GET','POST'])
def signup():
    #print(request.form)
    if request.method=='POST':        
        email=request.form.get('email')
        fName = request.form.get('first-name')
        pswd=request.form.get('password')
        conf_pswd=request.form.get('conf-password')

        user = User.query.filter_by(email=email).first( )

        if user:
            flash("Email already exist",category="danger")        
        elif len(email) < 4:
            flash('Email must be greater than 4 chracters', category="danger")
        elif len(fName) < 3:
            flash('First name must be greater than 2 chracters', category="danger")
        elif pswd != conf_pswd:
            flash('Password and confirm password do not match', category="danger")    
        elif len(pswd)<6:
            flash('Password is less than 6 characters', category="danger")   
        else:
            new_user = User(email=email,password=generate_password_hash(pswd,method="sha256"),first_name=fName)
            db.session.add(new_user)
            db.session.commit()
            flash('Account successfully created, You are loggin in',category='success')
            login_user(user,remember=True)
            return redirect(url_for('views.home'))  


    return render_template('signup.html', user=current_user)



@auth.route('/logout', methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash("You have been logged out!", category='success')
    return render_template('login.html',user =current_user)