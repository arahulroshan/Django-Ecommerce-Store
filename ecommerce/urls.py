from django.contrib import admin
from django.urls import path
from store import views


urlpatterns = [

    path('admin/', admin.site.urls),

    # Home
    path('', views.home, name='home'),

    # Product Details
    path(
        'product/<int:product_id>/',
        views.product_detail,
        name='product_detail'
    ),

    # Cart
    path(
        'add-to-cart/<int:product_id>/',
        views.add_to_cart,
        name='add_to_cart'
    ),

    path(
        'cart/',
        views.cart,
        name='cart'
    ),

    path(
        'remove-from-cart/<int:product_id>/',
        views.remove_from_cart,
        name='remove_from_cart'
    ),

    path(
        'increase-quantity/<int:product_id>/',
        views.increase_quantity,
        name='increase_quantity'
    ),

    path(
        'decrease-quantity/<int:product_id>/',
        views.decrease_quantity,
        name='decrease_quantity'
    ),

    # Authentication
    path(
        'register/',
        views.register,
        name='register'
    ),

    path(
        'login/',
        views.login_view,
        name='login'
    ),

    path(
        'logout/',
        views.logout_view,
        name='logout'
    ),

    # Checkout
    path(
        'checkout/',
        views.checkout,
        name='checkout'
    ),

    # Orders
    path(
        'order-success/<int:order_id>/',
        views.order_success,
        name='order_success'
    ),

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),

    # Cancel Order
    path(
        'cancel-order/<int:order_id>/',
        views.cancel_order,
        name='cancel_order'
    ),
]