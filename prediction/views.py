from django.http import HttpResponse
from django.shortcuts import render,redirect
from disease_prediction.models import Post_image 
import tensorflow as tf
from disease_prediction.forms import *
import cv2
import os
from datetime import date
import pandas as pd
import numpy as np
import pickle
from django.core.files.storage import FileSystemStorage
from sklearn.preprocessing import StandardScaler
from django.contrib.auth import get_user_model
from django_email_verification import send_email
from accounts.models import DoctorInfo


# from django.contrib.staticfiles.templatetags.staticfiles import static


def home_page(request):
    # print('its home')
    return render(request,"home.html",{})

def test_page(request):
    # print('its test')
    return render(request ,"test.html",{})

def  pneumonia(request):
	return render(request,'pneumonia.html',{})
def  covid(request):
    return render(request,'covid.html',{})
def  brain(request):
    return render(request,'brain_tumor.html',{})
def  breast_cancer(request):
    return render(request,'breast_cancer.html',{})

def prepare(filepath,idi,height=224,width=224):
    # IMG_SIZE = 70  # 50 in txt-based
    # cv2.imshow(filepath)
    
    # IMAGE_SIZE =224
    path='.' + filepath
    img_array = cv2.imread(path) 
    print(img_array)
    # print(img_array.shape) # read in the image, convert to grayscale
    new_array = cv2.resize(img_array, (height, width))  # resize image to match model's expected sizing
    return new_array.reshape(-1, height, width, idi)  # return the image with shaping that TF wants.


