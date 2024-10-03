"""Emp_proj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from Emp_App import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name="index"),
    path('login_page',views.login_page),
    path('logout',views.logout),
    
    path('admin_index',views.admin_index),
    path('emp_details',views.emp_details),
    path('admin_salary',views.admin_salary),
    path('emp_details_ins',views.emp_details_ins),
    path('emp_table',views.emp_table),
    path('emp_table1',views.emp_table1),
    path('delete',views.delete),
    path('edit',views.edit),
    path('update',views.update),
    path('admin_emp_salary',views.admin_emp_salary),
    path('admin_emp_salary_p',views.admin_emp_salary_p),
    path('admin_emp_salary_c',views.admin_emp_salary_c),
    path('admin_edit_salary',views.admin_edit_salary),
    path('add_salary',views.add_salary),
    
    path('emp_index',views.emp_index),
    path('payslip',views.payslip),
    path('p_slip/<str:month>',views.GeneratePdf.as_view(),name="p_slip"),
    path('emp_payslip',views.emp_payslip),
    
    path('finance_index',views.finance_index),
    path('f_salary',views.f_salary),
    path('f_emp_salary',views.f_emp_salary),
    path('f_emp_salary1',views.f_emp_salary1),
    path('f_edit_salary',views.f_edit_salary),
    path('f_appr_salary',views.f_appr_salary),
   
]
