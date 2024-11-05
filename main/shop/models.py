from django.db import models
from django.urls import reverse
import os
from django.conf import settings
from admin.singleton_model import SingletonModel

class ShopSettings(SingletonModel):
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="META заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="META описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="META keywords")
  download_catalog = models.FileField(upload_to='shop-catalog/', blank=True, null=True, verbose_name="PDF каталог")

# Категория
class Category(models.Model):
  name = models.CharField(max_length=150, db_index=True, unique=True, verbose_name="Название категории")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
  description = models.TextField(null=True, blank=True,  verbose_name="Описание категории")
  image = models.ImageField(upload_to="category_image", blank=True, null=True, verbose_name="Изображение категории")
  parent = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Дочерняя категория")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="META заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="META описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="META keywords")
  add_menu = models.BooleanField(default=False, blank=True, null=True, verbose_name="Выводить в меню ? ")
  updated_at = models.DateTimeField(auto_now=True)  # Поле для даты последнего обновления
  related_categories = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related_to')
  
  class Meta:
    db_table = 'category' 
    verbose_name = 'Категория'
    verbose_name_plural = "Категории"
    
  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
        return reverse("category_detail", kwargs={"slug": self.slug})

# Продукт 
class Product(models.Model):
  model = models.CharField(max_length=255, blank=True, null=True, verbose_name="Модель")
  article = models.CharField(max_length=255, blank=True, null=True, verbose_name="Артикл")
  name = models.CharField(max_length=150, db_index=True, verbose_name="Наименование")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
  category = models.ForeignKey("Category", on_delete=models.CASCADE, null=True, default=None, verbose_name='День недели')
  price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена со скидкой")
  sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Цена со скидкой")
  polished_sides = models.CharField(max_length=50, blank=True, null=True, verbose_name="Количество полированных сторон")
  description = models.TextField(blank=True, null=True, verbose_name="Описание")
  delivery = models.TextField(blank=True, null=True, verbose_name="Описание доставки")
  image = models.ImageField(upload_to="product_iamge", blank=True, null=True, verbose_name="Изображение товара")
  discount = models.DecimalField(default=0, max_digits=10, decimal_places=2, verbose_name="Скидака в %")
  quantity = models.PositiveIntegerField(default=0, verbose_name="Количество")
  weight = models.CharField(max_length=100, blank=True, null=True, verbose_name="Вес")
  quantity_purchase = models.IntegerField(default=0, verbose_name="Количество купленных")
  latest = models.BooleanField(default=False, verbose_name="Новинка ?")
  status = models.BooleanField(default=True, verbose_name="Опубликовать ?")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  updated_at = models.DateTimeField(auto_now=True)  # Поле для даты последнего обновления
  type_image = models.BooleanField(default=False, verbose_name="Вид отображение картинки")
  catalog = models.BooleanField(default=True, verbose_name="Выводить в каталог")
  related_products = models.ManyToManyField('self', blank=True, symmetrical=False, related_name='related')
  

  class Meta:
    db_table = 'product' 
    verbose_name = 'Продукт'
    verbose_name_plural = "Продукты"
    ordering = ("-id",)
    
  def get_all_children_products(self):
        children = self.children.all()
        products = []
        for child in children:
            products += child.products.filter(status=True)
        return products
      
  def get_image_url(self):
    if self.image and os.path.isfile(os.path.join(settings.MEDIA_ROOT, self.image.name)):
      return self.image.url
    return '/core/theme/mb/images/no-image.png'  # Замените на реальный путь к заглушке
  
    
  def __str__(self):
    return f'{self.name}'
    
  """ Данный метод добавляет к id нули в начале """
  def display_id(self):
    return f'{self.id:05}' #self.id:05 - сделает так чтобы id состоял из 5 символов, если не хватате символов в начало добавить 0
  
  """ Данный метод возвращает цену со скидкой"""
  def sell_price(self):
    if self.discount:
      return round(self.price - self.price * self.discount / 100, 2)
    
    return self.price
  
  def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})

  def get_related_products(self):
    related_categories = self.category.related_categories.all()
    related_products = Product.objects.filter(category__in=related_categories).exclude(id=self.id)[:5]
    return related_products

class ProductImage(models.Model):
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images", verbose_name="Привязка к продукту")
    src = models.ImageField(upload_to="product_iamge", null=True, blank=True, verbose_name="Дополнительны изображения")
    class Meta:
      verbose_name = 'Изображение'


class CharGroup(models.Model):
  name = models.CharField(max_length=250, verbose_name="Название группы", null=True, blank=True)
  
  def __str__(self):
    return self.name


class CharName(models.Model):
    group = models.ForeignKey(CharGroup, on_delete=models.SET_NULL, related_name='g_chars', null=True, blank=True)
    text_name = models.CharField(max_length=250, null=True, blank=True, verbose_name="Название характеристики")
    filter_add = models.BooleanField(default=False, verbose_name='Включить фильтрацию по характеристике', null=True, blank=True)
    filter_name = models.CharField(max_length=250, verbose_name='Название характеристики для фильтра (сокращенно на английском)', null=True, blank=True, unique=True)
    sort_order = models.PositiveIntegerField(default=0, verbose_name='Порядок сортировки', null=True, blank=True)

    def __str__(self):
        return self.text_name


class CharDefault(models.Model):
    value = models.CharField(max_length=250, verbose_name='Значение', null=True, blank=True)
    char = models.ForeignKey(CharName, on_delete=models.CASCADE, related_name='defaults', verbose_name='Характеристика', null=True, blank=True)

    def __str__(self):
        return self.value

    class Meta:
        verbose_name = 'Значение по умолчанию'
        verbose_name_plural = 'Значения по умолчанию'

class ProductChar(models.Model):
    char_name = models.ForeignKey(CharName, on_delete=models.CASCADE, related_name='c_chars', null=True, blank=True)
    parent = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='chars', null=True, blank=True)
    char_value = models.TextField()

    def __str__(self):
        return self.char_value
      
      
class ColorProduct(models.Model):
  name = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name="Название цвета")
  code_color = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name="Код цвета")
  image_color = models.ImageField(upload_to="product_color", null=True, blank=True, verbose_name="Изображение цвета")
  active = models.BooleanField(default=True, verbose_name="Выводить на сайте")
      
 
# class Char(models.Model):
#   name  = models.CharField(max_length=250, null=True, blank=True, verbose_name="Название характеристики")

# class CharValue(models.Model):
#   char_name = models.ForeignKey(Char, on_delete=models.CASCADE, related_name="char", verbose_name="Характеристика")
  
  
  