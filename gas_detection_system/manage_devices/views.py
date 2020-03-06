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

class Manage(View):
    def get(self, request, *args, **kwargs):
        acc_id = self.kwargs['acc_id']
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM devices WHERE accounts_acc_id={}".format(acc_id))
            devices=dictfetchall(cursor)
        return render(request,template_name='manage_devices/manage.html',context={'devices':devices,'acc_id':acc_id})

    def post(self, request, *args, **kwargs):
        acc_id = self.kwargs['acc_id']
        device_id = request.POST["device_id"]
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM devices WHERE device_id={}".format(device_id))
        return redirect("/devices/{}/manage/".format(acc_id))

class Register(View):
    def get(self, request, *args, **kwargs):
        acc_id = self.kwargs['acc_id']
        return render(request,template_name='manage_devices/register.html',context={'acc_id':acc_id})

    def post(self, request, *args, **kwargs):
        acc_id = self.kwargs['acc_id']
        device_id = request.POST["device_id"]
        room = request.POST["room"]
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO devices VALUES({},'{}',{})".format(device_id, room, acc_id))
        return redirect("/devices/{}/manage/".format(acc_id))

        