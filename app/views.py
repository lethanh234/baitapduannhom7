from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import JsonResponse
import openai
from django.db.models import Q
import pandas as pd


def ask_openai(message):
    response = openai.ChatCompletion.create(  
        model="gpt-3.5-turbo",  
        messages=[ 
            {"role": "user", "content": message}
        ]
    )
    answer = response['choices'][0]['message']['content'].strip()  
    return answer


def chatbot(request):
    if request.method == 'POST':
        message = request.POST.get('message')  
        k = message.lower()  
        a = []
        word = ''
        for i in k + ' ':
            if i.isalpha() or i.isdigit(): 
                word += i 
            else:
                if word:  
                    a.append(word)
                word = ''
        query = Q()
        for word in a:  
            query |= Q(name__icontains=word)  # tìm các sản phẩm trên database
            # |= là or 
        res = Product.objects.filter(query) # lấy các sản phẩm trên database 
        if res.exists():  # kiểm tra xem có sản phẩm tìm đc k
            response = []
            for i in res:
                response.append(f"tên sản phẩm  : {i.name}, giá : {i.price}")
        else:
            response = ["Không tìm thấy sản phẩm phù hợp."]
        
        return JsonResponse({'message': message, 'response': response})
    
    return render(request, 'app/chatbot.html')



        


def register(request):
    form = CreateUserForm() # tạo form
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request,'app/register.html',context)


def loginPage(request):
    if request.user.is_authenticated: # ktra ng dùng login chưa
        return redirect('home') # đã login chuyển đến trang home
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username = username , password = password) # lấy thông tin từ trang login và check 
        if user is not None:
            login(request,user)
            return redirect('home')
        else: messages.info(request,'user or password not correct!')
    context = {}
    return render(request,'app/login.html',context)

def logoutPage(request):
    logout(request)
    return redirect('login')

def home(request):
    products = Product.objects.all() 
    context= {'products': products}
    return render(request,'app/home.html',context)



def search(request):
    if request.method == "POST":
        searched = request.POST["searched"]
        keys = Product.objects.filter(name__contains = searched)
    return render(request,'app/search.html',{"searched":searched,"keys":keys})



def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
    else :
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
    context= {'items':items,'order':order}
    return render(request,'app/cart.html',context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all()
    else :
        items = []
        order = {'get_cart_items':0,'get_cart_total':0}
    context= {'items':items,'order':order}
    return render(request,'app/checkout.html',context)


