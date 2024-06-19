from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('client_login/', views.client_login),
    path('client_register/', views.client_register),
    path('client_logout/', views.client_login_out),
    path('client_home/', views.client_home_page),

    # Order Page
    path('client_order/', views.client_order_page),
    path('client_order_status/', views.client_order_status),
    path('client_payment/', views.client_payment),
    path('client_payamount/<int:id>/', views.client_payamount),


    path('client_view/<int:id>/', views.client_view),


]
urlpatterns += static(settings.MEDIA_URL,document_root=settings
                      .MEDIA_ROOT)