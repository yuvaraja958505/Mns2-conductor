from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from App_Integration.models import *
from Manganese_Process.models import *
from Client.models import *


# Mg Home Page

def app_home_page(request):
    return render(request,'App_Integration/app_home.html')




# mg Register Page

def app_register(request):

    if request.method == 'POST':
        username = request.POST['username']
        designation = request.POST['designation']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']


        try:
            existing_user = Application_register.objects.get(email=email)
            messages.error(request, 'Email already in use. Please use a different email.')
            return redirect('/app_integration/app_register/')

        except Application_register.DoesNotExist:
            try:
                apps= Application_register(username=username, designation=designation, email=email, phone=phone, password=password)
                apps.save()
                messages.success(request, 'Successfully Application Team Registered')
                return render(request, 'App_integration/login_page.html')


            except IntegrityError as e:
                messages.error(request,f'An error occurred while registering: {e}')
                return redirect('app_integration/app_login/')

    return render(request, 'App_Integration/login_page.html')



# mg Login Page

def app_login(request):
    if request.method=='POST':
        uemail = request.POST['useremail']
        upassword = request.POST['password']

        try:
            user = Application_register.objects.get(email=uemail)
            if user.password == upassword:
                if user.app_admin_lg:
                    request.session['application'] = uemail
                    messages.success(request, 'APP Integartion Team Successfully Logged In')
                    return redirect('/app_integration/app_home/')

                else:
                    messages.success(request, 'Please Wait for Admin Approval')
                    return render(request, 'App_integration/login_page.html')
            else:
                messages.error(request, 'Incorrect password. Please try again')
                return render(request, 'App_integration/login_page.html')

        except ObjectDoesNotExist:
            messages.error(request, 'No APP Integartion with these credentials.')
            return render(request, 'App_integration/login_page.html')

    return render(request, 'App_integration/login_page.html')





def app_login_out(request):
    try:
        if 'application' in request.session:
            del request.session['application']
            messages.success(request, 'APP Integartion Team logged out successfully')
    except KeyError:
        messages.error(request, 'Error occurred during logout')
    return redirect('/')





def mang_team_report_view(request):
    client_orders = Client_orders.objects.exclude(mang_admin_approve=False)
    return render(request, 'App_integration/mang_team_view_report.html', {'client_orders': client_orders})


def mang_team_report_mg_view(request,id):
    mg_calculations = Client_orders.objects.get(id=id)
    return render(request, 'App_integration/mang_view_mg_analysis.html', {'mg_calculations': mg_calculations})



# APP PROCESS PAGE

def app_process_view(request):
    client_orders = Client_orders.objects.exclude(mang_admin_approve=False)
    return render(request, 'App_integration/app_process.html', {'client_orders': client_orders})



def start_integrate(request,id):
    order = Client_orders.objects.get(id=id)
    order.app_process = True
    order.save()
    messages.success(request,'Successfully Integrated')
    return redirect('/app_integration/app_process_view/')





def app_final_report(request):
    client_orders = Client_orders.objects.exclude(app_process=False)
    return render(request, 'App_integration/app_team_fin_report.html', {'client_orders': client_orders})




def app_comp_views(request,id):
    client_orders = Client_orders.objects.get(id=id)
    product = client_orders.product
    components = Components_required.objects.filter(product=product)
    return render(request, 'App_integration/app_final_component.html', {'components': components})

