"""dbms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', include('stadium.urls')),
    path('admin/', admin.site.urls),
    path('login/', include('stadium.urls')),
    path('register1/', include('stadium.urls')),
    path('register2/',include('stadium.urls')),
    path('search/', include('stadium.urls')),
    path('privacypolicy/', include('stadium.urls')),
    path('logout/', include('stadium.urls')),
    path('t&c/', include('stadium.urls')),
    path('seats/', include('stadium.urls')),
    path('seats2/', include('stadium.urls')),
    path('payment/', include('stadium.urls')),
    path('ticket/', include('stadium.urls')),
    path('search2/', include('stadium.urls')),
    path('find/', include('stadium.urls')),
    path('cancel/', include('stadium.urls')),
    path('stadiumupdates/', include('stadium.urls')),
    path('account/', include('stadium.urls')),
    path('search3/', include('stadium.urls'))
]
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)