def predict_pneumonia(request):
    if request.method == 'POST' and request.FILES['selectfile']:
        myfile = request.FILES['selectfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)
        # prepare(uploaded_file_url)
    # image = request.POST['selectfile']
    # tag =  "pneumonia"
    infor     =pd.read_csv('./static/Models/pneumonia.txt',sep=";")
    info      = infor['Information'][0]
    natural   = infor['Natural'][0]
    exercise  = infor['Exercise'][0]
    diet      = infor['Diet'][0]
    
    model_path= "./static/Models/Pneumonia.h5"
    
    model = tf.keras.models.load_model(model_path)
    #print(model.summary())
    prediction = model.predict([prepare(uploaded_file_url,3)])
    # label = "Pneumonia"
    print('prediction',prediction)
    result = int(prediction[0])
    if result == 1 :
        data = DoctorInfo.objects.filter(specialization="Pneumonia")
        value = {'result':uploaded_file_url,'info':info,'natural':natural,'exercise':exercise,'diet':diet,'value':"Suffering from Pneumonia",'query':data}
        print('Infected',result)
    else:
        value = {'result':uploaded_file_url,'value':"Its Normal ",'normal':'nornal'}
        print('normal ')
    return render(request,'pneumonia.html',context=value)
def predict_brain_tumor(request):
    if request.method == 'POST' and request.FILES['selectfile']:
        myfile = request.FILES['selectfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        uploaded_file_url = fs.url(filename)
        # print(uploaded_file_url)
        # prepare(uploaded_file_url)
    infor     = pd.read_csv('./static/Models/brain_tumor.txt',sep=";")
    info      = infor['Information'][0]
    natural   = infor['Natural'][0]
    exercise  = infor['Exercise'][0]
    diet      = infor['Diet'][0]

    model_path= "./static/Models/BrainTumor.h5"
    
    model = tf.keras.models.load_model(model_path)
    #print(model.summary())
    prediction = model.predict([prepare(uploaded_file_url,3,256,256)])
    
    print("prediction - ",prediction)
    result = int(prediction[0])
    if result == 1 :
        data = DoctorInfo.objects.filter(specialization="Brain Tumor")
        value = {'result':uploaded_file_url,'info':info,'natural':natural,'exercise':exercise,'diet':diet,'value':"Its Infected to brain Tumor",'query':data}
        print('Infected')
    else:
        value = {'result':uploaded_file_url,'value':"Report is Normal ",'normal':'noramal'}
        print('normal')
        
    return render(request,'brain_tumor.html',context=value)


   
   
   
def predict_covid(request):
    if request.method == 'POST' and request.FILES['selectfile']:
        myfile = request.FILES['selectfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        uploaded_file_url = fs.url(filename)

    model_path= "./static/Models/Covid_pre_original.h5"
    
    model = tf.keras.models.load_model(model_path)
    # print(model.summary())
    prediction = model.predict([prepare(uploaded_file_url,3)])
    # label = "Pneumonia"
    result = int(prediction[0])
    print("result ",result)
    if result == 0 :
        data = DoctorInfo.objects.filter(specialization="Covid treatment")
        infor     =pd.read_csv('./static/Models/infected_covid.txt',sep=";")
        infected_information = infor['information'][0] + infor['information'][1]+infor['information'][2]+infor['information'][3]
        infected_precaution      = infor['Precautions'][2]
        value = {'result':uploaded_file_url,'information':infected_information,'precaution':infected_precaution,'value':"Suffering from Covid ",'infected':1,'query':data}
        print('Infected')
        # value = {'value':"Its normal",}
        # print('normal')
    else:
        value={}
        infor     =pd.read_csv('./static/Models/disinfected_covid.txt',sep=";")
        information = infor['precautions '].values
        for val in range(len(information)):
            value[f'pre{val}'] = information[val]
        # value = {'information':infected_information,'precaution':infected_precaution,'value':"Suffering from Covid ",'infected':1}
        # print('Infected')
        value1 = {'value':"Report is normal",'result':uploaded_file_url}
        value = {**value,**value1}
        print('normal')
        print(value)
    return render(request,'covid.html',context=value)

   
    # if request.method == 'POST' :
    #     form = disease_form(request.POST,request.FILES)
    #     if form.is_valid():
    #         form.save()
            
    # else:
    #     form = disease_form()
    # return render(request,'pneumonia.html',{'form':form})
def predict_breast_cancer(request):
    if request.method == 'POST' and request.FILES['selectfile']:
        myfile = request.FILES['selectfile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        prepare(uploaded_file_url,1)
    # image = request.POST['selectfile']
    # tag =  "pneumonia"
    infor     =pd.read_csv('./static/Models/breast_cancer.txt',sep=";")
    info      = infor['Informationm'][0]
    natural   = infor['Natural remedies'][0]
    exercise  = infor['Exercise'][0]
    diet      = infor['Diet'][0]
    # print(data)
    # print(type(data))
    
    model_path= "./static/Models/BC.h5"
    
    model = tf.keras.models.load_model(model_path)
    print(model.summary())
    prediction = model.predict([prepare(uploaded_file_url,1)])
    # label = "Pneumonia"
    result = int(prediction[0])
    value={}
    data = DoctorInfo.objects.filter(specialization="Breast Cancer")
    if result == 0 :
        value = {'result':uploaded_file_url,'info':info,'natural':natural,'exercise':exercise,'diet':diet,'value':"Breast Cancer Of Type Benign",'query':data}
        print('normal')
    else:
        
        value = {'result':uploaded_file_url,'info':info,'natural':natural,'exercise':exercise,'diet':diet,'value':"Brease Cancer Of Type Malignant",'query':data}
        print('Infected')
    return render(request,'breast_cancer.html',context=value)

def success(request):
    return HttpResponse("Uploaded Successfully .....")

def heart(request):
    
    return render(request,'heart_disease.html')

def standard_scaler(val):
    scaler=StandardScaler()
    path="./static/Models/heart_disease.csv"
    file =pd.read_csv(path)
    data=scaler.fit(file)
    transformed_data=data.transform(val)
    return transformed_data
    
def predict_heart_disease(request):
    
    value={}
    model_path= "./static/Models/Heat_disease.h5"
    infor     = pd.read_csv('./static/Models/heart_disease.txt',sep=";")
    information = infor['Information'][0] + infor['Information'][1]+infor['Information'][2]+infor['Information'][3] +infor['Information'][4]+infor['Information'][5]
    natural_remidies =infor['Natural'][5]
    exercise = infor['Exercise'][5]
    diet = infor['Diet'][5]
    # for val in range(len(information)):
    #         value[f'pre{val}'] = information[val]
    model = tf.keras.models.load_model(model_path)
    print(model.summary())
    

    dt =date.today()
    dt=str(dt)[:4]
    age=request.POST['age'][:4]
    age =abs(int(age) -int(dt))
    heit = request.POST['height']
    width  = request.POST['width']
    gender = request.POST['gender']  
    Ap_high = request.POST['ap_high']
    Ap_low  = request.POST['ap_low']
    cholestrol = request.POST['cholestrol']
    glucose    = request.POST['glucose']
    alcohol    = request.POST['alcohol']

    x=[[age,int(gender),int(heit),int(width),int(Ap_high),int(Ap_low),int(cholestrol),int(glucose),int(alcohol)]]

    result=standard_scaler(x)
    prediction = model.predict(result)
    print(int(prediction[0][0]))
    if int(prediction[0][0]) == 1 :
        value={'msg':'Its Normal','normal':'normal'}
    else:
        
        data = DoctorInfo.objects.filter(specialization="Heart Disease")
        for d in data:
            print(d.clinic_name)
        value={'msg':'you may suffer from heart disease','info':information,'natural':natural_remidies,'exercise':exercise,'diet':diet,'query':data}

    return render(request,'heart_disease.html',{'value':value})
    
    
def sendEmail(request):
    user =request.user
    # password = request.POST.get('password')
    # username = request.POST.get('username')
    # email = request.POST.get('email')
    user = get_user_model().objects.create(username=user.username,password=user.password,email=user.email)
    send_email(user)
    return render(request,'confirm_template.html')


