import json
from .models import *

def cookie_cart(request):
    try:
        cart = json.loads(request.COOKIES['cart'])
    except:
        cart ={}

    items = []
    order = {'order_subtotal': 0, 'items_in_cart': 0, 'order_tax': 0, 'order_total': 0, 'shipping_cost': 0}
    items_in_cart = order['items_in_cart']

    for i in cart:
        try:
            items_in_cart += cart[i]['quantity']

            product = Product.objects.get(id=i)
            total = (product.price) * cart[i]['quantity']

            # Update order dictionary with new amounts
            order['order_subtotal'] += total
            order['items_in_cart'] += cart[i]['quantity']

            # Manually create an orderitem based on same attributes that our model has
            # and append it to the existing list 'items' that will get passed into the 
            # context dictionary
            item = {
                'product': {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'digital': product.digital,
                    'image_url': product.image_url,
                    'category': product.category,
                },
                'quantity': cart[i]['quantity'],
                'cart_price': total,
            }

            items.append(item)

            if product.digital == False:
                order['shipping'] = True
        except:
            pass

    order['order_tax'] = order['order_subtotal'] * 0.06
    order['order_total'] = order['order_subtotal'] + order['order_tax']

    return {
        'items_in_cart': items_in_cart,
        'order': order,
        'items': items,
    }

def cart_data(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        items_in_cart = order.items_in_cart

    else:
        cookie_data = cookie_cart(request)
        items_in_cart = cookie_data['items_in_cart']
        order = cookie_data['order']
        items = cookie_data['items']

    return {
        'items_in_cart': items_in_cart,
        'order': order,
        'items': items,
    }

def category_mgr(request):
    # Returns a dictionary of each category and all the products contained within each respectively

    products_anime = Product.objects.all().filter(category="Anime")    
    products_apparel = Product.objects.all().filter(category="Apparel")    
    products_manga = Product.objects.all().filter(category="Manga")
    products_merchandise = Product.objects.all().filter(category="Merchandise")
    products_wallpaper = Product.objects.all().filter(category="Wallpaper")

    return {
        'anime': ['ANIME', products_anime],
        'apparel': ['APPAREL', products_apparel],
        'manga': ['MANGA', products_manga],
        'merchandise': ['MERCHANDISE', products_merchandise],
        'wallpaper': ['WALLPAPER', products_wallpaper],
    }

def guest_order(request, user_data):
        print('User is not logged in')
        print('Cookies: ', request.COOKIES)

        name = user_data['name']
        email = user_data['email']

        cookie_data = cookie_cart(request)
        items = cookie_data['items']

        # Using information the guest user submitted, create a guest customer model object with the email as the identifier
        customer, created = Customer.objects.get_or_create(email=email)
        customer.name = name
        customer.save()

        # Create an order model object using the above customer and "manually" add the appropriate order items
        order = Order.objects.create(
            customer=customer,
            complete=False,
        )

        for item in items:
            product = Product.objects.get(id=item['product']['id'])
            order_item = OrderItem.objects.create(
                product= product,
                order= order,
                quantity= item['quantity']
            )

        return customer, order