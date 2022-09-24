from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
import requests
from bs4 import BeautifulSoup
from tensorflow.keras.models import *
import tensorflow as tf
from tensorflow import Graph
import numpy as np
from keras.preprocessing import image
from django.core.files.storage import FileSystemStorage
from wwo_hist import retrieve_hist_data
import pandas as pd
import pandas as pd
import numpy as np
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import date
import dateutil
import googletrans
from googletrans import Translator

"""model_graph = Graph()
with model_graph.as_default():
    tf_session = tf.compat.v1.Session()
    with tf_session.as_default():
        model=load_model('./models/plantdis1.h5')
"""
model=load_model('./models/abc.h5')

# Create your views here.
def index(request):
    return render(request,'index.html')

def farmerlogin(request):
    return render(request,'farmer_login.html')

def volunteerlogin(request):
    return render(request,'volunteer_login.html')

def selectcity(request):
    if request.method=="POST":
        global vname
        vname=request.POST['state']
        URL=''
        URL='https://market.todaypricerates.com/'+vname+'-vegetables-price'
        print(URL)
        r=requests.get(URL)
        soup=BeautifulSoup(r.text,'html.parser')
        states=["Select your area"]
        for tag in soup.find_all('tfoot'):
            for t in tag.find_all('a'):
                states.append(t.text)
        return render(request,'select_city.html',{"states":states,"visible":"visible"})

def selectcity1(request):
    if request.method=="POST":
        cname=request.POST['state1']
        URL='https://market.todaypricerates.com/'+cname+'-vegetables-price-in-'+vname
        print(URL)
        r=requests.get(URL)
        soup=BeautifulSoup(r.text,'html.parser')
        v=[]
        for row in soup.find_all('div',attrs={'class':'Row'}):
            t=[]
            for r in row.find_all('div',attrs={'class':'Cell'}):
                t.append(r.text)
            v.append(t)
        print(v)
        return render(request,'prices.html',{"prices":v})

    return render(request,'select_city.html',{"visible":"hidden"})

