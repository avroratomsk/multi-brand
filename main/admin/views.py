import math
import os
import zipfile
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib import messages
from admin.forms import BlogSettingsForm, CategoryForm, CharGroupForm, CharNameForm, ColorProductForm, GalleryCategoryForm, GalleryCategorySettingsForm, GalleryForm, GlobalSettingsForm, HomeTemplateForm, PostForm, ProductCharForm, ProductForm, ProductImageForm, ReviewsForm, RobotsForm, ServiceForm, ServicePageForm, ShopSettingsForm, StockForm, SubdomainForm, UploadFileForm
from home.models import BaseSettings, Gallery, GalleryCategory, HomeTemplate, RobotsTxt, Stock
from blog.models import BlogSettings, Post
from main.settings import BASE_DIR
from subdomain.models import Subdomain
from service.models import Service, ServicePage
from reviews.models import Reviews
from shop.models import CharGroup, CharName, ColorProduct, Product,Category, ProductChar, ProductImage, ShopSettings
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, get_list_or_404
import openpyxl
import pandas as pd
from django.core.files.images import ImageFile
from django.contrib.auth.decorators import user_passes_test

# @user_passes_test(lambda u: u.is_superuser)
# def sidebar_show(request): 
   
#     request.session['sidebar'] = 'True' 
    
#     return redirect('admin')

# @user_passes_test(lambda u: u.is_superuser)

@user_passes_test(lambda u: u.is_superuser)
def admin(request):
  """Данная предстовление отобразает главную страницу админ панели"""
  return render(request, "page/index.html")

def admin_settings(request):
  try:
    settings = BaseSettings.objects.get()
  except:
    settings = BaseSettings()
    settings.save()
  
  if request.method == "POST":
    form_new = GlobalSettingsForm(request.POST, request.FILES, instance=settings)
    if form_new.is_valid():
      form_new.save()
      
      # subprocess.call(["touch", RESET_FILE])
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, "settings/general_settings.html", {"form": form_new})

  settings = BaseSettings.objects.get()

  form = GlobalSettingsForm(instance=settings)
  context = {
    "form": form,
    "settings":settings
  }  

  return render(request, "settings/general_settings.html", context)

def robots(request):
  try:
    robots = RobotsTxt.objects.get()
  except:
    robots = RobotsTxt()
    robots.save()
  
  if request.method == "POST":
    form_new = RobotsForm(request.POST, request.FILES, instance=robots)
    if form_new.is_valid():
      form_new.save()
      
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, "settings/robots.html", {"form": form_new})

  robots = RobotsTxt.objects.get()

  form = RobotsForm(instance=robots)
  
  context = {
    "form": form,
    "robots":robots
  }  

  return render(request, "settings/robots.html", context)

def admin_home_page(request):
  try:
    settings = HomeTemplate.objects.get()
  except:
    settings = HomeTemplate()
    settings.save()
  
  if request.method == "POST":
    form_new = HomeTemplateForm(request.POST, request.FILES, instance=settings)
    if form_new.is_valid():
      form_new.save()
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, "static/home_page.html", {"form": form_new})

  # settings = HomeTemplate.objects.get()

  form = HomeTemplateForm(instance=settings)
  context = {
    "form": form,
    "settings":settings
  }  

  return render(request, "static/home_page.html", context)

@user_passes_test(lambda u: u.is_superuser)
def admin_shop(request):
  try:
    shop_setup = ShopSettings.objects.get()
    form = ShopSettingsForm(instance=shop_setup)
  except:
    form = ShopSettingsForm()
    
  if request.method == "POST":
    try:
      shop_setup = ShopSettings.objects.get()
    except ShopSettings.DoesNotExist:
      shop_setup = None
    form_new = ShopSettingsForm(request.POST, request.FILES, instance=shop_setup)
    
    if form_new.is_valid:
      form_new.save()
      
      return redirect('admin_shop')
    else:
      return render(request, "shop/settings.html", {"form": form})
  
  context = {
    "form": form,
  }  
  return render(request, "shop/settings.html", context)

