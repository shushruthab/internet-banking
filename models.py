from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType
from accountnumber import account
import datetime

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)

# Models go below
class User(db.Model):
    """Create Users model to add users to database"""
    __tablename__ = "users"

    def __repr__(self):
        p = self
        return f"<User username={p.username} User_firstname={p.first_name} User_lastname={p.last_name}"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True,
                    nullable=False)

    username = db.Column(db.String(200),
                    unique=True,
                    nullable=False)

    password = db.Column(db.Text,
                        nullable=False)

    email = db.Column(EmailType,
                        unique=True,
                        nullable=False)

    first_name = db.Column(db.String(100),
                        nullable=False)

    last_name = db.Column(db.String(100),
                        nullable=False)

    @classmethod
    def register(cls, username, pwd, email, first_name, last_name):
        hashed = bcrypt.generate_password_hash(pwd)
        hashed_utf8 = hashed.decode("utf8")

        return cls(username=username, 
                password=hashed_utf8,
                email = email,
                first_name=first_name,
                last_name=last_name)
    
    @classmethod
    def authenticate(cls, username, pwd):
        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, pwd):
            return u 
        else:
            return False
            
class Profile(db.Model):
    """Create Profiles associated with username"""
    __tablename__ = "profiles"

    def __repr__(self):
        p = self
        return f"<Profile user_id={p.user_id} Profile_company={p.company} Profile_role={p.role}"

    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id'),
                    primary_key=True)

    account_created_date = db.Column(db.DateTime,
                                    nullable=False,
                                    default=datetime.date.today())

    address = db.Column(db.Text,
                        nullable=False)

    company = db.Column(db.Text,
                        nullable=False)

    role = db.Column(db.Text,
                        nullable=False)

    user = db.relationship('User', backref="profile")

    @classmethod
    def createprof(cls, userid):
        prof = Profile()
        return cls(company="XYZ",
                user_id=userid, 
                role="xyz",
                address="xyz")

class Account(db.Model):
    """Create Accounts associated with username"""
    __tablename__ = "accounts"

    def __repr__(self):
        p = self
        return f"<Account Accountno={p.account_no} Account_user_id={p.user_id}"

    account_no = db.Column(db.String(16),
                    primary_key=True,
                    unique=True,
                    nullable=False)
    
    account_balance = db.Column(db.Float,
                                default= 0.00)

    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id'))

    user = db.relationship('User', backref="accounts")

    @classmethod
    def create(cls, userid):
        num = account()
        return cls(account_no=num, 
                user_id=userid,
                account_balance=0)
    
class Purchase (db.Model):
    """Create table for unapproved purchases"""
    __tablename__ = "purchases"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True,
                    nullable=False)

    user_id = db.Column(db.Integer,
                    db.ForeignKey('users.id'))
    
    vendor = db.Column(db.Text)

    amount = db.Column(db.Float, 
                        nullable=False)

    description = db.Column(db.Text)     

class Transaction(db.Model):
    """Create Transactions associated with accounts"""
    __tablename__ = "transactions"

    def __repr__(self):
        p = self
        return f"<Transaction id={p.id} Transaction_amount={p.amount} Transaction_success={p.success}"

    id = db.Column(db.Integer,
                    primary_key=True,
                    autoincrement=True,
                    nullable=False)

    amount = db.Column(db.Float,
                        nullable=False)

    recipient = db.Column(db.String(16),
                            db.ForeignKey('accounts.account_no'),
                            nullable=True)

    transaction_date = db.Column(db.DateTime, 
                            nullable=False,
                            default=datetime.date.today())  

    transaction_time = db.Column(db.DateTime,
                                nullable=False,
                                default = datetime.datetime.now())    

    sender = db.Column(db.String(16),
                        db.ForeignKey('accounts.account_no'),
                        nullable=True)

    description = db.Column(db.Text)

    sender_acc = db.relationship("Account", foreign_keys=[sender])
    recipient_acc = db.relationship("Account", foreign_keys=[recipient])




  
            
    
    
