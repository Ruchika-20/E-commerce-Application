from email.mime import image
from http.client import HTTPResponse
from multiprocessing import context
from re import M
from urllib import request
from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Product
from django.views.generic import ListView

# Create your views here.
def index(request):
    return HttpResponse("Hello")


def products(request):
   page_obj=products=Product.objects.all()

#Search functionality begins 
   product_name =  request.GET.get('product_name')
   if product_name!='' and product_name is not None:
    page_obj = products.filter(name__icontains=product_name)   #this icontains method looks for an approximate match
   
#Search functionality ends 
   paginator = Paginator(page_obj,3)
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)
   context = {
        "page_obj": page_obj
   }
   return render(request,"myapp/index.html",context)

# Class based view demonstration for above view
# class ProductListView(ListView):
#     model= Product
#     template_name = 'myapp/index.html'
#     context_object_name = 'products'
#     paginate_by = 3
#     in order to use this for pagination we just need to replacet the context obj in index.html from page_obj to products since here the name is products.



def product_detail(request,id):
    product=Product.objects.get(id=id)
    context={
        "product": product
    }
    return render(request,"myapp/detail.html",context)
    # return HttpResponse("Id is : " + str(id) )

@login_required
def add_product(request):
    if request.method=="POST":
        name=request.POST.get('name')
        price=request.POST.get('price')
        desc=request.POST.get('desc')
        image=request.FILES.get('upload')
        seller_name = request.user
        product=Product(name=name,price=price,desc=desc,image=image,seller_name=seller_name)
        product.save()

    return render(request,"myapp/addproduct.html")


def update_product(request,id):
        product= Product.objects.get(id=id)
        if request.method == 'POST':
            product.name = request.POST.get('name')
            product.price = request.POST.get('price')
            product.desc = request.POST.get('desc')
            product.image = request.FILES.get('upload')
            product.save()
            return redirect('/myapp/products')
            
        context = {
            'product':product,
        }
        return render(request,'myapp/updateproduct.html',context)


def delete_product(request,id):
    product = Product.objects.get(id=id)
    if request.method == "POST":
        product.delete()
        return redirect('/myapp/products')
    context = {
        'product':product,

        }
    return render(request,'myapp/delete.html',context)


def my_listings(request):
    products = Product.objects.filter(seller_name=request.user)
    context={
        'products':products,
    }

    return render(request, 'myapp/mylistings.html',context)
