from django.shortcuts import render,redirect
from .models import Person_Details,Salary,User
from django.http import HttpResponse,JsonResponse
from django.conf import settings
from django.core.mail import send_mail
from django.template import loader
import json
from calendar import monthrange
from Emp_proj.u import render_to_pdf 
from django.views.generic import View
from operator import itemgetter
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

# Create your views here.

def index(request):
    return render(request,'auth/login.html')

def login_page(request):
    if request.method == "POST": 
        try:
            pwd=request.POST['password']
            user=request.POST['name']
            data=authenticate(request,username=user,password=pwd)
            data1=User.objects.get(username=user)
            request.session['username']=data1.username                       
            request.session['role']=data1.role                        
            request.session['empid']=data1.emp_id                        
            if data is not None:
                if data1.role == "admin":  
                    return redirect('/admin_index')
                elif data1.role == "user":            
                    return redirect('/emp_index')
                elif data1.role == "finance":            
                    return redirect('/finance_index')
                else:
                    return render(request,'auth/login.html') 
            else:
                  return render(request,'auth/login.html')   
        except User.DoesNotExist as e:
             return render(request,'auth/login.html')           
    return render(request,'auth/login.html')

def logout(request):
    del request.session['role']
    return redirect('/')

#admin_views
# @login_required
def admin_index(request):  
    data=Person_Details.objects.filter().count()
    data1=Person_Details.objects.filter(role="user").count()
    data2=Person_Details.objects.filter(role="finance").count()
    return render(request,'auth/admin_index.html',{'data':data,'data1':data1,'data2':data2})
    
 
def emp_details(request):
    data=Person_Details.objects.all().values('role')
    res=list(map(itemgetter('role'),data))
    d=tuple(set(res))
    return render(request,'auth/emp_details.html',{'d':d}) 
 
def admin_salary(request):
    return render(request,'auth/admin_salary.html')

def emp_details_ins(request):
      try:        
        data=Person_Details.objects.create(name=request.POST['name'],emp_id=request.POST['empid'],email=request.POST['email'],role=request.POST['role'],
        ctc=request.POST['ctc'],doj=request.POST['doj'])
        User.objects.create(username=request.POST['name'],password=make_password(request.POST['empid']),role=request.POST['role'],emp_id=request.POST['empid'])                      
        if not data.save():
            subject = 'Login Credentials'
            message = f'Hi{data.name},'
            email_from = settings.EMAIL_HOST_USER
            recipient_list =[data.email]
            html_message = loader.render_to_string(
                'auth/loginmail.html',
                {
                    'user_name': data.name,
                    'subject'  : data.emp_id
                    
                }
            )
            send_mail( subject, message, email_from, recipient_list,fail_silently=True,html_message=html_message )
            msg="vaild" 
        else:
            msg="invaild"             
        return HttpResponse(json.dumps(msg), content_type="application/json")      
      except:
           return render(request,'auth/emp_details.html')
       
def emp_table(request):  
    role=request.GET.get('role')
    if role=="All":
        result_list = list(Person_Details.objects.all()\
        .values('id','name', 'email','role','emp_id','ctc','doj'))
        return JsonResponse(result_list, safe=False)
    else:
        result_list = list(Person_Details.objects.filter(role=role)\
            .values('id','name', 'email','role','emp_id','ctc','doj'))
        return JsonResponse(result_list, safe=False)

def emp_table1(request): 
    result_list = list(Person_Details.objects.all()\
        .values('id','name', 'email','role','emp_id','ctc','doj'))
    return JsonResponse(result_list, safe=False)

def delete(request):
    id1 = request.GET.get('emp_id', None)
    Person_Details.objects.get(emp_id=id1).delete()
    User.objects.get(emp_id=id1).delete()
    data = {
        'deleted': True
    }
    return JsonResponse(data)

def edit(request):
    id1 = request.GET.get('emp_id', None)
    obj=Person_Details.objects.get(emp_id=id1)  
    user = {'id':obj.id,'name':obj.name,'empid':obj.emp_id, 'email':obj.email, 'role':obj.role,'ctc':obj.ctc,'doj':obj.doj,}
    data = {
        'user': user
    }
    return JsonResponse(data) 

def update(request):
    try:     
        id=request.POST.get('id1')       
        data=Person_Details.objects.get(emp_id=id)
        data.name=request.POST.get('name1')
        data.emp_id=request.POST.get('empid1')
        data.email=request.POST.get('email1')
        data.role=request.POST.get('role1')
        data.ctc=request.POST.get('ctc1')
        data.doj=request.POST.get('doj1')
        data.save()
        data1=User.objects.get(emp_id=id)
        data1.username=request.POST.get('name1')
        data1.role=request.POST.get('role1')
        data1.emp_id=request.POST.get('empid1')
        data1.save()                    
        if not data.save():
            msg="vaild" 
        else:
            msg="invaild"             
        return HttpResponse(json.dumps(msg), content_type="application/json")      
    except:
        return render(request,'auth/emp_details.html')
    
def admin_emp_salary(request):
    m=request.GET.get('month')
    d1=Salary.objects.filter(month=m).count()
    if d1 == 0:
        queryset =list(Person_Details.objects.all().values('id','emp_id','name','ctc'))           
    else:
        queryset1 =Salary.objects.select_related('sal_id_id').filter(month=m).values('id','emp_id','name','ctc')
        res=list(map(itemgetter('emp_id'),queryset1))
        queryset =list(Person_Details.objects.exclude(emp_id__in=res).values('id','emp_id','name','ctc'))       
    return JsonResponse(queryset,safe=False)

