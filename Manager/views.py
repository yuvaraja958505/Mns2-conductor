from django.core.mail import send_mail
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import messages
import random


from Manganese_Process.models import *
from Client.models import *
from App_Integration.models import *
from Porosity_Analysis.models import *


# MANAGER HOME PAGE
def manager_home_page(request):
    return render(request, 'Manager/manager_home.html')


# MANAGER LOGIN PAGE
def manager_login_page(request):
    if request.method =='POST':
        useremail = request.POST['useremail']
        password = request.POST['password']

        if useremail == "admin@gmail.com" and password == "admin":
            request.session['administrator'] = 'admin@gmail.com'
            messages.success(request, "Manager  logged in successfully")
            return redirect("/manager/manager_home/")

        elif useremail != "admin@gmail.com" and password == "admin":
            messages.error(request, "You have entered invalid email")
            return redirect('/manager/manager_login/')

        elif useremail == "admin@gmail.com" and password != "admin":
            messages.error(request, "You have entered wrong password")
            return redirect('/manager/manager_login/')

        elif useremail != "admin@gmail.com" and password != "admin":
            messages.error(request, "Invalid Credentials kinldy check")
            return redirect('/manager/manager_login/')

    return render(request,'Manager/login.html')


# MANAGER LOGOUT

def manager_login_out(request):
    if 'administrator' in request.session:
        print('If Block ')
        del request.session['administrator']
        messages.success(request, "Manager logged out successfully")
    else:
        print('Else Block')
        messages.info(request, "No user is currently logged in")

    return redirect('/')






# CLIENT LOGIN APPROVAL PAGE

def mg_app_login_client_view(request):
    datas = Client_register.objects.all()
    return render(request,'Manager/app_login_client.html',{'datas':datas})



def client_lg_approve_btn(request,id):
    if 'administrator' in request.session:
        values=Client_register.objects.get(id=id)
        values.cl_admin_lg=True #
        a = "CLI-"
        b = random.randint(1000,2000)
        c = str(a) + str(b)
        print(c)
        values.consumer_id=c
        values.save()
        messages.success(request,"Client details are verified and  approved, Client ID Genreated")
        return redirect("/manager/mg_app_login_client/")
    else:
        return redirect("/mg_app_login_client/")



def client_lg_reject_btn(request,id):
    if 'administrator' in request.session:
        values = Client_register.objects.get(id=id)
        values.delete()
        messages.success(request, "Client details are analyzed and access is denied")
        return redirect("/manager/mg_app_login_client/")
    else:
        return redirect("/manager/mg_app_login_client/")



 # **************

#  Manganese Page VIEW APPROVAl REJECT

def mg_app_login_mang_view(request):
    datas = Manganese_register.objects.all()
    return render(request,'Manager/app_login_manganese.html',{'datas':datas})




def manganese_login_approval(request,id):
    if 'administrator' in request.session:
        values=Manganese_register.objects.get(id=id)
        values.mg_admin_lg=True
        values.save()
        messages.success(request,"Supplier details are verified and  approved")
        return redirect("/manager/mg_app_login_manganese/")
    else:
        return redirect("/manager/mg_app_login_manganese/")


def manganese_login_reject(request,id):
    if 'administrator' in request.session:
        values = Manganese_register.objects.get(id=id)
        values.delete()
        messages.success(request, "Manganese details are analyzed and access is denied")
        return redirect("/manager/mg_app_login_manganese/")
    else:
        return redirect("/manager/mg_app_login_manganese/")






# APPLICANT VIEW APPROVAL REJECT

def mg_app_login_application_view(request):
    datas = Application_register.objects.all()
    return render(request,'Manager/app_login_application.html',{'datas':datas})




def application_login_approval(request,id):
    if 'administrator' in request.session:
        values=Application_register.objects.get(id=id)
        values.app_admin_lg=True
        values.save()
        messages.success(request,"Applicant details are verified and  approved")
        return redirect("/manager/mg_app_login_application/")
    else:
        return redirect("/manager/mg_app_login_application/")


def application_login_reject(request,id):
    if 'administrator' in request.session:
        values = Application_register.objects.get(id=id)
        values.delete()
        messages.success(request, "Applicant details are analyzed and access is denied")
        return redirect("/manager/mg_app_login_application/")
    else:
        return redirect("/manager/mg_app_login_application/")






