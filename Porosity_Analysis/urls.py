from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('por_login/',      views.por_login),
    path('por_register/',   views.por_register),
    path('por_logout/',     views.por_login_out),
    path('por_home/',       views.por_home_page),


    # Porosity Main VIEWS
    path('view_app_report/', views.porosity_view_app_report),
    path('porosity_comp_views/<int:id>/', views.porosity_comp_views),
    path('porosity_comp_views/<int:id>/', views.porosity_comp_views),

    # Porosity Analysis


    path('porosity_upload_view/', views.porosity_upload_view,name="porosity_upload_view"),

    path('upload_dataset/<int:id>/', views.porosity_upload_dataset),

    path('porosity_test/', views.porosity_test),
    path('porosity_process/<int:id>/', views.porosity_process),
    path('porosity_test_result/', views.porosity_test_result),


    path('display_porosity_data/<int:id>/', views.display_porosity_data),
    path('porosity_permissible/<int:id>/',  views.porosity_permissible),
    path('porosity_fin_report/',            views.porosity_fin_report),

    path('new_test_result/',         views.new_test_result),
    path('test1/<int:id>/',          views.test1),

    path('retest/<int:id>/',          views.test1),



]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)