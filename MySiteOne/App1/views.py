from django.db.models.query_utils import Q
from django.shortcuts import get_object_or_404, render,redirect
from django.views import *
from django.contrib import messages
from django.contrib import admin
from django.contrib.auth.models import auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from App1.models import Cart,Products,Customer,Orderplaced
from django.views import *



# def home(request):
#  return render(request, 'app/home.html')
def loginUser(req):
    if req.method == 'POST':
        try:
            obj = User.objects.get(username = req.POST['username'])
            if obj.pas1 == req.POST['password']:
                username = req.POST.get('username')
                req.session['tp'] = username 

                return redirect('home')
            else:
                return HttpResponse('<a href = ''>Password is incorrect!</a>')
        except:
            return HttpResponse('<a href = ''> Username not found!</a> ')
    return render(req, 'app/login.html')


def logoutUSer(req):
    if req.session.has_key('tp'):
        del req.session['tp']
    return redirect('home')

    

def customerregistration(req):
    if req.method == 'POST':
        username = req.POST['username']
        password1 = req.POST['pas1']
        password2 = req.POST['pas2']
        email = req.POST['email']
        phone = req.POST['phone']
        
        if password1 == password2:
            user = User()
            user.username = username
            user.password = password1
            user.pas2 = password2
            user.mail = email
            user.phone = phone
            user.save()

        else:
            return HttpResponse('<a href=''>Password Does Not Match</a>')


    return render(req, 'app/customerregistration.html')

class ProductView(View):
    def get(self,request):
        if request.session.has_key('tp'):
            email = request.session['tp']
            z=User.objects.get(username=email)
            topwears = Products.objects.filter(catogory='TW') 
            mobiles  = Products.objects.filter(catogory='M') #Mobile
            bottomwears = Products.objects.filter(catogory='BW') # Bottom wear
            laptops = Products.objects.filter(catogory='L') # Laptop
            # totalitems = len(Cart.objects.filter(user=request.user))
            return render(request, 'app/home.html',{'topwears':topwears,'mobiles':mobiles,'bottomwears':bottomwears,'laptops':laptops,'z':z})
        else:
            topwears = Products.objects.filter(catogory='TW') #Top-wear
            mobiles  = Products.objects.filter(catogory='M') #Mobile
            bottomwears = Products.objects.filter(catogory='BW') # Bottom wear
            laptops = Products.objects.filter(catogory='L') # Laptop
            # totalitems = len(Cart.objects.filter(user=request.user))
            return render(request, 'app/home.html',{'topwears':topwears,'mobiles':mobiles,'bottomwears':bottomwears,'laptops':laptops,})


        


# def product_detail(request):
#  return render(request, 'app/productdetail.html')


def productview(req,pk):
    # user = req.user
    product = Products.objects.get(pk=pk)
    return render(req,'app/productdetail.html',{'product':product})


def add_to_cart(req,pk):
    if req.session.has_key('tp'):
       a = req.session['tp']
       user = User.objects.get(username = a)
       print(user)
       product = Products.objects.get(pk=pk)
       if Cart.objects.filter(user_id=user.pk,product_id=product.id,status=False).exists():
           messages.info(req,'Item Already is in your cart view your cart ')
           return redirect('main')
       else:
        ob = Cart()
        ob.user = user
        ob.product = product
        ob.save()
        messages.info(req,'Add successfully')
        count = Cart.objects.filter(user_id=user.id,product_id=product.id).count()
        cart = Cart.objects.filter(user_id=user.id,product_id=product.id)
        print("####",count)
        if count>0:
            quantity = cart[0].quantity+1
            price = quantity*product.discounted_price.id
            Cart.objects.filter(user_id=user.id,product_id=product.id).update(quantity=quantity,price=price.id)
            return redirect('home')
        else:
            Cart(user_id=user.id,product_id=product.id,quantity=1,price=product.discounted_price).save()
            return redirect('home')

    
    

