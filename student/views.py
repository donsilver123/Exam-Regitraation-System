from eadmin.models import Course, Enrollments, Exam
from examiner.models import Results
from home.models import Applicant
from django.contrib.auth import logout as django_logout
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password, check_password
from datetime import date
from django.db import connection
from io import BytesIO


# from django.conf import settings
from django.http import HttpResponse
# from django.core.files.base import ContentFile
#
# from django.template import Context
from django.template.loader import get_template
# import datetime
# from xhtml2pdf import pisa
# from django.template.loader import get_template
#
# from xhtml2pdf import pisa


# Create your views here.


def shome(request):
    applicant = Applicant.objects.get(id=request.session['id'])
    rno = applicant.reg_no
    courses = Course.objects.all()
    examobj = Enrollments.objects.filter(reg_no=rno)
    request.session['examid'] ='EXCS102'
    #examobj = Exam.objects.filter(examdate=date.today())
    return render(request, 'student/shomepage.html', {'objs': courses})

def hallticket(request):
    applicant = Applicant.objects.get(id=request.session['id'])
    rno = applicant.reg_no
    fut_id = Exam.objects.filter(examdate__gt=date.today())
    fut_exam = Enrollments.objects.filter(id=rno, exam_id__examdate__gt=date.today())


        #fut_exam.objects.filter(examdate__gt=date.today())
        #cursor = connection.cursor()
        #cursor.execute("select * from Enrollments where Enrollments.id=rno and Enrollments.examid.examdate<SYSDATE")
        #fut_exam = cursor.fetchall()
    return render(request, 'student/hallticket.html', {'objs': fut_exam})


def profile(request):
    obj = Applicant.objects.get(id=request.session.get('id'))
    rno = obj.reg_no
    if request.method == 'POST':
        uname = request.POST["uname"]
        mno = request.POST["phno"]
        email = request.POST["email"]

        if len(uname) == 0 or len(mno) == 0 or len(email) == 0:
            msg = 'Please enter all the fields'
        elif Applicant.objects.filter(reg_no=reg_no).exists() and email != obj.email:
            msg = 'Email Id already exists'
        elif len(mno) < 10:
            msg = 'Please enter a valid Mobile No'
        elif Applicant.objects.filter(mobile_no=mno).exists() and mno != obj.mobile_no:
            msg = 'Mobile No already exists'
        else:
            msg = 'Your profile has been sucessfully updated'
            obj.email = email
            obj.mobile_no = mno
            obj.username = uname
            obj.save()
        return render(request, 'student/profile.html', {'msg': msg, 'obj': rno})
    else:
        return render(request, 'student/profile.html', {'obj': rno})

def password(request):
    if request.method == 'POST':
        oldpass = request.POST["opass"]
        npass = request.POST["npass"]
        rnpass = request.POST["rnpass"]
        rno = request.session['id']
        obj = Applicant.objects.get(id=rno)
        epass = obj.password
        if len(npass) == 0 or len(oldpass) == 0 or len(rnpass) == 0:
            msg = 'Please enter all the fields'
        elif not check_password(oldpass, epass):
            msg = 'Please enter the existing password'
        elif npass != rnpass:
            msg = 'Passwords do not match'
        else:
            unpass = make_password(npass)
            msg = 'Your password has been updated'
            obj.password = unpass
            obj.save()
        return render(request, 'student/password.html', {'msg': msg})
    else:
        return render(request, 'student/password.html', None)



def logout(request):
    django_logout(request)
    #return redirect('/ExamReg/')
    return render(request,'home\index.html', {'msg': 'You have sucessfully logged out!'})


def examregister(request):
    id = request.session['id']
    obj = Applicant.objects.get(id=id)
    obj1 = Exam.objects.filter(examdate__gt=date.today())

    if request.method == 'POST':
          uname = request.POST["uname"]
          reg_no = request.POST["reg_no"]
          mobile_no = request.POST["phno"]
          email = request.POST["email"]
          eid = request.POST["eid"]
          pay_ref = request.FILES["feefile"]

          rowcnt = Exam.objects.filter(examdate__gt=date.today(), examid=eid).count()
          if len(uname) == 0 or len(id) == 0 or len(mobile_no) == 0 or len(email) == 0 or len(eid) == 0:
             msg = 'Please Enter all the details'
          elif id != rno or obj.username != uname or obj.mobile_no != mobile_no or obj.email != email:
             msg = 'Please enter valid details'
          elif Enrollments.objects.filter(examid=eid, id=Applicant.objects.get(id=id)).exists():
              msg = 'Already registered'
          elif rowcnt == 0:
              msg = 'Please choose a valid ExamId'
          else:
               eobj=Exam.objects.get(examid=eid)
               #print(eobj.examid + eobj.examname)
               Enrollments.objects.create(id=Applicant.objects.get(id=id),
                                          examid=Exam.objects.get(examid=eid), status='pending', paymentref=pay_ref)
              #eobj.save()
               msg = 'Sucessfully Registered'

          #elif not Exam.

          #if flag == 0:
           # rno = Applicant.objects.get(id=request.session['id'])
            #cid = Course.objects.get(coursecode=course_id)
            #obj = Enrollments(id=rno, coursecode=cid, status='pending', paymentref=pay_ref)
            #obj.save()

          return render(request, 'student/exrg.html', {'msg': msg, 'objs': obj1})
    else:
          return render(request, 'student/exrg.html', {'objs': obj1})





def mycourses(request):
    return render(request, 'student/mycourses.html', None)

def pexam(request):
    id = request.session['id']
    obj=Results.objects.filter(id=id,examid__examdate__lt=date.today())
    return render(request, 'pastresult.html', {'obj': obj})

def examht(request,parameter):

        #print(parameter)
        id = request.session['id']
        obj = Applicant.objects.get(id=id)
        obj1 = Exam.objects.get(examid=parameter)
        return render(request, 'student/examhticket.html', {'robj': obj,'eobj': obj1})

