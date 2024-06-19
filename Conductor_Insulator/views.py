from django.shortcuts import render


def home_view(request):
    return render(request, 'Main_page/main_home.html')




