from django.shortcuts import render,redirect,HttpResponse
from django.contrib import messages
from Admin.models import *
from django.contrib.auth.models import User,auth
from django.contrib.auth.hashers import check_password
import json

# image loading
from  django.core.files.storage import FileSystemStorage
from PIL import Image
from django.core.files import File

# otp
import requests


# Create your views here.
def common_home(request):
    return render(request, 'common/commonhome.html')


def seeker_login(request):
    return render(request, 'seeker/seekerlogin.html')


def customer_login(request):
    if request.user.is_authenticated:
        return redirect(registered_customer_homepage)
    if request.method == "POST":
        user_name = request.POST['username']
        password = request.POST['password']
        customer = User.objects.filter(username=user_name).first()

        if customer is not None and check_password(password,customer.password):
            if customer.is_active == False:
                messages.info(request, 'user is blocked')
                return redirect(user_login)
            else:
                auth.login(request, customer)
                # return redirect(registered_user_home_page)
                return HttpResponse("Home Page Of Customer")
        else:   
            value={"username":user_name}
            messages.info(request, 'invalid credentials')
            return render(request, 'customer/customerlogin.html')
    else:
        return render(request, 'customer/customerlogin.html')
    

def customer_register(request):
    if request.user.is_authenticated:
        return redirect(registered_customer_homepage)
    if request.method == 'POST':
        name = request.POST['name']
        user_name = request.POST['username']
        email = request.POST['email']
        mobile = request.POST['phone']
        password = request.POST['password']    
        if User.objects.filter(username=user_name).exists() or User.objects.filter(email=email).exists():
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'username already exists')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already exists')
            return render(request, 'customer/registration.html')
        else:
            customer = User.objects.create_user(first_name=name, username=user_name, email=email, password=password, last_name=mobile)
            # customer.save()
            return redirect(customer_login)
    else:  
        return render(request, 'customer/registration.html')


def otp_login(request):
    if request.user.is_authenticated:
        return redirect(registered_customer_homepage)
    otp = 1
    if request.method == 'POST':
        phone_number = request.POST['phone']
        request.session['phone_number'] = phone_number
        
        if User.objects.filter(last_name=phone_number).exists():
            otp = 0
            # adding otp creation 
            phone_number = str(91) + phone_number
            url = "https://d7networks.com/api/verifier/send"

            payload = {'mobile': phone_number,
            'sender_id': 'SMSINFO',
            'message': 'Your otp code is {code}',
            'expiry': '900'}
            files = [

            ]
            headers = {
            # 'Authorization': 'Token 13ff28cd8a3bc23d426420f75b84879c7f958c4c'
            'Authorization': 'Token 7b965deb9feaf5d0601c369eda9ff2e04c56d9ce'   
            }
            response = requests.request("POST", url, headers=headers, data = payload, files = files)
            print(response.text.encode('utf8'))

            data=response.text.encode('utf8')
            datadict=json.loads(data)

            id=datadict['otp_id']
            request.session['id'] = id

             # //otp creation 
            return render(request, 'customer/otplogin.html', {'otp':otp})
        else:
            messages.info(request, 'Mobile Number does not exist')
            return render(request, 'customer/otplogin.html',{'otp':otp})
    else:
        return render(request, 'customer/otplogin.html', {'otp':otp})

   
def confirm_otp(request):
    if request.user.is_authenticated:
        return redirect(registered_customer_homepage)
        # return redirect(registered_user_home_page)
    else:
        if request.method == 'POST':
            otp_number = request.POST['otp']
            
            id_otp = request.session['id']
            url = "https://d7networks.com/api/verifier/verify"

            payload = {'otp_id': id_otp,
            'otp_code': otp_number}
            files = [
            ]
            headers = {
            'Authorization': 'Token 7b965deb9feaf5d0601c369eda9ff2e04c56d9ce'
            }
            response = requests.request("POST", url, headers=headers, data = payload, files = files)
            print(response.text.encode('utf8'))
            data=response.text.encode('utf8')
            datadict=json.loads(data)
            status=datadict['status']

            if status == 'success':
                phone_number = request.session['phone_number']  
                user = User.objects.filter(last_name=phone_number).first()
                if user is not None:
                    if user.is_active == False:
                        messages.info(request, 'customer is blocked')
                        return redirect(customer_login)
                    else:
                        auth.login(request, user)
                        # value = products.objects.all()
                        # return redirect(registered_user_home_page)
                        return HttpResponse("success")
                else:
                    return redirect(customer_login)
                
            else:
                messages.error(request,'User not Exist')
                return redirect(customer_login)

        else:
            return HttpResponse("oops")

def customer_homepage(request):
    if request.user.is_authenticated:
        return redirect(registered_customer_homepage)   
    seeker_detials = JobSeeker.objects.all()
    return render(request, 'customer/index.html', {"detials":seeker_detials})

def registered_customer_homepage(request):
    if request.user.is_authenticated:
        user = request.user
        seeker_detials = JobSeeker.objects.all()
        context = {'user':user, 'detials':seeker_detials}
        return render(request, 'customer/registeredcustomerhomepage.html',context)
    else:
        return redirect(customer_homepage)
    