def checkout(request):
    if 'tp' in request.session:
        totalitems = 0
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0.0
        shipping_amount = 40.00
        totalamount = 0.0
        cart_product = [p for p in Cart.objects.all() if p.user == user]
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.discounted_price)
                amount += tempamount
            totalamount = amount + shipping_amount
        totalitems = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items,'totalitems':totalitems})
    else:
        return redirect('loginuser')
    


def show_cart(request):
    if 'tp' in request.session:
        per = User.objects.get(username=request.session['tp'])
        totalitems = 0
        # user = request.user
        cart = Cart.objects.filter(user=per.pk)
        amount = 0.0
        shipping_amount = 40
        total_amount = 0.0
        lis = []

        for p in cart:
            lis.append(p.product)
            shipping_amount = shipping_amount + ((p.product.discounted_price)*(p.quantity))
            total_amount = amount + shipping_amount
            return render(request,'app/addtocart.html',{'totalamount':total_amount,'amount':amount,'shipping':shipping_amount,'carts':cart})
        else:
                return render(request,'app/emptycart.html')

        
       
            
    else:
        return redirect('loginuser')


# def plus_cart(request):
    # if request.method == 'GET':
    #     prod_id = request.GET['prod_id']
    #     c = Cart.objects.get(Q(product=prod_id) & Q(user = request.user)) 
    #     c.quantity += 1
    #     c.save()
    #     amount = 0.0
    #     shipping_amount = 40
    #     total_amount = 0.0
    #     cart_product = [p for p in Cart.objects.all() if p.user == request.user]
    #     for p in cart_product:
    #         tempamount = (p.quantity * p.product.discounted_price)
    #         amount += tempamount
    #         totalamount = amount + shipping_amount 

    #     data ={
    #         'quantity': c.quantity, 
    #         'amount': amount,
    #         'totalamount' : totalamount 
    #             }
    #     return JsonResponse(data)

def delete_product(request,pk):
    if 'tp' in request.session:
        totalitems = 0
        rm = get_object_or_404(Cart,pk=pk)
        if request.method == "POST":
            rm.delete()
            totalitems = len(Cart.objects.filter(user=request.user))
            return redirect('showcart')
        return render(request,'app/remove.html',{'carts':rm,'totalitems':totalitems})
    else:
        return redirect('loginuser')
    
def buy_now(request):
    if 'tp' in request.session:
        totalitems = 0
        return render(request, 'app/buynow.html')
    else:
        return redirect('loginuser')
    # totalitems = 0
    # user = request.user
    # product_id = request.GET.get('prod_id')
    # # print(user,product_id)
    # product = Product.objects.get(id=product_id)
    # Cart(user=user,product=product).save()
    # totalitems = len(Cart.objects.filter(user=request.user))

    # return redirect('buynow',{'totalitems':totalitems})


def profile(request):
    totalitems = 0
    if 'tp' in request.session:
        if request.POST:
            usr = request.user
            name = request.POST['name']
            local = request.POST['local']
            city = request.POST['city']
            state = request.POST['state']
            zipcode = request.POST['zipcode']

            data = Customer()
            data.user = usr
            data.name = name
            data.locality = local
            data.city = city
            data.zipcode = zipcode
            data.state = state
            data.save()
            totalitems = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/profile.htm',{'totalitems':totalitems})
    else:
        return redirect('loginuser')
   
def address(request):
    if 'tp' in request.session:
        totalitems = 0
        add = Customer.objects.filter(user=request.user)
        # deladd = get_object_or_404(Customer,pk=pk)
        # if request.method == 'POST':
        #     deladd.delete()
        #     return redirect('address')
        # return render(request, 'app/address.html',{'deladd':deladd})
        totalitems = len(Cart.objects.filter(user=request.user))

        return render(request, 'app/address.html',{'add':add,'totalitems':totalitems})
    else:
        return redirect('loginuser')

    

