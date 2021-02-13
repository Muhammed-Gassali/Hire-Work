from django.shortcuts import render,redirect,HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from Admin.models import *
from django.contrib.auth.models import User,auth
from django.contrib.auth.hashers import check_password
import json
from django.contrib import messages
import uuid

# image loading
from  django.core.files.storage import FileSystemStorage
from PIL import Image
from django.core.files import File

# otp
import requests

import razorpay

from rest_framework.views import APIView
from rest_framework.response import Response
from user.serializer import *
from rest_framework import status

from geopy.geocoders import Nominatim
# from .utils import get_geo
from geopy.distance import geodesic


import datetime 
from datetime import date as dt


# Create your views here.

#function for loading common home
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
                return render(request, 'customer/customerlogin.html')
            else:
                auth.login(request, customer,  backend='django.contrib.auth.backends.ModelBackend')
                return redirect(registered_customer_homepage)  
        else:   
            value={"username":user_name}
            messages.info(request, 'invalid credentials')
            return render(request, 'customer/customerlogin.html')
    else:
        return render(request, 'customer/customerlogin.html')

#function for customer login in rest api
class rest_customer_login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        customer = User.objects.filter(username=username).first()
        customer_id = customer.id

        if customer is not None and check_password(password,customer.password):
            if customer.is_active == False:
                return Response({"status":"failed"})
            else:
                auth.login(request, customer, backend='django.contrib.auth.backends.ModelBackend')
                # context = {"status":success, "username":username}
                return Response({"status":"success"})
                # return Response(customer_id)

                # customer_data = User.objects.filter(id=customer_id)
                # print(Customer_data)
                # customer_serialize = SerializeCustomer(customer_data,many=True)
                # return Response(customer_serialize.data)

        else:
            return Response({"status":"failed"})

def customer_register(request):
    if request.user.is_authenticated:
        return redirect(registered_customer_homepage)
    if request.method == 'POST':
        name = request.POST['name']
        user_name = request.POST['username']
        email = request.POST['email']
        last_name = request.POST['last_name']
        password = request.POST['password']    
        if User.objects.filter(username=user_name).exists() or User.objects.filter(email=email).exists():
            if User.objects.filter(username=user_name).exists():
                messages.info(request, 'username already exists')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already exists')
            return render(request, 'customer/registration.html')
        else:
            customer = User.objects.create_user(first_name=name, username=user_name, email=email, password=password, last_name=last_name)
            # customer.save()
            return redirect(customer_login)
    else:  
        return render(request, 'customer/registration.html')


class RestCustomerRegister(APIView):
    def post(self, request):
        first_name = request.data['fname']
        last_name = request.data['lname']
        user_name = request.data['username']
        email = request.data['email']
        mobile_number = request.data['phone']
        password = request.data['password']
        print(email)
        # return Response({"status":'done'})
        if User.objects.filter(username=user_name).exists() or User.objects.filter(email=email).exists():
            if User.objects.filter(username=user_name).exists():
                return Response({"status":"Username already exists"})
            elif User.objects.filter(email=email).exists():
                return Response({"status":"Email already exists"})
            return Response({"status":"failed"})
        else:
            customer = User.objects.create_user(first_name=first_name, username=user_name, email=email, password=password, last_name=last_name)
            return Response({"status":"success"})


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


class rest_otp_login(APIView):
    def post(self, request):
        phone_number = request.data['phone_number']
        request.session['phone_number'] = phone_number

        if User.objects.filter(last_name=phone_number).exists():
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
            return Response({"status":"enter otp"})
        else:
            return Response({"status":"mobile number does not exist"})



def confirm_otp(request):
    if request.user.is_authenticated:
        return redirect(registered_customer_homepage)
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
            # 'Authorization': 'Token 13ff28cd8a3bc23d426420f75b84879c7f958c4c'
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
                        auth.login(request, user,  backend='django.contrib.auth.backends.ModelBackend')
                        # value = products.objects.all()
                        return redirect(registered_user_home_page)
                        # return HttpResponse("success")
                else:
                    return redirect(customer_login)
                
            else:
                messages.error(request,'User not Exist')
                return redirect(customer_login)

        else:
            return HttpResponse("oops")


