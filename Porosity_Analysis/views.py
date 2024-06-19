from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
# from django.utils.baseconv import base64
from sklearn.model_selection import train_test_split
from PIL import Image
from Porosity_Analysis.models import *
from App_Integration.models import *
from Manganese_Process.models import *
from Client.models import *

import pandas as pd
from pandas.errors import ParserError, EmptyDataError
import random
from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

def por_home_page(request):
    return render(request,'Porosity/por_home.html')



# mg Register Page

def por_register(request):
    if request.method == 'POST':
        username = request.POST['username']
        designation = request.POST['designation']
        email = request.POST['email']
        phone = request.POST['phone']
        password = request.POST['password']


        try:
            existing_user = Porosity_register.objects.get(email=email)
            messages.error(request, 'Email already in use. Please use a different email.')
            return redirect('/porosity_analysis/por_register/')

        except Porosity_register.DoesNotExist:
            try:
                apps= Porosity_register(username=username, designation=designation, email=email, phone=phone, password=password)
                apps.save()
                messages.success(request, 'Successfully Porosity Team Registered')
                return render(request, 'Porosity/login_page.html')


            except IntegrityError as e:
                messages.error(request,f'An error occurred while registering: {e}')
                return redirect('/porosity_analysis/por_register/')

    return render(request, 'Porosity/login_page.html')




# mg Login Page

def por_login(request):
    if request.method=='POST':
        uemail = request.POST['useremail']
        upassword = request.POST['password']

        try:
            user = Porosity_register.objects.get(email=uemail)
            if user.password == upassword:
                if user.por_admin_lg:
                    request.session['porosity'] = uemail
                    messages.success(request, 'Porosity Team Successfully Logged In')
                    return redirect('/porosity_analysis/por_home/')

                else:
                    messages.success(request, 'Please Wait for Admin Approval')
                    return render(request, 'Porosity/login_page.html')
            else:
                messages.error(request, 'Incorrect password. Please try again')
                return render(request, 'Porosity/login_page.html')

        except ObjectDoesNotExist:
            messages.error(request, 'No Porosity with these credentials.')
            return render(request, 'Porosity/login_page.html')

    return render(request, 'Porosity/login_page.html')





def por_login_out(request):
    try:
        if 'porosity' in request.session:
            del request.session['porosity']
            messages.success(request, 'Porosity Team logged out successfully')
    except KeyError:
        messages.error(request, 'Error occurred during logout')
    return redirect('/')










#app_admin_approve



def porosity_view_app_report(request):
    client_orders = Client_orders.objects.exclude(app_admin_approve=False)
    return render(request, 'Porosity/porosity_b_viewreport.html', {'client_orders': client_orders})




def porosity_comp_views(request,id):
    client_orders = Client_orders.objects.get(id=id)
    product = client_orders.product
    components = Components_required.objects.filter(product=product)
    return render(request, 'Porosity/porosity_b2_app_component.html', {'components': components})



def porosity_upload_view(request):
    client_orders = Client_orders.objects.exclude(app_admin_approve=False)
    return render(request,'Porosity/porosity_c_upload_dataset.html', {'client_orders': client_orders})