def orders(request):
    if 'tp' in request.session:
        user = request.user
        totalitems = 0
        op = Orderplaced.objects.filter(user=user)
        totalitems = len(Cart.objects.filter(user=request.user))
        return render(request, 'app/orders.html',{'order_placed':op,'totalitems':totalitems})
    else:    
        return redirect('loginuser')
   

# def change_password(request):
#      totalitems = 0
#      if request.user.is_anonymous:

#         return redirect('loginuser')

#      return render(request, 'app/changepassword.html')

def mobile(request,data=None):
    totalitems = 0
    if data == None:
        mobiles = Products.objects.filter(catogory = 'M')
    elif data == 'Iphone' or data == 'Redmi':
        mobiles = Products.objects.filter(catogory = 'M').filter(brand=data)
    elif data == 'below':
        mobiles = Products.objects.filter(catogory = 'M').filter(discounted_price__lte=10000 )
    elif data == 'above':
        mobiles = Products.objects.filter(catogory = 'M').filter(discounted_price__gt=10000 )
    totalitems = len(Cart.objects.filter(user=request.user))


    return render(request, 'app/mobile.html',{'mobiles':mobiles,'totalitems':totalitems})

def laptop(request,data=None):
    totalitems = 0
    
    if data == None:
        laptops = Products.objects.filter(catogory = 'L')
    elif data == 'Asus' or data == 'Hp' or data == 'MacBook':
       laptops = Products.objects.filter(catogory = 'L').filter(brand=data)
    elif data == 'below':
        laptops = Products.objects.filter(catogory = 'L').filter(discounted_price__lte=50000 )
    elif data == 'above':
        laptops = Products.objects.filter(catogory = 'L').filter(discounted_price__gt=50000 )
    # totalitems = len(Cart.objects.filter(user=request.user))


    return render(request, 'app/laptop.html',{'laptops':laptops,'totalitems':totalitems})

def top(request,data=None):
    totalitems = 0
   
    if data == None:
        tops = Products.objects.filter(catogory = 'TW')
    elif data == 'T-shirt' or data == 'my-top':
        tops = Products.objects.filter(catogory = 'TW').filter(brand=data)
    elif data == 'below':
        tops = Products.objects.filter(catogory = 'TW').filter(discounted_price__lte=1000 )
    elif data == 'above':
        tops = Products.objects.filter(catogory = 'TW').filter(discounted_price__gt=1000 )
    totalitems = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/top.html',{'tops':tops,'totalitems':totalitems})

def bottom(request,data=None):
    totalitems = 0
    
    if data == None:
        bottoms = Products.objects.filter(catogory = 'BW')
    elif data == 'My-Sell' or data == 'jean':
        bottoms = Products.objects.filter(catogory = 'BW').filter(brand=data)
    elif data == 'below':
        bottoms = Products.objects.filter(catogory = 'BW').filter(discounted_price__lte=1000 )
    elif data == 'above':
        bottoms = Products.objects.filter(catogory = 'BW').filter(discounted_price__gt=1000 )
    totalitems = len(Cart.objects.filter(user=request.user))

    return render(request, 'app/bottom.html',{'bottoms':bottoms,'totalitems':totalitems})


# def loginUser(req):
#     if req.method == 'POST':
#         username = req.POST.get('username')
#         password = req.POST.get('password')
#         print(username,password)
#         user = authenticate(username=username, password=password)
#         print(user)
#         if user is not None:
#         # A backend authenticated the credentials
#             login(req,user)
#             return render(req,'app/home.html')
#         else:
#         # No backend authenticated the credentials
#             return render(req,'app/login.html')

#     return render(req, 'app/login.html')




def payment_done(request):
    if 'tp' in request.session:
        user = request.user
        custid = request.GET.get('custid')
        customer = Customer.objects.get(id=custid)
        cart = Cart.objects.filter(user=user)
        for c in cart:
            Orderplaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
            c.delete()
        return redirect('orders')
    else:
        return redirect('loginuser')
   