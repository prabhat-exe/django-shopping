from django import template
from myapp.models import Customers,Product,Category

register= template.Library()

@register.filter
def profile_pic_url(id):
    user_profile = Customers.objects.get(id=id)
    return user_profile.profile_pic.url

@register.filter
def name_from_id(id):
    user_name=Customers.objects.get(id=id)
    return user_name.fname


@register.filter
def get_item(dictionary, key):
    return dictionary.get(str(key), 0)  # default to 0 if the key is not found

@register.filter
def Checkbutton(pid,cart):
    print(cart,pid)
    val=list(cart.keys())
    for i in val:
        if int(i)==pid:
            return True
    else:
        return False    
    

@register.filter(name='get_cart_quantity')
def get_cart_quantity(cart, product_id):
    return cart.get(str(product_id),0)

@register.filter
def get_total(cart,product_id):
    pro=Product.objects.get(id=int(product_id))
    # print(pro)
    qty=cart[str(pro.id)]
    return pro.price*qty

@register.filter
def grand_total(cart):
    sum=0
    for k in cart.keys():   
        sum = sum + get_total(cart,k)
    return sum



