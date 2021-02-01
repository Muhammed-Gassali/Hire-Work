from django.shortcuts import render,redirect
from django.contrib import messages
from .models import Category,JobSeeker
from django.contrib.auth.models import User,auth
from  django.core.files.storage import FileSystemStorage
from PIL import Image
from django.core.files import File  
# Create your views here.

def admin_login(request):
    if request.session.has_key('admin_username'):
        return redirect(admin_homepage)
    if request.method == "POST":
        admin_username = request.POST['name']
        admin_password = request.POST['password']
        if admin_username == "admin" and admin_password == "5554":
            request.session['admin_username']= admin_username
            return  render(request, 'admin/index.html')
        else:
            messages.info(request, 'invalid credentials')
            return render(request, 'admin/adminlogin.html')
    else:
        return render(request, 'admin/adminlogin.html')


# class rest_admin_login(APIView):
#     def post(self, request):
#         username = request.data['username']
#         password = request.data['password']
#         if username =="admin" and password =="5554":
#             return Response({"status":"success"})
#         else:
#              return Response({"status":"failed"})



def admin_homepage(request):
    if request.session.has_key('admin_username'):
        return render(request, 'admin/index.html')
    else:
        return render(request, 'admin/adminlogin.html')

def customer_management(request):
    if request.session.has_key('admin_username'):
        value = User.objects.all()
        return render(request, 'admin/customermanage.html', {"value":value})
    else:
        return render(request, 'admin/adminlogin.html')

def add_customer(request):
    if request.session.has_key('admin_username'):
        if request.method == 'POST':
            full_name = request.POST['name']
            email = request.POST['email']
            phone_number = request.POST['phone']
            user_name = request.POST['username']
            password1 = request.POST['password']
            password2 = request.POST['password1']
            if password1 == password2:
                if User.objects.filter(username=user_name).exists() or User.objects.filter(email=email).exists():
                    if User.objects.filter(username=user_name).exists():
                        messages.info(request, 'username already exists')
                        return render(request, 'admin/addcustomer.html')
                    elif User.objects.filter(email=email).exists():
                        messages.info(request, 'email already exists')
                        return render(request, 'admin/addcustomer.html')
                else:
                    customer = User.objects.create_user(first_name=full_name, username=user_name, email=email, password=password1, last_name=phone_number)
                    customer.save()
                    return redirect(customer_management)
            else:
                messages.info(request, 'password does not match')
                return render(request, 'admin/addcustomer.html')
        else:
            return render(request, 'admin/addcustomer.html')
    else:
        return render(request, 'admin/adminlogin.html')

def delete_customer(request, id):
    if request.session.has_key('admin_username'):
        value = User.objects.get(id = id)
        value.delete()
        messages.info(request, 'deleted successfully')
        return redirect(customer_management)
    else:
        return render(request, 'admin/adminlogin.html')

def edit_customer(request, id):
    if request.session.has_key('admin_username'):
        data = User.objects.get(id=id)
        return render(request, 'admin/editcustomer.html', {'data':data})
    else:
        return render(request, 'admin/adminlogin.html')

def save_edit(request, id):
    if request.session.has_key('admin_username'):
        if request.method == "POST":
            value = User.objects.get(id=id)
            value.first_name = request.POST['name']
            value.last_name = request.POST['phone']
            value.email = request.POST['email']
            value.save()
            messages.info(request, 'Edited successfully')
            return redirect(customer_management)
    else:
        return render(request, 'admin/adminlogin.html')

def seeker_manage(request):
    if request.session.has_key('admin_username'):
        seeker = JobSeeker.objects.all()
        for s in seeker:
            print(s.ImageURL)
        return render(request, 'admin/seekermanage.html', {'seeker':seeker})
    else:
        return render(request, 'admin/adminlogin.html')

