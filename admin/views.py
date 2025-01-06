from django.shortcuts import render, redirect
from .models import App
from django.contrib.auth.models import User, auth
from django.contrib import messages
# Create your views here.

# def admin(request):
#     if request.method =='POST':
        
#         # app_icon = request.POST.get('app_icon')
#         app_icon = request.FILES.get('app_icon')
        
#         app_name = request.POST.get('app_name')
#         app_link = request.POST.get('app_link')
#         app_category = request.POST.get('app_category')
#         sub_category = request.POST.get('sub_category')
#         points = request.POST.get('points')

#         fb = App(app_icon=app_icon, app_name=app_name,app_link=app_link,app_category=app_category,sub_category=sub_category,points=points)
#         fb.save()
        
#         return render(request, 'admin.html')


#     a = App.objects.all()
#     # aa = App.objects.filter(app_name='Facebook').values()

#     # print(aa)
#     return render(request, 'admin.html')
from django.shortcuts import render, redirect
from .models import App
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required  # Ensure the admin is logged in
def admin(request):
    if request.method == 'POST':
        app_icon = request.FILES.get('app_icon')  # Get uploaded file
        app_name = request.POST.get('app_name')
        app_link = request.POST.get('app_link')
        app_category = request.POST.get('app_category')
        sub_category = request.POST.get('sub_category')
        points = request.POST.get('points')

        # Validate form inputs
        if not app_icon or not app_name or not app_link or not app_category or not sub_category or not points:
            messages.error(request, "All fields are required.")
            return render(request, 'admin.html')

        # Save the new App instance
        fb = App(
            app_icon=app_icon,
            app_name=app_name,
            app_link=app_link,
            app_category=app_category,
            sub_category=sub_category,
            points=points
        )
        fb.save()
        messages.success(request, "App added successfully!")
        
        # Redirect to the admin page to prevent form resubmission
        return redirect('admin')  # Redirect to admin page

    # Retrieve all Apps for displaying in the admin panel
    apps = App.objects.all()
    return render(request, 'admin.html', {'apps': apps})



def signin(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        

        if password1 == password2:

            if User.objects.filter(username=username).exists():
                messages.info(request, 'username taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'email already taken')
                return redirect('register')
            else:
                user = User.objects.create_user(
                username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.is_staff = True
                user.save()
                messages.info(request, 'registration successful')
                return redirect('register')
        else:
            messages.info(request, 'password not matching')
            return redirect('register')

        
        

    else:
        return render(request, 'register.html')
    


# def login(request):

#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = auth.authenticate(username=username, password=password)

#         if user is not None:
#             auth.login(request, user)
#             # messages.info(request, 'login successful')
#             return render(request, 'admin.html')
#         else:
#             messages.info(request, 'Invalid Credentials')
#             return render(request, 'login.html')
#     else:
#         return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            if user.is_staff:  # Check if the user is a staff member
                auth.login(request, user)
                # Redirect to the admin page or any other desired page
                return render(request, 'admin.html')
            else:
                messages.error(request, 'Invalid Credentials')  # Non-staff users cannot log in
                return render(request, 'login.html')
        else:
            messages.error(request, 'Invalid Credentials')  # Incorrect username or password
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')

from rest_framework import viewsets
from .models import App
from .serializers import AppSerializer

class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.all()
    serializer_class = AppSerializer