def farmersignup(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        pno=request.POST['pno']
        village=request.POST['village']
        district=request.POST['district']
        state=request.POST['state']
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        if(farmer.objects.filter(uname=uname)):
            print("user name should be unique");
        else:
            farmer.objects.create(fname=fname,lname=lname,pno=pno,village=village,district=district,state=state,uname=uname,pwd=pwd)
            print("created successfully")
            return render(request,'farmer_login.html')
    else:
        return render(request,'farmer_signup.html')

def farmerlogin(request):
    if request.method == 'GET':
        return render(request,'farmer_login.html')
    else:
        username = request.POST['uname']
        password = request.POST['psw']
        try :
            farmer_object = farmer.objects.get(uname=username)
        except :
            print("No such user exists")
            return render(request,'farmer_login.html', context={'error': 'No such user exists'})

        if farmer_object.pwd == password :
            request.session['member_id'] = farmer_object.id
            return redirect('/predictindex')
        else:
            print("your username and password didn't match")
            return render(request,'farmer_login.html', context={'error': 'our username and password does not match'})

def volunteersignup(request):
    if request.method=="POST":
        fname=request.POST['fname']
        lname=request.POST['lname']
        pno=request.POST['pno']
        village=request.POST['village']
        district=request.POST['district']
        state=request.POST['state']
        uname=request.POST['uname']
        pwd=request.POST['pwd']
        des=request.POST['des']
        if(volunteer.objects.filter(uname=uname)):
            print("user name should be unique")
        else:
            volunteer.objects.create(fname=fname,lname=lname,pno=pno,village=village,district=district,state=state,uname=uname,pwd=pwd,des=des)
            print("created successfully")
            return render(request,'volunteer_login.html')
    return render(request,'volunteer_signup.html')

def volunteerlogin(request):
    if request.method == 'GET':
        return render(request,'volunteer_login.html')
    else:
        username = request.POST['uname']
        password = request.POST['psw']
        try :
            volunteer_object = volunteer.objects.get(uname=username)
        except :
            print("No such user exists")
            return render(request,'volunteer_login.html', context={'error': 'No such user exists'})

        if volunteer_object.pwd == password :
            request.session['v_member_id'] = volunteer_object.id
            return render(request,'volunteer_dash.html')
        else:
            print("your username and password didn't match")
            return render(request,'volunteer_login.html', context={'error': 'our username and password does not match'})

def questions(request):
    qobj = list(question.objects.filter(far_id=request.session['member_id']))
    print(qobj,request.session['member_id'])
    return render(request,'questions.html',context={'q':qobj})

def questions1(request):
    vobj = volunteer.objects.get(id=request.session['v_member_id'])
    qobj = list(question.objects.all())
    que=[]
    for q in qobj:
        if q.far.village.lower()==vobj.village.lower() or q.far.district.lower()==vobj.district.lower():
            que.append(q)
    print(que)
    return render(request,'questions1.html',context={'que':que})

def newques(request):
    if request.method == 'GET':
        return render(request,'newques.html')
    txt=request.POST['q1']
    farmer_object = farmer.objects.get(id=request.session['member_id'])
    que=question(ques=txt,far=farmer_object)
    que.save()
    qobj = list(question.objects.filter(far_id=request.session['member_id']))
    return render(request,'questions.html',context={'q':qobj})

def queshigh(request):
    q=request.POST['ques']
    q=q.split(" ")
    print(type(q),q)
    q_object = question.objects.get(id=int(q[2][1:-1]))
    l=list(q_object.comsf.all())
    l1=list(q_object.comsv.all())
    return render(request,'qhigh.html',context={'q':q_object,'qobj':l,'qobj1':l1})

def queshigh1(request):
    q=request.POST['ques']
    q=q.split(" ")
    print(type(q),q)
    q_object = question.objects.get(id=int(q[2][1:-1]))
    l=list(q_object.comsf.all())
    l1=list(q_object.comsv.all())
    return render(request,'qhigh1.html',context={'q':q_object,'qobj':l,'qobj1':l1})

def comsub(request):
    txt=request.POST['c1']
    farmer_object = farmer.objects.get(id=request.session['member_id'])
    f1=far_comment(com=txt,far=farmer_object)
    f1.save()
    q=request.POST['qc']
    q=q.split(" ")
    q_object = question.objects.get(id=int(q[2][1:-1]))
    q_object.comsf.add(f1)
    l=list(q_object.comsf.all())
    print(l)
    l1=list(q_object.comsv.all())
    return render(request,'qhigh.html',context={'qobj':l,'q':q_object,'qobj1':l1})

def comsub1(request):
    txt=request.POST['c1']
    vol_object = volunteer.objects.get(id=request.session['v_member_id'])
    f1=vol_comment(com=txt,vol=vol_object)
    f1.save()
    q=request.POST['qc']
    q=q.split(" ")
    q_object = question.objects.get(id=int(q[2][1:-1]))
    q_object.comsv.add(f1)
    l=list(q_object.comsf.all())
    l1=list(q_object.comsv.all())
    return render(request,'qhigh1.html',context={'q':q_object,'qobj':l,'qobj1':l1})

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    return render(request, 'index.html')

def predictindex(request):
    try:
        if(request.session['member_id']):
            return render(request,'predictindex.html')
    except KeyError:
        return redirect('/')

def volunteerdash(request):
    try:
        if(request.session['v_member_id']):
            return render(request,'volunteer_dash.html')
    except KeyError:
        return redirect('/')

def diseaseupload(request):
    try:
        if(request.session['member_id']):
            return render(request,'disease_upload.html',context={"v":"hidden"})
    except KeyError:
        return redirect('/')

def citySelect(request):
    try:
        if(request.session['member_id']):
            return render(request,'city_select.html')
    except KeyError:
        return redirect('/')

d={0: 'Apple___Apple_scab',
 1: 'Apple___Black_rot',
 2: 'Apple___Cedar_apple_rust',
 3: 'Apple___healthy',
 4: 'Cherry___healthy',
 5: 'Cherry___Powdery_mildew',
 6: 'Corn___Cercospora_leaf_spot_Gray_leaf_spot',
 7: 'Corn___Common_rust',
 8: 'Corn___healthy',
 9: 'Corn___Northern_Leaf_Blight',
 10: 'Grape___Black_rot',
 11: 'Grape___Esca_(Black_Measles)',
 12: 'Grape___healthy',
 13: 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)',
 14: 'Orange___Haunglongbing_(Citrus_greening)',
 15: 'Peach___Bacterial_spot',
 16: 'Peach___healthy',
 17: 'Pepper,_bell___Bacterial_spot',
 18: 'Pepper,_bell___healthy',
 19: 'Potato___Early_blight',
 20: 'Potato___healthy',
 21: 'Potato___Late_blight',
 22: 'Squash___Powdery_mildew',
 23: 'Strawberry___healthy',
 24: 'Strawberry___Leaf_scorch',
 25: 'Tomato___Bacterial_spot',
 26: 'Tomato___Early_blight',
 27: 'Tomato___healthy',
 28: 'Tomato___Late_blight',
 29: 'Tomato___Leaf_Mold',
 30: 'Tomato___Septoria_leaf_spot',
 31: 'Tomato___Spider_mites Two-spotted_spider_mite',
 32: 'Tomato___Target_Spot',
 33: 'Tomato___Tomato_mosaic_virus',
 34: 'Tomato___Tomato_Yellow_Leaf_Curl_Virus'}