def registered_customer_logout(request):
    if request.user.is_authenticated:
        auth.logout(request)
        return redirect(customer_homepage)
    else:
        return redirect(customer_homepage)
    
def customer_profile(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            phone_number = request.POST['mobile']
            address = request.POST['address']
            place = request.POST['place']

            user = request.user
            print(user)
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            user.save()
            if CustomerDetials.objects.filter(user=user).exists():
                detials = CustomerDetials.objects.get(user=user)
                detials.mobile_number = phone_number
                detials.address = address
                detials.place = place
                detials.save()
                context = {"value":user, "customer_detials":detials}
                return render(request, 'customer/customerprofile.html', context)
            else:   
                detials = CustomerDetials.objects.create(user=user, mobile_number=phone_number, address=address, place=place)
                context = {"value":user, "customer_detials":detials}
                return render(request, 'customer/customerprofile.html', context)
        else:
            user = request.user
            detials = User.objects.filter(username=user)
            customer_detials = CustomerDetials.objects.get(user=user)
            context = {"detials":detials, 'value':user, 'customer_detials':customer_detials}
            return render(request, 'customer/customerprofile.html', context)
    else:
        return render(customer_homepage)


def quickview(request, id):
    if request.user.is_authenticated:
        detials = JobSeeker.objects.filter(id=id).first()
        seekers = JobSeeker.objects.all()
        category = detials.category.category_name
        index = 0
        context = {"detials":detials, "seekers":seekers, "category":category, "index":index}
        return render(request, 'customer/quickview.html', context)
    else:
        detials = JobSeeker.objects.filter(id=id).first()
        seekers = JobSeeker.objects.all()
        category = detials.category.category_name
        index = 1
        context = {"detials":detials, "seekers":seekers, "category":category, "index":index}
        return render(request, 'customer/quickview.html', context)
    

def collection(request):
    if request.user.is_authenticated:
        data = Collection.objects.all()
        total_price = 0
        for x in data:
            total_price = total_price + x.get_total

        context = {"data":data, "total_price":total_price}
        return render(request, 'customer/collection.html', context)
    else:
        return redirect(customer_homepage)

def add_to_collection(request, id):
    if request.user.is_authenticated:
        user = request.user
        seeker = JobSeeker.objects.get(id=id)
        if Collection.objects.filter(customer=user, seeker=seeker).exists():
            return redirect(registered_customer_homepage)
        else:
            data = Collection.objects.create(customer=user, seeker=seeker, total_price=seeker.expected_salary)
            print(data)
            return redirect(registered_customer_homepage)
    else:
        return redirect(customer_homepage)

def delete_collection(request, id):
    if request.user.is_authenticated:
        value = Collection.objects.get(id = id)
        value.delete()
        messages.info(request, 'deleted successfully')
        return redirect(collection)
    else:
        return redirect(customer_homepage)


# *****************************************************************************seeker************************************************************************************************

def seeker_profile(request):
    if request.session.has_key('user_name'):
        user_name = request.session['user_name']
        seeker = JobSeeker.objects.filter(username=user_name).first()
        context = {"detials":seeker}
        return render(request, 'seeker/seekerprofile.html', context)
    else:
        return redirect(seeker_login)
    
    

def seeker_login(request):
    if request.session.has_key('user_name'):
        return redirect(seeker_profile)
    if request.method == "POST":
        user_name = request.POST['username']
        password = request.POST['password']
        seeker = JobSeeker.objects.filter(username=user_name).first()

        if JobSeeker.objects.filter(username=user_name, password=password):
            request.session['user_name']= user_name
            return redirect(seeker_profile)
        else:
            return HttpResponse("fail")
    else:
        return render(request, 'seeker/seekerlogin.html')

        # if customer is not None and check_password(password,customer.password):
        #     if customer.is_active == False:
        #         messages.info(request, 'user is blocked')
        #         return redirect(user_login)
        #     else:
        #         auth.login(request, customer)
        #         # return redirect(registered_user_home_page)
        #         return HttpResponse("Home Page Of Customer")
        # else:   
        #     value={"username":user_name}
        #     messages.info(request, 'invalid credentials')
        #     return render(request, 'customer/customerlogin.html')
    # else:
    #     return render(request, 'customer/customerlogin.html')


    
def seeker_logout(request):
    if request.session.has_key('user_name'):
        request.session.flush()
        return redirect(seeker_login)
    else:
        return render(request, 'seeker/seekerlogin.html')
        

def seeker_available(request, id):
    if request.session.has_key('user_name'):
        seeker = JobSeeker.objects.filter(id=id).first()
        seeker.available = False
        print(seeker.available)
        seeker.save()
        return redirect(seeker_profile)

    else:
        return render(request, 'seeker/seekerlogin.html')

def seeker_not_available(request, id):
    if request.session.has_key('user_name'):
        seeker = JobSeeker.objects.filter(id=id).first()
        seeker.available = True
        print(seeker.available)
        seeker.save()
        return redirect(seeker_profile)

    else:
        return render(request, 'seeker/seekerlogin.html')