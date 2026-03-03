from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect


def home(request):
    return redirect('/api/users/login/')   # 👈 redirect to login


urlpatterns = [
    path('', home),
    path('admin/', admin.site.urls),
    path('api/users/', include('users.urls')),
]