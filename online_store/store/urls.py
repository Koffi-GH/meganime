from django.urls import path
from . import views

urlpatterns = [
    # Main html pages
    path('', views.home, name="home"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    
    # Individual category pages
    path('products/<str:category>/', views.product_page, name="product_page"),

    # Individual category pages - DEPRECATED
    path('apparel/', views.apparel, name="apparel"),
    path('anime/', views.anime, name="anime"),
    path('manga/', views.manga, name="manga"),
    path('merchandise/', views.merchandise, name="merchandise"),
    path('wallpaper/', views.wallpaper, name="wallpaper"),
    
    # Individual product page (id is number given to product upon admin creation)
    path('<int:id>', views.details, name="details"),

    # Miscellaneous pages
    path('login/', views.login, name="login"),
    path('search/', views.search, name="search"),
    path('about/', views.about, name="about"),

    # Javascript related views
    path('update_item/', views.update_item, name="update_item"),
    path('process_order/', views.process_order, name="process_order"),
    path('update_shipping/', views.update_shipping, name="update_shipping")

]


