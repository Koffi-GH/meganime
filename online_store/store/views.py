from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import random
import json
import datetime
from .utils import cart_data, category_mgr, cookie_cart, guest_order

def home(request):
    data = cart_data(request)

    items_in_cart = data['items_in_cart']
    order = data['order']
    items = data['items']  

    products = category_mgr(request)

    featured_anime = random.choice(products['anime'][1])
    featured_manga = random.choice(products['manga'][1])
    featured_merchandise = random.choice(products['merchandise'][1])
    featured_apparel = random.choice(products['apparel'][1])
    featured_wallpaper = random.choice(products['wallpaper'][1])

    featured_items = [
        featured_anime, featured_manga, featured_merchandise, featured_apparel, featured_wallpaper
    ]
    
    context = {"featured_items": featured_items, "items_in_cart": items_in_cart}

    return render(request, 'home.html', context)

def cart(request):    
    data = cart_data(request)

    items_in_cart = data['items_in_cart']
    order = data['order']
    items = data['items']

    context = {"items": items, "items_in_cart": items_in_cart, 'order': order, 'shipping_flag': False}
    
    return render(request, 'cart.html', context)

def checkout(request):
    data = cart_data(request)

    items_in_cart = data['items_in_cart']
    order = data['order']
    items = data['items']

    # if request.user.is_authenticated:
    #     pass
    # else:
    #    order_shipping = order['order_shipping']
    


    context = {"order": order, "items": items, "items_in_cart": items_in_cart}

    return render(request, 'checkout.html', context)

def anime(request):
    # DEPRECATED
    data = cart_data(request)

    items_in_cart = data['items_in_cart']
    order = data['order']
    items = data['items']


    products_anime = Product.objects.all().filter(category="Anime")    

    context = {"products_anime" : products_anime, "items_in_cart": items_in_cart}

    return render(request, 'anime.html', context)

def apparel(request):
    # DEPRECATED
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        items_in_cart = order.items_in_cart

    else:
        items = []
        order = {'order_subtotal': 0, 'items_in_cart': 0, 'shipping_flag': False}
        items_in_cart = order['items_in_cart']


    products_apparel = Product.objects.all().filter(category="Apparel") 

    context = {"products_apparel" : products_apparel, "items_in_cart": items_in_cart}

    return render(request, 'apparel.html', context)

def manga(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        items_in_cart = order.items_in_cart

    else:
        items = []
        order = {'order_subtotal': 0, 'items_in_cart': 0, 'shipping_flag': False}
        items_in_cart = order['items_in_cart']


    products_manga = Product.objects.all().filter(category="Manga")

    context = {"products_manga" : products_manga, "items_in_cart": items_in_cart}

    return render(request, 'manga.html', context)

def merchandise(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        items_in_cart = order.items_in_cart

    else:
        items = []
        order = {'order_subtotal': 0, 'items_in_cart': 0, 'shipping_flag': False}
        items_in_cart = order['items_in_cart']


    products_merchandise = Product.objects.all().filter(category="Merchandise")

    context = {"products_merchandise" : products_merchandise, "items_in_cart": items_in_cart}

    return render(request, 'merchandise.html', context)

def wallpaper(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        items_in_cart = order.items_in_cart

    else:
        items = []
        order = {'order_subtotal': 0, 'items_in_cart': 0, 'shipping_flag': False}
        items_in_cart = order['items_in_cart']


    products_wallpaper = Product.objects.all().filter(category="Wallpaper")

    context = {"products_wallpaper" : products_wallpaper, "items_in_cart": items_in_cart}

    return render(request, 'wallpaper.html', context)

def search(request):
    data = cart_data(request)

    items_in_cart = data['items_in_cart']
    order = data['order']
    items = data['items']


    query = request.GET.get('search')
    if query:
        query_set = Product.objects.filter(name__icontains=query)
    else:
        query_set = None

    context = {"items_in_cart": items_in_cart, "query_set": query_set}

    return render(request, 'search.html', context)

def about(request):
    data = cart_data(request)

    items_in_cart = data['items_in_cart']
    order = data['order']
    items = data['items']


    context = {"items_in_cart": items_in_cart}

    return render(request, 'about.html', context)

def login(request):
    data = cart_data(request)

    items_in_cart = data['items_in_cart']
    order = data['order']
    items = data['items']

    
    context = {"items_in_cart": items_in_cart}

    return render(request, 'login.html', context)

def product_page(request, category):
    # Category should be a string stating the name of the category
    data = cart_data(request)
    product_data = category_mgr(request)

    items_in_cart = data['items_in_cart']
    order = data['order']
    items = data['items']

    product_category = product_data[category][0]
    products = product_data[category][1]

    context = {"product_category": product_category, "products": products, "items_in_cart": items_in_cart}

    return render(request, 'product.html', context)

def details(request, id):
    data = cart_data(request)

    items_in_cart = data['items_in_cart']
    order = data['order']
    items = data['items']

    highlighted_product = Product.objects.get(pk=id)    
        
    context = {"items_in_cart": items_in_cart, "highlighted_product": highlighted_product}

    return render(request, 'details.html', context)

def update_item(request):
    # Load information passed from POST request at front end and store in 2 variables
    data = json.loads(request.body)
    product_id = data['productId']
    action = data['action']

    print(action, product_id)

    # Query customer and retrieve appropriate order item given the order, the product, and the customer
    customer = request.user.customer
    product = Product.objects.get(id=product_id)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        order_item.quantity += 1
    elif action == 'remove':
        order_item.quantity -= 1
    order_item.save()

    if order_item.quantity <= 0:
        order_item.delete()

    return JsonResponse('Item was added to cart', safe=False)

def process_order(request):
    # Load information passed from POST request at front end and store in 2 variables
    data = json.loads(request.body)
    user_data = data['user']
    shipping_data = data['shipping']
    total = user_data['total']
    
    # Assign ID to transaction based on time of transaction
    transaction_id = datetime.datetime.now().timestamp()

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)



    else:
        customer, order = guest_order(request, user_data)
   
    order.transaction_id = transaction_id       

    if total == user_data['shipping'] + order.order_total:                  
        order.complete = True       
    order.save()

    if order.shipping_flag:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=shipping_data['address'],
            city=shipping_data['city'],
            state=shipping_data['state'],
            zipcode=shipping_data['zipcode']
        )

    return JsonResponse('Payment submitted, information received from front end', safe=False)

def update_shipping(request):
    # Load shipping cost passed from POST request at front end and use to set
    # order model's total cost and shipping cost attributes

    data = json.loads(request.body)
    shipping_cost = data['cost']
    

    # If customer is logged in
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

        order.shipping_cost = shipping_cost
        order.save()


    # If customer is a guest user
    else:
        cart_info = cart_data(request)
        abc = cart_info['order']['order_shipping']