class rest_otp_verify(APIView):
    def post(self, request):
        otp_number = request.data['otp']
        id_otp = request.session['id']
        url = "https://d7networks.com/api/verifier/verify"

        payload = {'otp_id': id_otp,
        'otp_code': otp_number}
        files = [
            ]
        headers = {
        'Authorization': 'Token 7b965deb9feaf5d0601c369eda9ff2e04c56d9ce'
        # 'Authorization': 'Token 13ff28cd8a3bc23d426420f75b84879c7f958c4c'
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
                    return Response({"status":"customer is blocked"})
                else:
                    auth.login(request, user,  backend='django.contrib.auth.backends.ModelBackend')
                    return Response({"status":"success"})
            else:
                return Response({"status":"otp entered is incorrerct"})
        else:
            return Response({"status":"user not exist"})


def customer_homepage(request):
    if request.user.is_authenticated:
        return redirect(registered_customer_homepage)   
    seeker_detials = JobSeeker.objects.all()
    return render(request, 'customer/index.html', {"detials":seeker_detials})



def registered_customer_homepage(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            place = request.POST['place']
            print(place)
            geolocator = Nominatim(user_agent='user')
        
            destination = geolocator.geocode(place)
            print(destination)
            d_lon = destination.longitude
            d_lat = destination.latitude
            pointA = (d_lat, d_lon)
     
            data  = JobSeeker.objects.all()
            values = []

            for x in data:
                place_sample = x.place
                destiny = geolocator.geocode(place_sample)
                sample_lat = destiny.latitude
                sample_lon = destiny.longitude
                pointB = (sample_lat, sample_lon)
                distance = round(geodesic(pointA, pointB).km, 2)
    
                if distance <= 50:
                    values.append(x)
            # value = JobSeeker.objects.filter(place__in=places)
            return render(request, 'customer/registeredcustomerhomepage.html', {"detials":values})

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
            last_name = request.POST['name_last']
            email = request.POST['email']
            phone_number = request.POST['number']
            address = request.POST['address']
            place = request.POST['place']
            print(last_name)
            print(phone_number)


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
            if CustomerDetials.objects.filter(user=user).exists():
                customer_detials = CustomerDetials.objects.get(user=user)
                context = {"detials":detials, 'value':user, 'customer_detials':customer_detials}
            else:
                context = {"detials":detials, 'value':user}
            return render(request, 'customer/customerprofile.html', context)
    else:
        return redirect(customer_homepage)


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
        user = request.user
        data = Collection.objects.filter(customer=user)
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
            messages.warning(request, 'You already hired  ' + seeker.name )
            return redirect(registered_customer_homepage)
        else:
            data = Collection.objects.create(customer=user, seeker=seeker, total_price=seeker.expected_salary)
            messages.success(request,seeker.name+'  were added to collection' )
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


def order_verify(request):
    if request.user.is_authenticated:
        user = request.user
        collection = Collection.objects.filter(customer=user)
        total_price = 0
        for x in collection:
            total_price = total_price + x.get_total

        if request.method == "POST":
            name = request.POST['full_name']
            address = request.POST['ad']    
            mobile_number = request.POST['mobile']
            place = request.POST['place']
            land_mark = request.POST['mark']
            durability = request.POST['type']
            time = request.POST['time']
            date = request.POST['date']
            mode_of_payment = request.POST['button']
            transaction_id = uuid.uuid4()
            # payment = request.POST['paymentMethod']
            # collection = Collection.objects.filter(customer=user)

            if durability == "Half day":
                total_price = total_price/2

            
            # to check the distance between customer and seeker 
            for data in collection:
                seeker_place = data.seeker.place
                geolocator = Nominatim(user_agent='user')
        
                destination = geolocator.geocode(seeker_place)
                print(destination)
                d_lon = destination.longitude
                d_lat = destination.latitude
                pointA = (d_lat, d_lon)

                destiny = geolocator.geocode(place)
                sample_lat = destiny.latitude
                sample_lon = destiny.longitude
                pointB = (sample_lat, sample_lon)
                distance = round(geodesic(pointA, pointB).km, 2)

                if distance >= 50:
                    messages.warning(request, 'Sorry,  one of you selected person in 50 km far from you. please select your location and hire people from Home page')
                    return redirect(order_verify)
            
            for x in collection:
                price = x.seeker.expected_salary
                if durability == "Half day":
                    price = price/2
                confirm_order = order.objects.create(customer=user,seeker=x.seeker, durability=durability, total_price=price, name=name, address=address, mobile_number=mobile_number, place=place, land_mark=land_mark, mode_of_payment=mode_of_payment, time=time, date=date, transaction_id=transaction_id)
            collection.delete()

            order_phone = order.objects.filter(transaction_id=transaction_id)
            for x in order_phone:
                phone_number=x.seeker.phone_number
            
                # sms verificaion
                # mobile_number = str(91) + phone_number
                # url = "https://http-api.d7networks.com/send"
                # querystring = {
                # "username":"imjq2616",
                # "password":"MfEcnAqr",
                # "from":"Test%20SMS",
                # "content":"Hi sir, you are hired.Detials you can see in your profile, Please confirm it ASAP",
                # "dlr-method":"POST",
                # "dlr-url":"https://4ba60af1.ngrok.io/receive",
                # "dlr":"yes",
                # "dlr-level":"3",
                # "to":mobile_number,
                # }
                # headers = {
                # 'cache-control': "no-cache"
                # }
                # response = requests.request("GET", url, headers=headers, params=querystring)
                # print(response.text)
                # //sms verification
            
            return redirect(registered_customer_homepage)
        amount = 50000
        order_currency = 'INR'
        # order_receipt = 'order_rcptid_11'
        # notes = {'Shipping address': 'Bommanahalli, Bangalore'} 
        client = razorpay.Client(auth=('rzp_test_7aA8MfBmXS1RVM', 'jO3wj005U2brXjw6XezQfIgZ'))
        payment = client.order.create({'amount':amount, 'currency':'INR', 'payment_capture':'1'})
        detials = CustomerDetials.objects.get(user=user)
        context = {"customer":user, "detials":detials, "collections":collection, "total_price":total_price}
        return render(request, 'customer/order.html', context)
    else:
        return redirect(customer_homepage)


def razorpay_confirm(request):
    if request.user.is_authenticated:
        user = request.user
        collection = Collection.objects.filter(customer=user)
        total_price = 0
        for x in collection:
            total_price = total_price + x.get_total

        if request.method == 'POST':
            user = request.user
            name = request.POST['full_name']
            address = request.POST['ad']    
            mobile_number = request.POST['mobile']
            place = request.POST['place']
            land_mark = request.POST['mark']
            durability = request.POST['type']
            time = request.POST['time']
            date = request.POST['date']
            # mode_of_payment = request.POST['button']
            transaction_id = uuid.uuid4()
            payment = request.POST['paymentMethod']

            print(payment)

            if durability == "Half day":
                total_price = total_price/2

            # to check the distance between customer and seeker 
            for data in collection:
                seeker_place = data.seeker.place
                geolocator = Nominatim(user_agent='user')
        
                destination = geolocator.geocode(seeker_place)
                print(destination)
                d_lon = destination.longitude
                d_lat = destination.latitude
                pointA = (d_lat, d_lon)

                destiny = geolocator.geocode(place)
                sample_lat = destiny.latitude
                sample_lon = destiny.longitude
                pointB = (sample_lat, sample_lon)
                distance = round(geodesic(pointA, pointB).km, 2)

                if distance >= 50:
                    messages.warning(request, 'Sorry,  one of you selected person in 50 km far from you. please select your location and hire people from Home page')
                    return JsonResponse('distance_over',safe=False)

            for x in collection:
                price = x.seeker.expected_salary
                if durability == "Half day":
                    price = price/2
                confirm_order = order.objects.create(customer=user,seeker=x.seeker, durability=durability, total_price=price, name=name, address=address, mobile_number=mobile_number, place=place, land_mark=land_mark, mode_of_payment=payment, time=time, date=date, transaction_id=transaction_id)
            collection.delete()

            order_phone = order.objects.filter(transaction_id=transaction_id)
            for x in order_phone:
                phone_number=x.seeker.phone_number
            
                # sms verificaion
                # mobile_number = str(91) + phone_number
                # url = "https://http-api.d7networks.com/send"
                # querystring = {
                # "username":"imjq2616",
                # "password":"MfEcnAqr",
                # "from":"Test%20SMS",
                # "content":"Hi sir, you are hired.Detials you can see in your profile, Please confirm it ASAP",
                # "dlr-method":"POST",
                # "dlr-url":"https://4ba60af1.ngrok.io/receive",
                # "dlr":"yes",
                # "dlr-level":"3",
                # "to":mobile_number,
                # }
                # headers = {
                # 'cache-control': "no-cache"
                # }
                # response = requests.request("GET", url, headers=headers, params=querystring)
                # print(response.text)
                # //sms verification
            return JsonResponse('success',safe=False)     
    else:
        return redirect(customer_homepage)






def order_confirmation(request):
    if request.user.is_authenticated:
        user =request.user
        print(user)
        order_verify = order.objects.filter(customer=user)
        context = {"order":order_verify}
        return render(request, 'customer/orderconfirmation.html', context)
    else:
        return redirect(customer_homepage)
    


def contact(request):
    if request.user.is_authenticated:
        value = 0
        context = {"value":value}
        return render(request, 'customer/contact.html', context)
    else:
        value = 1
        context = {"value":value}
        return render(request, 'customer/contact.html', context)



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
            messages.info(request, 'invalid credentials')
            return render(request, 'seeker/seekerlogin.html')
    else:
        return render(request, 'seeker/seekerlogin.html')

       
    
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


def edit_profile(request, id):
    if request.session.has_key('user_name'):
        seeker = JobSeeker.objects.get(id=id)
        print(seeker.name)
        context = {"seeker":seeker}
        return render(request, 'seeker/editprofile.html', context)
    else:
        return render(request, 'seeker/seekerlogin.html')
    

def editing_profile(request):
    if request.session.has_key('user_name'):
        if request.method == "POST":
            user = request.session['user_name']
            seeker = JobSeeker.objects.get(username=user)
            # name = request.POST['name']
            # print(name)
            
            seeker.name = request.POST['name']
            seeker.place = request.POST['place']
            seeker.address = request.POST['address']
            seeker.email = request.POST['email']
            seeker.phone_number = request.POST['phone']
            seeker.expected_salary = request.POST['salary']
            seeker.age = request.POST['age']
            seeker.experience = request.POST['experience']
            seeker.username = request.POST['username']
            seeker.image = request.FILES.get('image')
            seeker.save()

        # else
        seeker = JobSeeker.objects.get(username=user)
        context = {"seeker":seeker}
        return render(request, 'seeker/editprofile.html', context)
    else:
        return render(request, 'seeker/seekerlogin.html')



def seeker_order(request, id):
    if request.session.has_key('user_name'):
        print(id)
        my_order = order.objects.filter(seeker=id)
        print(my_order)
        seeker = JobSeeker.objects.get(id=id)
        context = {"my_order":my_order, "seeker":seeker}
        return render(request, 'seeker/seekerorder.html', context)

    else:
        return render(request, 'seeker/seekerlogin.html')


def customer_order_cancel(request, id):
    if request.user.is_authenticated:
        order_data = order.objects.get(id=id)
        mobile_number = str(91) + order_data.seeker.phone_number
        if order_data.customer_cancel == False:
            order_data.customer_cancel = True
        else:
            # sms notification 
            # url = "https://http-api.d7networks.com/send"
            # querystring = {
            # "username":"ibmg4607",
            # "password":"8Hw24TjM",
            # "from":"Test%20SMS",
            # "content":"Sorry.. your order is cancelled by "+ order_data.customer.first_name + order_data.customer.last_name +". Please check your profile for more detials.",
            # "dlr-method":"POST",
            # "dlr-url":"https://4ba60af1.ngrok.io/receive",
            # "dlr":"yes",
            # "dlr-level":"3",
            # "to":mobile_number
            # }
            # headers = {
            # 'cache-control': "no-cache"
            # }
            # response = requests.request("GET", url, headers=headers, params=querystring)
            # print(response.text)
            # //sms notification
            order_data.customer_cancel = False
        order_data.save()
        return redirect(order_confirmation)

    else:
        return redirect(customer_homepage)



def seeker_order_confirm(request, id):
    if request.session.has_key('user_name'):
        order_data = order.objects.get(id=id)
        if order_data.order_verify == False:
            order_data.order_verify = True
            # mobile_number = str(91) + order_data.mobile_number
            # # sms notification 
            # url = "https://http-api.d7networks.com/send"
            # querystring = {
            # "username":"ibmg4607",
            # "password":"8Hw24TjM",
            # "from":"Test%20SMS",
            # "content":"Your order is confirmed by "+ order_data.seeker.name +". Please check your order confirmation for more detials.",
            # "dlr-method":"POST",
            # "dlr-url":"https://4ba60af1.ngrok.io/receive",
            # "dlr":"yes",
            # "dlr-level":"3",
            # "to":mobile_number
            # }
            # headers = {
            # 'cache-control': "no-cache"
            # }
            # response = requests.request("GET", url, headers=headers, params=querystring)
            # print(response.text)
            # //sms notification
        else:
            order_data.order_verify = False
            # mobile_number = str(91) + order_data.mobile_number
            # # sms notification 
            # url = "https://http-api.d7networks.com/send"
            # querystring = {
            # "username":"ibmg4607",
            # "password":"8Hw24TjM",
            # "from":"Test%20SMS",
            # "content":"Your order is cancelled by "+ order_data.seeker.name +" . Please check your order confirmation for more detials.",
            # "dlr-method":"POST",
            # "dlr-url":"https://4ba60af1.ngrok.io/receive",
            # "dlr":"yes",
            # "dlr-level":"3",
            # "to":mobile_number
            # }
            # headers = {
            # 'cache-control': "no-cache"
            # }
            # response = requests.request("GET", url, headers=headers, params=querystring)
            # print(response.text)
            # //sms notification
        order_data.save()
        id = order_data.seeker.id
        return redirect(seeker_order, id)
    else:
        return render(request, 'seeker/seekerlogin.html')



def seeker_feedback(request, id):
    if request.session.has_key('user_name'):
        if request.method =="POST":
            feedback = request.POST['feedback']
            value = order.objects.get(id=id)
            value.seeker_feedback = feedback
            value.save()
            id = value.seeker.id
            return redirect(seeker_order, id)
            # return HttpResponse("success")
    else:
        return render(request, 'seeker/seekerlogin.html')

def customer_feedback(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            feedback = request.POST['feedback']
            value = order.objects.get(id=id)
            value.customer_feedback = feedback
            value.save()
            return redirect(order_confirmation)
    else:
        return redirect(customer_homepage)


def seeker_register(request):
    value = Category.objects.all()
    context = {"value":value}
    if request.method == "POST":
        full_name = request.POST['name']
        email = request.POST['email']
        phone_number = request.POST['phone']
        address = request.POST['address']
        place = request.POST['place']
        age = request.POST['age']
        gender = request.POST['gender']
        cat = Category.objects.get(id=request.POST['category'])
        expected_salary = request.POST['salary']
        user_name = request.POST['username']
        pswrd =  request.POST['password']
        password2 =  request.POST['password1']
        img = request.FILES.get('image')
        experience =  request.POST['experience']
        id_proof = request.FILES.get('proof')

        if pswrd == password2:
            if JobSeeker.objects.filter(username=user_name).exists() or User.objects.filter(email=email).exists():
                if JobSeeker.objects.filter(username=user_name).exists():
                    messages.info(request, 'username already exists')
                    return render(request, 'seeker/register.html', context)
                elif JobSeeker.objects.filter(email=email).exists():
                    messages.info(request, 'email already exists')
                    return render(request, 'seeker/register.html', context)
            else:
                seeker = JobSeeker.objects.create(category=cat,name=full_name,gender=gender,place=place,email=email,phone_number=phone_number,address=address,expected_salary=expected_salary,age=age,username=user_name,password=password2,image=img,experience=experience,id_proof=id_proof)
                return redirect(seeker_login)
        else:
            messages.info(request, 'Password does not match')
            return render(request, 'seeker/register.html')

    else:
        return render(request, 'seeker/register.html', context)

    
def seeker_otp_login(request):
    otp = 1
    if request.method == 'POST':
        phone_number = request.POST['phone']
        request.session['phone_number'] = phone_number
        
        if JobSeeker.objects.filter(phone_number=phone_number).exists():
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
            return render(request, 'seeker/otplogin.html', {'otp':otp})
        else:
            messages.info(request, 'Mobile Number does not exist')
            return render(request, 'seeker/otplogin.html',{'otp':otp})
    else:
        return render(request, 'seeker/otplogin.html', {'otp':otp})


def seeker_otp_verify(request):
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
        # 'Authorization': 'Token 13ff28cd8a3bc23d426420f75b84879c7f958c4c'
        }
        response = requests.request("POST", url, headers=headers, data = payload, files = files)
        print(response.text.encode('utf8'))
        data=response.text.encode('utf8')
        datadict=json.loads(data)
        status=datadict['status']

        if status == 'success':
            phone_number = request.session['phone_number']  
            seeker = JobSeeker.objects.filter(phone_number=phone_number).first()
            user_name = seeker.username
            request.session['user_name'] = user_name
            return redirect(seeker_profile)
        else:
            messages.info(request, 'entered otp is incorrect')
            return redirect(seeker_otp_login)
    else:
        return redirect(seeker_otp_login)


            
 ################################################################### rest API ##############################################################

class rest(APIView):
    def get(self, requests):
        return Response({"status":'done'})

    def post(self, request):
        print(request.data['username'])
        return Response({"status":'done'})

    

class rest_common_home(APIView):
    def get(self, requests):
        return Response({"status":"done"})



#function for giving category detials in rest
class RestCustomerHomepage(APIView):
    def get(self, request):
        category = Category.objects.all()
        category_serialize = SerializeCustomerHomepage(category,many=True)
        return Response(category_serialize.data)

    # def post(get, request):
    #     serializeobj = SerializeCustomerHomepage(data=request.data)
    #     if serializeobj.is_valid():
    #         serializeobj.save()
    #         return Response(serializeobj.data,status=status.HTTP_201_CREATED)
    #     return Response(serializeobj.errors,status=status.HTTP_400_BAD_REQUEST)

#class for giving carpenters detials in rest
class RestSeekerCarpenterDetials(APIView):
    def get(self, request):
        seekers = JobSeeker.objects.filter(category=6)
        print(seekers)
        seekers_serialize = SerilazeSeekerCarpenterDetials(seekers,many=True)
        return Response(seekers_serialize.data)

class RestSeekerConstructionDetials(APIView):
    def get(self, request):
        seekers = JobSeeker.objects.filter(category=11)
        print(seekers)
        seekers_serialize = SerilazeSeekerCarpenterDetials(seekers,many=True)
        return Response(seekers_serialize.data)

class RestSeekerPlumberDetials(APIView):
    def get(self, request):
        seekers = JobSeeker.objects.filter(category=2)
        print(seekers)
        seekers_serialize = SerilazeSeekerCarpenterDetials(seekers,many=True)
        return Response(seekers_serialize.data)


class RestSeekerPainterDetials(APIView):
    def get(self, request):
        seekers = JobSeeker.objects.filter(category=4)
        print(seekers)
        seekers_serialize = SerilazeSeekerCarpenterDetials(seekers,many=True)
        return Response(seekers_serialize.data)

class RestSeekerCateringDetials(APIView):
    def get(self, request):
        seekers = JobSeeker.objects.filter(category=8)
        print(seekers)
        seekers_serialize = SerilazeSeekerCarpenterDetials(seekers,many=True)
        return Response(seekers_serialize.data)


class RestSeekerMaidDetials(APIView):
    def get(self, request):
        seekers = JobSeeker.objects.filter(category=9)
        print(seekers)
        seekers_serialize = SerilazeSeekerCarpenterDetials(seekers,many=True)
        return Response(seekers_serialize.data)


class RestSeekerWelderDetials(APIView):
    def get(self, request):
        seekers = JobSeeker.objects.filter(category=10)
        print(seekers)
        seekers_serialize = SerilazeSeekerCarpenterDetials(seekers,many=True)
        return Response(seekers_serialize.data)

class RestSeekerDriverDetials(APIView):
    def get(self, request):
        seekers = JobSeeker.objects.filter(category=7)
        print(seekers)
        seekers_serialize = SerilazeSeekerCarpenterDetials(seekers,many=True)
        return Response(seekers_serialize.data)