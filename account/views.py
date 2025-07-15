from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import *
import requests
from bs4 import BeautifulSoup
import numpy as np
from django.core.files.storage import FileSystemStorage
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from datetime import date
import dateutil
import os
import logging
from .models import Resource
from .models import Message
from django.db import models
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta

# Set up logging
logger = logging.getLogger(__name__)

# Remove top-level model loading
model = None

def get_model():
    global model
    if model is None:
        from tensorflow.keras.models import load_model
        from django.conf import settings
        import os
        model_path = os.path.join(settings.BASE_DIR, 'ml_models', 'abc.h5')
        if os.path.exists(model_path):
            model = load_model(model_path)
            print("Model loaded successfully")
        else:
            print(f"Model file not found at {model_path}")
            model = None
    return model

# Create your views here.
def index(request):
    farmer_id = request.session.get('member_id')
    volunteer_id = request.session.get('v_member_id')
    context = {
        'is_farmer': bool(farmer_id),
        'is_volunteer': bool(volunteer_id),
    }
    return render(request, 'index.html', context)

def volunteerlogin(request):
    if request.session.get('v_member_id'):
        return redirect('/volunteerdash')
    return render(request,'volunteer_login.html')

def selectcity(request):
    if request.method=="POST":
        global vname
        vname=request.POST['state']
        URL=''
        URL='https://market.todaypricerates.com/'+vname+'-vegetables-price'
        print(URL)
        try:
            r=requests.get(URL, timeout=10)
            soup=BeautifulSoup(r.text,'html.parser')
            states=["Select your area"]
            for tag in soup.find_all('tfoot'):
                for t in tag.find_all('a'):
                    states.append(t.text)
            return render(request,'select_city.html',{"states":states,"visible":"visible"})
        except Exception as e:
            print(f"Error fetching market data: {e}")
            return render(request,'select_city.html',{"states":["Select your area"],"visible":"hidden","error":"Unable to fetch market data"})
    return render(request,'select_city.html',{"states":["Select your area"],"visible":"hidden"})

def selectcity1(request):
    if request.method=="POST":
        cname=request.POST['state1']
        URL='https://market.todaypricerates.com/'+cname+'-vegetables-price-in-'+vname
        print(URL)
        try:
            r=requests.get(URL, timeout=10)
            soup=BeautifulSoup(r.text,'html.parser')
            v=[]
            for row in soup.find_all('div',attrs={'class':'Row'}):
                t=[]
                for r in row.find_all('div',attrs={'class':'Cell'}):
                    t.append(r.text)
                v.append(t)
            print(v)
            return render(request,'prices.html',{"prices":v})
        except Exception as e:
            print(f"Error fetching price data: {e}")
            return render(request,'prices.html',{"prices":[],"error":"Unable to fetch price data"})

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
            return render(request,'farmer_signup.html',{"error":"Username already exists"})
        else:
            farmer.objects.create(fname=fname,lname=lname,pno=pno,village=village,district=district,state=state,uname=uname,pwd=pwd)
            print("created successfully")
            return render(request,'farmer_login.html',{"success":"Account created successfully"})
    else:
        return render(request,'farmer_signup.html')

def farmerlogin(request):
    if request.session.get('member_id'):
        return redirect('/predictindex')
    if request.method == 'GET':
        return render(request,'farmer_login.html')
    else:
        username = request.POST['uname']
        password = request.POST['psw']
        try :
            farmer_object = farmer.objects.get(uname=username)
        except farmer.DoesNotExist:
            print("No such user exists")
            return render(request,'farmer_login.html', context={'error': 'No such user exists'})

        if farmer_object.pwd == password :
            request.session['member_id'] = farmer_object.id
            return redirect('/predictindex')
        else:
            print("your username and password didn't match")
            return render(request,'farmer_login.html', context={'error': 'Your username and password does not match'})

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
            return render(request,'volunteer_signup.html',{"error":"Username already exists"})
        else:
            volunteer.objects.create(fname=fname,lname=lname,pno=pno,village=village,district=district,state=state,uname=uname,pwd=pwd,des=des)
            print("created successfully")
            return render(request,'volunteer_login.html',{"success":"Account created successfully"})
    return render(request,'volunteer_signup.html')

