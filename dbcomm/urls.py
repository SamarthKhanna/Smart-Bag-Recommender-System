from django.conf.urls import url
from django.urls import path 
from dbcomm import views

urlpatterns = [
    url(r'^api/signup$',views.signup_user),
    url(r'^api/login$',views.login_user),
    path('api/products/<str:cat>/',views.products),
    path('api/smartbag/<int:id>/',views.smartbag_products),
    path('api/products/',views.products_all),
    path('api/orders/<str:id>',views.order_by_user),
    path('api/frontpage/',views.load_front_page)
]