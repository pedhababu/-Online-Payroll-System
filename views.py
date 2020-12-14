from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import User
import random
import http.client
import json
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from .models import  Emp_pay_slip,Emp_Leaves,Emp_basic_update,Hr_Data,Finance_Login,Emp_account,Emp_Data,Company,Finance_Data,Hr_Login,Emp_Login
from.forms import Hr_LoginForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import auth
# Create your views here.
def home(request):
    return render(request, 'home.html')
@login_required
def mylogin(request):
    if request.user.is_authenticated:
        qs = Company.objects.all()
        if request.user.is_hr:
            return render(request,'hr.html',{"qs":qs})
        elif request.user.is_finance:
            return render(request,'finance.html',{"qs":qs})
        elif request.user.is_emp:
            return render(request,'emp.html',{"qs":qs})
def hr_pwd_chg(request):
    res = otp_send(request)
    if res:
        return render(request, "hr_otpvalid.html")
    else:
        print("sms sending failed")
        return render(request, "hr.html")
def hr_otpvalid(request):
    reeotp=request.POST["ot"]
    print(request.session["otp"])
    if request.session["otp"]==reeotp:
        data=request.session["details"]

        hd=Hr_Data(hrid=data['hrid'],fname=data['fname'],lname=data['lname'],
                   email=data['email'],mobno=data['mobno'],comapny_id=data['cmpid'])
        hd.save()
        hrlg=Hr_Login(hrid=data['hrid'],company_id=data['cmpid'],uname=data["uname"],pwd=data["pwd"])
        hrlg.save()
        return render(request,"hr_home.html")
    else:
        return render(request, "hr_update.html")

def hr_login(request):
    if request.method == "POST":
        MyLoginForm = Hr_LoginForm(request.POST)
        if MyLoginForm.is_valid():
            un =MyLoginForm.cleaned_data['user']
            pw=MyLoginForm.cleaned_data['pwd']
            dbuser = Hr_Login.objects.filter(uname=un,pwd=pw)
            if not dbuser:
                return HttpResponse('login faild')
            else:
                for p in dbuser:
                    request.session["cmpid"] = p.company_id
                return render(request,'hr_dashbord.html',{"uname":un})
    else:
        form = Hr_LoginForm()
        return render(request,'hr_login.html',
                      {'form': form})

def emp_pwd_chg(request):
    res=otp_send(request)
    if res:
        return render(request, "emp_otpvalid.html")
    else:
        print("sms sending failed")
        return render(request, "emp.html")
def emp_otpvalid(request):
    reeotp=request.POST["ot"]
    print(reeotp)
    print(request.session["otp"])
    if request.session["otp"]==reeotp:
        data=request.session["details"]

        hd=Emp_Data(empid=data['empid'],fname=data['fname'],lname=data['lname'],
                   email=data['email'],mobno=data['mobno'],company_id=data['cmpid'])
        hd.save()
        hrlg=Emp_Login(empid=data['empid'],company_id=data['cmpid'],uname=data["uname"],pwd=data["pwd"])
        hrlg.save()
        print("rec inserted")
        User.objects.get(id=request.session.get("_auth_user_id")).delete()
        return render(request,"emp_home.html")
    else:
        return render(request, "emp_update.html")

def emp_login(request):
    if request.method == "POST":
        MyLoginForm = Hr_LoginForm(request.POST)
        if MyLoginForm.is_valid():
            un =MyLoginForm.cleaned_data['user']
            pw=MyLoginForm.cleaned_data['pwd']
            dbuser = Emp_Login.objects.filter(uname=un,pwd=pw)
            if not dbuser:
                return HttpResponse('login faild')
            else:
                for p in dbuser:
                    request.session["empid"] = p.empid
                    request.session["cmpid"] = p.company_id
                    request.session["user"]=un
                return render(request,'emp_dashbord.html',{"uname":un})
    else:
        form = Hr_LoginForm()
        return render(request,'emp_login.html',
                      {'form': form})


def accountupdate(request):
    if request.method=="GET":
        return render(request,'accountupdate.html')
    else:
        ea=Emp_account(acno=int(request.POST['accno']),
                       bankname=request.POST['bankname'],
                       ifsccode=request.POST['ifsccode'],
                       branchname=request.POST['branchname'],
                       empid=request.session['empid'],cmpid=request.session['cmpid'])
        ea.save()
        return render(request,'emp_dashbord.html')