def porosity_upload_dataset(request,id):
    client_id = id
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['porosity-file']
            data = pd.read_csv(uploaded_file)

            max = 0
            mercury = 0
            for index, row in data.iterrows():
                print('Index',index,'row:',row)
                if max > row['Cumulative Volume (cm³/g)']:
                    max = max
                else:
                    max = row['Cumulative Volume (cm³/g)']
                    mercury = row['Volume of Mercury Intruded (cm³/g)']

                instance = Porosity_data(
                    pressure_psi=row['Pressure (psi)'],
                    volume_mercury_intruded=row['Volume of Mercury Intruded (cm³/g)'],
                    cumulative_volume=row['Cumulative Volume (cm³/g)'],
                    pore_diameter_nm=row['Pore Diameter (nm)'],
                    specific_surface_area =row['Specific Surface Area (m²/g)'],
                    avg_pore_size_nm=row['Average Pore Size (nm)'],
                    median_pore_size_nm =   row['Median Pore Size (nm)'],

                    total_pore_volume=row['Total Pore Volume (cm³/g)'],
                    tortuosity=row['Tortuosity'],
                    permeability_mDarcy=row['Permeability (mDarcy)'],
                    adsorption_capacity=row['Adsorption Capacity (mmol/g)'],
                    client_id = client_id,
                )
                instance.save()
            print('maximum value:',max,'Mercury Intruduced:',mercury)
            client_orders = Client_orders.objects.get(id=id)
            client_orders.maxi = max
            client_orders.mercury = mercury
            client_orders.porosity_upload = True
            client_orders.save()
            messages.success(request, "Porosity Data uploaded successfully")
            print(99999999999)
            return redirect('porosity_upload_view')

        except ParserError as e:
            messages.error(request, f"Error parsing the CSV file: {e}")
        except EmptyDataError as e:
            messages.error(request, f"The CSV file is empty: {e}")
        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
    return render(request,'Porosity/porosity_data_upload.html',{'client_id':client_id})





def porosity_test(request):
    client_orders = Client_orders.objects.exclude(porosity_upload=False)
    return render(request, 'Porosity/porosity_test_page.html', {'client_orders': client_orders})




def porosity_process(request,id):
    client_orders = Client_orders.objects.get(id=id)
    fin_porosity_value = client_orders.maxi
    mercury_intuduced  = client_orders.mercury
    client_orders.porsity_value = fin_porosity_value
    client_orders.mercury_intuduced = mercury_intuduced
    client_orders.fin_porosity_value = True
    client_orders.save()
    messages.success(request,'Porosity Test Conducted and Datas are Analysed')
    return redirect('/porosity_analysis/porosity_test/')



def porosity_test_result(request):
    client_orders = Client_orders.objects.filter(fin_porosity_value=True)
    return render(request, 'Porosity/porosity_test_result.html', {'client_orders': client_orders})



def display_porosity_data(request,id):
    porosity_data = Porosity_data.objects.filter(client_id= id)
    return render(request, 'Porosity/porosity_excel.html', {'porosity_data': porosity_data})




from django.http import HttpResponse
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pandas as pd
from PIL import Image



def porosity_permissible(request, id):
    porosity = Client_orders.objects.get(id=id)
    cum_value = porosity.porsity_value
    mercury_intuduced = porosity.mercury_intuduced
    mat_volume = porosity.material_volume

    # Your file path might differ here



    file_path = r'{0}\utility\4porosity_test_report_final.csv'.format(BASE_DIR)

    # Read the CSV file into a DataFrame
    dataset = pd.read_csv(file_path)

    # Assuming these columns exist in your dataset
    X = dataset[['Cumulative Volume', 'Mercury Intruded', 'Material Volume']]
    y = dataset['Porosity']

    # Splitting data for training and testing (you might want to adjust this)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

    # Use RandomForestRegressor instead of BaggingRegressor with DecisionTreeRegressor
    random_forest_regressor = RandomForestRegressor(n_estimators=100, random_state=42)
    random_forest_regressor.fit(X_train, y_train)

    # Create a DataFrame with fetched values for prediction
    input_data = pd.DataFrame([[cum_value, mercury_intuduced, mat_volume]],
                              columns=['Cumulative Volume', 'Mercury Intruded', 'Material Volume'])

    # Use the trained model to predict using the fetched values
    prediction = random_forest_regressor.predict(input_data)
    print(prediction)

    # Calculate MSE for validation purposes
    mse = mean_squared_error(y_test, random_forest_regressor.predict(X_test))
    print(f'Porosity: {mse}')  # This could be removed or adjusted for logging

    fprediction = float(round(prediction[0],2) )
    print('fprediction',fprediction)

    if fprediction <= 5:
        porosity_result = f"Porosity is low ({fprediction}%) - High conductivity and safe operation."

    elif fprediction <= 10:
        porosity_result = f"Porosity is optimal ({fprediction}%) Good Conductivity & best suitablity"

    elif fprediction <= 15:
        porosity_result = f"Porosity is moderate ({fprediction:.2f}%) - Optimal to use"

    elif fprediction <= 20:
        porosity_result = f"Porosity is moderate ({fprediction:.2f}%) -Moderate Conductivity"

    else:
        porosity_result = f"Porosity is high ({fprediction:.2f}%)- Monitor performance and consider further analysis."

    porosity.prediction = fprediction
    porosity.porosity_result = porosity_result
    porosity.porosity_fin_report = True
    porosity.save()
    messages.success(request,'Porosity Report analysed')

    return redirect('/porosity_analysis/porosity_test_result/')





