from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from core.forms import ProductForm,BrandForm,SupplierForm,CategoryForm
from core.models import Product,Brand,Supplier,Category
from django.contrib import messages

# Create your views here.

def home(request):
   data = {
        "title1":"Autor | TeacherCode",
        "title2":"Super Mercado Economico"
   }
   return render(request,'core/home.html',data)

  #  return HttpResponse(f"<h1>{data['title2']}<h1>\
  #                        <h2>Le da la Bienvenida  a su selecta clientela</h2>")
  #  products = ["aceite","coca cola","embutido"]
  #  prods_obj=[{'nombre': producto} for producto in products] # json.dumps()
  #  return JsonResponse({'mensaje2': data,'productos':prods_obj})

 
  #  return HttpResponse(f"<h1>{data['title2']}<h1>\
  #                      <h2>Le da la Bienvenida  a su selecta clientela</h2>")
# vistas de productos: listar productos 

def signup(request):

    if request.method=='GET':
        return render(request,"signup.html",{
            'form':UserCreationForm  
        })
    else:
        if request.POST['password1']==request.POST['password2']:
            try:
                user = User.objects.create_user(username=request.POST['username'],password=request.POST['password1'])
                user.save()
                login(request,user)
                return redirect('home')
            except IntegrityError:
                return render(request,"signup.html",{
                    'form':UserCreationForm,"error":"El usuario ya existe"
                })
        return render(request,"signup.html",{
            'form':UserCreationForm,"error":"Las contraseñas no coinciden"
        })