def volunteerlogin(request):
    if request.session.get('v_member_id'):
        return redirect('/volunteerdash')
    if request.method == 'GET':
        return render(request,'volunteer_login.html')
    else:
        username = request.POST['uname']
        password = request.POST['psw']
        try :
            volunteer_object = volunteer.objects.get(uname=username)
        except volunteer.DoesNotExist:
            print("No such user exists")
            return render(request,'volunteer_login.html', context={'error': 'No such user exists'})

        if volunteer_object.pwd == password :
            request.session['v_member_id'] = volunteer_object.id
            return redirect('/volunteerdash')
        else:
            print("your username and password didn't match")
            return render(request,'volunteer_login.html', context={'error': 'Your username and password does not match'})

def questions(request):
    try:
        qobj = list(question.objects.filter(far_id=request.session['member_id']))
        print(qobj,request.session['member_id'])
        return render(request,'questions.html',context={'q':qobj})
    except KeyError:
        return redirect('/')

def questions1(request):
    try:
        vobj = volunteer.objects.get(id=request.session['v_member_id'])
        print(f"Volunteer: {vobj.village} / {vobj.district}")
        que = question.objects.filter(
            models.Q(far__village__iexact=vobj.village) | models.Q(far__district__iexact=vobj.district)
        ).order_by('-id')
        for q in que:
            print(f"Q: {q.ques} (Farmer: {q.far.village} / {q.far.district})")
        return render(request,'questions1.html',context={'que':que})
    except KeyError:
        return redirect('/')

def create_notification(recipient_type, recipient_id, notification_type, title, message, related_obj=None):
    """Create a notification for a user"""
    try:
        if recipient_type == 'farmer':
            recipient = farmer.objects.get(id=recipient_id)
            notification = Notification(
                recipient_farmer=recipient,
                notification_type=notification_type,
                title=title,
                message=message
            )
        else:
            recipient = volunteer.objects.get(id=recipient_id)
            notification = Notification(
                recipient_volunteer=recipient,
                notification_type=notification_type,
                title=title,
                message=message
            )
        
        if related_obj:
            if isinstance(related_obj, question):
                notification.related_question = related_obj
            elif isinstance(related_obj, Message):
                notification.related_message = related_obj
            elif isinstance(related_obj, Resource):
                notification.related_resource = related_obj
        
        notification.save()
        return notification
    except Exception as e:
        print(f"Error creating notification: {e}")
        return None

def newques(request):
    if request.method == 'GET':
        return render(request,'newques.html')
    txt=request.POST['q1']
    try:
        farmer_object = farmer.objects.get(id=request.session['member_id'])
        que=question(ques=txt,far=farmer_object)
        que.save()
        
        # Create notifications for volunteers in the same area
        volunteers = volunteer.objects.filter(
            models.Q(village__iexact=farmer_object.village) | 
            models.Q(district__iexact=farmer_object.district)
        )
        for vol in volunteers:
            create_notification(
                'volunteer', vol.id, 'question',
                f'New Question from {farmer_object.fname} {farmer_object.lname}',
                f'Farmer {farmer_object.fname} {farmer_object.lname} has posted a new question: {txt[:50]}...',
                que
            )
        
        return redirect('/questions')
    except KeyError:
        return redirect('/')

def queshigh(request):
    q=request.POST['ques']
    q=q.split(" ")
    print(type(q),q)
    try:
        q_object = question.objects.get(id=int(q[2][1:-1]))
        l=list(q_object.comsf.all())
        l1=list(q_object.comsv.all())
        return render(request,'qhigh.html',context={'q':q_object,'qobj':l,'qobj1':l1})
    except (IndexError, ValueError, question.DoesNotExist):
        return render(request,'questions.html',context={'q':[],'error':'Question not found'})

