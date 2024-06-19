from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('app_login/', views.app_login),
    path('app_register/', views.app_register),
    path('app_logout/', views.app_login_out),
    path('app_home/', views.app_home_page),



    path('mang_team_report_view/',views.mang_team_report_view),
    path('mang_team_report_mg_view/<int:id>/',views.mang_team_report_mg_view),

    # Process Components
    path('app_process_view/',views.app_process_view),
    path('start_integrate/<int:id>/',views.start_integrate),

    # Final Report Page
    path('app_final_report/',views.app_final_report),


    path('app_comp_views/<int:id>/', views.app_comp_views),





]