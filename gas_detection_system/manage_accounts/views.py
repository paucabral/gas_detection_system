from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.db import connection
from django.contrib.auth.hashers import make_password, check_password
from operator import itemgetter

# Create your views here.
def dictfetchall(cursor): 
    "Returns all rows from a cursor as a dict" 
    desc = cursor.description 
    return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall() 
    ]

class Login(View):
    def get(self, request, *args, **kwargs):
        return render(request,template_name='manage_accounts/login.html',context={})

    def post(self, request, *args, **kwargs):
        username = request.POST["username"]
        raw_password = request.POST["password"]

        with connection.cursor() as cursor:
            sql = "SELECT*FROM accounts WHERE username = '{}'".format(username)
            cursor.execute(sql)
            try:
                result = dictfetchall(cursor)[0]
            except:
                print("Account does not exists")
                return redirect("/")    
        
        if check_password(raw_password, result['password']):
            return redirect("/home/{}".format(result['acc_id']))
        else:
            return redirect("/")

class Profile(View):
    def get(self, request, *args, **kwargs):
        acc_id = self.kwargs['acc_id']
        with connection.cursor() as cursor:
            sql = "SELECT*FROM accounts WHERE acc_id = '{}'".format(acc_id)
            cursor.execute(sql)
            acc = dictfetchall(cursor)[0]
        return render(request,template_name='manage_accounts/profile.html',context={'acc':acc, 'acc_id':acc_id})

    def post(self, request, *args, **kwargs):
        acc_id = self.kwargs['acc_id']
        username = request.POST["username"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        contact_num = request.POST["contact_num"]
        raw_password = request.POST["password"]

        hashed_password = make_password(raw_password)

        with connection.cursor() as cursor:
            cursor.execute("UPDATE accounts SET username='{}' WHERE acc_id={}".format(username, acc_id))
            cursor.execute("UPDATE accounts SET fname='{}' WHERE acc_id={}".format(fname, acc_id))
            cursor.execute("UPDATE accounts SET lname='{}' WHERE acc_id={}".format(lname, acc_id))
            cursor.execute("UPDATE accounts SET email='{}' WHERE acc_id={}".format(email, acc_id))
            cursor.execute("UPDATE accounts SET contact_num='{}' WHERE acc_id={}".format(contact_num, acc_id))
            cursor.execute("UPDATE accounts SET password='{}' WHERE acc_id={}".format(hashed_password, acc_id))
        
        return redirect("/home/{}".format(acc_id))
        

class Register(View):
    def get(self, request, *args, **kwargs):
        return render(request,template_name='manage_accounts/register.html',context={})

    def post(self, request, *args, **kwargs):
        username = request.POST["uname"]
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        contact_num = request.POST["contact_num"]
        raw_password = request.POST["password"]

        hashed_password = make_password(raw_password)

        with connection.cursor() as cursor:
            cursor.execute("SELECT*FROM accounts WHERE username = '{}'".format(username))
            accounts = dictfetchall(cursor)
            try:
                for i in accounts:
                    if i['username'] == username:
                        print('Account already exists!')
                        return redirect("/register")
                sql = 'INSERT INTO accounts(username, fname, lname, email, contact_num, password) VALUES("{}","{}","{}","{}","{}","{}")'.format(username, fname, lname, email, contact_num, hashed_password)
                cursor.execute(sql)
                return redirect("/")
            except:
                sql = 'INSERT INTO accounts(username, fname, lname, email, contact_num, password) VALUES("{}","{}","{}","{}","{}","{}")'.format(username, fname, lname, email, contact_num, hashed_password)
                cursor.execute(sql)
                return redirect("/")