from django.shortcuts import render

from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from Client.models import *



# Client Home Page

def client_home_page(request):
    return render(request,'Clients/home_page.html')




# Client Register Page

def client_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        location = request.POST['location']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']

        try:
            existing_user = Client_register.objects.get(email=email)
            messages.error(request, 'Email already in use. Please use a different email.')
            return redirect('/clients/client_register/')

        except Client_register.DoesNotExist:
            try:
                client = Client_register(username=username, location=location, email=email, phone=phone, password=password)
                client.save()
                messages.success(request, 'Successfully Client Registered')
                return render(request, 'Clients/login_page.html')

            except IntegrityError as e:
                messages.error(request,f'An error occurred while registering: {e}')
                return redirect('clients/client_login/')
    return render(request, 'Clients/login_page.html')




# Client Login Page

def client_login(request):
    if request.method=='POST':
        uemail = request.POST['useremail']
        upassword = request.POST['password']

        try:
            user = Client_register.objects.get(email=uemail)

            if user.password == upassword:
                if user.cl_admin_lg:
                    request.session['client'] = uemail
                    messages.success(request, 'Client Successfully Logged In')
                    return redirect('/clients/client_home/')
                else:
                    messages.success(request, 'Please Wait for Admin Approval')
                    return render(request, 'Clients/login_page.html')
            else:
                messages.error(request, 'Incorrect password. Please try again')
                return render(request, 'Clients/login_page.html')

        except ObjectDoesNotExist:
            messages.error(request, 'No Client with these credentials.')
            return render(request, 'Clients/login_page.html')

    return render(request, 'Clients/login_page.html')



# Client Logout

def client_login_out(request):
    try:
        if 'client' in request.session:
            del request.session['client']
            messages.success(request, 'Client logged out successfully')
    except KeyError:
        messages.error(request, 'Error occurred during logout')
    return redirect('/')






# Client Order Page


def client_order_page(request):
    user_email = request.session.get('client')

    if request.method == 'POST':
        try:
            user_detail = Client_register.objects.get(email=user_email)
            quantity = request.POST.get('quantity')
            product = request.POST.get('product')

            order = Client_orders(
                email=user_detail.email,
                username=user_detail.username,
                product=product,
                quantity=quantity,
                consumer_id = user_detail.consumer_id
            )
            order.save()
            messages.success(request,'Order Successfully Placed')
            return redirect('/clients/client_home/')

        except Client_register.DoesNotExist:
            messages.error(request, 'Error in placing the Order')
            return redirect('/clients/client_order/')

    elif user_email:
        try:
            user_detail = Client_register.objects.get(email=user_email)
            return render(request, 'Clients/order_page.html', {'user_detail': user_detail})

        except Client_register.DoesNotExist:
            messages.error(request, 'User details not found.')
            return redirect('/clients/client_login/')


    return redirect('/clients/client_login/')





def client_order_status(request):
   return render(request,'Clients/order_payment.html')






def client_order_status(request):
    try:
        email = request.session['client']
        client_orders = Client_orders.objects.filter(email=email)
        name = [order.username for order in client_orders][0]
        if not client_orders:
            message = "No Orders"
        else:
            message = 'Thankyou For your Orders'



    except KeyError:
        message = "Session not found. Please Login Again"
        return redirect('/clients/client_login/')
    except:
        messages.error(request,'No Orders Placed Yet')
        return redirect('/clients/client_home/')

    return render(request, 'Clients/order_status.html', {'client_orders': client_orders, 'message': message,'name':name})



def client_payment(request):
    try:
        email = request.session['client']
        client_orders = Client_orders.objects.filter(email=email)
        name = [order.username for order in client_orders][0]
        if not client_orders:
            message = "No Orders"
        else:
            message = 'Thankyou For your Orders'

    except KeyError:
        message = "Session not found. Please Login Again"
        return redirect('/clients/client_login/')

    return render(request, 'Clients/order_payment.html', {'client_orders': client_orders, 'message': message,'name':name})





def client_payamount(request,id):
    order = Client_orders.objects.get(id=id)
    if request.method =='POST':
        order.client_payment = True
        order.save()
        messages.success(request,'Payment Done Successfully')
        return redirect('/clients/client_payment/')
    return render(request,'Clients/Payment_page.html',{'order':order})



def client_view(request,id):
    values =  Client_orders.objects.get(id=id)
    return render(request, 'Clients/view_file.html', {'values': values})

