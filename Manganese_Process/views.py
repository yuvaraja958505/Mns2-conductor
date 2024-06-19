from django.shortcuts import render
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from Manganese_Process.models import *
from Client.models import *
import pandas as pd
from pandas.errors import ParserError, EmptyDataError
import math



# Mg Home Page

def mg_home_page(request):
    return render(request,'Manganese/manganese_home.html')




# mg Register Page

def mg_register(request):

    if request.method == 'POST':
        username = request.POST['username']
        designation = request.POST['designation']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']


        try:
            existing_user = Manganese_register.objects.get(email=email)
            messages.error(request, 'Email already in use. Please use a different email.')
            return redirect('/Manganese/mg_register/')

        except Manganese_register.DoesNotExist:
            try:
                mang = Manganese_register(username=username, designation=designation, email=email, phone=phone, password=password)
                mang.save()
                messages.success(request, 'Successfully Manganese Team Registered')
                return render(request, 'Manganese/login_page.html')


            except IntegrityError as e:
                messages.error(request,f'An error occurred while registering: {e}')
                return redirect('Manganese/mg_login/')

    return render(request, 'Manganese/login_page.html')




# mg Login Page

def mg_login(request):

    if request.method=='POST':
        uemail = request.POST['useremail']
        upassword = request.POST['password']

        try:
            user = Manganese_register.objects.get(email=uemail)

            if user.password == upassword:
                if user.mg_admin_lg:
                    request.session['manganese'] = uemail
                    messages.success(request, 'MG Team Successfully Logged In')
                    return render(request, 'Manganese/manganese_home.html')

                else:
                    messages.success(request, 'Please Wait for Admin Approval')
                    return render(request, 'Manganese/login_page.html')
            else:
                messages.error(request, 'Incorrect password. Please try again')
                return render(request, 'Manganese/login_page.html')

        except ObjectDoesNotExist:
            messages.error(request, 'No manganese Team with these credentials.')
            return render(request, 'Manganese/login_page.html')

    return render(request, 'Manganese/login_page.html')





def mg_login_out(request):
    try:
        if 'manganese' in request.session:
            del request.session['manganese']
            messages.success(request, 'MG Team logged out successfully')
    except KeyError:
        messages.error(request, 'Error occurred during logout')
    return redirect('/')






def client_order_view(request):
    client_orders = Client_orders.objects.all()
    return render(request, 'Manganese/mg_client_order_view.html',{'client_orders':client_orders})





def mg_data_set_upload(request):
    components_count = Components_required.objects.count()
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['comp_file']
            data = pd.read_csv(uploaded_file)

            for index, row in data.iterrows():
                instance = Components_required(
                    component=row['Component'],
                    material=row['Material'],
                    product=row['Product']
                )
                instance.save()
            messages.success(request, "Components Dataset uploaded successfully")
            return redirect('/manganese_process/mg_data_set_upload/')

        except ParserError as e:
            messages.error(request, f"Error parsing the CSV file: {e}")
        except EmptyDataError as e:
            messages.error(request, f"The CSV file is empty: {e}")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    return render(request, 'Manganese/mg_dataset_upload.html',{'components_count': components_count})


def mg_process_data(request):
    client_orders = Client_orders.objects.all()
    return render(request, 'Manganese/mg_process_data.html', {'client_orders': client_orders})



def mg_qnty_process(request,id):
    client_orders = Client_orders.objects.get(id =id)
    product  = client_orders.product
    qnty     =  client_orders.quantity

    components      = Components_required.objects.filter(product=product)
    first_component = components.first()

    manganese_Comp   = first_component.component
    manganese_form   = first_component.material
    manganese_size   = '50mm x 20mm x 3 micrometre'
    manganese_mass   = 0


    if product == 'Pressure Sensor':  # Pressure sensor Size : 50mm x 20mm x 3 μm
        manganese_size = '50mm x 20mm x 3 micrometre'

        manganese_density = 3.99
        length_mm    = 50
        width_mm     = 20
        thickness_mm = (3/1000)

        volume_mm3 = length_mm * width_mm * thickness_mm
        # Calculate mass of Manganese in grams
        manganese_mass = volume_mm3 * manganese_density

        # Print or return the calculated mass of Manganese
        print(f"Estimated mass of Manganese required: {manganese_mass} grams")

    elif product == 'Battery': # Battery Size : DIAMETER:14.3 - 14.4 mm , Length =50.3 - 50.4 mm
        manganese_size = 'DIA : 14.3 mm - 14.4 mm & Length: 50.3 - 50.4 mm'

        mns2_density = 3.99   # Example density value (unit: g/mm^3)
        # Dimensions of MnS2 cathode (averaged values from the range)
        diameter_mm = (14.3 + 14.4) / 2
        radius_mm = diameter_mm / 2
        length_mm = (50.3 + 50.4) / 2


        volume_mm3 = math.pi * (radius_mm ** 2) * length_mm  * (1/1000)
        manganese_mass = volume_mm3 * mns2_density

    elif product == 'RRAM':    # RRAM Size :50nm x 100nm x 5nm
        manganese_size = '50mm x 10mm x 5micrometre'
        mns2_density = 3.99

        # Dimensions of MnS2 active layer in nanometers (convert to millimeters)
        length_mm = 50
        width_mm  = 10
        thickness_mm = 5 / 1000

        volume_mm3 = length_mm * width_mm * thickness_mm

        # Calculate mass of Manganese Sulphide in grams
        manganese_mass = volume_mm3 * mns2_density

    elif product == 'Super Capacitors':

        manganese_size = '50mm x 20mm x 50 micrometre'

        manganese_density = 3.99
        length_mm    = 50
        width_mm     = 20
        thickness_mm = 50 / 10000
        volume_mm3   = length_mm * width_mm * thickness_mm
        # Calculate mass of Manganese in grams
        manganese_mass = volume_mm3 * manganese_density

    client_orders.manganese_Comp = manganese_Comp
    client_orders.manganese_form = manganese_form
    client_orders.manganese_size = manganese_size
    client_orders.manganese_mass = round(float(manganese_mass) * qnty, 4)
    client_orders.material_volume   = round(volume_mm3,3)


    client_orders.save()
    messages.info(request,'Processed successfully!')
    return redirect('/manganese_process/mg_process_data/')




# MANGANESE PROCESSED REPORT (3 VIEWS )


def mg_view_report(request):
    client_orders = Client_orders.objects.exclude(manganese_Comp__isnull=True)
    return render(request, 'Manganese/mg_view_report.html', {'client_orders': client_orders})




def mg_view_report_mganalysis(request,id):
    mg_calculations = Client_orders.objects.get(id=id)
    return render(request, 'Manganese/mg_view_report_mg_analysis.html', {'mg_calculations': mg_calculations})

















