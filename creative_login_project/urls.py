from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_intro(request):
    return redirect('intro')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', redirect_to_intro),         
    path('', include('login.urls')),
]
