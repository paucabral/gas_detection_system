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

class Home(View):
    def get(self, request, *args, **kwargs):
        acc_id = self.kwargs['acc_id']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM notifications WHERE accounts_acc_id={} ORDER BY time DESC LIMIT 5".format(acc_id))
            notifs=dictfetchall(cursor)
            cursor.execute("SELECT * FROM accounts WHERE acc_id={}".format(acc_id))
            acc=dictfetchall(cursor)[0]

        return render(request,template_name='notifs/home.html',context={'notifs':notifs, 'acc':acc, 'acc_id':acc_id})

    def post(self, request, *args, **kwargs):
        pass

class Notifs(View):
    def get(self, request, *args, **kwargs):
        acc_id = self.kwargs['acc_id']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM notifications WHERE accounts_acc_id={} ORDER BY time DESC LIMIT 5".format(acc_id))
            notifs=dictfetchall(cursor)
            cursor.execute("SELECT * FROM accounts WHERE acc_id={}".format(acc_id))
            acc=dictfetchall(cursor)[0]

        return render(request,template_name='notifs/notifs.html',context={'notifs':notifs, 'acc':acc, 'acc_id':acc_id})

    def post(self, request, *args, **kwargs):
        pass

class Logs(View):
    def get(self, request, *args, **kwargs):
        acc_id = self.kwargs['acc_id']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM notifications WHERE accounts_acc_id={} ORDER BY time DESC".format(acc_id))
            notifs=dictfetchall(cursor)
            cursor.execute("SELECT * FROM accounts WHERE acc_id={}".format(acc_id))
            acc=dictfetchall(cursor)[0]

        return render(request,template_name='notifs/logs.html',context={'notifs':notifs, 'acc':acc, 'acc_id':acc_id})

    def post(self, request, *args, **kwargs):
        pass