# porosity_fin_report

def porosity_fin_report(request):
    client_orders = Client_orders.objects.filter(porosity_fin_report=True)
    return render(request, 'Porosity/porosity_final_report.html', {'client_orders': client_orders})




def new_test_result(request):
    client_orders = Client_orders.objects.exclude(porosity_fin_report=False)
    return render(request, 'Porosity/porosity_i_test_result.html', {'client_orders': client_orders})







list=[]

def test1(request,id):
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.tree import DecisionTreeRegressor
    from sklearn.metrics import mean_squared_error
    from sklearn.preprocessing import StandardScaler
    from sklearn.multioutput import MultiOutputRegressor
    import matplotlib.pyplot as plt
    from io import BytesIO
    from django.core.files.base import ContentFile
    import time
    clientdata = Client_orders.objects.get(id=id)
    if request.method=="POST":
        temperature=request.POST['temperature']
        pressure=request.POST['pressure']
        concentration=request.POST['concentration']
        quantity=request.POST['quantity']
        material=request.POST['material']
        CrystallizeSize=request.POST['CrystallizeSize']
        PoreSize=request.POST['PoreSize']
        EquilibriumTime=request.POST['EquilibriumTime']
        strain=request.POST['strain']
        mp=request.POST['mp']
        clientdata = Client_orders.objects.get(id=id)



        #TIME TEST
        start_time = time.time()

##### TEST 1  TEMPERATURE POROSITY #####
        # Load your dataset
        file_path = r'{0}\utility\final_temp_dataset.csv'.format(BASE_DIR)

        df = pd.read_csv(file_path)

        # Define features and labels
        features = df[['Temperature', 'Porosity','CrystallizeSize','PoreSize','EquilibriumTime']]
        labels = df[['BandGapIncrease', 'ConductivityIncrease']]

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3)

        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Create and train the decision tree model with MultiOutputRegressor
        tree_model = MultiOutputRegressor(DecisionTreeRegressor())
        tree_model.fit(X_train_scaled, y_train)

        # Make predictions on the test set
        predictions = tree_model.predict(X_test_scaled)

        # Evaluate the model
        mse = mean_squared_error(y_test, predictions)
        print(f'Mean Squared Error: {mse}')

        # Assume user_input is defined earlier in your code
        user_input = {
                'Temperature': temperature,
                'Porosity': clientdata.prediction,
                'CrystallizeSize':CrystallizeSize,
                'PoreSize':PoreSize,
                'EquilibriumTime':EquilibriumTime

        }
        user_df = pd.DataFrame([user_input])
        user_scaled = scaler.transform(user_df)
        user_predictions = tree_model.predict(user_scaled)
        temp_bangap=user_predictions[0][0]
        temp_conductivity=user_predictions[0][1]

        print('Test 1 - Temperature Analysis Done')

