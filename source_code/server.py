'''
Created on Apr 20, 2024

'''

from flask import Flask, flash, render_template, redirect, url_for, request, session
from module.database import Database
import pdb


app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = Database()

@app.route('/')
def index():
    data = db.read(None)

    return render_template('index.html', data = data)

@app.route('/add/')
def add():
    return render_template('add.html')

@app.route('/addaccount', methods = ['POST', 'GET'])
def addaccount():
    if request.method == 'POST' and request.form['save']:
        print(request.form)
        if db.insert(request.form):
            flash("A new bank account has been added")
        else:
            flash("A new bank account can not be added")

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/update/<int:id>/')
def update(id):
    data = db.read(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['update'] = id
        return render_template('update.html', data = data)

@app.route('/updateaccount', methods = ['POST'])
def updateaccount():
    if request.method == 'POST' and request.form['update']:

        if db.update(session['update'], request.form):
            flash('A bank account has been updated')

        else:
            flash('A bank account can not be updated')

        session.pop('update', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
@app.route('/deposit/<int:id>/')
def deposit(id):
    data = db.read(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['deposit'] = id
        return render_template('deposit.html', data = data)
    
@app.route('/depositamount', methods = ['POST'])
def depositamount():
    if request.method == 'POST' and request.form['deposit']:
        
        if db.deposit(session['deposit'], request.form):
            if float(request.form['deposit_amount']) > float(200000.00):
                flash('Deposit amount should not be more than 200000.00')
            else:
                flash('Amount has been deposited to the bank account')
        else:
            flash('Amount has not been deposited to the bank account')

        session.pop('deposit', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))
    
@app.route('/withdraw/<int:id>/')
def withdraw(id):
    data = db.read(id)

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['withdraw'] = id
        return render_template('withdraw.html', data = data)
    
@app.route('/withdrawamount', methods = ['POST'])
def withdrawamount():
    if request.method == 'POST' and request.form['withdraw']:
        
        if db.withdraw(session['withdraw'], request.form):
            if float(request.form['withdraw_amount']) > float(request.form['balance']):
                flash("Your account doesn't have sufficient balance to withdraw")
            else:
                flash('Amount has been withdrawn from the bank account')
        else:
            flash('Amount has not been withdrawn from the bank account')

        session.pop('withdraw', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.route('/delete/<int:id>/')
def delete(id):
    data = db.read(id);

    if len(data) == 0:
        return redirect(url_for('index'))
    else:
        session['delete'] = id
        return render_template('delete.html', data = data)

@app.route('/deleteaccount', methods = ['POST'])
def deleteaccount():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('A bank account has been deleted')

        else:
            flash('A bank account can not be deleted')

        session.pop('delete', None)

        return redirect(url_for('index'))
    else:
        return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')

if __name__ == '__main__':
    app.run(debug=True)
