from django import forms
from core.models import Product,Brand,Supplier,Category

class ProductForm(forms.ModelForm):
    class Meta:
        model=Product
        fields=['description','price','stock','brand','categories','line','supplier','expiration_date','image','state']

class BrandForm(forms.ModelForm):
    class Meta:
        model=Brand
        fields=['description','state']

class SupplierForm(forms.ModelForm):
    class Meta:
        model=Supplier
        fields=['name','ruc','address','phone','state']

class CategoryForm(forms.ModelForm):
    class Meta:
        model=Category
        fields=['description','state']