##### TEST 2  PRESSURE&POROSITY #####

        file_path = r'{0}\utility\Book2.csv'.format(BASE_DIR)

        df = pd.read_csv(file_path)

        # Define features and labels
        features = df[['Pressure', 'Porosity']]
        labels = df[['BandGapIncrease', 'ConductivityIncrease']]

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3)

        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Create and train the decision tree model with MultiOutputRegressor
        tree_model = MultiOutputRegressor(DecisionTreeRegressor())
        tree_model.fit(X_train_scaled, y_train)

        # Make predictions on the test set
        predictions = tree_model.predict(X_test_scaled)

        mse = mean_squared_error(y_test, predictions)
        print(f'Mean Squared Error: {mse}')


        user_input = {
                'Pressure': pressure,
                'Porosity': clientdata.prediction,
        }

        # Convert user input to a DataFrame
        user_df = pd.DataFrame([user_input])

        user_scaled = scaler.transform(user_df)

        user_predictions = tree_model.predict(user_scaled)
        pres_bandgap=user_predictions[0][0]
        pres_conduct=user_predictions[0][1]
        print(pres_conduct)
        print('Test 2 - Pressure Analysis Done')

 ##### TEST 3  DOPING ANALYSIS #####

        mn_mass         = float(clientdata.manganese_mass)
        mn_density      = 3.99
        mn_volume       = (mn_mass / mn_density)
        porosity_pred   = float(clientdata.prediction)

        file_path = r'{0}\utility\doping_dataset.csv'.format(BASE_DIR)

        df = pd.read_csv(file_path)


        # Map string values to integers
        dopant_mapping = {'Al': 0, 'Ga': 1, 'In': 2, 'Sn': 3, 'Zn': 4, 'Fe': 5, 'Si': 6, 'Ti': 7, 'Cu': 8, 'Mg': 9}
        df['DopantSelection'] = df['DopantSelection'].map(dopant_mapping)

        # Define features and labels
        features = df[['DopantSelection', 'DopantConcentration', 'VolumeofMnS2', 'MassofMnS2', 'DensityofMnS2', 'DopantQuantity','Porosity']]
        labels = df[['BandGapChange', 'Conductivitychange']]

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3)

        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Create and train the decision tree model with MultiOutputRegressor
        tree_model = MultiOutputRegressor(DecisionTreeRegressor())
        tree_model.fit(X_train_scaled, y_train)

        # Make predictions on the test set
        predictions = tree_model.predict(X_test_scaled)

        # Evaluate the model
        mse = mean_squared_error(y_test, predictions)
        print(f'Mean Squared Error: {mse}')


        user_input = {
            'DopantSelection': material,
            'DopantConcentration': concentration,
            'VolumeofMnS2': mn_volume,
            'MassofMnS2': mn_mass,
            'DensityofMnS2': mn_density,
            'DopantQuantity': quantity,
            'Porosity':porosity_pred,
        }

        # Convert user input to a DataFrame
        user_df = pd.DataFrame([user_input])

        # Map user input string to int
        user_df['DopantSelection'] = user_df['DopantSelection'].map(dopant_mapping)

        # Standardize the user input
        user_scaled = scaler.transform(user_df)

        # Make predictions using the trained model
        user_predictions = tree_model.predict(user_scaled)
        dop_bandgap=user_predictions[0][0]

        dop_conduct=float(user_predictions[0][1])

        print('Test 3 - Strain Analysis Done')