def blog_settings(request):
  try:
    setup = BlogSettings.objects.get()
    form = BlogSettingsForm(instance=setup)
  except:
    form = BlogSettingsForm()
    
  if request.method == "POST":
    try:
      setup = BlogSettings.objects.get()
    except BlogSettings.DoesNotExist:
      setup = None
    form_new = BlogSettingsForm(request.POST, request.FILES, instance=setup)
    
    if form_new.is_valid:
      form_new.save()
      
      return redirect('.')
    else:
      return render(request, "blog/blog_settings.html", {"form": form})
  
  context = {
    "form": form,
  }  
  return render(request, "blog/blog_settings.html", context)

def gallery_settings(request):
  try:
    setup = GalleryCategory.objects.get()
    form = GalleryCategorySettingsForm(instance=setup)
  except:
    form = GalleryCategorySettingsForm()
    
  if request.method == "POST":
    try:
      setup = GalleryCategory.objects.get()
    except GalleryCategory.DoesNotExist:
      setup = None
    form_new = GalleryCategorySettingsForm(request.POST, request.FILES, instance=setup)
    
    if form_new.is_valid:
      form_new.save()
      
      return redirect('.')
    else:
      return render(request, "gallery/gallery_settings.html", {"form": form})
  
  context = {
    "form": form,
  }  
  return render(request, "gallery/gallery_settings.html", context)

def admin_product(request):
  """
  View, которая возвращаяет и отрисовывает все товары на странице
  и разбивает их на пагинацию 
  """
  page = request.GET.get('page', 1)
  
  products = Product.objects.all()
  paginator = Paginator(products, 10)
  current_page = paginator.page(int(page))
  
  context = {
    "items": current_page
  }
  return render(request, "shop/product/product.html", context)

def product_edit(request, pk):
  """
    View, которая получает данные из формы редактирования товара
    и изменяет данные внесенные данные товара в базе данных
  """
  product = Product.objects.get(id=pk)
  form = ProductForm(instance=product)
  image_form = ProductImageForm()
  product_char_form = ProductCharForm()
  chars = ProductChar.objects.filter(parent_id=pk)
  all_chars = CharName.objects.all()
  
  form_new = ProductForm(request.POST, request.FILES, instance=product) 
  if request.method == 'POST':
    if form_new.is_valid():
      form_new.save()
      product = Product.objects.get(slug=request.POST['slug'])
      images = request.FILES.getlist('src')
      # Характеристики 
      char_name = request.POST.getlist('text_name')
      char_value = request.POST.getlist('char_value')
      char_count = 0

      for char in char_name:

          value = char_value[char_count]
          product_char = ProductChar(
              char_name_id = char,
              parent = product,
              char_value = value
          )
          product_char.save()
          char_count += 1

      old_char_id = request.POST.getlist('old_char_id')
      old_char_name = request.POST.getlist('old_text_name')
      old_char_value = request.POST.getlist('old_char_value')
      old_char_count = 0

      for id in old_char_id:

          old_char = ProductChar.objects.get(id=id)
          old_char.char_name_id = old_char_name[old_char_count]
          old_char.char_value = old_char_value[old_char_count]
          
          old_char.save()
          old_char_count += 1
      for image in images:
          img = ProductImage(parent=product, src=image)
          img.save()
      return redirect(request.META.get('HTTP_REFERER'))
    else:
      return render(request, 'shop/product/product_edit.html', {'form': form_new})
  context = {
    "form":form,
    'image_form': image_form,
    "product_char_form": product_char_form,
    "all_chars": all_chars,
    "chars": chars,
  }
  return render(request, "shop/product/product_edit.html", context)

def product_add(request):
  form = ProductForm()
  
  if request.method == "POST":
    form_new = ProductForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_product')
    else:
      return render(request, "shop/product/product_add.html", {"form": form_new})
    
  context = {
    "form": form
  }
  
  return render(request, 'shop/product/product_add.html', context)

def product_delete(request,pk):
  product = Product.objects.get(id=pk)
  product.delete()
  
  return redirect('admin_product')

def admin_attribute(request):
  chars = ProductSpecification.objects.all()
  
  context = {
    "title": "Характеристики товара",
    "chars": chars,
  }
  
  return render(request, "shop/char/char.html", context)

def attribute_add(request):
  pass
  # if request.method == "POST":
  #   form_new = ProductCharForm(request.POST)
  #   if form_new.is_valid():
  #     form_new.save()
  #     return redirect('admin_attribute')
  #   else:
  #     return render(request, 'shop/char/char_add.html', {'form': form})
  
  # form = ProductCharForm()
  # context = {
  #   "title": "Добавление характиристик",
  #   "form": form
  # }
  # return render(request, "shop/char/char_add.html", context)


