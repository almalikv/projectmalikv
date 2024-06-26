from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import *
from .form import *

# Create your views here.
def landing(request):
    # dictionary for initial data with 
    # field names as keys
    context ={}
 
    # add the dictionary during initialization
    context["products"] = Product.objects.all()
    return render(request, "index.html", context)


def detail_view(request, id):
    print(request.get_full_path())
    context ={}


    # add the dictionary during initialization
    context["data"] = Product.objects.get(ProductID = id)
    context["rev"] = Review.objects.filter(product_id = id)
    return render(request, "product.html", context)

def contact_view(request):
    if request.method == "POST":
        form = ContactsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('contact')
    # context = {}
    # context["products"] = Products.objects.all()
    return render(request, "contact.html")

def cart_view(request):
    if request.method == "POST":
        pass
    return render(request, "cart.html") 


def create_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST or None)
        if form.is_valid():
            form.save()
            id = request.POST.get('product_id')
            return redirect('detail', id = id)
        else:
            # Handle invalid form submission here
            return HttpResponse("Form is not valid", status=400)
    else:
        # Handle other HTTP methods (e.g., GET) if needed
        return HttpResponse("Method not allowed", status=405)

        
def custom_404(request, exception):
    return render(request, '404.html',)

# signup page
def register_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignupForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)    
                return redirect('home')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def user_logout(request):
    logout(request)
    return redirect('login')