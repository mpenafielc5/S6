from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth import login,logout,authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from core.forms import ProductForm,BrandForm,SupplierForm,CategoryForm
from core.models import Product,Brand,Supplier,Category

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

# crear un producto
def product_create(request):
    data = {"title1": "Productos","title2": "Ingreso De Productos"}
   
    if request.method == "POST":
        #print(request.POST)
        form = ProductForm(request.POST,request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.user = request.user
            product.save()
            return redirect("core:product_list")

    else:
        data["form"] = ProductForm() # controles formulario sin datos

    return render(request, "core/products/form.html", data)

# editar un producto
def product_update(request,id):
    data = {"title1": "Productos","title2": ">Edicion De Productos"}
    product = Product.objects.get(pk=id)
    if request.method == "POST":
      form = ProductForm(request.POST,request.FILES, instance=product)
      if form.is_valid():
            form.save()
            return redirect("core:product_list")
    else:
        form = ProductForm(instance=product)
        data["form"]=form
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

#Vista de marcas: Crear marcas
def brand_create(request):
    data={"title1":"Marcas","title2":"Ingreso de marcas"}

    if request.method=="POST":
        form=BrandForm(request.POST,request.FILES)
        if form.is_valid():
            brand=form.save(commit=False)
            brand.user=request.user
            brand.save()
            return redirect("core:brand_list")
    else:
        data["form"] = BrandForm()

    return render(request,"core/brands/form.html",data)

#Vista de marcas: Editar una marca
def brand_update(request,id):
    data={"title1": "Marcas","title2": ">Edicion de Marcas"}
    brand=Brand.objects.get(pk=id)
    if request.method=="POST":
        form = BrandForm(request.POST,request.FILES,instance=brand)
        if form.is_valid():
            form.save()
            return redirect("core:brand_list")
    else:
        form = BrandForm(instance=brand)
        data["form"]=form
    return render(request,"core/brands/form.html", data)

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
    data = {"title1": "Proveedores","title2": "Ingreso De Proveedores"}
   
    if request.method == "POST":
        form = SupplierForm(request.POST,request.FILES)
        if form.is_valid():
            supplier = form.save(commit=False)
            supplier.user = request.user
            supplier.save()
            return redirect("core:supplier_list")

    else:
        data["form"] = SupplierForm() # controles formulario sin datos

    return render(request, "core/suppliers/form.html", data)
    
def supplier_update(request,id):
    data = {"title1": "Proveedores","title2": ">Edicion De Proveedores"}
    supplier = Supplier.objects.get(pk=id)
    if request.method == "POST":
        form = SupplierForm(request.POST,request.FILES,instance=supplier)
        if form.is_valid():
            form.save()
            return redirect("core:supplier_list")
    else:
        form = SupplierForm(instance=supplier)
        data["form"]=form
    return render(request,"core/suppliers/form.html", data)

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

def category_create(request):
    data = {"title1": "Categorias","title2": "Ingreso De Categorias"}
   
    if request.method == "POST":
        form = CategoryForm(request.POST,request.FILES)
        if form.is_valid():
            category = form.save(commit=False)
            category.user = request.user
            category.save()
            return redirect("core:category_list")

    else:
        data["form"] = CategoryForm() # controles formulario sin datos

    return render(request, "core/categories/form.html", data)
    
def category_update(request,id):
    data = {"title1": "Categorias","title2": ">Edicion De Categorias"}
    category = Category.objects.get(pk=id)
    if request.method == "POST":
        form = CategoryForm(request.POST,request.FILES,instance=category)
        if form.is_valid():
            form.save()
            return redirect("core:category_list")
    else:
        form = CategoryForm(instance=category)
        data["form"]=form
    return render(request,"core/categories/form.html", data)

def category_delete(request,id):
    category = Category.objects.get(pk=id)
    data = {"title1": "Eliminar","title2":"Eliminar una categoria","category":category}
    if request.method == "POST":
        category.delete()
        return redirect("core:category_list")
    
    return render(request,"core/categories/delete.html", data)