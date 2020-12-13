from flask import Flask, request, redirect, jsonify
from flask import render_template
from flask_cors import CORS, cross_origin
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import xml.etree.ElementTree as ET
from haversine import haversine
import pandas as pd
import sys
import pymysql

app = Flask(__name__)
CORS(app)
app.config['JSON_AS_ASCII'] = False

gpslist = []
information = []
name = []
pos = []
dbresult = ()
db = pymysql.connect(host='127.0.0.1', port=330, user='root', passwd='0000', db='mountain', charset='utf8')
cursor = db.cursor()
sql = 'select * from data'
cursor.execute(sql)
dbresult = cursor.fetchall()
tmp = dbresult
db.close()

@app.route('/result.html')
def resultlist():
    global gpslist
    print(gpslist)
    return render_template('result.html', lists = gpslist)

def namefind():
    print('calculate!')
    global name, pos, dbresult
    API_KEY = unquote(
        'Kta%2F9Kod3QYKj5%2BGOCSeMwH8Btt6f16uCKiNN9bBUk0wQYtxIquqcwZ%2FP8DAKIvSZE%2FZbjQgR87dRZI9fszUTw%3D%3D')
    tname = unquote(name)
    tpos = unquote(pos)
    url = 'http://openapi.forest.go.kr/openapi/service/cultureInfoService/gdTrailInfoOpenAPI'
    queryParams = '?' + urlencode(
        {quote_plus('ServiceKey'): API_KEY, quote_plus('searchMtNm'): tname, quote_plus('searchArNm'): tpos,
         quote_plus('pageNo'): '1', quote_plus('numOfRows'): '10'})

    request = Request(url + queryParams)
    request.get_method = lambda: 'GET'
    response_body = urlopen(request).read()
    xtree = (ET.fromstring(response_body))
    xroot = xtree.findall('body/items/item')

    global gpslist
    global information

    gpslist = []

    for node in xroot:
        n_mntcd = node.find('mntcd')
        n_mntnm = node.find('mntnm')
        n_submn = node.find('subnm')
        n_mntheight = node.find('mntheight')
        n_aeatreason = node.find('aeatreason')
        n_overview = node.find('overview')
        n_adetails = node.find('details')
        n_tourisminf = node.find('tourisminf')
        n_etccourse = node.find('etccourse')

        infolist = []
        infolist.append(n_mntcd)
        infolist.append(n_mntnm)
        infolist.append(n_submn)
        infolist.append(n_mntheight)
        infolist.append(n_aeatreason)
        infolist.append(n_overview)
        infolist.append(n_adetails)
        infolist.append(n_tourisminf)
        infolist.append(n_etccourse)

        information.append(infolist)

        for name, lat, lot in dbresult:
            #print(n_mntnm.text, name, lat, lot)
            if (n_mntnm.text == name):
                smalllist = []
                smalllist.append(n_mntnm.text)
                smalllist.append(lat)
                smalllist.append(lot)
                gpslist.append(smalllist)

    return redirect("/result.html")

'''
@app.route("/")
def database():
    my_res = Flask.response()
    my_res.headers.add("Access-Control-Allow-Origin", "*")
    return render_template("view.html")
    '''

@app.route('/test')
def test():
    return render_template('test.html')

@app.route('/result', methods = ['POST', 'GET'])
def result():
    if request.method == 'POST':
        global name, pos
        requests = request.form
        for key in requests.keys():
            for value in requests.getlist(key):
                print (key, ":", value)

        name = request.form['name']
        pos = request.form['local']
        namefind()
        return redirect("/result.html")

@app.route("/index.html")
def index():
    return render_template("index.html")

@app.route("/portfolio-details.html", methods = ['POST', 'GET'])
def pro():
    if request.method == 'POST':
        mnname = request.form
        for key in mnname.keys():
            for value in mnname.getlist(key):
                print (key, ":", value)

    return render_template("portfolio-details.html")

@app.route("/ppt.html")
def ppt():
        return render_template("ppt.html")

@app.route("/inner-page.html")
def inner(name):
    return render_template("inner-page.html")

@app.route("/service.html")
def service():
    return render_template("service.html")

@app.route("/hiking.html")
def hiking():
    return render_template("gpxviewer.html")

tmp2 = []
tmp3 = []
tmp33 = []
tmp4 = []
tmp5 = []
passdata = 0.0
@app.route('/', methods=['GET','POST'])
def pos():
    global tmp33
    passdata = 0
    if request.method == 'POST':
        try:
            tmp3 = []
            value = request.form['form_name']
            value = str(value)
            arr = value.split("/")
            lat = float(arr[0])
            lon = float(arr[1])
            my_loc = (lat, lon)
            for a, b, c in tmp:
                tmp2 = []
                com_loc = (float(b), float(c))
                passdata = haversine(my_loc, com_loc)
                passdata = round(passdata, 2)

                tmp2.insert(0, a)
                tmp2.insert(1, passdata)
                tmp3.append(tmp2)

            print(str(tmp3))
            tmp33 = tmp3

            tmp3.sort(key=lambda x: x[1])
            if len(tmp3) > 10:
                tmp6 = []
                for i in range(0, 10):
                    tmp6.append(tmp3[i])
                return render_template('view.html', getdata=tmp3[9][1], getlist=tmp6)

            #com_loc = (36.984651947738186, 128.25628173348173)
            #passdata = haversine(my_loc, com_loc)
            #passdata = round(passdata, 2)
            #print(str(passdata) + "km")
            return render_template('view.html', getdata=tmp3[len(tmp3)-1][1], getlist=tmp3)
        except:
            try:
                value = request.form['form_name2']
                value = str(value)
                print(value)
                tmp5 = []
                value = round(float(value), 2)
                for a,b in tmp33:
                    if value > b:
                        tmp4 = []
                        tmp4.insert(0, a)
                        tmp4.insert(1, b)
                        tmp5.append(tmp4)
                return render_template('view.html', getdata=value, getlist=tmp5)
            except:
                value = request.form['form_name3']
                value = str(value)
                print(value)
                tmp5 = []
                value = round(float(value), 2)
                for a,b in tmp33:
                    if value > b:
                        tmp4 = []
                        tmp4.insert(0, a)
                        tmp4.insert(1, b)
                        tmp5.append(tmp4)
                return render_template('view.html', getdata=value, getlist=tmp5)

    else:
        return render_template('view.html', getdata=0)


if __name__ == "__main__":
    app.run()