def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method=='GET':
        return render(request,'signin.html',{
            'form': AuthenticationForm
        })
    else:
        user = authenticate(request,username=request.POST['username'],password=request.POST['password'])
        if user is None:
            return render(request,'signin.html',{
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        else:
            login(request,user)
            return redirect('home')


def product_List(request):
    data = {
        "title1": "Productos",
        "title2": "Consulta De Productos"
    }
    products = Product.objects.all() # select * from Product
    data["products"]=products
    return render(request,"core/products/list.html",data)

# Vistas de productos: Crear producto
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            
            # Validar si el producto ya existe
            if Product.objects.filter(description=product.description).exists():
                form.add_error('description', '¡El producto ya existe!')
            else:
                product.save()
                form.save_m2m()  # Guardar la relación ManyToMany después de guardar el objeto principal
                messages.success(request, 'Producto creado con éxito')
                return redirect('core:product_list')
    else:
        form = ProductForm()
    
    # Filtrar solo elementos activos
    form.fields['brand'].queryset = Brand.objects.filter(state=True)
    form.fields['supplier'].queryset = Supplier.objects.filter(state=True)
    form.fields['categories'].queryset = Category.objects.filter(state=True)

    return render(request, 'core/products/form.html', {'form': form, 'title2': 'Crear Producto'})

# Vistas de productos: Actualizar producto
def product_update(request, id):
    data = {"title1": "Productos", "title2": "Edición De Productos"}
    product = get_object_or_404(Product, pk=id)
    
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            try:
                form.save()
                return redirect("core:product_list")
            except IntegrityError:
                form.add_error(None, 'Error de integridad: Producto ya existente.')
    else:
        form = ProductForm(instance=product)

    data["form"] = form
    return render(request, "core/products/form.html", data)

# eliminar un producto
def product_delete(request,id):
    product = Product.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Un Producto","product":product}
    if request.method == "POST":
        product.delete()
        return redirect("core:product_list")
 
    return render(request, "core/products/delete.html", data)



# vistas de marcas: Listar marcas
def brand_List(request):
    data = {
        "title1": "Marcas",
        "title2": "Consulta De Marcas De Productos"
    }
    brands = Brand.objects.all()
    data["brands"]=brands
    return render(request,"core/brands/list.html",data)

# Vistas de marcas: Crear marca
def brand_create(request):
    data = {"title1": "Marcas", "title2": "Ingreso De Marcas"}
   
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.save(commit=False)
            brand.user = request.user
            try:
                brand.save()
                messages.success(request, 'Marca creada con éxito')
                return redirect("core:brand_list")
            except IntegrityError:
                form.add_error(None, 'Marca ya existente.')
    else:
        form = BrandForm()

    data["form"] = form
    return render(request, "core/brands/form.html", data)
    
def brand_update(request, id):
    data = {"title1": "Marcas", "title2": "Edición De Marcas"}
    brand = get_object_or_404(Brand, pk=id)
    
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            try:
                form.save()
                return redirect("core:brand_list")
            except IntegrityError:
                form.add_error(None, 'Error de integridad: El nombre de la marca ya está en uso.')
    else:
        form = BrandForm(instance=brand)

    data["form"] = form
    return render(request, "core/brands/form.html", data)

#Vista de marcas: Eliminar una marca
def brand_delete(request,id):
    brand = Brand.objects.get(pk=id)
    data = {"title1":"Eliminar","title2":"Eliminar Una Marca","brand":brand}
    if request.method == "POST":
        brand.delete()
        return redirect("core:brand_list")
    
    return render(request,"core/brands/delete.html",data)


#Vista de proveedores: Listar proveedores
def supplier_List(request):
    data = {
        "title1": "Proveedores",
        "title2": "Consulta De Proveedores"
    }
    suppliers = Supplier.objects.all() # select * from Product
    data["suppliers"]=suppliers
    return render(request,"core/suppliers/list.html",data)

def supplier_create(request):
    data = {"title1": "Proveedores", "title2": "Ingreso De Proveedores"}
   
    if request.method == "POST":
        form = SupplierForm(request.POST, request.FILES)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.user = request.user
            try:
                supplier.save()
                messages.success(request, 'Proveedor creado con éxito')
                return redirect("core:supplier_list")
            except IntegrityError:
                form.add_error(None, 'El número de cédula o teléfono ya está en uso.')
    else:
        form = SupplierForm()

    data["form"] = form
    return render(request, "core/suppliers/form.html", data)
    
def supplier_update(request, id):
    data = {"title1": "Proveedores", "title2": "Edición De Proveedores"}
    supplier = get_object_or_404(Supplier, pk=id)
    
    if request.method == "POST":
        form = SupplierForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            try:
                form.save()
                return redirect("core:supplier_list")
            except IntegrityError:
                form.add_error(None, 'Error de integridad: El RUC o el número de teléfono ya está en uso.')
    else:
        form = SupplierForm(instance=supplier)

    data["form"] = form
    return render(request, "core/suppliers/form.html", data)

def supplier_delete(request,id):
    supplier = Supplier.objects.get(pk=id)
    data = {"title1": "Eliminar","title2":"Eliminar un proveedor","supplier":supplier}
    if request.method == "POST":
        supplier.delete()
        return redirect("core:supplier_list")
    
    return render(request,"core/suppliers/delete.html", data)

############CATEGORIAS

def category_List(request):
    data = {
        "title1": "Categorias",
        "title2": "Consulta De Categorias"
    }
    categories = Category.objects.all() # select * from Product
    data["categories"]=categories
    return render(request,"core/categories/list.html",data)

# Vistas de categorías: Crear categoría
def category_create(request):
    data = {"title1": "Categorias", "title2": "Ingreso De Categorias"}
   
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            try:
                category.save()
                messages.success(request, 'Categoria creada con éxito')
                return redirect("core:category_list")
            except IntegrityError:
                form.add_error(None, 'El nombre de la categoria ya está en uso.')
    else:
        form = CategoryForm()

    data["form"] = form
    return render(request, "core/categories/form.html", data)

# Vistas de categorías: Actualizar categoría
def category_update(request, id):
    data = {"title1": "Categorias", "title2": "Edición De Categorias"}
    supplier = get_object_or_404(Category, pk=id)
    
    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=supplier)
        if form.is_valid():
            try:
                form.save()
                return redirect("core:category_list")
            except IntegrityError:
                form.add_error(None, 'Error de integridad: El nombre de la categoria ya está en uso.')
    else:
        form = CategoryForm(instance=supplier)

    data["form"] = form
    return render(request, "core/categories/form.html", data)

def category_delete(request,id):
    category = Category.objects.get(pk=id)
    data = {"title1": "Eliminar","title2":"Eliminar una categoria","category":category}
    if request.method == "POST":
        category.delete()
        return redirect("core:category_list")
    
    return render(request,"core/categories/delete.html", data)