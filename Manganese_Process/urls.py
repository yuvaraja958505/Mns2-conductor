from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('mg_login/', views.mg_login),
    path('mg_register/', views.mg_register),
    path('mg_logout/', views.mg_login_out),
    path('mg_home/', views.mg_home_page),


    path('mg_client_order_view/', views.client_order_view),
    path('mg_data_set_upload/', views.mg_data_set_upload),
    path('mg_process_data/', views.mg_process_data),
    path('mg_qnty_process/<int:id>/', views.mg_qnty_process),

    # View report
    path('mg_view_report/', views.mg_view_report),

    path('mg_view_report_mganalysis/<int:id>/', views.mg_view_report_mganalysis),




]