from models import Purchase, db, connect_db, User, Profile, Account, Transaction, Purchase
from app import app
import datetime

connect_db(app)
db.drop_all()
db.create_all()

# Users

test_1 = User.register("testuser1", "123456", "test1@gmail.com", "John", "Doe")
test_2 = User.register("testuser2", "123456", "test2@gmail.com", "Lisa", "Swann")
test_3 = User.register("testuser3", "123456", "test3@gmail.com", "Joe", "Morgan")

db.session.add(test_1)
db.session.add(test_2)
db.session.add(test_3)
db.session.commit

# Profiles
prof_1 = Profile.createprof(1,"Credit Suisse", "Analyst", "1150 West 50th Ave Vancouver BC")
prof_2 = Profile.createprof(2,"Kiewitt Corp", "Civil Eng", "1151 West 50th Ave Vancouver BC")
prof_3 = Profile.createprof(3,"Hobnobs Inc", "Biscuit-maker", "1152 West 50th Ave Vancouver BC")

db.session.add(prof_1)
db.session.add(prof_2)
db.session.add(prof_3)
db.session.commit

#Accounts

act_1 = Account.create(1)
act_2 = Account.create(2)
act_3 = Account.create(3)

db.session.add(act_1)
db.session.add(act_2)
db.session.add(act_3)
db.session.commit

# Transactions
salary1 = 4000
salary2 = 5000
salary3 = 6000 

txn_dates =[]

def createdates():
    for month in range(6,9):
        txn_dates.append(datetime.date(year=2022, month=month, day=1))
        txn_dates.append(datetime.date(year=2022, month=month, day=16))
         
createdates()
def addtxnsdb(act_no, amt):
    act = Account.query.get(act_no)
    for n in range(1, 7):
        new_txn = Transaction(amount=amt, 
                        recipient=act.account_no,
                        transaction_date=txn_dates[n-1],
                        description="Salary",
                        transaction_time=datetime.datetime.now())
        
        db.session.add(new_txn)
        db.session.commit()


addtxnsdb(1, salary1)
addtxnsdb(2, salary2)
addtxnsdb(3, salary3)

#Purchases
vendors = ['Apple', 'Samsung', 'Nike', 'Adidas', 'Godaddy', 'Loblaws']
amt = [4200.01, 1450.36, 244.99, 145.69, 25.99, 45.11]
description = ["iPhone 55", "Book2 765", "Airmax 5000", "Bounce 1000", "Domain purchase", "Groceries weekly"]

def createpurchasesreqs(id, idx):
    for n in range(idx, idx + 4):
        new_req = Purchase(user_id=id, 
                        vendor=vendors[n],
                        amount=amt[n],
                        description=description[n])
        
        db.session.add(new_req)
        db.session.commit()

createpurchasesreqs(1, 0)
createpurchasesreqs(2, 1)
createpurchasesreqs(3, 2)