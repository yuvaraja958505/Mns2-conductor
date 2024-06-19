from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('manager_home/',views.manager_home_page ),
    path('manager_login/',views.manager_login_page),
    path('manager_logout/',views.manager_login_out),


    # Manager Login Approval View
    path('mg_app_login_client/',      views.mg_app_login_client_view),
    path('mg_app_login_manganese/',   views.mg_app_login_mang_view),
    path('mg_app_login_application/', views.mg_app_login_application_view),
    path('mg_app_login_porosity/',    views.mg_app_login_porosity_view),


    # Client Login approve/reject

    path('app_client_lg/<int:id>/',          views.client_lg_approve_btn),
    path('app_client_lg_reject/<int:id>/',   views.client_lg_reject_btn),

    path('app_manganese_lg/<int:id>/',        views.manganese_login_approval),
    path('app_manganese_lg_reject/<int:id>/', views.manganese_login_reject),

    path('app_application_lg/<int:id>/',        views.application_login_approval),
    path('app_application_lg_reject/<int:id>/', views.application_login_reject),

    path('app_porosity_lg/<int:id>/', views.porosity_login_approval),
    path('app_porosity_lg_reject/<int:id>/', views.porosity_login_reject),



    # Manganese Team Report To Admin
    path('mg_view_report/', views.mg_view_report),
    path('mg_view_report_mganalysis/<int:id>/', views.mg_view_report_mganalysis),
    path('mg_final_report_approve/<int:id>/', views.mg_final_report_approve),


    # APP INTEGRATION REPORT
    path('app_view_report/', views.app_view_report),
    path('app_view_Component/<int:id>/', views.app_view_Component),
    path('app_final_report_approve/<int:id>/', views.app_final_report_approve),

    # ADMIN VIEW AND AND APPROVE
    path('porosity_fin_report_view/',views.porosity_fin_report_view),
    path('por_admin_approve/<int:id>/',views.por_final_report_admin_approve),
    path('por_admin_reject/<int:id>/',views.por_final_report_admin_reject),


    # PAYMENT VIEW AND DISPATCH
    path('payment_view/',views.payment_view),
    path('dispatch/<int:id>/',views.dispatch)




]
