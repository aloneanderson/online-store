from django.urls import path
from .views import MyloginView, RegisterUserView, MyUserlogout, ProductView, CreateProductView, UpdateProductView, \
    ReturnProductView, ProductListView, PurchasesView, PurchaseReturnsView, PurchasesListView, PurchaseReturnsView, \
    PurchaseReturnsDeleteView, PurchasesReturnsDeleteView

urlpatterns = [
    path('', ProductView.as_view(), name='index'),
    path('login/', MyloginView.as_view(), name='login_page'),
    path('register/', RegisterUserView.as_view(), name='register_page'),
    path('logout/', MyUserlogout.as_view(), name='logout_page'),
    path('create_product/', CreateProductView.as_view(), name='create_product'),
    path('update_product/<int:pk>/', UpdateProductView.as_view(), name='update_product'),
    path('return_product/', ReturnProductView.as_view(), name='return_product'),
    path('product_list/', ProductListView.as_view(), name='product_list'),
    path('purchase_create/<int:pk>/', PurchasesView.as_view(), name='purchase_create'),
    path('my_purchase/', PurchasesListView.as_view(), name='my_purchase'),
    path('return/', PurchaseReturnsView.as_view(), name='return'),
    path('purchase_return_accept/<int:pk>/', PurchaseReturnsDeleteView.as_view(), name='purchase_return_accept'),
    path('purchase_return_reject/<int:pk>/', PurchasesReturnsDeleteView.as_view(), name='purchase_return_reject'),
]