def queshigh1(request):
    q=request.POST['ques']
    q=q.split(" ")
    print(type(q),q)
    try:
        q_object = question.objects.get(id=int(q[2][1:-1]))
        l=list(q_object.comsf.all())
        l1=list(q_object.comsv.all())
        return render(request,'qhigh1.html',context={'q':q_object,'qobj':l,'qobj1':l1})
    except (IndexError, ValueError, question.DoesNotExist):
        return render(request,'questions1.html',context={'que':[],'error':'Question not found'})

def comsub(request):
    txt=request.POST['c1']
    try:
        farmer_object = farmer.objects.get(id=request.session['member_id'])
        f1=far_comment(com=txt,far=farmer_object)
        f1.save()
        q=request.POST['qid']
        qobj=question.objects.get(id=q)
        qobj.comsf.add(f1)
        
        # Create notification for volunteers
        volunteers = volunteer.objects.filter(
            models.Q(village__iexact=farmer_object.village) | 
            models.Q(district__iexact=farmer_object.district)
        )
        for vol in volunteers:
            create_notification(
                'volunteer', vol.id, 'answer',
                f'New Farmer Comment',
                f'Farmer {farmer_object.fname} {farmer_object.lname} commented on a question: {txt[:50]}...',
                qobj
            )
        
        return redirect('/questions')
    except KeyError:
        return redirect('/')

def comsub1(request):
    txt=request.POST['c1']
    try:
        volunteer_object = volunteer.objects.get(id=request.session['v_member_id'])
        v1=vol_comment(com=txt,vol=volunteer_object)
        v1.save()
        q=request.POST['qid']
        qobj=question.objects.get(id=q)
        qobj.comsv.add(v1)
        
        # Create notification for the farmer who asked the question
        create_notification(
            'farmer', qobj.far.id, 'answer',
            f'New Volunteer Answer',
            f'Volunteer {volunteer_object.fname} {volunteer_object.lname} answered your question: {txt[:50]}...',
            qobj
        )
        
        return redirect('/questions1')
    except KeyError:
        return redirect('/')

def logout(request):
    try:
        del request.session['member_id']
    except KeyError:
        pass
    try:
        del request.session['v_member_id']
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

def pending_questions(request):
    try:
        vobj = volunteer.objects.get(id=request.session['v_member_id'])
        print(f"Volunteer: {vobj.village} / {vobj.district}")
        qobj = question.objects.filter(
            models.Q(far__village__iexact=vobj.village) | models.Q(far__district__iexact=vobj.district)
        )
        pending = []
        for q in qobj:
            print(f"Question: {q.ques} (Farmer: {q.far.village} / {q.far.district}) | Volunteer comments: {q.comsv.count()}")
            if q.comsv.count() == 0:
                pending.append(q)
        return render(request, 'pending_questions.html', {'pending': pending})
    except KeyError:
        return redirect('/')

