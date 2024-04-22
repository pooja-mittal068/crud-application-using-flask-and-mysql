'''
Created on Apr 20, 2024

'''

import pymysql
import random
import pdb


class Database:
    def connect(self):

        return pymysql.connect(host="localhost", user="root", password="123456", database="bank_db", charset='utf8mb4')

    def read(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            if id == None:
                cursor.execute("SELECT * FROM bank_account order by first_name asc")
            else:
                cursor.execute(
                    "SELECT * FROM bank_account where id = %s order by first_name asc", (id,))

            return cursor.fetchall()
        except:
            return ()
        finally:
            con.close()

    def insert(self, data):
        con = Database.connect(self)
        cursor = con.cursor()
        try:
            account_number = random.randint(1000000000000000,9999999999999999)
            cursor.execute("INSERT INTO bank_account(first_name,last_name,email,phone,age,gender,dob,account_number,balance) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                           (data['first_name'], data['last_name'], data['email'],data['phone'],data['age'],data['gender'],data['dob'],account_number,data['balance']))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def update(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("UPDATE bank_account set first_name = %s, last_name = %s, email = %s, phone = %s, age = %s, gender = %s, dob = %s, account_number = %s, balance = %s where id = %s",
                           (data['first_name'], data['last_name'], data['email'],data['phone'],data['age'],data['gender'],data['dob'],data['account_number'],data['balance'], id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def deposit(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            if float(data['deposit_amount']) < float(200000.00):
                total_balance = float(data['deposit_amount']) + float(data['balance'])
            else:
                total_balance = float(data['balance'])
            
            cursor.execute("UPDATE bank_account set balance = %s where id = %s",
                           (total_balance, id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def withdraw(self, id, data):
        con = Database.connect(self)
        cursor = con.cursor()
        
        try:
            if float(data['withdraw_amount']) < float(data['balance']):
                total_balance = float(data['balance']) - float(data['withdraw_amount'])
            else:
                total_balance = float(data['balance'])
            cursor.execute("UPDATE bank_account set balance = %s where id = %s",
                           (total_balance, id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()

    def delete(self, id):
        con = Database.connect(self)
        cursor = con.cursor()

        try:
            cursor.execute("DELETE FROM bank_account where id = %s", (id,))
            con.commit()

            return True
        except:
            con.rollback()

            return False
        finally:
            con.close()
