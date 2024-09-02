from django.shortcuts import render,redirect,get_list_or_404
from django.http import HttpResponse
from .models import Customers,Category,Product,Cart
import os
from django.core.mail import send_mail,EmailMessage
import random

# Create your views here.
def admin_login(request):
    if request.session.get('admin'):
        request.session.flush()
    
    if request.method=='POST':
        adminname=request.POST.get('adminname')
        pin=request.POST.get('Pin')
        if adminname=='admin' and pin=='1234':
            print('hello')
            request.session['admin']='admin'
            return render(request,'admin_dashboard.html')
    return render(request,'admin_login.html')

def admin_dashboard(request):
    if request.session.get('admin'):
        if request.method=='POST':
            value=request.POST.get('logout')
            print(value)
        return render(request,'admin_dashboard.html')
    else:
        return redirect('admin_login')


def admin_add_section(request):
    if request.session.get('admin'):
        print(request.session.get('admin'))
        id_queryset = Category.objects.values_list('id', flat=True)
        if id_queryset:
            max_integer = max([int(id[1:]) for id in id_queryset if id.startswith('C')], default=0)
            next_id = f'C{max_integer + 1}'
        else:
            next_id = 'C1'
        print(id_queryset)
        
        if request.method == 'POST':
            name = request.POST.get('name').upper()
            des = request.POST.get('des')
            new_category = Category(id=next_id, name=name, des=des)
            new_category.save()
            next_id = f'C{max_integer + 1}'
            return redirect('add_section')
        return render(request, 'admin_add_section.html', {'msg': next_id})
    else:
        return redirect('admin_login')





def admin_add_product(request):
    if request.session.get('admin'):
        categories = Category.objects.all()
        
        # ids = [category.id for category in categories]
        # names = [category.name for category in categories]
        # print(ids,names)
        if request.method=='POST':
            pn=request.POST.get('pname').title()
            price=request.POST.get('price')
            cat=request.POST.get('category')
            if not cat:
                return render(request,'admin_add_product.html',{'id':categories})
                
            cat=Category.objects.get(id=cat)
            des=request.POST.get('des')
            img=request.FILES['image']
            obj=Product(pname=pn,price=price,category=cat,des=des,image=img)
            obj.save()
            print(categories)
            return render(request,'admin_add_product.html',{'id':categories})
        return render(request,'admin_add_product.html',{'id':categories})
    else:
        return redirect('admin_login')
    

def admin_view_product(request):
    if request.session.get('admin'):
        obj=Product.objects.all()
        return render(request,'admin_view_product.html',{'pro':obj})
    else:
        return redirect('admin_login')

def admin_edit_product(request,id):
    obj=Product.objects.get(id=id)
    
    categories = Category.objects.all()
    if request.method=='POST':
        pn=request.POST.get('pname')
        price=request.POST.get('price')
        cat=request.POST.get('category')
        cat=Category.objects.get(id=cat)
        des=request.POST.get('des')
        img=request.FILES.get('image')

        if img:
            print('hello')
            obj=Product(id=obj.id,pname=pn,price=price,category=cat,des=des,image=img)
            obj.save()
            return render(request,'admin_edit_product.html',{'pro':obj,'id':categories})
        else:
            obj=Product(id=obj.id,pname=pn,price=price,category=cat,des=des,image=obj.image )
            obj.save()
            return render(request,'admin_edit_product.html',{'pro':obj,'id':categories})        
    
    return render(request,'admin_edit_product.html',{'pro':obj,'id':categories})


def delete_product(request,id):
    product = Product.objects.get( id=id)
    if request.method == 'POST':
        product.delete()
        os.remove(product.image.path)
        return redirect('view_product')
    return render(request,'delete_product.html')

