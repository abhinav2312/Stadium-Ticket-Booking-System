from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import snacks, stadium, ticket, book, matches, seats
from django.db import transaction, connection
import mysql.connector
# Create your views here.

# conn = mysql.connector.connect(
#   host="localhost",
#   user="root",
#   password="ABHI@123",
#   database="myproject"
# )
num = 'BOOK'
match = 0
Price = 1500
seat = 0
snacks = 0
temp2 = 0
name = 'name'
date = '2022-05-04'
stad = 0
def index(request):
    return render(request, 'index.html', )

def login(request):
    return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')
    
def tc(request):
    return render(request, 't&c.html')

def search2(request):
    results3 = stadium.objects.all().values_list('name', flat = True).distinct()
    return render(request, 'search2.html', {"results3":results3})
    
def find(request):
    if 'ticket_cancel' in request.POST:
        current_user = request.user
        global temp2
        temp2 = 0
        mycursor = connection.cursor()
        global num
        num = request.POST['number']
        mycursor.execute("SELECT * from stadium_ticket where ticket = %s", [num])
        b = mycursor.fetchone()
        if not b:
            messages.info(request, 'Invalid ticket number')
            mycursor.close()
            return redirect("/search2/")
        elif current_user.username != b[1]:
            messages.info(request, 'Cannot access that ticket')
            mycursor.close()
            return redirect("/search2/")
        else:
            mycursor.execute("SELECT snacks from stadium_snacks where snacks_id = %s", [b[10]])
            c = mycursor.fetchone()
            mycursor.close()
            return render(request, 'cancel.html', {"b":b, "c":c, "temp2":temp2})
    elif 'stadium_cancel' in request.POST:
        temp2 = 1
        mycursor = connection.cursor()
        global name
        name = request.POST['game']
        global date
        date = request.POST['date']
        mycursor.execute("Select * from stadium_book where date = %s and name = %s", [date, name])
        b = mycursor.fetchone()
        if not b:
            messages.info(request, 'Stadium not available')
            mycursor.close()
            return redirect("/search2/")
        else:
            return render(request, 'cancel.html', {"b":b, "temp2":temp2})

def cancel(request):
    if temp2 == 0:
        mycursor = connection.cursor()
        mycursor.execute("select seat, match_id from stadium_ticket where ticket = %s", [num])
        b = mycursor.fetchone()
        seat = b[0]
        match = b[1]
        mycursor.execute(f"update stadium_seats set S{seat} = {seat} where match_id = {match}")        
        mycursor.execute("delete from stadium_ticket where ticket = %s", [num])
        mycursor.close()
        return render(request, 'index.html')
    else:
        mycursor = connection.cursor()
        mycursor.execute("delete from stadium_book where date = %s and name = %s", [date, name])
        mycursor.close()
        return render(request, 'index.html')
def ticket(request):
    if request.method == 'POST':
        mycursor = connection.cursor()
        cno = request.POST['Cno']
        expiry = request.POST['expiry']
        cvv = request.POST['cvv']
        month = expiry[0]+expiry[1]
        year = expiry[3]+expiry[4]
        if len(cno)!=12 or not cno.isdigit():
            messages.info(request, 'Invalid Card number')
            mycursor.close()
            return redirect("/payment/")
        elif len(expiry)!=5 or expiry[2]!='/' or not (month.isdigit() and year.isdigit()) or (int(month)>0 and int(month)<=12):
            messages.info(request , 'Invalid expiry')
            mycursor.close()
            return redirect("/payment/")
        elif len(cvv)!=3 or not cvv.isdigit():
            messages.info(request, 'Invalid cvv')
            mycursor.close()
            return redirect("/payment/")
        else:
            if temp2 == 0:
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
                current_user = request.user
                mycursor.execute("Insert into stadium_ticket values(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", [tick, current_user.username, b[0], match, b[3], b[2], b[1], b[4], seat, Price, snacks])
                mycursor.execute("SELECT snacks from stadium_snacks where snacks_id = %s", [snacks])
                c = mycursor.fetchone()
                mycursor.execute(f"Update stadium_seats set S{seat} = 0 where match_id = {match}")
                mycursor.close()
                return render(request, 'ticket.html', {"b":b, "Price":Price, "username":current_user.username, "tick":tick, "c":c, "seat":seat, "temp2":temp2})
            else:
                mycursor.execute("SELECT game, name, city, pin, rent from stadium_stadium where stadium_id = %s", [stad])
                b = mycursor.fetchone()
                current_user = request.user
                print(b)
                mycursor.execute("Insert into stadium_book values(NULL, %s, %s, %s, %s, %s, %s, %s, %s)", [stad, b[0], b[1], date, current_user.username, b[2], b[3], b[4]])
                mycursor.close()
                return render(request, 'ticket.html', {"temp2":temp2, "b":b, "date":date, "username":current_user.username})
    return render(request, 'ticket.html')

def payment(request):
    if 'stad' in request.POST:
        mycursor = connection.cursor()
        global temp2
        temp2 = 1
        global stad
        stad = int(request.POST['radio'])
        mycursor.execute("SELECT rent from stadium_stadium where stadium_id = %s", [stad])
        global Price
        Price = mycursor.fetchone()[0]
        mycursor.close()
        return render(request, 'payment.html', {"Price":Price})
    elif 'tick' in request.POST:
        mycursor = connection.cursor()
        temp2 = 0
        snk = request.POST['snk']
        value = request.POST['radio'] 
        if snk!="default":
            mycursor.execute("SELECT price from stadium_snacks where snacks_id = %s", [snk])
            b = mycursor.fetchone()
            Price = 1500 + b[0]
            global snacks
            snacks = int(snk)
        else:
            Price = 1500
            snacks = 0
        global seat
        seat = int(value)
        mycursor.close()
        return render(request, 'payment.html', {"Price":Price})
    else:
        return render(request, 'payment.html', {"Price":Price})

