from django.shortcuts import render
from django.shortcuts import redirect
from .models import MyUser, Product, Purchase, PurchaseReturns
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from .forms import AutUserForm, RegisterUserView, ReturnPurchaseForm, CreateProductViewForm, UpdateProductViewForm, \
    ReturnProductForm, CreatePurchaseForm


# Create your views here.

class ProductView(ListView):
    model = Product
    template_name = 'index.html'
    extra_context = {'form': CreatePurchaseForm}


class ProductListView(ListView):
    model = Product
    template_name = 'product_list.html'
    content_object_name = 'pl'
    extra_context = {'form': CreatePurchaseForm}


class RegisterUserView(CreateView):
    models = MyUser
    form_class = RegisterUserView
    template_name = 'register.html'
    success_url = '/'

    def get_success_url(self):
        return self.success_url

    def form_valid(self, form):
        form_valid = super().form_valid(form)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        aut_user = authenticate(username=username, password=password)
        login(self.request, aut_user)
        return form_valid


class MyloginView(LoginView):
    template_name = 'login.html'
    form_class = AutUserForm
    success_url = '/'

    def get_success_url(self):
        return self.success_url


class MyUserlogout(LogoutView):
    next_page = '/'


class CreateProductView(PermissionRequiredMixin, CreateView):
    permission_required = 'is_superuser'
    model = Product
    form_class = CreateProductViewForm
    template_name = 'create_product.html'
    success_url = '/'


class UpdateProductView(PermissionRequiredMixin, UpdateView):
    permission_required = 'is_superuser'
    model = Product
    template_name = 'update_product.html'
    success_url = '/'
    form_class = UpdateProductViewForm


class ReturnProductView(ListView):
    model = PurchaseReturns
    template_name = 'return_product.html'
    form_class = ReturnProductForm


class PurchasesView(CreateView):
    model = Purchase
    form_class = CreatePurchaseForm
    template_name = 'product_buy.html'
    success_url = '/'

    def form_valid(self, form):
        object = form.save(commit=False)
        object.user = self.request.user
        product = Product.objects.get(id=self.request.POST['product_pk'])
        object.product = product
        sum = object.stock * product.price
        if object.stock > product.stock:
            messages.error(self.request, 'Out of stock')
            return redirect('/')
        elif self.request.user.wallet < sum:
            messages.error(self.request, 'Not enough money')
            return redirect('/')
        else:
            product.stock = product.stock - object.stock
            product.save()
            user = MyUser.objects.get(username=self.request.user)
            user.wallet -= sum
            user.save()
        return super().form_valid(form=form)


class PurchasesListView(ListView):
    model = Purchase
    template_name = 'my_purchase.html'
    context_object_name = 'my_purchases'

    def get_queryset(self):
        return super().get_queryset().filter(user=self.request.user)


class PurchaseReturnsView(CreateView):
    model = PurchaseReturns
    success_url = '/my_purchase/'
    template_name = 'my_purchase.html'
    form_class = ReturnPurchaseForm

    def form_valid(self, form):
        object = form.save(commit=False)
        product = Purchase.objects.get(id=self.request.POST['purchases_return'])
        object.product_return = product
        object.save()
        return super().form_valid(form=form)


class PurchaseReturnsAdminView(ListView):
    model = PurchaseReturns
    template_name = 'product_return.html'
    context_object_name = 'return_purchases'


class PurchaseReturnsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'is_superuser'
    model = PurchaseReturns
    success_url = '/'
    template_name = 'purchase_return_accept.html'

    def post(self, request, *args, **kwargs):
        product = Product.objects.get(id=self.request.POST['product_pk'])
        purchase = Purchase.objects.get(id=self.request.POST['stock'])
        sum = purchase.stock * product.price
        product.stock += purchase.stock
        product.save()
        user = MyUser.objects.get(username=self.request.POST['users'])
        user.wallet += sum
        user.save()
        purchase.delete()
        return super().post(request, *args, **kwargs)


class PurchasesReturnsDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = 'is_superuser'
    model = PurchaseReturns
    success_url = '/'
    template_name = 'purchase_return_reject.html'
