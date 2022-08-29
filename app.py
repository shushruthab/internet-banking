from flask import Flask, render_template, redirect, session, flash, url_for, request
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Profile, Account, Transaction, Purchase
from forms import RegisterForm, LoginForm, TransferForm, ProfileForm
from sqlalchemy import or_
from sqlalchemy import desc
import os
import re


app = Flask(__name__)
uri = os.environ.get('DATABASE_URL', 'postgresql:///satozbank')
if uri.startswith("postgres://"):
 uri = uri.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = os.environ.get('SECRET_KEY', 'abc123')
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


toolbar = DebugToolbarExtension(app)

connect_db(app)


db.create_all()

# ------Homepage-----------------------------
@app.route("/")
def homepage():
    return redirect("/login")
    
# ---------Login and Register----------------
@app.route("/login", methods=["GET", "POST"])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.authenticate(username, password)

        if user:
            session['username'] = user.username
            return redirect(f"/user/{session['username']}")
        else:
            form.username.errors = ["Invalid username or password"]
    
    return render_template("login.html", form=form)

@app.route("/register", methods=["GET", "POST"])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
    
        new_User = User.register(username, password, email, first_name, last_name)
        db.session.add(new_User)
        db.session.commit()

        session["username"] = new_User.username
        return redirect(f"/user/{new_User.username}/createaccount")
    
    else:
        return render_template("register.html", form=form)

#  -------Logout--------------------------------
@app.route('/logout')
def logout():
    session.pop("username")
    return redirect('/')

# ----------------------------Dashboard----------------------------------

@app.route('/user/<username>')
def userdashboard(username):
    if "username" not in session:
        flash("Please log in to your account")
        return redirect('/login')

    username=session["username"]
    user = User.query.filter_by(username=username).first()
    return render_template("dashboard.html", user=user)

# ----------------Account ----------------------------------------------
@app.route('/user/<username>/createaccount')
def createaccount(username):
    if "username" not in session:
        flash("Please log in to your account")
        return redirect('/login')

    username = session["username"]
    user = User.query.filter_by(username=username).first()
    existing_user_check = Account.query.filter_by(user_id=user.id).first()
    if (existing_user_check):
        return redirect(f"/user/{username}")
    else:
        new_account = Account.create(user.id)
        db.session.add(new_account)
        db.session.commit()
        return redirect(f"/{user.username}/createprofile")

@app.route('/user/<username>/account')
def viewact(username):
    if "username" not in session:
        flash("Please log in to your account")
        return redirect('/login')

    username=session["username"]
    user = User.query.filter_by(username=username).first()
    act = user.accounts[0]
    return render_template("account.html", user=user, act=act)

@app.route('/user/<username>/txns')
def viewtxn(username):
    if "username" not in session:
        flash("Please log in to your account")
        return redirect('/login')

    # Get transactions associated with username
    username=session["username"]
    user = User.query.filter_by(username=username).first()
    act = user.accounts[0]
    txns = Transaction.query.filter(or_(Transaction.sender == act.account_no, Transaction.recipient == act.account_no)).order_by(desc(Transaction.id)).all()

    return render_template("txns.html", txns=txns, user=user, act=act)


# -------Dashboard Profile---------------
@app.route('/<username>/createprofile')
def createprof(username):
    if "username" not in session:
        flash("Please log in to your account")
        return redirect('/login')

    username = session["username"]
    user = User.query.filter_by(username=username).first()
    existing_profile_check = Profile.query.get(user.id)
    if (existing_profile_check):
        return redirect(f"/user/{username}")
    else:
        new_profile = Profile.createprof(user.id)
        db.session.add(new_profile)
        db.session.commit()
        return redirect(f"/user/{user.username}")

@app.route('/user/<username>/profile', methods=["GET"])
def viewprofile(username):
    if "username" not in session:
        flash("Please log in to your account")
        return redirect('/login')
    
    username=session["username"]
    user = User.query.filter_by(username=username).first()
    profile = Profile.query.get(user.id)
    if profile:
        return render_template("profile.html", profile=profile, 
                                        user=user)
    else: 
        return redirect(f"/{user.username}/createprofile")
    

