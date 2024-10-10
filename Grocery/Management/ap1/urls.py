from django.urls import path,include
from . import views
from .views import add_bill, bill_list 
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import login_view, logout_view, dashboard, product_list, add_product, add_bill, bill_list,add_product
#from .views import admin

urlpatterns = [
   path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('bills/', views.bill_list, name='bill_list'),
    path('bills/add/', views.add_bill, name='add_bill'),
    path('products/<int:product_id>/update/', views.update_product, name='update_product'),
    
    path('dashboard/calculate_total_amount/', views.calculate_total_amount, name='calculate_total_amount'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)