folder = 'upload/'

from PIL import Image

def upload_goods(request):
    form = UploadFileForm()
    if request.method == 'POST':
      form = UploadFileForm(request.POST, request.FILES)
      if form.is_valid():
          file = request.FILES['file']
          
          destination = open(os.path.join('upload/', file.name), 'wb+')
          for chunk in file.chunks():
              destination.write(chunk)
          destination.close()
              
          # Распаковка архива
          with zipfile.ZipFile('upload/upload.zip', 'r') as zip_ref:
              zip_ref.extractall('media/')
              
          # Удаление загруженного архива
          os.remove('upload/upload.zip')
          
          # Сжатие фотографий
          for filename in os.listdir('media/upload'):
            
            if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.JPG') or filename.endswith('.JPEG') or filename.endswith('.jpeg'):
              with Image.open(os.path.join('media/upload', filename)) as img:
                temp = filename.replace('.jpeg', '')
                temp_one = temp.replace('№', '')
                temp_b = temp_one.replace('В', 'B')
                temp_e = temp_one.replace('Э', 'E')
                img.save(os.path.join('media/goods', temp_e), quality=60)  # quality=60 для JPEG файла
                
          # Очистка временной папки
          os.system('rm -rf media/upload')
          return redirect('upload-succes')
      else:
        form = UploadFileForm()
    return render(request, 'upload/upload.html', {'form': form})

def upload_succes(request):
  return render(request, "upload/upload-succes.html")


path = f"{BASE_DIR}/upload/upload.xlsx"

from pytils.translit import slugify
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

def parse_exсel(path):
  workbook = openpyxl.load_workbook(path)
  sheet = workbook.active
  start_row = 2
    
  Product.objects.all().delete()
  CharName.objects.all().delete()
  
  for row in sheet.iter_rows(min_row=start_row, values_only=True):
    model = row[0]
    slug = slugify(model)
    article = row[1]
    name = row[2]
    if row[3]:
      category_name = row[3]
    else:
      pass
    category_slug = slugify(category_name)
    try:
      category = Category.objects.get(slug=category_slug)
    except ObjectDoesNotExist:
      if not Category.objects.filter(name=category_name).exists():
        category = Category.objects.create(
          name=category_name,
          slug=category_slug
        )
      else:
        category = Category.objects.filter(name=category_name).first()
    price = row[4]
    polished_sides = row[9]
    quantity = 1
    description = row[11]
    delivery = row[12]
    meta_h1 = ''
    meta_title = ''
    meta_description = ''
    meta_keywords = ''
    try:
      name_image = row[13].replace("№","")
      # print(name_image)
      name_two = name_image.replace('Э', 'E')
      print(name_two)
      image = f"goods/{name_two}"
    except:
      pass
    
    # weight = row[18]
    status = True
    
    try:
      image_list = row[14].split(',')
    except: 
      pass
    
    
    # sale_price = 0.0
    
    # if row[6] == None:
    #   discount = 0
    # else:
    #   discount = int(row[6])
    #   sale_price = round(price - price * discount / 100, 1)
    
    # status = True
  # Получаем строку с материалом и делим по запятой
    chars = row[5].split(',')
    char_name = sheet['F1'].value
    char_eng = slugify(char_name)
    
    try:
      char = CharName.objects.get(filter_name=char_eng)
    except ObjectDoesNotExist:
      if not CharName.objects.filter(filter_name=char_eng).exists():
        char = CharName.objects.create(
          text_name=char_name,
          filter_add = True,
          filter_name=char_eng,
          sort_order=0
        )
      else:
        char = CharName.objects.filter(filter_name=char_eng).first()
    
    chars_color = row[6].split(',')
    char_color_name = sheet['G1'].value
    char_color_eng = slugify(char_color_name)
       
    try:
      char_color = CharName.objects.get(filter_name=char_color_eng)
    except ObjectDoesNotExist:
      if not CharName.objects.filter(filter_name=char_color_eng).exists():
        char_color = CharName.objects.create(
          text_name=char_color_name,
          filter_add = True,
          filter_name=char_color_eng,
          sort_order=0
        )
      else:
        char_color = CharName.objects.filter(filter_name=char_color_eng).first()
        
    chars_size = row[8].split(',')
    char_size_name = sheet['I1'].value
    char_size_eng = slugify(char_size_name)
    
    try:
      char_size = CharName.objects.get(filter_name=char_size_eng)
    except ObjectDoesNotExist:
      if not CharName.objects.filter(filter_name=char_size_eng).exists():
        char_size = CharName.objects.create(
          text_name=char_size_name,
          filter_add = True,
          filter_name=char_size_eng,
          sort_order=0
        )
      else:
        char_size = CharName.objects.filter(filter_name=char_size_eng).first()
  
    try:
      new_product = Product.objects.get(slug=slug)
    except ObjectDoesNotExist:
      if not Product.objects.filter(name=model).exists():
        try:
            new_product = Product.objects.create(
            model=model,
            article=article,
            polished_sides=polished_sides,
            delivery=delivery,
            name=name,
            slug=slug,
            # weight=weight,
            description=description,
            meta_h1=meta_h1,
            meta_title=meta_title,
            meta_description=meta_description,
            meta_keywords=meta_keywords,
            image=image,
            price=price,
            quantity=quantity,
            category=category,
            status=status
          )
        except Exception as e:
          print(e)
          
      else:
        new_product = Product.objects.filter(name=model).first() 
      
      for ch in chars:
        try:
          product_char_create = ProductChar.objects.create(
            char_name = char,
            parent = new_product,
            char_value = ch
          )
        except Exception as e:
          print(e)
      
      for ch in chars_color:
        try:
          product_char_color_create = ProductChar.objects.create(
            char_name = char_color,
            parent = new_product,
            char_value = ch
          )
        except Exception as e:
          print(e)
          
      for ch in chars_size:
        try:
          product_char_size_create = ProductChar.objects.create(
            char_name = char_size,
            parent = new_product,
            char_value = ch
          )
        except Exception as e:
          print(e)
        
      for image in image_list:
        try:
          image_file = open('media/goods/' + image, 'rb')
          image_image = ImageFile(image_file)
          image_create = ProductImage.objects.create(
              parent=new_product,
              src=image_image
          )
        except Exception as e: 
          pass
        