def add_seeker(request):
    if request.session.has_key('admin_username'):
        value = Category.objects.all()
        if request.method == 'POST':
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
            print(img)
            print(gender)
            if pswrd == password2:
                if JobSeeker.objects.filter(username=user_name).exists() or User.objects.filter(email=email).exists():
                    if JobSeeker.objects.filter(username=user_name).exists():
                        messages.info(request, 'username already exists')
                        return render(request, 'admin/addseeker.html', {"value":value}  )
                    elif JobSeeker.objects.filter(email=email).exists():
                        messages.info(request, 'email already exists')
                        return render(request, 'admin/addseeker.html', {"value":value})
                else:
                    seeker = JobSeeker.objects.create(category=cat,name=full_name,gender=gender,place=place,email=email,phone_number=phone_number,address=address,expected_salary=expected_salary,age=age,username=user_name,password=password2,image=img,experience=experience,id_proof=id_proof)
                    # seeker.save()
                    return redirect(seeker_manage)
            else:
                messages.info(request, 'Password does not match')
                return render(request, 'admin/addseeker.html', {"value":value})
        else:
            return render(request, 'admin/addseeker.html', {"value":value})
    else:
        return render(request, 'admin/adminlogin.html')

def delete_seeker(request, id):
    if request.session.has_key('admin_username'):
        value = JobSeeker.objects.get(id = id)
        value.delete()
        messages.info(request, 'deleted successfully')
        return redirect(seeker_manage)
    else:
        return render(request, 'admin/adminlogin.html')

def category_management(request):
    if request.session.has_key('admin_username'):
        category_name = Category.objects.all()
        return render(request, 'admin/categorymanage.html', {"category_name":category_name})
    else:
        return render(request, 'admin/adminlogin.html')

def add_category(request):
    if request.session.has_key('admin_username'):
        if request.method == 'POST':
            category = request.POST['category_name']
            print(category)
            value = Category.objects.create(category_name=category)
            return redirect(category_management)
        else:
            return render(request, 'admin/addcategory.html')
    else:
        return render(request, 'admin/adminlogin.html')


def delete_category(request, id):
    if request.session.has_key('admin_username'):
        value = Category.objects.get(id = id)
        value.delete()
        messages.info(request, 'deleted successfully')
        return redirect(category_management)
    else:
        return render(request, 'admin/adminlogin.html')

def edit_category(request, id):
    if request.session.has_key('admin_username'):
        data = Category.objects.get(id=id)
        return render(request, 'admin/editcategory.html', {'data':data})
    else:
        return render(request, 'admin/adminlogin.html')

def update_category(request, id):
    if request.session.has_key('admin_username'):
        if request.method == "POST":
            value = Category.objects.get(id=id)
            value.category_name = request.POST['name']
            value.image = request.FILES.get('image')
            print(value.image)
            value.save()
            messages.info(request, 'Edited successfully')
            return redirect(category_management)
    else:
        return render(request, 'admin/adminlogin.html')

def admin_logout(request):
    if request.session.has_key('admin_username'):
        request.session.flush()
        return redirect(admin_login)
    else:
        return render(request, 'admin/adminlogin.html')

def edit_seeker(request, id):
    if request.session.has_key('admin_username'):
        if request.method =="POST":
            value = JobSeeker.objects.get(id=id)
            value.name = request.POST['name']
            value.email = request.POST['email']
            value.phone_number = request.POST['phone']
            value.address = request.POST['address']
            value.place = request.POST['place']
            value.age = request.POST['age']
            value.expected_salary = request.POST['salary']
            value.experience = request.POST['experience']
            value.username = request.POST['username']
            

            if 'image' not in request.POST:
                image = request.FILES.get('image')
            else:
                image = value.image
            value.image = image
            value.save()
            return redirect(seeker_manage)

        seeker = JobSeeker.objects.get(id=id)
        category = Category.objects.all()
        context = {"detials":seeker, "category":category}
        return render(request, 'admin/editseeker.html', context)
    else:
        return render(request, 'admin/adminlogin.html')