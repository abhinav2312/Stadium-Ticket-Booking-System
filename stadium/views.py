from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import showcity, showmatch, showsnack
from django.db import transaction, connection
import mysql.connector
# Create your views here.

conn = mysql.connector.connect(
  host="localhost",
  user="root",
  password="ABHI@123",
  database="myproject"
)
num = 'BOOK'
match = 0
Price = 0
seat = 0
snacks = 0
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
def tc(request):
    return render(request, 't&c.html')

def search2(request):
    return render(request, 'search2.html')
def find(request):
    mycursor = conn.cursor()
    global num
    num = request.POST['number']
    print(num)
    mycursor.execute("SELECT * from stadium_ticket where ticket = %s;", [num])
    b = mycursor.fetchone()
    if not b:
        messages.info(request, 'Invalid ticket number')
        mycursor.close()
        return redirect("/search2/")
    else:
        mycursor.execute("SELECT snacks from stadium_snacks where snacks_id = %s", [b[10]])
        c = mycursor.fetchone()
        mycursor.close()
        return render(request, 'cancel.html', {"b":b, "c":c})
    mycursor.close()

def cancel(request):
    mycursor = conn.cursor()
    mycursor.execute("select seat, match_id from stadium_ticket where ticket = %s", [num])
    b = mycursor.fetchone()
    seat = b[0]
    match = b[1]
    mycursor.execute(f"Update stadium_seats set S{seat} = {seat} where match_id = {match}")
    mycursor.execute("delete from stadium_ticket where ticket = %s", [num])
    mycursor.close()
    return render(request, 'index.html')

def ticket(request):
    if request.method == 'POST':
        # cursor = connection.cursor()
        mycursor = conn.cursor()
        cno = request.POST['Cno']
        expiry = request.POST['expiry']
        cvv = request.POST['cvv']
        month = expiry[0]+expiry[1]
        year = expiry[3]+expiry[4]
        if len(cno)!=12 or not cno.isdigit():
            messages.info(request, 'Invalid Card number')
            return redirect("/payment/")
        elif len(expiry)!=5 or expiry[2]!='/' or not (month.isdigit() and year.isdigit()) or (int(month)>0 and int(month)<=12):
            messages.info(request , 'Invalid expiry')
            return redirect("/payment/")
        elif len(cvv)!=3 or not cvv.isdigit():
            messages.info(request, 'Invalid cvv')
            return redirect("/payment/")
        else:
            mycursor.execute("SELECT name, date, city, stadium, time from stadium_matches where match_id = %s", [match])
            b = mycursor.fetchone()
            tick = 'BOOK'
            if match<10:
                tick = tick+'0'+'0'+ str(match)
            elif match<100:
                tick =tick + '0'+str(match)
            else:
                tick +=str(match)
            if seat<10:
                tick=tick+'0'+str(seat)
            else:
                tick+=str(seat)
            temp = Price + 1500
            current_user = request.user
            mycursor.execute("Insert into myproject.stadium_ticket values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [tick, current_user.username, b[0], match, b[3], b[2], b[1], b[4], seat, temp, snacks])
            mycursor.execute("SELECT snacks from stadium_snacks where snacks_id = %s", [snacks])
            c = mycursor.fetchone()
            mycursor.execute(f"Update stadium_seats set S{seat} = 0 where match_id = {match}")
            mycursor.close()
            return render(request, 'ticket.html', {"b":b, "temp":temp, "tick":tick, "c":c, "seat":seat})
    return render(request, 'ticket.html')

def payment(request):
    if request.method == 'POST':
        mycursor = conn.cursor()
        snk = request.POST['snk']
        value = request.POST['radio'] 
        if snk!="default":
            mycursor.execute("SELECT price from stadium_snacks where snacks_id = %s", [snk])
            b = mycursor.fetchone()
            global Price
            Price = b[0]
            global snacks
            snacks = int(snk)
        else:
            snacks = 0
        global seat
        seat = int(value)
        mycursor.close()
        return render(request, 'payment.html', {"value":value, "snack":snk})
    return render(request, 'payment.html')

def seats2(request):
    results4 = showsnack.objects.all()
    if request.method=='POST':
        mycursor = conn.cursor()
        global match
        match = int(request.POST['radio'])
        mycursor.execute("SELECT S1, S2, S3, S4, S5, S6, S7, S8, S9, S10 from stadium_seats where match_id = %s;", [match])
        b = mycursor.fetchall()[0]
        mycursor.close()
        return render(request, 'seats2.html', {"b":b, "results4":results4})


def seats(request):
    if request.method == 'POST':
        mycursor = conn.cursor()
        city = request.POST['Cityname']
        date = request.POST['Date']
        match = request.POST['Match']
        if match=='default'and city == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s;", [date])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect("/search/")
            return render(request, 'seats.html', {"b":b})
        elif match == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and city = %s", [date, city])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect("/search/")
            mycursor.close()
            return render(request, 'seats.html', {"b":b})
        elif city == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and match_id = %s", [date, match])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect('/search/')
            return render(request, 'seats.html', {"b":b})
        else:
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and match_id = %s and city = %s", [date, match, city])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect("/search/")
            mycursor.close()
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