def answer_history(request):
    try:
        vobj = volunteer.objects.get(id=request.session['v_member_id'])
        answers = vol_comment.objects.filter(vol=vobj)
        answer_data = []
        for a in answers:
            related_questions = question.objects.filter(comsv=a)
            for q in related_questions:
                answer_data.append({
                    'question': q.ques,
                    'answer': a.com,
                })
        return render(request, 'answer_history.html', {'answer_data': answer_data})
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
    try:
        model = get_model()
        if model is None:
            return render(request,'disease_upload.html',context={"error":"Model not available"})
            
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
        
        if not os.path.exists(testimage):
            return render(request,'disease_upload.html',context={"error":"Uploaded file not found"})
            
        test_image = image.load_img(testimage, target_size = (200, 200))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis = 0)
        test_image = test_image/255.0
        result = model.predict(test_image)
        o=np.argmax(result)
        print(o)
        
        # Read disease data
        disease_file = os.path.join(settings.BASE_DIR, 'ml_models', 'pd1.txt')
        if not os.path.exists(disease_file):
            return render(request,'disease_upload.html',context={"error":"Disease data file not found"})
            
        with open(disease_file, "r", errors="ignore") as f:
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
            # Simple translation mapping for common languages
            translations = {
                'hindi': {'name': d1[j], 'des': d2[j], 'sol': d3[j]},
                'tamil': {'name': d1[j], 'des': d2[j], 'sol': d3[j]},
                'telugu': {'name': d1[j], 'des': d2[j], 'sol': d3[j]},
                'bengali': {'name': d1[j], 'des': d2[j], 'sol': d3[j]},
                'gujarati': {'name': d1[j], 'des': d2[j], 'sol': d3[j]},
                'kannada': {'name': d1[j], 'des': d2[j], 'sol': d3[j]},
                'malayalam': {'name': d1[j], 'des': d2[j], 'sol': d3[j]},
                'marathi': {'name': d1[j], 'des': d2[j], 'sol': d3[j]},
                'punjabi': {'name': d1[j], 'des': d2[j], 'sol': d3[j]}
            }
            
            if sname in translations:
                context={'name':d1[j],'des':d2[j],'sol':d3[j],'tname':translations[sname]['name'],'tdes':translations[sname]['des'],'tsol':translations[sname]['sol']}
            else:
                context={'name':d1[j],'des':d2[j],'sol':d3[j],'tname':d1[j],'tdes':d2[j],'tsol':d3[j]}
            return render(request,'disease_upload.html',context)
    except Exception as e:
        print(f"Error in predictImage: {e}")
        return render(request,'disease_upload.html',context={"error":f"Error processing image: {str(e)}"})

def weatherfetch(request):
    if request.method == "POST":
        city = request.POST['city'].strip()
        api_key = "177bd440ee2d7663de6777cf3bae62bb"
        possible_cities = [city, f"{city},IN"]
        for city_query in possible_cities:
            # Current weather API
            current_url = f"http://api.openweathermap.org/data/2.5/weather?q={city_query}&appid={api_key}&units=metric"
            current_response = requests.get(current_url)
            current_data = current_response.json()
            # Forecast API
            url = f"http://api.openweathermap.org/data/2.5/forecast?q={city_query}&appid={api_key}&units=metric"
            response = requests.get(url)
            data = response.json()
            print("Current API response:", current_data)
            print("Forecast API response:", data)
            if (
                data.get("cod") == "200"
                and "list" in data
                and len(data["list"]) > 0
                and current_data.get("cod") == 200
            ):
                # Current weather
                current_temp = current_data["main"]["temp"]
                current_humidity = current_data["main"]["humidity"]
                current_precip = current_data.get("rain", {}).get("1h", 0)
                current_desc = current_data["weather"][0]["description"].capitalize()
                # Next 24 hours forecast
                forecast_list = data["list"][:8]
                forecast_data = []
                for entry in forecast_list:
                    dt_txt = entry["dt_txt"]
                    temp = entry["main"]["temp"]
                    humidity = entry["main"]["humidity"]
                    precip = entry.get("rain", {}).get("3h", 0)
                    forecast_data.append({
                        "datetime": dt_txt,
                        "temp": temp,
                        "humidity": humidity,
                        "precip": precip,
                    })
                context = {
                    "cname": city_query,
                    "forecast_data": forecast_data,
                    "current_temp": current_temp,
                    "current_humidity": current_humidity,
                    "current_precip": current_precip,
                    "current_desc": current_desc,
                }
                return render(request, "weather_data.html", context)
        error_msg = data.get("message", "City not found or API error")
        return render(request, "city_select.html", {"error": f"City not found or API error: {error_msg}"})
    return render(request, "city_select.html")

def resource_list(request):
    resources = Resource.objects.all().order_by('-uploaded_at')
    return render(request, 'resource_list.html', {'resources': resources})

