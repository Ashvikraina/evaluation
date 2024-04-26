import pymongo
from flask import Flask, render_template, request, redirect, flash, session
from pymongo.mongo_client import MongoClient
import time

app=Flask('eval')

app.secret_key = b'_5#y2L"F4Q8znxec]/'

uri = "mongodb+srv://ashvik:zkodUMm4A5e5a60W@cluster0.erpzoit.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(uri, tls=True, tlsAllowInvalidCertificates=True)

db=client.evaluation

@app.route('/',methods=['GET','POST'])
def index():
    if request.method=="GET":
        return render_template('page.html')
    if request.method=="POST":
        if "sign1" in request.form:
            if db.users.find_one({"email":request.form['email']}):
                flash('Already Exists')
            else:
                doc={}
                doc['name']=request.form['name']
                doc['email']=request.form['email']
                doc['password']=request.form['password']
                doc['address']=request.form['address']
                doc['number']=request.form['number']
                doc['cart']=[]
                db.users.insert_one(doc)
                flash('Signed up')
            return redirect('/')
        if 'login1' in request.form:
            if not db.users.find_one({"email":request.form['email']}):
                print('no account created!')
                return redirect('/')
            else:
                if request.form['password'] == db.users.find_one({'email': request.form['email']})['password']:
                    session['email'] = request.form['email']
                    print("Logged in!")
                    return render_template('cart.html')
                else:
                    flash('Incorrect!')
        if 'fruit' in request.form:
            email = session.get('email')
            user = db.users.find_one({"email": email})
            for fruit, quantity in request.form.items():
                if quantity.isdigit() and int(quantity) > 0:
                    for e in range(int(quantity)):
                        user['cart'].append(fruit)
            db.users.update_one({"email": email}, {"$set": {"cart": user['cart']}})
            flash('Fruits added to cart')
            return redirect('/')
app.run(debug=True)