def finance_pwd_chg(request):
    res = otp_send(request)
    if res:
        return render(request, "finance_otpvalid.html")
    else:
        print("sms sending failed")
        return render(request, "finance.html")
def finance_otpvalid(request):
    reeotp=request.POST["ot"]
    print(request.session["otp"])
    if request.session["otp"]==reeotp:
        data=request.session["details"]

        hd=Finance_Data(acid=data['acid'],fname=data['fname'],lname=data['lname'],
                   email=data['email'],mobno=data['mobno'],
                        company_id=data['cmpid'])
        hd.save()
        hrlg = Finance_Login(acid=data['acid'], company_id=data['cmpid'], uname=data["uname"], pwd=data["pwd"])
        hrlg.save()
        auth.logout(request)
        return render(request,"finance_home.html")
    else:
        return render(request, "finance_update.html")
def finance_login(request):
    if request.method == "POST":
        MyLoginForm = Hr_LoginForm(request.POST)
        if MyLoginForm.is_valid():
            un =MyLoginForm.cleaned_data['user']
            pw=MyLoginForm.cleaned_data['pwd']
            dbuser = Finance_Login.objects.filter(uname=un,pwd=pw)
            if not dbuser:
                return HttpResponse('login faild')
            else:
                rec=dbuser.get(uname=un)
                request.session["uname"]=un
                request.session["cmpid"]=rec.company_id
                return render(request,'finance_dashbord.html',{'uname':un})
    else:
        form = Hr_LoginForm()
        return render(request,'finance_login.html',
                      {'form': form})

def empdetails(request):
    emps=Emp_account.objects.filter(cmpid=request.session['cmpid'])
    return render(request,"empdetails.html",{"emps":emps})

def activate(request):
   myacno= request.GET["acno"]
   Emp_account.objects.filter(acno=myacno).update(isactivated=True)
   emps = Emp_account.objects.filter(cmpid=request.session['cmpid'])
   return render(request, "empdetails.html", {"emps": emps})


def empactive(request):
    emps = Emp_account.objects.filter(cmpid=request.session['cmpid'],isactivated=True)
    return render(request, "empactive.html", {"emps": emps})
def empbasicupdate(request):
    emps = Emp_account.objects.filter(cmpid=request.session['cmpid'],isactivated=True)
    return render(request, "empbasicupdate.html", {"emps": emps})
def basicpay(request):
    if request.method=="GET":
        empid=request.GET["empid"]
        return render(request,'basicupdate.html',{'empid':empid})
    else:
        empid1=request.POST['eid']
        bpay1=float(request.POST['bpay'])
        dbuser=Emp_Data.objects.filter(empid=empid1)
        rec=dbuser.get(empid=empid1)
        cid=rec.company_id
        e1=Emp_basic_update(empid=empid1,basicpay=bpay1,comapny_id=cid)
        e1.save()
        return render(request,'hr_dashbord.html')
def empleavesupdate(request):
    emps = Emp_basic_update.objects.filter(comapny=request.session['cmpid'])
    return render(request, "leaves_update.html", {"emps": emps})
