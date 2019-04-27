from django.shortcuts import render
from django.http import HttpResponse
from Fyle.config import properties
import psycopg2
from django.template.loader import get_template


# Create your views here.
def homepage(request):
    return render(request, 'FyleApp/home.html')

def search_form(request):
    return render(request, 'FyleApp/search_form.html')

def search(request):
    if 'q' in request.GET:
        search_for=request.GET['q']
        res= db_conn(search_for)
        print(res,"res")

        if(not(res)):
            return HttpResponse('<h1 style="color:red; margin:5%; text-align:center">Data Not Found!</h1>')
        t = get_template('ifsc_result.html')
        html = t.render({'result': res})
        return HttpResponse(html)
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

def db_conn(q):
    conn_info = {
        'host': properties.host,
        'port': properties.port,
        'user': properties.user,
        'password': properties.password,
        'database': properties.database,
            }

    # simple connection, with manual close
    connection = psycopg2.connect(**conn_info)
    # dothings
    con = connection.cursor()
    con.execute("select * from bank_branches where ifsc="+"'"+q+"';")
    result = 'Ankita'
    result = con.fetchone()
    if (not(result) ):
        return result
    # print(result)
    num_fields = len(con.description)
    field_names = [i[0] for i in con.description]
    details = {}
    for f in range(0,num_fields):
        details[field_names[f]]=result[f]
    return details

def search_bank_branches_form(request):
    return render(request, 'FyleApp/search_banks_form.html')

def search_banks(request):
    if ('q' in request.GET and 'p' in request.GET) :
        name=request.GET['p']
        city=request.GET['q']
        message = 'You searched for: %r' % name
        res= connect_db(name,city)
        print(res)
        lenres=len(res)
        if (lenres== 0):
            return HttpResponse('<h1 style="color:red; margin:5%; text-align:center">Data Not Found!</h1>')
        # return{'result':res}
        # render(request,"ifsc_result.html", res)
        t = get_template('bank_branches.html')
        html = t.render({'result': res,'count':lenres,'city':city,'bank':name})
        return HttpResponse(html)
    else:
        message = 'You submitted an empty form.'
    return HttpResponse(message)

def connect_db(p,q):
    conn_info = {
        'host': properties.host,
        'port': properties.port,
        'user': properties.user,
        'password': properties.password,
        'database': properties.database,
            }

    # simple connection, with manual close
    connection = psycopg2.connect(**conn_info)
    # dothings
    con = connection.cursor()

    query = "select * from bank_branches where bank_name=" + "'" +p.upper() + "'" +" and city=" + "'" + q.upper() + "';"
    # print(query)
    con.execute(query)

    result = 'Ankita'
    result = con.fetchall()
    # print(result,"result")
    if (len(result) == 0):
        return result
    num_fields = len(con.description)
    field_names = [i[0] for i in con.description]
    data=[]
    for f in result:
        details = {}
        details[field_names[0]] = f[0]
        details[field_names[1]] = f[1]
        details[field_names[2]] = f[2]
        details[field_names[3]] = f[3]
        details[field_names[4]] = f[4]
        details[field_names[5]] = f[5]
        details[field_names[6]] = f[6]
        details[field_names[7]] = f[7]
        data.append(details)



    # print(data,"details")
    return data