def upload_resource(request):
    if request.method == 'GET':
        return render(request, 'upload_resource.html')
    
    title = request.POST.get('title')
    description = request.POST.get('description')
    file_obj = request.FILES.get('file')
    link = request.POST.get('link')
    
    try:
        volunteer_object = volunteer.objects.get(id=request.session['v_member_id'])
        resource = Resource(
            title=title,
            description=description,
            uploaded_by=volunteer_object
        )
        
        if file_obj:
            resource.file = file_obj
        if link:
            resource.link = link
            
        resource.save()
        
        # Create notifications for farmers in the same area
        farmers = farmer.objects.filter(
            models.Q(village__iexact=volunteer_object.village) | 
            models.Q(district__iexact=volunteer_object.district)
        )
        for f in farmers:
            create_notification(
                'farmer', f.id, 'resource',
                f'New Resource Available',
                f'Volunteer {volunteer_object.fname} {volunteer_object.lname} shared a new resource: {title}',
                resource
            )
        
        return redirect('/resource_list')
    except Exception as e:
        print(f"Error uploading resource: {e}")
        return redirect('/upload_resource')

def message_list(request):
    farmer_id = request.session.get('member_id')
    volunteer_id = request.session.get('v_member_id')
    if farmer_id:
        user = farmer.objects.get(id=farmer_id)
        messages = Message.objects.filter(receiver_farmer=user) | Message.objects.filter(sender_farmer=user)
    elif volunteer_id:
        user = volunteer.objects.get(id=volunteer_id)
        messages = Message.objects.filter(receiver_volunteer=user) | Message.objects.filter(sender_volunteer=user)
    else:
        return redirect('/')
    messages = messages.order_by('sent_at')
    return render(request, 'message_list.html', {'messages': messages})

def send_message(request):
    if request.method == 'GET':
        try:
            volunteer_object = volunteer.objects.get(id=request.session['v_member_id'])
            farmers = farmer.objects.filter(
                models.Q(village__iexact=volunteer_object.village) | 
                models.Q(district__iexact=volunteer_object.district)
            )
            return render(request, 'send_message.html', {'farmers': farmers})
        except KeyError:
            return redirect('/')
    
    to_farmer_id = request.POST.get('to_farmer')
    message_text = request.POST.get('message')
    
    try:
        volunteer_object = volunteer.objects.get(id=request.session['v_member_id'])
        farmer_object = farmer.objects.get(id=to_farmer_id)
        
        msg = Message(
            sender_volunteer=volunteer_object,
            receiver_farmer=farmer_object,
            message=message_text
        )
        msg.save()
        
        # Create notification for farmer
        create_notification(
            'farmer', farmer_object.id, 'message',
            f'New Message from Volunteer',
            f'Volunteer {volunteer_object.fname} {volunteer_object.lname} sent you a message: {message_text[:50]}...',
            msg
        )
        
        return redirect('/message_list')
    except Exception as e:
        print(f"Error sending message: {e}")
        return redirect('/message_list')

def get_notifications(request):
    """API endpoint to get notifications for current user"""
    try:
        if 'member_id' in request.session:  # Farmer
            notifications = Notification.objects.filter(
                recipient_farmer_id=request.session['member_id'],
                is_read=False
            ).order_by('-timestamp')[:10]
        elif 'v_member_id' in request.session:  # Volunteer
            notifications = Notification.objects.filter(
                recipient_volunteer_id=request.session['v_member_id'],
                is_read=False
            ).order_by('-timestamp')[:10]
        else:
            notifications = []
        
        data = []
        for notif in notifications:
            data.append({
                'id': notif.id,
                'type': notif.notification_type,
                'title': notif.title,
                'message': notif.message,
                'timestamp': notif.timestamp.strftime('%Y-%m-%d %H:%M'),
                'is_read': notif.is_read
            })
        
        return JsonResponse({'notifications': data})
    except Exception as e:
        return JsonResponse({'error': str(e)})

