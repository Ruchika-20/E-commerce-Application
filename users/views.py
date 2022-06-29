from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from .models import Profile
from django.contrib.auth.models import User
# Create your views here.

def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)    #created the object of class newuserform
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request,"Registration Successful.")
            return redirect('myapp:products')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="users/register.html", context={"form":form})
   

@login_required         
def profile(request):
    return render(request,'users/profile.html')

def create_profile(request):
    if request.method == "POST":
        contact_number =  request.POST.get('contact_number')
        image = request.FILES['upload']
        user = request.user
        profile=Profile(user=user,image=image,contact_number=contact_number)
        profile.save()
    return render(request,'users/createprofile.html')

def seller_profile(request,id):
    seller = User.objects.get(id=id)
    context = {
        'seller':seller,
    }
    return render(request,'users/sellerprofile.html',context)