##### TEST 4  STRAIN-DENSITY_MELTING POINT #####

        file_path = r'{0}\utility\dataset_mns2final.csv'.format(BASE_DIR)

        df = pd.read_csv(file_path)

        # Define features and labels
        features = df[['Strain','Density','Melting Point']]
        labels = df[['Band Gap','Conductivity']]

        # Split the data
        X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3)

        # Standardize the features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        # Create and train the decision tree model with MultiOutputRegressor
        tree_model = MultiOutputRegressor(DecisionTreeRegressor())
        tree_model.fit(X_train_scaled, y_train)

        # Make predictions on the test set
        predictions = tree_model.predict(X_test_scaled)

        mse = mean_squared_error(y_test, predictions)
        print(f'Mean Squared Error: {mse}')

        user_input = {
                'Strain': strain,
                'Density': mn_density,
                'Melting Point': mp,
        }

        # Convert user input to a DataFrame
        user_df = pd.DataFrame([user_input])

        user_scaled = scaler.transform(user_df)

        user_predictions = tree_model.predict(user_scaled)
        mp_bandgap = user_predictions[0][0]
        mp_conduct = user_predictions[0][1]

        # print("dop:",dop_conduct)
        # print("dop:",dop_bandgap)
        # print("temp",temp_bangap)
        # print("temp",temp_conductivity)
        # print("mp",mp_bandgap)
        # print("mp",mp_conduct)
        # print("press",pres_bandgap)
        # print(pres_conduct)
        global list
        list.append(dop_conduct)
        list.append(temp_conductivity)
        list.append(mp_conduct)
        list.append(pres_conduct)
        print('Test 4 -Done')








### TEST 5 - GRAPH PLOTING

        import pandas as pd
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeRegressor
        from sklearn.metrics import mean_squared_error
        from sklearn.preprocessing import StandardScaler
        from sklearn.multioutput import MultiOutputRegressor
        import matplotlib.pyplot as plt
        from io import BytesIO
        from django.core.files.base import ContentFile
        import time

        list2=list
        clientdata = Client_orders.objects.get(id=id)

        l=[float(list2[0]),float(list2[1]),float(list2[3]),float(list2[2])]
        maxi=max(l)
        if maxi==list2[0]:
            res=f'Doping impurities produces more conductivity:{list2[0]}'
        elif maxi==list2[1]:
            res=f"Temperature Factor Produces more conductivity:{list2[1]}"
        elif maxi==list2[2]:
            res=f"Melting Point Factor Produces more conductivity:{list2[2]}"
        elif maxi==list2[3]:
            res=f"Pressure Factor Produces more conductivity:{list2[3]}"
        clientdata.res=res
        clientdata.fintest=True
        clientdata.save()
        plt.figure()

        # Plot the data
        plt.plot(['dop_conduct', 'temp_conductivity', 'mp_conduct', 'pres_conduct'],
                 [list2[0], list2[1], float(list2[2]), list2[3]],
                 marker='o', linestyle='dashdot', color='g')

        # Add title and labels
        plt.title('REPORT')
        plt.xlabel('Parameters')
        plt.ylabel('Values')

        # Save the plot as an image
        plt.savefig(f'material_report1{clientdata.consumer_id}.png')


        # Show the plot
        # plt.show()
        # plt.figure()

        # Plot the data
        plt.plot(['dop_conduct', 'temp_conductivity', 'mp_conduct', 'pres_conduct'],
                 [list2[0], list2[1], list2[2], list2[3]],
                 marker='o', linestyle='dashdot', color='skyblue')

        # Add title and labels
        plt.title('REPORT')
        plt.xlabel('Parameters')
        plt.ylabel('Values')

        for i, txt in enumerate([float(list2[0]), float(list2[1]), float( list2[2]),float(list2[3])]):
            plt.annotate(f'{txt:.2f}', (i, txt), textcoords="offset points", xytext=(0, 10), ha='center')

        buffer = BytesIO()
        plt.savefig(buffer, format='png')

        clientdata.graph.save('conductivity.png', ContentFile(buffer.getvalue()))
        clientdata.save()
        print('Test 5 -Graph Plot Done ')




