from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Record
from .forms import RegisterNewUser, AddRecord

# Create your views here.
def home(request):
    record = Record.objects.all()
    #check if loggin
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You Have Been Logged In")
            return redirect('home')
        else:
            messages.success(request, "There Was An Error")
            return redirect('home')
    else:
        context = {'record':record}
        return render(request,'crmapp/home.html', context)

def login_user(request):
    pass

def logout_user(request):
    logout(request)
    messages.success(request, "You've Been Log Out")
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = RegisterNewUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(request, username=username, password=password)
            login(request, user)
            messages.success(request," You Have Been Registred")
            return redirect('home')
    else:
        form = RegisterNewUser()
    context = {'form': form}
    return render(request, 'crmapp/register.html', context)

def record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(pk=pk)
        context ={'customer_record': customer_record}
        return render(request, 'crmapp/record.html', context)
    else:
        messages.success(request, "You Have to Loggin To Be Able To See Any Data")
        redirect('home')

def delete_user(request, pk):
    if request.user.is_authenticated:
        delete = Record.objects.get(pk=pk)
        delete.delete()
        messages.success(request, "Record Deleted")
        redirect('home')
    else:
        messages.success(request, "You Must Be Loggin .....")
        redirect('home')

def new_record(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = AddRecord(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Record Added")
                return redirect('home')
        else:
            form = AddRecord()
        context = {'form': form}
        return render(request, 'crmapp/addrecord.html', context)
    else:
        messages.success(request, "You Must Be Loggin .....")
        redirect('home')

def update(request, pk):
   if  request.user.is_authenticated:
        current_record = Record.objects.get(pk=pk)
        form = AddRecord(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated")
            return redirect('home')
        else:
            form = AddRecord(instance=current_record)
        context = {'form': form}
        return render(request, 'crmapp/update.html', context)
   else:
       messages.success(request, "You Must Be Loggin .....")
       redirect('home')