txamt=0.0
tx1=0
def empleavesupdate1(request):
    if request.method == "GET":
        empid1 = request.GET["empid"]
        empbasic=Emp_basic_update.objects.filter(empid=empid1)
        rec = empbasic.get(empid=empid1)
        bp=rec.basicpay
        return render(request,'leaves_update1.html',{'empid':empid1,'bp':bp})
    else:
        empid1 = request.POST['eid']
        tnwd1 = int(request.POST['tnwd'])
        pl1 = int(request.POST['pl'])
        npl1 = int(request.POST['npl'])
        bp=float(request.POST['bp'])
        dbuser = Emp_Data.objects.filter(empid=empid1)
        rec = dbuser.get(empid=empid1)
        cid = rec.company_id
        e1 = Emp_Leaves(empid=empid1,basic_pay=bp,total_no_of_work_days=tnwd1,paid_leaves=pl1,non_paid_leaves=npl1, comapny_id=cid,)
        e1.save()
        a=bp/tnwd1
        twd=tnwd1-npl1
        c=a*twd
        da1=1.2*c
        hra1=0.3*bp
        pf1=0.1*bp
        pt1=200
        np=bp+da1+hra1-pf1-pt1
        asal=np*12
        global txamt
        global tx1
        if asal<250000.00:
            tx1=0
        elif asal<500000.00:

            txamt=asal-250000.00
            tx1=txamt*0.05
        elif asal<1000000.00:
            txamt=asal-500000.00
            tx1=txamt*.20+12500.00
        else:
            txamt=asal-1000000.00
            tx1=txamt*0.3+112500.00
        mtx=tx1/12
        tsal1=np-mtx
        em1 = Emp_Data.objects.filter(empid=empid1)
        rec = em1.get(empid=empid1)
        fname=rec.fname
        lname=rec.lname
        nm=fname+" "+lname
        cmp = Company.objects.filter(cmpid=cid)
        cmpi=cmp.get(cmpid=cid)
        p1=Emp_pay_slip(empid=empid1,empname=nm,basicpay=c,hra=hra1,pf=pf1,
                        pt=pt1,tax=mtx,tsal=tsal1,comapny=cmpi,da=da1)
        p1.save()
        return render(request,'hr_dashbord.html')
def viewpayslip(request):
    recs=Emp_pay_slip.objects.filter(comapny_id=request.session['cmpid'])
    return render(request,'view_payslip.html',{'recs':recs})
def displaypayslip(request):
    cmp = Emp_pay_slip.objects.filter(empid=request.session['empid'])
    dic={}
    for p in cmp:
        dic['empid']=p.empid
        dic['empname']=p.empname
        dic['basicpai']=p.basicpay
        dic['da']=p.da
        dic['hra']=p.hra
        dic['pf']=p.pf
        dic['pt']=p.pt
        dic['tax']=p.tax
        dic['tsal']=p.tsal
    return render(request,'displaypayslip.html',dic)
def downloadpayslip(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="payslip.pdf"'
    p = canvas.Canvas(response)

    cmp = Emp_pay_slip.objects.filter(empid=request.session['empid'])
    for x in cmp:
        p.drawString(100,100, "empid:"+str(x.empid))
        p.drawString(200,100, "empname:"+x.empname)
        p.drawString(300,100, "basicpay:"+str(x.basicpay))
        p.drawString(400,100, "da:"+str(x.da))
        p.drawString(500,100, "hra:"+str(x.hra))
        p.drawString(600,100, "pf:"+str(x.pf))
        p.drawString(700,100, "pt:"+str(x.pt))
        p.drawString(800,100, "tax:"+str(x.tax))
        p.drawString(900,100, "tax:"+str(x.tsal))
        p.showPage()
        p.save()

    return response
def otp_send(request):
    ot = str(random.randint(100000, 999999))
    # request.session["pwd"]=request.POST["t1"]
    mobno = request.POST["mobno"]
    temail=request.POST["email"]
    subject="transaction password"
    From_mail = settings.EMAIL_HOST_USER
    to_list = [temail]

    send_mail(subject, ot, From_mail, to_list, fail_silently=False)
    print("otp sent to email")
    request.session["details"] = request.POST
    request.session["otp"] = ot
    conn = http.client.HTTPConnection("api.msg91.com")
    payload = "{ \"sender\":\"LKSHIT\", \"route\": \"4\", \"country\": \"91\", \"sms\": [ { \"message\":\"" + ot + "\",\"to\": [ \"" + mobno + "\" ] } ] }"
    headers = {
        'authkey': "268966AWr8jk1yF5c967d25",  # PLEASE ENTER THE AUTHKEY BEFORE EXECUTING THE PROGRAM
        'content-type': "application/json"
    }

    conn.request("POST",
                 "/api/v2/sendsms?country=91&sender=&route=&mobiles=&authkey=&encrypt=&message=&flash=&unicode=&schtime=&afterminutes=&response=&campaign=",
                 payload, headers)

    data = conn.getresponse()
    res = json.loads(data.read().decode("utf-8"))
    print(res)
    if res["type"] == "success":
        return True
    else:
        return False
def leaves(request):
    return render(request,'leaves_home.html',{"uname":request.session["user"]})
def applyforleave(request):
    if request.method=="GET":
        return render(request,'leaves_dashbord.html',{"uname":request.session["user"]})
