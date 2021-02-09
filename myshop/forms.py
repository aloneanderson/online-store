from django import forms
from .models import MyUser, Purchase, Product, PurchaseReturns
from django.contrib.auth.forms import AuthenticationForm


class AutUserForm(AuthenticationForm, forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class RegisterUserView(forms.ModelForm):
    class Meta:
        model = MyUser
        fields = ('username', 'password')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CreateProductViewForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class UpdateProductViewForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class ReturnProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'


class CreatePurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['stock']


class ReturnPurchaseForm(forms.ModelForm):
    class Meta:
        model = PurchaseReturns
        exclude = ['product_return']