def admin_emp_salary_p(request):
    m=request.GET.get('month')
    d1=list(Salary.objects.filter(status="pending",month=m).values('id','emp_id','name','ctc'))       
    return JsonResponse(d1,safe=False)

def admin_emp_salary_c(request):
    m=request.GET.get('month')
    d1=list(Salary.objects.filter(status="completed",month=m).values('id','emp_id','name','ctc'))       
    return JsonResponse(d1,safe=False)

def admin_edit_salary(request):
    id = request.GET.get('id', None)
    m=request.GET.get('month').split('-')
    year=m[0]
    month=m[1]    
    obj = Person_Details.objects.get(id=id) 
    m1=obj.ctc
    m=round(int(m1)/12)
    m3=monthrange(int(year),int(month))[1]
    day_salary=float(int(m)/25)
    data = {'id':obj.id,'name':obj.name,'emp_id':obj.emp_id, 'ctc':obj.ctc,'mnth_ctc':m,'day_salary':day_salary,'sal_id_id':obj.id} 
    return JsonResponse(data)

def add_salary(request):
    try:
        data=Salary.objects.create(name=request.POST['name'],emp_id=request.POST['empid'],ctc=request.POST['ctc'],month_ctc=request.POST['mnth_ctc'],month=request.POST['mnth'],day_salary=request.POST['day_salry'],present_days=request.POST['pres_days'],net_salary=request.POST['net_salry'],status="pending",sal_id_id=request.POST['id'])
        if not data.save():
            msg="vaild" 
        else:
            msg="invaild"            
        return HttpResponse(json.dumps(msg), content_type="application/json")      
    except:
        return render(request,'auth/admin_salary.html')
    
#emp_Views        
def emp_index(request):   
    return render(request,'auth/emp_index.html')

def payslip(request):
    empid=request.session.get('empid')
    d=Salary.objects.filter(emp_id=empid,status="completed").values('month')
    res=list(map(itemgetter('month'),d))
    return render(request,'auth/payslip.html',{'d':res})   

class GeneratePdf(View):
    def get(self,request,month):
        empid=request.session.get('empid')
        obj=Salary.objects.get(emp_id=empid,status="completed",month=month)
        obj1=Person_Details.objects.get(emp_id=empid)
        lpay=25-int(obj.present_days)
        net=obj.net_salary
        net1=round(float(net))
        deduc=int(obj.month_ctc)-int(net1)
        data = {'jdate':obj1.doj,'name':obj.name,'emp_id':obj.emp_id,'pday':obj.present_days,'net_sal':net1,'m_ctc':obj.month_ctc,'month':month,'lpay':lpay,'deduc':deduc} 
        pdf = render_to_pdf('auth/p_slip_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')

def emp_payslip(request):
    try:
        empid=request.session.get('empid')
        month=request.POST.get('month')
        obj=Salary.objects.get(emp_id=empid,status="completed",month=month)
        obj1=Person_Details.objects.get(emp_id=empid)
        data={'jdate':obj1.doj,'name':obj.name,'emp_id':obj.emp_id,'pday':obj.present_days,'net_sal':obj.net_salary,'m_ctc':obj.month_ctc,'month':obj.month} 
        user={'user':data}
        return JsonResponse(user,safe=False)
    except Salary.DoesNotExist as e:
        user={'user':"invaild"}
        return JsonResponse(user,safe=False)
        

# #finance_views
def finance_index(request):   
    return render(request,'auth/finance_index.html')

def f_salary(request):   
    return render(request,'auth/finance_salary.html')

def f_emp_salary(request): 
    m=request.POST.get('month')
    queryset =list(Salary.objects.filter(status="pending",month=m).values('id','emp_id','name','ctc','month_ctc','month','day_salary','present_days','net_salary','status'))     
    return JsonResponse(queryset,safe=False)

def f_emp_salary1(request): 
    m=request.POST.get('month')
    queryset =list(Salary.objects.filter(status="completed",month=m).values('id','emp_id','name','ctc','month_ctc','month','day_salary','present_days','net_salary','status'))     
    return JsonResponse(queryset,safe=False)
 
def f_edit_salary(request):
    id = request.GET.get('id', None)
    obj = Salary.objects.get(id=id) 
    data = {'id':obj.id,'emp_id':obj.emp_id,'net_salary':obj.net_salary,'present_days':obj.present_days} 
    return JsonResponse(data)

def f_appr_salary(request):
    try:  
        id=request.POST.get('id')
        empid=request.POST.get('empid')   
        data1=Salary.objects.get(id=id)
        data2=Person_Details.objects.get(emp_id=empid)
        data1.status="completed"
        data1.save()                     
        if not data1.save():
            subject = 'Payslip-Released'
            message = f'hi{data1.name},'
            msg=f'Your payslip for the month of {data1.month} has been released.'
            email_from = settings.EMAIL_HOST_USER
            recipient_list =[data2.email]
            html_message = loader.render_to_string(
                'auth/sendmail.html',
                {
                    'user_name':data1.name,
                    'subject'  :'Your payslip for the month of  '+ data1.month+' has been released.'
                    
                }
            )
            send_mail(subject,message+msg, email_from, recipient_list,fail_silently=True,html_message=html_message)
            msg="vaild" 
        else:
            msg="invaild"             
        return HttpResponse(json.dumps(msg), content_type="application/json")      
    except:
        return render(request,'auth/emp_details.html')    