def home(request):
    
    obj=Product.objects.all()
    obj2=Category.objects.all()
    if request.method=='POST':
     if request.POST.get('cvalue'):
        value=request.POST.get('cvalue')
        obj=Product.objects.filter(category_id=value)
        if not value:
            obj=Product.objects.all()
        return render(request,'home.html',{'obj':obj,'categories':obj2})
     if request.session.get('id'):
      if request.POST.get('pro_id'):
             proid=request.POST.get('pro_id')
             cart=request.session.get('cart',{})
             cart[proid]=1
             request.session['cart']=cart
             val=request.session.get('cart')
     else:
         return redirect('login')
            #  print(val)
     if request.POST.get('pluse'):
            cart=request.session.get('cart',{})
            val=request.POST.get('pluse')
            if val in cart:
                qty=cart[val]
                cart[val]=qty+1
                request.session['cart']=cart
                print(request.session['cart'])
            #  print(request.session.cart)
     if request.POST.get('minus'):
            cart=request.session.get('cart',{})
            val=request.POST.get('minus')
            if val in cart:
                qty=cart[val]
                cart[val]=qty-1
                if cart[val]<=0:
                    del cart[val]
                request.session['cart']=cart
    # print(request.session['cart'],'==============')    
    return render(request,'home.html',{'obj':obj,'categories':obj2})

def signup(request):
     if request.method == 'POST':
        fname = request.POST.get('fname').title()
        lname = request.POST.get('lname').title()
        father = request.POST.get('father').title()
        email = request.POST.get('email')
        obj=Customers.objects.values('email')
        for i in obj:
            if i['email']==email:
                return render(request,'signup.html',{'msg':'Email already found!!'})
        pass1 = request.POST.get('pass1')
        phone = request.POST.get('phone')
        obj1=Customers.objects.values('phone')
        
        for i in obj1:
            if i['phone']==str(phone):
                return render(request,'signup.html',{'msg':'Phone number already found!!'})
                # return redirect('login')
        profile_pic = request.FILES.get('profile_pic')
        
        # Create a new customer instance
        new_customer = Customers( fname=fname,lname=lname,father=father,email=email,pass1=pass1,phone=phone,
            profile_pic=profile_pic
        )
        
        # Save the new customer instance
        new_customer.save()


        return redirect('login') 
    
     return render(request,'signup.html')

def login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        obj1=Customers.objects.values('email')
        # print(obj1)
        for i in obj1:
            if i['email']==email:
                pass1=request.POST.get('Pin')
                obj=Customers.objects.get(email=email)
                if obj:
                    if pass1 == obj.pass1:
                        request.session['id']=obj.id
                        obj=Cart.objects.filter(cus_id=obj.id)
                        
                        # print(obj.values())
                        d={}
                        for ob in obj.values():
                            print(ob,'=========== ob')
                            d[str(ob['product_id'])]=ob['quantity']
                            print(ob['id'])
                        request.session['cart']=d
                        print(d,'=========== dictionary ')
                        # print(request.session.get('cart'),'========== sesssion cart')
                          
                        return redirect('home')
                    else:
                        return render(request,'login.html',{'msg':'Password is incorrect!!'})      
        else:
            return render(request,'login.html',{'msg':'Email is incorrect!!'})        
     
    return render(request,'login.html')

def logout(request):
    
    request.session.flush()
    return redirect('login')



def profile(request):
    customer_id = request.session.get('id')
    if customer_id:
        customer = Customers.objects.get(id=customer_id)
        return render(request, 'profile.html', {'customer': customer})
    else:
        pass


