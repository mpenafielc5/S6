from django import forms
from core.models import Product, Brand, Supplier, Category
from django.core.exceptions import ValidationError

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'description', 'price', 'stock', 'brand', 'categories', 
            'line', 'supplier', 'expiration_date', 'image', 'state'
        ]

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        self.fields['brand'].queryset = Brand.objects.filter(state=True)
        self.fields['supplier'].queryset = Supplier.objects.filter(state=True)
        self.fields['categories'].queryset = Category.objects.filter(state=True)

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if Product.objects.filter(description=description).exclude(id=self.instance.id).exists():
            raise ValidationError('El nombre del producto ya está en uso.')
        return description

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price < 0.1:
            raise ValidationError('El precio mínimo debe ser 0.1.')
        return price
    
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['description', 'state']

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if Brand.objects.filter(description=description).exclude(id=self.instance.id).exists():
            raise ValidationError('El nombre de la marca ya está en uso.')
        return description

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'ruc', 'address', 'phone', 'state']

    def clean_ruc(self):
        ruc = self.cleaned_data.get('ruc')
        if Supplier.objects.filter(ruc=ruc).exclude(id=self.instance.id).exists():
            raise ValidationError('El RUC ya está en uso.')
        return ruc

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if Supplier.objects.filter(phone=phone).exclude(id=self.instance.id).exists():
            raise ValidationError('El número de teléfono ya está en uso.')
        return phone


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['description', 'state']

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if Category.objects.filter(description=description).exclude(id=self.instance.id).exists():
            raise ValidationError('La categoría ya existe.')
        return description
