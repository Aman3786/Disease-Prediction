from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import DoctorInfo
from django.core.files.storage import FileSystemStorage


# Create your views here.


def register_uer(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            
            return render(request,'doctor_info.html')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm
    # print(dir(form))
    if request.user.is_authenticated:
        return redirect("home")
    else:
        return render (request=request, template_name="register.html", context={"register_form":form})

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                # everything = DoctorInfo.objects.get(id=request.user.id)
                # print(everything)
                # print(type(everything))
                return redirect("home")
            else:
                messages.error(request,"Invalid username or password.")
                return redirect('/accounts/login/')
        else:
            messages.error(request,"Invalid username or password.")
            return redirect('/accounts/login/')
    form = AuthenticationForm()
    if request.user.is_authenticated:
        return redirect("home")
    else:
        return render(request=request, template_name="login.html", context={"login_form":form})

def Logout(request):
    logout(request)
    return redirect("login")

def home(request):

    return render(request,'home.html')
def doctor_page(request):
    if request.user.is_authenticated:
        return render(request,'doctor_info.html')
    else:
        return redirect('/accounts/login/')
def Doctor_info(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            myfile = request.FILES['Img']
            fs = FileSystemStorage()
            filename = fs.save("profile_images/"+myfile.name,myfile)
            uploaded_file_url = fs.url(filename)
            print("URL ",uploaded_file_url)
            data = request.POST
            print(data)
            user = User.objects.get(username=request.user.username)
            doctor_info = DoctorInfo(firstName=data['fname'],lastName=data['lname'],username=user,address=data['cadd'],clinic_name=data['cname'],phone=int(data['phone']),specialization= data['special'],description=data['desc'],image=uploaded_file_url)
            doctor_info.save()
            messages.info(request,"You Have Successfully  Created Your Public Profile")
            return render(request,'doctor_info.html')
    else:
        messages.error(request, "Your are not athenticated user")
        return redirect('/accounts/login/')
def doctor_profile(request):
    # user = User.objects.get(username=request.user.username)
    # print(user)
    if request.user.is_authenticated:
        data = DoctorInfo.objects.filter(username=request.user.id)
        print(data)
        # dic ={}
        # c =0
        # for d in data.values():
        #     if int(d['username_id']) == int(request.user.id):
        #         c +=1
        #         dic[f'data{c}'] = list(d.values())
        # print(dic)
        return render(request,'profile.html',{'dic':data})
    else:
        return redirect('/accounts/login/')

def just_for_testing(request):

    return render(request,'testing.html')

# 'user': ['asraf27'], 'fname': ['amaan'], 'lname': ['shaikh'], 
# 'cname': ['asiya hospital'], 'cadd': ['gaon me'], 'phone': ['99977799988'], 
# 'special': ['Breast Cancer'], 'desc': ['I can cure you']}>
