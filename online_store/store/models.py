from django.db import models
from django.contrib.auth.models import User



class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200)

    def __str__(self):
        return self.name


class Product(models.Model):    
    name = models.CharField(max_length=200)    
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)    
    image = models.ImageField(null=True, blank=True)    

    CATEGORIES = (
        ("Anime", "Anime"),
        ("Apparel", "Apparel"),
        ("Manga", "Manga"),
        ("Merchandise", "Merchandise"),
        ("Wallpaper", "Wallpaper"),
    )
    category = models.CharField(max_length=50, choices=CATEGORIES, default="Anime")
    
    def __str__(self):
        return self.name



    @property
    def image_url(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url




class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    shipping_cost = 0

    def __str__(self):
        return str(self.id)

    @property
    def order_subtotal(self):
        order_items = self.orderitem_set.all()
        subtotal = sum([item.cart_price for item in order_items])
        return subtotal

    @property
    def order_tax(self):
        tax = .06 * self.order_subtotal
        return tax

    @property
    def order_total(self):
        total = 1.06 * self.order_subtotal        
        return round(total, 2)

    @property
    def items_in_cart(self):
        # returns how many items are in the cart/order
        order_items = self.orderitem_set.all()
        total = sum([item.quantity for item in order_items])
        return total

    @property
    def shipping_flag(self):
        # returns true if at least one item in the order is NOT digital (ie needs to be shipped)
        shipping_flag = False
        order_items = self.orderitem_set.all()
        for i in order_items:
            if i.product.digital == False:
                shipping_flag = True
        return shipping_flag
    
    # @property
    # def shipping_cost(self):
    #     # returns the shipping cost of the order based on customer's choice in checkout
    #     return 0


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def cart_price(self):
        # returns cost of however many of this particular orderitem exist in cart
        total = self.quantity * self.product.price
        return total

    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    