# parse_exсel(path)

def admin_category(request):
  categorys = Category.objects.all()
  
  context ={
    "categorys": categorys,
  }
  return render(request, "shop/category/category.html", context)

def category_add(request):
  form = CategoryForm()
  if request.method == "POST":
    form_new = CategoryForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_category")
    else:
      return render(request, "shop/category/category_add.html", {"form": form_new})
    
  context = {
    "form": form
  }
  return render(request, "shop/category/category_add.html", context)

def category_edit(request, pk):
  categorys = Category.objects.get(id=pk)
  form = CategoryForm(request.POST, request.FILES, instance=categorys)
  
  if request.method == "POST":
    
    if form.is_valid():
      form.save()
      return redirect("admin_category")
    else:
      return render(request, "shop/category/category_edit.html", {"form": form, 'image_path': image_path})
  
  context = {
    "form": CategoryForm(instance=categorys),
    "categorys": categorys
  }

  return render(request, "shop/category/category_edit.html", context)

def category_delete(request, pk):
  category = Category.objects.get(id=pk)
  category.delete()
  
  return redirect('admin_category')

def day_product(request):
  # pass
  # days = Day.objects.all().exclude(slug="ezhednevno")
  
  # context = {
  #   "days": days,
  # }
  
  return render(request, "days/days.html")

def day_edit(request, pk):
  pass
  # day = Day.objects.get(id=pk)
  # form = DayForm(instance=day)
  
  # form_new = DayForm(request.POST, instance=day)
  # if request.method == "POST":
  #   if form_new.is_valid():
  #     form_new.save()
  #     return redirect("admin_day")
  #   else:
  #     return render(request, "days/days_edit.html", {"form": form_new})

  # context = {
  #   "form": form,
  # }
  
  # return render(request, "days/days_edit.html", context)

def day_add(request):
  pass
  # form = DayForm()
  # if request.method == "POST":
  #   form_new = DayForm(request.POST)
  #   if form_new.is_valid():
  #     form_new.save()
  #     return redirect("admin_day")
  #   else:
  #     return render(request, "days/days_add.html", {"form": form_new})
  # context = {
  #   "form": form
  # }
  
  # return render(request, "days/days_add.html", context)