###################### NOW WORKING HEREEEEE.
### TEST 6 - GENERATING PDF

        import base64
        from io import BytesIO
        from PIL import Image as PILImage
        from reportlab.lib.pagesizes import letter
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet
        from django.core.files.base import ContentFile

        def generate_pdf_with_image_and_save(coutput, cinput,pinput,poutput,minput,moutput,val):
            from reportlab.lib.styles import getSampleStyleSheet
            from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
            from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
            from reportlab.lib.pagesizes import letter
            cid = clientdata.consumer_id
            oid = clientdata.id

            end_time     = time.time()
            elapsed_time = end_time - start_time
            print('Elapsed Time :',elapsed_time)


            path = r'{0}\utility\Report-{1}-{2}.pdf'.format(BASE_DIR, cid, oid)

            doc = SimpleDocTemplate(path, pagesize=letter)
            # Create a stylesheet
            styles = getSampleStyleSheet()
            normal_style = styles["Normal"]

            # Define the content for the PDF
            content = []

            title_style = ParagraphStyle(name='TitleStyle',fontSize=16,alignment=1)
            content.append(Paragraph("FINAL REPORT", title_style))
            content.append(Spacer(1, 35))

            # table3 -MANG
            content.append(Paragraph("MANGANESE REPORT", normal_style))
            content.append(Spacer(1, 35))
            data3 = [
                ["S.No", "CONTENT", "RESULT ANALYSIS"],
                ["1", minput['a'], moutput['a']],
                ["2", minput['b'], moutput['b']],
                ["3", minput['c'], moutput['c']],
                ["4", minput['d'], moutput['d']],
            ]

            table3 = Table(data3)
            table3.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.skyblue),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

            content.append(table3)
            content.append(Spacer(1, 35))



            # Table2 Porosity
            content.append(Paragraph("POROSITY REPORT", normal_style))
            content.append(Spacer(1, 35))
            data2 = [
                ["S.No", "CONTENT", "RESULT ANALYSIS"],
                ["1", pinput['a'], poutput['a']],
                ["2", pinput['b'], poutput['b']],
                ["3", pinput['c'], poutput['c']],
                ["4", pinput['d'], poutput['d']],
            ]

            table2 = Table(data2)
            table2.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.skyblue),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

            content.append(table2)
            content.append(Spacer(1, 35))

            #### CONDUCTIVITY 3
            content.append(Paragraph("CONDUCTIVITY REPORT", normal_style))
            content.append(Spacer(1, 35))

            elements = {''}

            data1 = [
                ["Parameters",           "Input",                          "Expected(S/m)",      "Conductivity Value(S/m)"],
                ["Doping (gms) ",        cinput['doping']+"  " + quantity, val['dop'] , coutput['dop_conduct']],
                ["Temperature (°C) ",    cinput['temp'],                   val['temperature'] , coutput['temp_conductivity']],
                ["Melting Point (°C) ",  cinput['melt'],                   val['melt'],  coutput['mp_conduct']],
                ["Pressure  (MPa) ",     cinput['pressure'],               val['pressure']    , coutput['pres_conduct']]
            ]

            table1 = Table(data1)
            table1.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),
                                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
                                        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                        ('BACKGROUND', (0, 1), (-1, -1), colors.skyblue),
                                        ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

            content.append(table1)
            content.append(Spacer(1, 65))