@app.route('/user/<username>/editprofile')
def editprof(username):
    form = ProfileForm()
    user = User.query.filter_by(username=username).first()
    profile = Profile.query.filter_by(user_id = user.id).first()
    return render_template("editprofile.html", form=form, user=user, profile=profile)

@app.route('/user/<username>/saveprofile', methods=["POST"])
def saveprofile(username):
    if "username" not in session:
        flash("Please log in to your account")
        return redirect('/login')

    form = ProfileForm()
    username=session["username"]
    user = User.query.filter_by(username=username).first()
    profile = Profile.query.filter_by(user_id = user.id).first()
    
    address = form.address.data
    company = form.company.data
    role = form.role.data

    profile.address = address
    profile.company = company
    profile.role = role
    
    db.session.add(profile)
    db.session.commit()
    return redirect(f"/user/{username}/profile")

# -----------------------Transfer------------------------------

@app.route('/user/<username>/transfer', methods=["GET", "POST"])
def transfermoney(username):
    form = TransferForm()
    if "username" not in session:
        flash("Please log in to your account")
        return redirect('/login')

    # Get data associated with transferring funds
    if form.validate_on_submit():
        email = form.email.data
        amount = form.amount.data

        username=session["username"]
        rec_email = User.query.filter_by(email=email).first()
        if rec_email:
                sendr = User.query.filter_by(username=username).first().accounts[0]
                receivr = rec_email.accounts[0]
                
                new_txn = Transaction(amount=amount,
                                    recipient=receivr.account_no,
                                    sender=sendr.account_no,
                                    description="Intrabank Transfer")

                account1 = Account.query.get(sendr.account_no)
                account2 = Account.query.get(receivr.account_no)
                account1.account_balance = account1.account_balance - amount
                account2.account_balance = account2.account_balance + amount

                db.session.add(account1)
                db.session.add(account2)
                db.session.add(new_txn)
                db.session.commit()
                return redirect(f"/user/{username}")
        else:
                form.username.errors = ["Invalid recipient email address"]

    return render_template("transfer.html", form=form, username=username)


# ----------------- Purchase------------------------------------
# send a post request to this link using postman, insomnia or a similar tool

@app.route('/user/<username>/purchases')
def showpurchaserequests(username):
    if "username" not in session:
        flash("Please log in to your account")
        return redirect('/login')
        
    user = User.query.filter_by(username=username).first()
    purchases = Purchase.query.filter_by(user_id=user.id).all()
    return render_template("purchases.html", user=user, purchases=purchases)

@app.route('/purchase', methods=["POST"])
def listenpurchases():
    
    data = request.json
    if (data.get('username')):
        username = data.get('username')
        user = User.query.filter_by(username=username).first()
        user_id = user.id
    else:
        return "username is required"    
    
    if (data.get('vendor')):
        vendor = data.get('vendor')
    else:
        return "Vendor is required"

    if (data.get('amount')):
        amount = data.get('amount')
    else:
        return "Amount is required"

    if (data.get('description')):
        description = data.get('description')
    else:
        return "Enter a description of upto 100 characters"

    new_purchase = Purchase(user_id=user_id,
                            vendor=vendor,
                            amount=amount,
                            description=description)
    db.session.add(new_purchase)
    db.session.commit()

    return f"Request to purchase {vendor} for a price of {amount} has been sent to the buyer"

@app.route('/<purchaseid>/approve')
def approvepurchases(purchaseid):
    if "username" not in session:
        flash("Please log in to your account")
        return redirect('/login')

    username =session["username"] 
    user = User.query.filter_by(username=username).first()
    account = user.accounts[0]
    purchase = Purchase.query.get(purchaseid)
    new_txn = Transaction(amount=purchase.amount,
                          sender=account.account_no,
                          description=purchase.description + purchase.vendor)
    db.session.add(new_txn)
    db.session.commit()  
    account.account_balance = account.account_balance - purchase.amount
    db.session.delete(purchase)
    db.session.commit()  
    return redirect(f"/user/{username}/purchases")

@app.route('/<purchaseid>/del')
def delpurchases(purchaseid):
    if "username" not in session:
        flash("Please log in to your account")
        return redirect('/login')

    username =session["username"] 
    purchase = Purchase.query.get(purchaseid)
    db.session.delete(purchase)
    db.session.commit()
    return redirect(f"/user/{username}/purchases")