def admin_fillial(request):
  pass
  # fillials = Subsidiary.objects.all()
  
  # context = {
  #   "fillials": fillials
  # }
  
  # return render(request, "fillials/fillial.html", context)

def fillial_edit(request, pk):
  pass
  # fillial = Subsidiary.objects.get(id=pk)
  # form = FillialForm(instance=fillial)
  
  # if request.method == "POST":
  #   form_new = FillialForm(request.POST, request.FILES, instance=fillial)
  #   if form_new.is_valid():
  #     form_new.save()
  #     return redirect("admin_fillial")
  #   else:
  #     return render(request, "fillials/fillial_edit.html", {"form": form_new})
  
  # context = {
  #   "form": form,
  # }
  
  # return render(request, "fillials/fillial_edit.html", context)

def fillial_add(request):
  pass
  # form = FillialForm()
  # if request.method == "POST":
  #   form_new = FillialForm(request.POST, request.FILES)
  #   if form_new.is_valid():
  #     form_new.save()
  #     return redirect("admin_fillial")
  #   else:
  #     return render(request, "fillials/fillial_add.html", {"form": form_new})
    
  # context = {
  #   "form": form
  # }
  
  return render(request, "fillials/fillial_add.html", context)

def admin_home(request):
  try:
    home_page = HomeTemplate.objects.get()
  except:
    home_page = HomeTemplate()
    home_page.save()
    
  if request.method == "POST":
    form_new = HomeTemplateForm(request.POST, request.FILES, instance=home_page)
    if form_new.is_valid():
      form_new.save()
      
      # subprocess.call(["touch", RESET_FILE])
      return redirect("admin")
    else:
      return render(request, "static/home_page.html", {"form": form_new})
  
  home_page = HomeTemplate.objects.get()
  
  form = HomeTemplateForm(instance=home_page)
  context = {
    "form": form,
    "home_page":home_page
  }  
  
  return render(request, "static/home_page.html", context)

def admin_service_page(request):
  try:
    service_page = ServicePage.objects.get()
  except:
    service_page = ServicePage()
    service_page.save()
    
  if request.method == "POST":
    form_new = ServicePage(request.POST, request.FILES, instance=service_page)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin")
    else:
      return render(request, "serv/serv_settings.html", {"form": form_new})
  
  service_page = HomeTemplate.objects.get()
  
  form = HomeTemplateForm(instance=service_page)
  context = {
    "form": form,
    "service_page":service_page
  }  
  
  return render(request, "static/home_page.html", context)

def admin_reviews(request):
  reviews = Reviews.objects.all()
  
  context = {
    "items": reviews
  }
  
  return render(request, "reviews/reviews.html", context)

def admin_reviews_edit(request, pk):
  review = Reviews.objects.get(id=pk)
  form = ReviewsForm(instance=review)
  
  if request.method == "POST":
    form_new = ReviewsForm(request.POST, request.FILES, instance=review)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_reviews")
    else:
      return render(request, "reviews/reviews_edit.html", {"form": form_new})
  
  context = {
    "review":review,
    "form": form
  }
  
  return render(request, "reviews/reviews_edit.html", context)

def admin_reviews_add(request):
  form = ReviewsForm()
  if request.method == "POST":
    form_new = ReviewsForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_reviews")
    else:
      return render(request, "reviews/reviews_add.html", {"form": form_new})
    
  context = {
    "form": form
  }
  
  return render(request, "reviews/reviews_add.html", context)

def admin_reviews_delete(request, pk):
  pass

def admin_stock(request):
  stocks = Stock.objects.all()
  
  context = {
    "stocks": stocks
  }
  
  return render(request, "stock/stock.html", context)

