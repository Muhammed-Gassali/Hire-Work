from django.shortcuts import render,redirect,HttpResponse
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

from rest_framework.views import APIView
from rest_framework.response import Response

from geopy.geocoders import Nominatim
# from .utils import get_geo
from geopy.distance import geodesic



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

        if customer is not None and check_password(password,customer.password):
            if customer.is_active == False:
                return Response({"status":"failed"})
            else:
                auth.login(request, customer, backend='django.contrib.auth.backends.ModelBackend')
                context = {"status":success, "username":username}
                return Response(context)
        else:
            return Response({"status":"failed"})

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


# def rest_customer_register(APIView):
#     def post(self, request):
#         name = request.data[]

# fuction for toking location from customer
# def location(request):
#     if request.method == 'POST':
#         place = request.POST['place']
#         # geolocator = Nominatim(user_agent='user')
        
#         # destination = geolocator.geocode(place)
#         # print(destination)
#         # d_lon = destination.longitude
#         # d_lat = destination.latitude
#         # pointA = (d_lat, d_lon)
     
#         # data  = JobSeeker.objects.all()
        
#         # for x in data:
#         #     place_sample = x.place
#         #     destiny = geolocator.geocode(place_sample)
#         #     sample_lat = destiny.latitude
#         #     sample_lon = destiny.longitude
#         #     pointB = (sample_lat, sample_lon)
#         #     distance = round(geodesic(pointA, pointB).km, 2)
#         #     # print(place_sample)
#         #     # print(distance)
#         #     if distance <= 100:
#         #         places = []
#         #         places.append(x)
#         #         print(places)
#         # request.session['places'] = places
#         # context = {"places":places}     
#         return redirect(registered_customer_homepage)
#     else: 
#         return render(request, 'customer/location.html')


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
        # data = Collection.objects.all()
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


def order_verify(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == "POST":
            name = request.POST['full_name']
            address = request.POST['ad']    
            mobile_number = request.POST['mobile']
            place = request.POST['place']
            land_mark = request.POST['mark']
            pincode = request.POST['pin']
            time = request.POST['time']
            date = request.POST['date']
            transaction_id = uuid.uuid4()
            collection = Collection.objects.filter(customer=user)
            for x in collection:
                confirm_order = order.objects.create(customer=user,seeker=x.seeker, name=name, address=address, mobile_number=mobile_number, place=place, land_mark=land_mark, pincode=pincode, time=time, date=date, transaction_id=transaction_id)
            collection.delete()

            order_phone = order.objects.filter(transaction_id=transaction_id)
            for x in order_phone:
                phone_number=x.seeker.phone_number
            
                # sms verificaion
                mobile_number = str(91) + phone_number
                url = "https://http-api.d7networks.com/send"
                querystring = {
                "username":"imjq2616",
                "password":"MfEcnAqr",
                "from":"Test%20SMS",
                "content":"Hi sir, you are hired.Detials you can see in your profile, Please confirm it ASAP",
                "dlr-method":"POST",
                "dlr-url":"https://4ba60af1.ngrok.io/receive",
                "dlr":"yes",
                "dlr-level":"3",
                "to":mobile_number,
                }
                headers = {
                'cache-control': "no-cache"
                }
                response = requests.request("GET", url, headers=headers, params=querystring)
                print(response.text)
                # //sms verification

            return redirect(registered_customer_homepage)
        detials = CustomerDetials.objects.filter(user=user)
        collections = Collection.objects.filter(customer=user)
        total_price = 0
        for x in collections:
            total_price = total_price + x.get_total

        context = {"customer":user, "detials":detials, "collections":collections, "total_price":total_price}
        return render(request, 'customer/order.html', context)
    else:
        return redirect(customer_homepage)


def order_paytm(request):
    param_dict={

            'MID': 'WorldP64425807474247',
            'ORDER_ID': 'order.order_id',
            'TXN_AMOUNT': '1',
            'CUST_ID': 'email',
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL':'http://127.0.0.1:8000/order',

    }
    return  render(request, 'customer/order.html', {'param_dict': param_dict})
    return render(request, 'customer/order.html')
   



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
    return render(request, 'customer/contact.html')

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
        context = {"my_order":my_order}
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
            url = "https://http-api.d7networks.com/send"
            querystring = {
            "username":"ibmg4607",
            "password":"8Hw24TjM",
            "from":"Test%20SMS",
            "content":"Sorry.. your order is cancelled by "+ order_data.customer.first_name + order_data.customer.last_name +". Please check your profile for more detials.",
            "dlr-method":"POST",
            "dlr-url":"https://4ba60af1.ngrok.io/receive",
            "dlr":"yes",
            "dlr-level":"3",
            "to":mobile_number
            }
            headers = {
            'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
            # //sms notification
            order_data.customer_cancel = False
        order_data.save()
        return redirect(order_confirmation)

    else:
        return redirect(customer_homepage)



def seeker_order_confirm(request, id):
    if request.session.has_key('user_name'):
        order_data = order.objects.get(seeker=id)
        if order_data.order_verify == False:
            order_data.order_verify = True
            mobile_number = str(91) + order_data.mobile_number
            # sms notification 
            url = "https://http-api.d7networks.com/send"
            querystring = {
            "username":"ibmg4607",
            "password":"8Hw24TjM",
            "from":"Test%20SMS",
            "content":"Your order is confirmed by "+ order_data.seeker.name +". Please check your order confirmation for more detials.",
            "dlr-method":"POST",
            "dlr-url":"https://4ba60af1.ngrok.io/receive",
            "dlr":"yes",
            "dlr-level":"3",
            "to":mobile_number
            }
            headers = {
            'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
            # //sms notification
        else:
            order_data.order_verify = False
            # sms notification 
            url = "https://http-api.d7networks.com/send"
            querystring = {
            "username":"ibmg4607",
            "password":"8Hw24TjM",
            "from":"Test%20SMS",
            "content":"Your order is cancelled by "+ order_data.seeker.name +" . Please check your order confirmation for more detials.",
            "dlr-method":"POST",
            "dlr-url":"https://4ba60af1.ngrok.io/receive",
            "dlr":"yes",
            "dlr-level":"3",
            "to":mobile_number
            }
            headers = {
            'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
            # //sms notification
        order_data.save()
        return redirect(seeker_order, id)
    else:
        return render(request, 'seeker/seekerlogin.html')

 ################################################################### rest API ##############################################################

class rest(APIView):
    def get(self, requests):
        return Response({"status":'done'})

    def post(self, request):
        print(request.data['username'])
        return Response({"status":'done'})

    

class rest_admin_login(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']
        if username =="admin" and password =="5554":
            return Response({"status":"ok"})
        else:
             return Response({"status":"failed"})


class rest_common_home(APIView):
    def get(self, requests):
        return Response({"status":"done"})


        # ip  = '72.14.207.99'
        # country, city, lat, lon = get_geo(ip)
        # print('location country', country)
        # print('location city', city)
        # print('location lat, lon', lat, lon)
        
        # taking ip's location
        # location = geolocator.geocode(city)
        # print('^%$^%$%', location)