# POROSITY VIEW APPROVE DENY


def mg_app_login_porosity_view(request):
    datas = Porosity_register.objects.all()
    return render(request,'Manager/app_login_porosity.html',{'datas':datas})





def porosity_login_approval(request,id):
    if 'administrator' in request.session:
        values=Porosity_register.objects.get(id=id)
        values.por_admin_lg=True
        values.save()
        messages.success(request,"Porosity Team details are verified and approved")
        return redirect("/manager/mg_app_login_porosity/")
    else:
        return redirect("/manager/mg_app_login_porosity/")


def porosity_login_reject(request,id):
    if 'administrator' in request.session:
        values = Porosity_register.objects.get(id=id)
        values.delete()
        messages.success(request, "Porosity Team details are analyzed and access is denied")
        return redirect("/manager/mg_app_login_porosity/")
    else:
        return redirect("/manager/mg_app_login_porosity/")




##### CURRENTLY WORKING ###



# MANGANESE PROCESSED REPORT (3 VIEWS )


def mg_view_report(request):
    client_orders = Client_orders.objects.exclude(manganese_Comp__isnull=True)
    return render(request, 'Manager/mang_final_report_view.html', {'client_orders': client_orders})






def mg_view_report_mganalysis(request,id):
    mg_calculations = Client_orders.objects.get(id=id)
    return render(request, 'Manager/mang_final_report_mganalysis.html', {'mg_calculations': mg_calculations})



def mg_final_report_approve(request,id):
    final = Client_orders.objects.get(id=id)
    final.mang_admin_approve = True
    final.save()
    messages.success(request,'Successfully Manganese Team Report Approved By Manager')
    return redirect('/manager/mg_view_report/')





# APP INTEGRATION VIEW


def app_view_report(request):
    client_orders = Client_orders.objects.exclude(app_process=False)
    return render(request, 'Manager/app_final_report_view.html', {'client_orders': client_orders})



def app_view_Component(request,id):
    client_orders = Client_orders.objects.get(id=id)
    product = client_orders.product
    components = Components_required.objects.filter(product=product)
    return render(request, 'Manager/manager_final_component.html', {'components': components})


def app_final_report_approve(request,id):
    client_orders = Client_orders.objects.get(id=id)
    client_orders.app_admin_approve =True
    client_orders.save()
    messages.success(request,'Integration Report Approved by Manager')
    return redirect('/manager/app_view_report/')





# POROSITY TEAM REPORT VIEW AND APPROVE

def porosity_fin_report_view(request):
    client_orders = Client_orders.objects.filter(porosity_fin_report=True)
    return render(request, 'Manager/porosity_final_report_view.html', {'client_orders': client_orders})




def por_final_report_admin_approve(request,id):
    client_orders = Client_orders.objects.get(id=id)
    client_orders.por_rep_admin_approve =True
    client_orders.fintest = True
    client_orders.retest = False

    product = client_orders.product
    qnt     = client_orders.quantity

    price = {
        'Pressure Sensor': 120,
        'Battery': 75,
        'RRAM': 250,
        'Super Capacitors': 130,
    }
    total_price = int(price[product]) * int(qnt)
    client_orders.amount = total_price
    client_orders.save()

    messages.success(request,'Porosity Report Approved by Manager')
    return redirect('/manager/porosity_fin_report_view/')





def por_final_report_admin_reject(request,id):
    client_orders = Client_orders.objects.get(id=id)
    client_orders.fintest = False
    client_orders.retest  = True
    client_orders.por_rep_admin_reject  = True
    client_orders.save()


    send_mail(
        'Update The Conductivity Test',
        'Conductvity Test result are not satisfied,Conduct the test Again',
        'anvi.aadiv@gmail.com',
        ['yuvar1018@gmail.com'],
        fail_silently=False,
    )

    messages.success(request,'Porosity Report Rejected by Manager')
    return redirect('/manager/porosity_fin_report_view/')














def payment_view(request):
    Order_payment = Client_orders.objects.filter(por_rep_admin_approve=True)
    return render(request,'Manager/payment_view.html',{'Order_payment':Order_payment})


def dispatch(request,id):
    dispatch_orders = Client_orders.objects.get(id=id)
    dispatch_orders.dispatch = True
    dispatch_orders.save()
    messages.success(request,'Successfully Dsipatched')
    return redirect('/manager/payment_view/')