def stock_add(request):
  form = StockForm()
  
  if request.method == "POST":
    form_new = StockForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_stock")
    else: 
      return render(request, "stock/stock_add.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "stock/stock_add.html", context)

def stock_edit(request, pk):
  stock = Stock.objects.get(id=pk)
  form = StockForm(instance=stock)
  if request.method == "POST":
    form_new = StockForm(request.POST, request.FILES, instance=stock)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_stock")
    else:
      return render(request, "stock/stock_edit.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "stock/stock_edit.html", context)

def stock_delete(request, pk):
  stock = Stock.objects.get(id=pk)
  stock.delete()
  return redirect("admin_stock")

def admin_service(request):
  services = Service.objects.all()
  
  context = {
    "services": services
  }
  
  return render(request, "serv/admin_serv.html", context)

def service_add(request):
  form = ServiceForm()
  
  if request.method == "POST":
    form_new = ServiceForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_service")
    else: 
      return render(request, "serv/serv_add.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "serv/serv_add.html", context)

def service_edit(request, pk):
  services = Service.objects.get(id=pk)
  form = ServiceForm(instance=services)
  if request.method == "POST":
    form_new = ServiceForm(request.POST, request.FILES, instance=services)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_service")
    else:
      return render(request, "serv/stock_edit.html", {"form": form_new})
  
  context = {
    "form": form
  }
  
  return render(request, "serv/serv_edit.html", context)

def service_delete(request, pk):
  service = Service.objects.get(id=pk)
  service.delete()
  return redirect("admin_service")

def admin_char(request):
  chars = CharName.objects.filter(group=None)
  groups = CharGroup.objects.all()
  
  context = {
        "groups": groups,
        "chars": chars
    }
  return render(request, "shop/char/char.html", context)

def char_add(request):
  if request.method == 'POST':
        form_new = CharNameForm(request.POST)
        if form_new.is_valid():
            form_new.save()
            return redirect('admin_char')
        else:
            return render(request, 'shop/char/char_add.html', {'form': form})

  form = CharNameForm()
  context = {
      'form': form,
  }
  return render(request, 'shop/char/char_add.html', context)

def char_edit(request, pk):
  char = CharName.objects.get(id=pk)
  
  if request.method == 'POST':
      form_new = CharNameForm(request.POST, instance=char)
      if form_new.is_valid():
          form_new.save()
          return redirect('admin_char')
      else:
          return render(request, 'shop/char/char_edit.html', {'form': form})

  form = CharNameForm(instance=char)
  context = {
      'form': form,
  }
  return render(request, 'shop/char/char_edit.html', context)

def char_delete(request, pk):
  char = CharName.objects.get(id=pk)
  char.delete()
  return redirect('admin_char')

def char_group_add(request):
  if request.method == 'POST':
      form_new = CharGroupForm(request.POST)
      if form_new.is_valid():
          form_new.save()
          return redirect('admin_char')
      else:
          return render(request, 'shop/char/char_group_add.html', {'form': form})

  form = CharGroupForm()
  context = {
      'form': form,
  }
  return render(request, 'shop/char/char_group_add.html', context)

def char_group_edit(request, pk):
  char_group = CharGroup.objects.get(id=pk)
  if request.method == "POST":
    form_new = CharGroupForm(request.POST, instance=char_group)
    if form_new.is_valid():
      form_new.save()
      return redirect("admin_char")
    else:
      return render(request, "shop/char/char_group_edit.html", {"form": form})
  form = CharGroupForm(instance=char_group)
  
  context = {
    "form": form,
  }
  
  return render(request, "shop/char/char_group_edit.html", context)


def char_group_delete(request, pk):
  char_group = CharGroup.objects.get(id=pk)
  char_group.delete()
  return redirect('admin_char')


def admin_subdomain(request):
  subdomains = Subdomain.objects.all()
  
  context = {
    "subdomains": subdomains,  
  }
  
  return render(request, "subdomain/subdomain.html", context)


def subdomain_add(request):
  form = SubdomainForm()
  
  if request.method == "POST":
    form_new = SubdomainForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_subdomain')
    else:
      return render(request, "subdomain/subdomain_add.html", { "form": form_new })
    
  context = {
    "form": form, 
  }  
    
  return render(request, "subdomain/subdomain_add.html", context)

def subdomain_edit(request, pk):
  subdomain = Subdomain.objects.get(id=pk)
  
  if request.method == "POST":
    form_new = SubdomainForm(request.POST, request.FILES, instance=subdomain)
    
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_subdomain')
    else:
      return render(request, "subdomain/subdomain_edit.html", { "form": form_new })
  
  form = SubdomainForm(instance=subdomain)
  context = {
    "form": form,
  }  
    
  return render(request, "subdomain/subdomain_edit.html", context)

def subdomain_delete(request, pk):
  subdomain = Subdomain.objects.get(id=pk)
  subdomain.delete()
  return redirect(request.META.get('HTTP_REFERER'))


def admin_color(request):
  items = ColorProduct.objects.all()
  
  context = {
    "items": items,  
  }
  
  return render(request, "shop/color/color.html", context)


def admin_color_add(request):
  form = ColorProductForm()
  
  if request.method == "POST":
    form_new = ColorProductForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_color')
    else:
      return render(request, "shop/color/color_add.html", { "form": form_new })
    
  context = {
    "form": form, 
  }  
    
  return render(request, "shop/color/color_add.html", context)

def admin_color_edit(request, pk):
  item = ColorProduct.objects.get(id=pk)
  
  if request.method == "POST":
    form_new = ColorProductForm(request.POST, request.FILES, instance=item)
    
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_color')
    else:
      return render(request, "shop/color/color_edit.html", { "form": form_new })
  
  form = ColorProductForm(instance=item)
  context = {
    "form": form,
  }  
    
  return render(request, "shop/color/color_edit.html", context)

def admin_color_delete(request, pk):
  subdomain = Subdomain.objects.get(id=pk)
  subdomain.delete()
  return redirect(request.META.get('HTTP_REFERER'))

def admin_gallery(request):
  items = Gallery.objects.all()
  
  context = {
    "items": items,  
  }
  
  return render(request, "gallery/gallery.html", context)


def admin_gallery_add(request):
  form = GalleryForm()
  
  if request.method == "POST":
    form_new = GalleryForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_gallery')
    else:
      return render(request, "gallery/gallery_add.html", { "form": form_new })
    
  context = {
    "form": form, 
  }  
    
  return render(request, "gallery/gallery_add.html", context)

def admin_gallery_edit(request, pk):
  item = Gallery.objects.get(id=pk)
  
  if request.method == "POST":
    form_new = GalleryForm(request.POST, request.FILES, instance=item)
    
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_gallery')
    else:
      return render(request, "gallery/gallery_edit.html", { "form": form_new })
  
  form = GalleryForm(instance=item)
  context = {
    "form": form,
  }  
    
  return render(request, "gallery/gallery_edit.html", context)

def admin_color_delete(request, pk):
  subdomain = Subdomain.objects.get(id=pk)
  subdomain.delete()
  return redirect(request.META.get('HTTP_REFERER'))


def admin_gallery_category(request):
  items = GalleryCategory.objects.all()
  
  context = {
    "items": items,
  }
  
  return render(request, "gallery/gallery_category.html", context)


def gallery_category_add(request):
  form = GalleryCategoryForm()
  
  if request.method == "POST":
    form_new = GalleryCategoryForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_gallery_category')
    else:
      return render(request, "gallery/gallery_category_add.html", { "form": form_new })
    
  context = {
    "form": form, 
  }  
    
  return render(request, "gallery/gallery_category_add.html", context)

def gallery_category_edit(request, pk):
  item = GalleryCategory.objects.get(id=pk)
  
  if request.method == "POST":
    form_new = GalleryCategoryForm(request.POST, request.FILES, instance=item)
    
    if form_new.is_valid():
      form_new.save()
      return redirect('admin_gallery')
    else:
      return render(request, "gallery/gallery_category_edit.html", { "form": form_new })
  
  form = GalleryCategoryForm(instance=item)
  context = {
    "form": form,
  }  
    
  return render(request, "gallery/gallery_category_edit.html", context)

def gallery_category_delete(request):
  pass



def article(request):
  items = Post.objects.all()
  
  context ={
    "items": items,
  }
  return render(request, "blog/blog_post/blog_post.html", context)

def article_add(request):
  form = PostForm()
  if request.method == "POST":
    form_new = PostForm(request.POST, request.FILES)
    if form_new.is_valid():
      form_new.save()
      return redirect("article")
    else:
      return render(request, "blog/blog_post/post_add.html", {"form": form_new})
    
  context = {
    "form": form
  }
  
  return render(request, "blog/blog_post/post_add.html", context)

def article_edit(request, pk):
  item = Post.objects.get(id=pk)
  form = PostForm(request.POST, request.FILES, instance=item)
  
  if request.method == "POST":
    
    if form.is_valid():
      form.save()
      return redirect("article")
    else:
      return render(request, "blog/blog_post/post_edit.html", {"form": form, 'image_path': image_path})
  
  context = {
    "form": PostForm(instance=item),
    "item": item
  }

  return render(request, "blog/blog_post/post_edit.html", context)

def article_delete(request, pk):
  category = Category.objects.get(id=pk)
  category.delete()
  
  return redirect('admin_category')
