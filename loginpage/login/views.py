from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from django.http import HttpResponse
from login.models import log
from django import forms
import pandas as pd
from django.core.files.storage import FileSystemStorage
import xlrd

# Create your views here.
class loginpage(TemplateView):
    template_name = 'loginpage.html'

class adminpagefunc(TemplateView):
    template_name = 'adminlogin.html'

def uploadpage(request):
    #admin name say admin_name
    #admin password say admin@123
    name = request.POST['adminname']
    password = request.POST['adminpassword']
    if(name == "admin_name" and password == "admin@123" ):
        return render(request, 'adminupload.html')
    else:
        return HttpResponse("Admin could not login")


def data(request):
    user = str(request.POST['UserName'])
    password = str(request.POST['Password'])
    try:
        t = log.objects.get(studentcode = user)
        if(str(t.dob) == password):
            return render(request,'loggedinpage.html',{'code': t.studentcode , 'name': t.studentname , 'admin': t.adminno , 'class' : t.classname ,
            'section': t.section , 'result' : t.result})
        else:
            return render(request,"failed.html ")
    except:
        return render(request,"failed.html")


def uploading(request):
    upload_file = request.FILES['excel']
    file = FileSystemStorage()
    file.save(upload_file.name,upload_file)
    name = upload_file.name
    path =  'media\\'+ name
    wb = xlrd.open_workbook(path)
    sheet = wb.sheet_by_index(0)
    sheet.cell_value(0, 0)
    total_attribute = ' '.join(sheet.row_values(0)).split()
    print(total_attribute)
    for i in range(1,sheet.nrows):
        data = sheet.row_values(i)
        data = [i for i in data if i!= '']
        print(total_attribute,data)
        if(len(total_attribute) == len(data)):
            log_obj = log(
                studentcode = data[0],
                adminno = data[1],
                studentname = data[2],
                classname = data[3],
                section = data[4],
                dob = data[5],
                result = data[6],
            )
            log_obj.save()
            print(data)
    return HttpResponse("data upload successfully")
