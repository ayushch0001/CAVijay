import json
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.csrf import csrf_exempt

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Log in user after registration
            return redirect('home')  # Redirect to homepage
    else:
        form = UserRegisterForm()
    
    return render(request, r'templates\\base\\register.html', {'form': form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    
    return render(request, r'templates\\base\\login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def home(request):
    return render(request, r'templates\\base\\home.html')




def process_values(request):
    if request.method == "POST":
        values = request.POST.getlist("values[]")  # Retrieve values as a list
        print(values)
        return JsonResponse({"message": "Data received!", "values": values})
    return render(request, r"templates\\module\\form.html")


from django.http import JsonResponse


fruit_data = {
    "apple": "Red",
    "banana": "Yellow",
    "grape": "Purple",
    "orange": "Orange"
}

def get_dropdown_data(request):
     return JsonResponse(fruit_data) 
 
 
 
@csrf_exempt  # Temporarily disable CSRF (Not recommended for production)
def update_dropdown_data(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)  # Get JSON from request
            global fruit_data  # Modify global dictionary (Use DB in production)
            fruit_data.update(data)  # Update all values at once

            return JsonResponse({"message": "Data updated successfully!"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON format"}, status=400)
    
    return JsonResponse({"error": "Only POST allowed"}, status=405)



def home2(request):
    return render(request, r'templates\\module\\dropdown.html')