def cart(request):    
    cart = request.session.get('cart', {})
    key = list(map(int, cart.keys()))
    product = Product.objects.filter(id__in=key)
    if request.POST.get('pluse'):
            cart=request.session.get('cart',{})
            val=request.POST.get('pluse')
            if val in cart:
                qty=cart[val]
                cart[val]=qty+1
                request.session['cart']=cart
                # print(request.session['cart'])
            #  print(request.session.cart)
    if request.POST.get('minus'):
            cart=request.session.get('cart',{})
            val=request.POST.get('minus')
            if val in cart:
                qty=cart[val]
                cart[val]=qty-1
                if cart[val]<=0:
                    del cart[val]
                request.session['cart']=cart
                print(request.session['cart'])
    # print(request.session.get('cart'))
    print(request.POST)
    if request.POST.get('delete'):
        pro_id = request.POST.get('delete')
        print(pro_id,'================= delete ')
        if pro_id in cart:
            del cart[pro_id]  
            request.session['cart'] = cart
        customer=request.session['id']
        customer_cart_items = Cart.objects.filter(cus_id=customer)
        for cart_item in customer_cart_items:
            if str(cart_item.product.id) not in cart:
                cart_item.delete()
        return redirect('home')
            
    
    cart = request.session.get('cart', {})
    key = list(map(int, cart.keys()))
    product = Product.objects.filter(id__in=key)
    
    if request.POST.get('chk_out'):
        customer_id = request.session.get('id')
        if customer_id:
                customer = Customers.objects.get(id=customer_id)
                for product_id, quantity in cart.items():
                    product_id = int(product_id)
                    product = Product.objects.get(id=product_id)
                    cart_item, created = Cart.objects.get_or_create(product=product, cus_id=customer, defaults={'quantity': quantity})
                    if not created:
                        cart_item.quantity = quantity
                        cart_item.save()
                customer_cart_items = Cart.objects.filter(cus_id=customer)
                for cart_item in customer_cart_items:
                    if str(cart_item.product.id) not in cart:
                        cart_item.delete()
                return redirect('home')
            
    cart = request.session.get('cart', {})
    key = list(map(int, cart.keys()))
    product = Product.objects.filter(id__in=key)
    return render(request, 'cart.html', {'products': product})

                


def profile_view(request):
    val = request.session.get('id')
    if val:
        customer = Customers.objects.get(id=int(val))
        return render(request, 'profile.html', {'customer': customer})
    
def change_pass(request):
    if request.method=='POST':
        old_pass=request.POST.get('old_password')
        id=request.session['id']
        cust=Customers.objects.get(id=id)
        if cust.pass1==old_pass:
            n1_pass=request.POST.get('new_password1')
            n2_pass=request.POST.get('new_password2')
            if n1_pass==n2_pass:
                obj=Customers(id=id,fname=cust.fname,lname=cust.lname,father=cust.father,email=cust.email,pass1=n1_pass,phone=cust.phone,profile_pic=cust.profile_pic)
                obj.save()
                return redirect('home')
            else:
                err_msg='Password not matching!!'
                return render(request,'change_password.html',{'err_msg':err_msg})
        else:
            err_msg='Old password is not correct'
            return render(request,'change_password.html',{'err_msg':err_msg})
    return render(request,'change_password.html')


def emailOtp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        if 'otp' in request.session:
            stored_otp = request.session['otp']
            if otp == str(stored_otp):
                if pass1 == pass2:
                    id = request.session['id']
                    cust = Customers.objects.get(id=id)
                    cust.pass1 = pass1
                    cust.save()
                    return redirect('home')
                else:
                    msg = 'Passwords do not match!'
                    return render(request, 'emailotp.html', {'msg':msg})
            else:
                msg = 'Invalid OTP!'
                return render(request, 'emailotp.html', {'msg':msg})
        else:
            msg = 'OTP has not been generated!'
            return render(request, 'emailotp.html', {'msg':msg})

    # Generate OTP and send email
    id = request.session.get('id')
    if id:
        cust = Customers.objects.get(id=id)
        rm = random.randint(13800, 29990)
        request.session['otp'] = rm
        subject = 'OTP VERIFICATION'
        message = f'This is your OTP {rm}'
        email = cust.email
        try:
            send_mail(subject, message, 'gogobhaiya7458@gmail.com', [email])
            print(f'OTP sent to {email}')
        except Exception as e:
            msg = f'Error sending email: {e}'
            return render(request, 'emailotp.html', {'msg': msg})

    return render(request, 'emailotp.html')