def seats2(request):
    mycursor = connection.cursor()
    mycursor.execute("SELECT snacks_id, snacks from stadium_snacks")
    results4 = mycursor.fetchall()
    if request.method=='POST':
        global match
        match = int(request.POST['radio'])
        mycursor.execute("SELECT S1, S2, S3, S4, S5, S6, S7, S8, S9, S10 from stadium_seats where match_id = %s;", [match])
        b = mycursor.fetchone()
        if b:
            mycursor.close()
            return render(request, 'seats2.html', {"b":b, "results4":results4})
        else:
            messages.info(request, 'Stadium is full')
            return redirect('/search/')


def seats(request):
    if request.method == 'POST':
        mycursor = connection.cursor()
        city = request.POST['Cityname']
        date = request.POST['Date']
        match = request.POST['Match']
        game = request.POST['game']
        if match=='default'and city == 'default' and game == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s;", [date])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect("/search/")
            mycursor.close()
            return render(request, 'seats.html', {"b":b})
        elif match == 'default' and game == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and city = %s", [date, city])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect("/search/")
            mycursor.close()
            return render(request, 'seats.html', {"b":b})
        elif city == 'default' and game == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and match_id = %s", [date, match])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect('/search/')
            mycursor.close()
            return render(request, 'seats.html', {"b":b})
        elif city == 'default' and match == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and game = %s", [date, game])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect('/search/')
            mycursor.close()
            return render(request, 'seats.html', {"b":b})
        elif city =='default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and match_id = %s and game = %s", [date, match, game])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect('/search/')
            mycursor.close()
            return render(request, 'seats.html', {"b":b})
        elif match == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and city = %s and game = %s", [date, city, game])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect('/search/')
            mycursor.close()
            return render(request, 'seats.html', {"b":b})
        elif game == 'default':
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and city = %s and match_id = %s", [date, city, match])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect('/search/')
            mycursor.close()
            return render(request, 'seats.html', {"b":b})
        else:
            mycursor.execute("SELECT name, city, date, match_id FROM stadium_matches where date = %s and match_id = %s and city = %s and game = %s", [date, match, city, game])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'No matches found')
                mycursor.close()
                return redirect("/search/")
            mycursor.close()
            return render(request, 'seats.html', {"b":b})
        
def search(request):
    results = stadium.objects.all().values_list('city', flat=True).distinct()
    results3 = stadium.objects.all().values_list('game', flat = True).distinct()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user is not None:
            auth.login(request, user)
            return render(request, 'search.html', {"results":results, "results3":results3})
        else:
            messages.info(request, 'Invalid credentials')
            return redirect('/login/')
    else:
        return render(request, 'search.html', {"results":results, "results3":results3})
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

def pp(request):
    return render(request, 'privacypolicy.html')

def stadiumupdates(request):
    mycursor = connection.cursor()
    mycursor.execute("SELECT * from stadium_matches order by date")
    b = mycursor.fetchall()
    mycursor.close()
    return render(request, 'stadiumupdates.html', {"b":b})

def account(request):
    current_user = request.user
    name = current_user.get_full_name
    email = current_user.email
    username = current_user.username
    mycursor = connection.cursor()
    mycursor.execute("SELECT * from stadium_ticket where username = %s", [username])
    b = mycursor.fetchall()
    mycursor.execute("SELECT * from stadium_book where username = %s", [username])
    c = mycursor.fetchall()
    print(c)
    mycursor.close()
    return render(request, 'account.html', {"name":name, "username":username, "email":email, "b":b, "c":c})

def search3(request):
    if request.method == 'POST':
        mycursor = connection.cursor()
        city = request.POST['Cityname']
        global date
        date = request.POST['Date']
        game = request.POST['game']
        if city == 'default' and game == 'default':
            mycursor.execute("select * from stadium_stadium where stadium_id not in (select stadium_id from stadium_matches where date = %s) and stadium_id not in (select stadium_id from stadium_book where date = %s);",[date, date])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'Stadium Not availabe')
                mycursor.close()
                return redirect('/search/')
            mycursor.close()
            return render(request, 'book.html', {"b":b})
        elif city == 'default':
            mycursor.execute("select * from stadium_stadium where stadium_id not in (select stadium_id from stadium_matches where date = %s) and stadium_id not in (select stadium_id from stadium_book where date = %s) and game = %s;",[date, date, game])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, "Stadiums Not available")
                mycursor.close()
                return redirect('/search/')
            mycursor.close()
            return render(request, 'book.html', {"b":b})
        elif game == 'default':
            mycursor.execute("select * from stadium_stadium where stadium_id not in (select stadium_id from stadium_matches where date = %s) and stadium_id not in (select stadium_id from stadium_book where date = %s) and city = %s;",[date, date, city])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'Stadium Not availablefound')
                mycursor.close()
                return redirect('/search/')
            mycursor.close()
            return render(request, 'book.html', {"b":b})
        else:
            mycursor.execute("select * from stadium_stadium where stadium_id not in (select stadium_id from stadium_matches where date = %s) and stadium_id not in (select stadium_id from stadium_book where date = %s) and game = %s and city = %s;",[date, date, game, city])
            b = mycursor.fetchall()
            if len(b) == 0:
                messages.info(request, 'Stadiums Not available')
                mycursor.close()
                return redirect('/search/')
            mycursor.close()
            return render(request, 'book.html', {"b":b})