def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    try:
        notification = Notification.objects.get(id=notification_id)
        notification.is_read = True
        notification.save()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': str(e)})

def dashboard_stats(request):
    """Get dashboard statistics for current user"""
    try:
        if 'member_id' in request.session:  # Farmer
            farmer_obj = farmer.objects.get(id=request.session['member_id'])
            stats = {
                'total_questions': question.objects.filter(far=farmer_obj).count(),
                'unread_notifications': Notification.objects.filter(
                    recipient_farmer=farmer_obj, is_read=False
                ).count(),
                'total_messages': Message.objects.filter(
                    receiver_farmer=farmer_obj
                ).count(),
                'unread_messages': Message.objects.filter(
                    receiver_farmer=farmer_obj, is_read=False
                ).count()
            }
        elif 'v_member_id' in request.session:  # Volunteer
            volunteer_obj = volunteer.objects.get(id=request.session['v_member_id'])
            print(f"[DEBUG] Volunteer: {volunteer_obj.village} / {volunteer_obj.district}")
            qobj = question.objects.filter(
                models.Q(far__village__iexact=volunteer_obj.village) | 
                models.Q(far__district__iexact=volunteer_obj.district)
            )
            print(f"[DEBUG] Total questions in area: {qobj.count()}")
            pending = 0
            for q in qobj:
                print(f"[DEBUG] Q: {q.ques} | Volunteer comments: {q.comsv.count()}")
                if q.comsv.count() == 0:
                    pending += 1
            print(f"[DEBUG] Pending questions counted: {pending}")
            stats = {
                'pending_questions': pending,
                'total_answers': vol_comment.objects.filter(vol=volunteer_obj).count(),
                'unread_notifications': Notification.objects.filter(
                    recipient_volunteer=volunteer_obj, is_read=False
                ).count(),
                'total_resources': Resource.objects.filter(uploaded_by=volunteer_obj).count()
            }
        else:
            stats = {}
        
        return JsonResponse(stats)
    except Exception as e:
        print(f"[DEBUG] Error in dashboard_stats: {e}")
        return JsonResponse({'error': str(e)})

def advanced_search(request):
    """Advanced search with filters"""
    query = request.GET.get('q', '')
    category = request.GET.get('category', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    try:
        if 'member_id' in request.session:  # Farmer search
            farmer_obj = farmer.objects.get(id=request.session['member_id'])
            questions = question.objects.filter(far=farmer_obj)
            
            if query:
                questions = questions.filter(ques__icontains=query)
            if date_from:
                questions = questions.filter(date__gte=date_from)
            if date_to:
                questions = questions.filter(date__lte=date_to)
                
        elif 'v_member_id' in request.session:  # Volunteer search
            volunteer_obj = volunteer.objects.get(id=request.session['v_member_id'])
            questions = question.objects.filter(
                models.Q(far__village__iexact=volunteer_obj.village) | 
                models.Q(far__district__iexact=volunteer_obj.district)
            )
            
            if query:
                questions = questions.filter(ques__icontains=query)
            if category == 'pending':
                questions = questions.filter(comsv__isnull=True)
            elif category == 'answered':
                questions = questions.filter(comsv__isnull=False)
            if date_from:
                questions = questions.filter(date__gte=date_from)
            if date_to:
                questions = questions.filter(date__lte=date_to)
        else:
            questions = []
        
        questions = questions.order_by('-date')
        
        data = []
        for q in questions:
            data.append({
                'id': q.id,
                'question': q.ques,
                'farmer': q.far.fname + ' ' + q.far.lname,
                'village': q.far.village,
                'date': q.date.strftime('%Y-%m-%d'),
                'answer_count': q.comsv.count() + q.comsf.count()
            })
        
        return JsonResponse({'questions': data})
    except Exception as e:
        return JsonResponse({'error': str(e)})