def predictImage(request):
    fileObj=request.FILES['filePath']
    sname=request.POST['state']
    fs=FileSystemStorage()
    filePathName=fs.save(fileObj.name,fileObj)
    filePathName=fs.url(filePathName)
    print(filePathName)
    filePathName=filePathName.replace("%20"," ")
    print(filePathName)
    testimage='.'+filePathName
    print(testimage)
    test_image = image.load_img(testimage, target_size = (200, 200))
    test_image = image.img_to_array(test_image)
    test_image = np.expand_dims(test_image, axis = 0)
    test_image = test_image/255.0
    result = model.predict(test_image)
    o=np.argmax(result)
    print(o)
    f = open("./models/pd1.txt", errors="ignore")
    txt=f.read()
    data=txt.split("\n")
    while("" in data) :
        data.remove("")
    n=[]
    dis=[]
    s=[]
    for i in range(0,len(data)-3,3):
        n.append(data[i])
        dis.append(data[i+1])
        s.append(data[i+2])
    d1={}
    d2={}
    d3={}
    for i in range(len(n)):
        d1[i]=n[i]
        d2[i]=dis[i]
        d3[i]=s[i]
    print(d1)
    print(d)
    j=-1
    for i in range(len(d1)):
        if d[o]==d1[i]:
            j=i
            print(d1[j])
            break
    if j==-1:
        context={'name':"The plant seems to be in good health"}
        return render(request,'disease_upload.html',context)
    else:
        translator = Translator()
        translation = translator.translate(d1[j], dest=sname)
        translation1 = translator.translate(d2[j], dest=sname)
        translation2 = translator.translate(d3[j], dest=sname)
        print(translation.text)
        context={'name':d1[j],'des':d2[j],'sol':d3[j],'tname':translation.text,'tdes':translation1.text,'tsol':translation2.text}
        return render(request,'disease_upload.html',context)

def weatherfetch(request):
    city = request.POST['city']
    print(city)
    frequency=3
    date1 = date.today()
    today=date1.strftime("%d-%b-%Y")
    delta = dateutil.relativedelta.relativedelta(months=3)
    start_date = date1 - delta
    start_date=start_date.strftime("%d-%b-%Y")
    end_date = today
    api_key = '16b811a4836e4dd5ac941230210606'
    location_list = [city]
    try:
        hist_weather_data = retrieve_hist_data(api_key,
                                    location_list,
                                    start_date,
                                    end_date,
                                    frequency,
                                    location_label = False,
                                    export_csv = True,
                                    store_df = True)
    except Exception as e:
        return render(request,'city_select.html',context={"error":"Sorry, this city content is not available"})
    data = pd.read_csv(city+".csv",index_col=0)
    df=data[::-1]
    df=df[:231]
    data_html = df.to_html()
    features=['maxtempC','mintempC','humidity','precipMM','pressure','tempC']
    df_f=data[features].values
    df_f1=data['tempC'].values
    df_f2=data['precipMM'].values
    df_f3=data['humidity'].values

    X=[]
    y=[]
    y1=[]
    y2=[]
    for i in range(30,len(df_f)-31,1):
        X.append(df_f[i-30:i])
        y.append(df_f1[i])
        y1.append(df_f2[i])
        y2.append(df_f3[i])

    X=np.array(X)
    y=np.array(y)
    y1=np.array(y1)
    y2=np.array(y2)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.2)
    X_train1, X_test1, y_train1, y_test1 = train_test_split(X, y1, test_size = 0.2)
    X_train2, X_test2, y_train2, y_test2 = train_test_split(X, y2, test_size = 0.2)

    X_train=X_train.reshape(len(X_train),-1)
    X_test=X_test.reshape(len(X_test),-1)
    X_train1=X_train1.reshape(len(X_train1),-1)
    X_test1=X_test1.reshape(len(X_test1),-1)
    X_train2=X_train2.reshape(len(X_train2),-1)
    X_test2=X_test2.reshape(len(X_test2),-1)

    rf = make_pipeline(StandardScaler(),RandomForestRegressor())
    rf1 = make_pipeline(StandardScaler(),RandomForestRegressor())
    rf2 = make_pipeline(StandardScaler(),RandomForestRegressor())

    rf.fit(X_train, y_train)
    rf1.fit(X_train1, y_train1)
    rf2.fit(X_train2, y_train2)

    d1=rf.predict([df_f[1:31].reshape(-1)])
    d2=rf1.predict([df_f[1:31].reshape(-1)])
    d3=rf2.predict([df_f[1:31].reshape(-1)])
    context = {'loaded_data': data_html,'temp':d1[0],'precip':round(d2[0],3),'humidity':d3[0],'cname':city}
    return render(request,'weather_data.html',context)
