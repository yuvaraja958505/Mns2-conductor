from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='home'),
    path('clients/', include('Client.urls')),
    path('manager/', include('Manager.urls')),
    path('porosity_analysis/', include('Porosity_Analysis.urls')),
    path('app_integration/', include('App_Integration.urls')),
    path('manganese_process/', include('Manganese_Process.urls')),

]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
