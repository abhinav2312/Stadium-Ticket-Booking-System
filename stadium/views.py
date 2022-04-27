from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import showcity, showmatch, showsnack
# from django.db import connection
import mysql.connector
# Create your views here.
conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ABHI@123",
  database="myproject"
)
mycursor = conn.cursor()
match = 0
Price = 0
ticket = 'BOOK'
seat = 0
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
def tc(request):
    return render(request, 't&c.html')

def ticket(request):
    if request.method == 'POST':
        cno = request.POST['Cno']
        expiry = request.POST['expiry']
        cvv = request.POST['cvv']
        if len(cno)!=12
            messages.info('Invalid Card number')
        
        return render(request, 'ticket.html', {"cvv":cvv})

def payment(request):
    if request.method == 'POST':
        snack = request.POST['snk']
        value = request.POST['radio'] 
        if value!="default":
            mycursor.execute("SELECT price from stadium_snacks where snacks_id = %s", [snack])
            b = mycursor.fetchone()
            print(b)
        global seat
        seat = value
        return render(request, 'payment.html', {"value":value, "snack":snack})
def seats2(request):
    results4 = showsnack.objects.all()
    if request.method=='POST':
        global match
        match = request.POST['radio']
        mycursor.execute("SELECT S1, S2, S3, S4, S5, S6, S7, S8, S9, S10 from stadium_seats where match_id = %s;", [match])
        b = mycursor.fetchall()[0]
        c =[]
        return render(request, 'seats2.html', {"b":b, "c":c, "results4":results4})


def seats(request):
    if request.method == 'POST':
        city = request.POST['Cityname']
        date = request.POST['Date']
        match = request.POST['Match']
        if match=='default'and city == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s;", [date])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                return redirect("/search/")
            return render(request, 'seats.html', {"b":b})
        elif match == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and city = %s", [date, city])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                return redirect("/search/")
            return render(request, 'seats.html', {"b":b})
        elif city == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and match_id = %s", [date, match])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                return redirect('/search/')
            return render(request, 'seats.html', {"b":b})
        else:
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and match_id = %s and city = %s", [date, match, city])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                return redirect("/search/")
            return render(request, 'seats.html', {"b":b})
        
def search(request):
    results = showcity.objects.all().values_list('city', flat=True).distinct()
    results2 = showmatch.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'search.html', {"results":results, "results2":results2})
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('/login/')
    else:
        return render(request, 'search.html', {"results":results, "results2":results2})
def register1(request):
    return render(request, 'registration1.html')

def register2(request):
    if request.method == 'POST' :
        firstname = request.POST["fname"]
        lastname = request.POST["lname"]
        email = request.POST["email"]
        username=request.POST["username"]
        password=request.POST["password"]
        confirmpassword = request.POST["confirmpassword"]
        if password == confirmpassword :
            if User.objects.filter(username = username).exists():
                messages.info(request, 'Username taken')
                return redirect('/register1')
            elif User.objects.filter(email = email).exists():
                messages.info(request, 'email taken')
                return redirect('/register1')
            else:
                user = User.objects.create_user(username = username, password = password, email = email, first_name = firstname, last_name = lastname)
                user.save()
                messages.info(request, 'Account created')

                return redirect('/login')
        else:
            messages.info(request, 'password not matching')
            return redirect('/register1')
        
    else:
        return render(request, 'home.html')
    
def adminlogin(request):
    return render(request, 'adminlogin.html')

def pp(request):
    return render(request, 'privacypolicy.html')