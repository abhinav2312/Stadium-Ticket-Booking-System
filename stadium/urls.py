from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name = 'index'),
    path('login/', views.login, name = 'login'),
    path('register1/', views.register1, name ='register1'),
    path('register2/', views.register2, name ='register2'),
    path('search/', views.search, name = 'search'),
    path('privacypolicy/', views.pp, name = 'pp'),
    path('logout/', views.logout, name = 'logout'),
    path('t&c/', views.tc, name = 'tc'),
    path('seats/', views.seats, name = 'seats'),
    path('seats2/', views.seats2, name = "seats2"),
    path('payment/', views.payment, name = "payment"),
    path('ticket/', views.ticket, name = "ticket"),
    path('search2/', views.search2, name = "search2"),
    path('find/', views.find, name = "find"),
    path('cancel/', views.cancel, name = "cancel"),
    path('stadiumupdates/', views.stadiumupdates, name = "stadiumupdates"),
    path('account/', views.account, name = "account"),
    path('search3/', views.search3, name = "search3")
]