### END IMAGES

            # Reading The Image
            image_data = clientdata.graph.read()
            image = PILImage.open(BytesIO(image_data))

            # Size Adjustment Of Image
            image_width, image_height = image.size
            aspect_ratio = image_width / image_height
            target_width = 450
            target_height = int(target_width / aspect_ratio)
            image.thumbnail((target_width, target_height), PILImage.LANCZOS)
            img_buffer = BytesIO()
            image.save(img_buffer, format="PNG")
            img_buffer.seek(0)
            img_data = base64.b64encode(img_buffer.getvalue())
            img = Image(BytesIO(base64.b64decode(img_data)))

            # Append Image

            content.append(Spacer(1, 5))
            content.append(img)

            content.append(Spacer(1, 35))
            content.append(Paragraph("DURATION OF ANALYSIS \t\t :  {0} seconds".format(round(elapsed_time,3)), normal_style))
            content.append(Spacer(1, 35))

            # Add the content to the PDF document
            pdf_buffer = BytesIO()
            doc.build(content)
            pdf_buffer.seek(0)


            path = r'{0}\utility\Report-{1}-{2}.pdf'.format(BASE_DIR, cid, oid)
            # Save the generated PDF into the database
            clientdata.report_pdf = path
            clientdata.por_rep_admin_approve = False
            clientdata.por_rep_admin_reject  = False

            clientdata.save()


        # Example usage:
        coutput = {'dop_conduct': str(dop_conduct) , 'temp_conductivity': str(temp_conductivity) ,
                    'mp_conduct': str(mp_conduct)  , 'pres_conduct': str(pres_conduct) }
        cinput = {'doping': material , 'temp': temperature , 'pressure': pressure, 'melt': mp }

        poutput = {'a': clientdata.porsity_value ,'b': clientdata.mercury_intuduced +' cm³/g', 'c': clientdata.prediction +' % ', 'd': clientdata.porosity_result,}
        pinput  = {'a':'Porosity Value','b':'Mercury Intruduced','c':'Prediction','d':'Result'}

        moutput = {'a': clientdata.manganese_Comp, 'b': clientdata.manganese_form, 'c': clientdata.manganese_size,
                   'd': clientdata.manganese_mass + ' grams' }
        minput = {'a': 'Manganese Composition', 'b': 'Manganese Form', 'c': 'Size', 'd': 'Weight'}

        uv = {'T': float(temperature), 'P': float(pressure), 'con': float(concentration), 'Q': float(quantity), 'a': float(mp)}

        val = experimental_test(id,uv)
        print('Values Dop:',val['melt'])


        generate_pdf_with_image_and_save(coutput, cinput,pinput,poutput,minput,moutput,val)
        client_orders = Client_orders.objects.filter(fin_porosity_value=True)
        messages.success(request,'Test Analysed and Report Generated')
        return render(request, 'Porosity/porosity_i_test_result.html', {'id': id,'client_orders': client_orders})
    return render(request, 'Porosity/porosity_conductivitytest.html', {'id': id,'data':clientdata})





def retest(request,id):
    test1(request, id)
    return HttpResponse('Retest Ends')



def experimental_test(cid,uv):
    clientdata = Client_orders.objects.get(id=cid)
    mass        = float(clientdata.manganese_mass)
    Vm          = (mass/3.99)
    pore_volume = float(clientdata.maxi)
    porosity    = (pore_volume/Vm) * 100


    # Temperature Test
    T_Celsius     = 470    #uv['T']       #User Temp
    T_Kelvin = T_Celsius + 273.15
    T_0 = 273.15
    sigma_0 = 1000
    alpha = 10
    temp_cond = sigma_0 + alpha * (T_Kelvin - T_0)


    # PRESSURE
    P_MPa  = uv['P'] #5250 # User value pressure
    P_0 = 5000
    sigma_0 = 1000
    beta = (10000 - 1000) / (10000 - 5000)
    con_p = sigma_0 + beta * (P_MPa - P_0)


    # Melting Point
    T_m_Celsius = uv['a']
    T_m0_Celsius = 29
    sigma_0 = 1000
    gamma = 9000 / 1639

    m_con = sigma_0 + gamma * (T_m_Celsius - T_m0_Celsius)
    m_con = round(m_con, 2)


    # Dopants
    C = uv['con']
    Q = uv['Q']
    import math
    sigma_base = 950
    beta = 200
    delta = 0.1
    gamma = 2.5

    dop_con = sigma_base + (beta * math.log(1 + delta * C)) * (gamma * math.sqrt(Q))
    dop_con = round(dop_con, 1)


    result = {'porosity': porosity, 'temperature': temp_cond, 'pressure': con_p, 'dop': dop_con,'melt':m_con}
    return result







