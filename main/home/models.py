from django.db import models
from django.urls import reverse

from admin.singleton_model import SingletonModel

class BaseSettings(SingletonModel):
  logo  = models.ImageField(upload_to="base-settings", blank=True, null=True, verbose_name="Логотип")
  phone = models.CharField(max_length=50, blank=True, null=True, db_index=True, verbose_name="Номер телефона")
  time_work = models.CharField(max_length=250, blank=True, null=True, db_index=True, verbose_name="Время работы")
  email = models.EmailField(max_length=250, blank=True, null=True, db_index=True, verbose_name="Email")
  address = models.CharField(max_length=250, blank=True, null=True, verbose_name="Адрес")
  whatsapp = models.CharField(max_length=250, blank=True, null=True, verbose_name="WhatsApp")
  telegram = models.CharField(max_length=250, blank=True, null=True, verbose_name="Telegram")
  vk = models.CharField(max_length=250, blank=True, null=True, verbose_name="Vk")
  map = models.TextField(blank=True, null=True, verbose_name="Vk")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  favicon = models.FileField(upload_to='base-settings/', blank=True, null=True, verbose_name="ФавИконка")
  

class HomeTemplate(SingletonModel):
  banner = models.ImageField(upload_to="home-page", blank=True, null=True, verbose_name="Картинка главной страницы")
  title_one = models.TextField(blank=True, null=True, verbose_name="Заголовок первого уровня")
  subtitle = models.CharField(max_length=250, blank=True, null=True, verbose_name="Подзаголовок")
  text_one_one = models.TextField(blank=True, null=True, verbose_name="Текст первого квадрата первого блока")
  text_one_two = models.TextField(blank=True, null=True, verbose_name="Текст второго квадрата первого блока")
  text_one_three = models.TextField(blank=True, null=True, verbose_name="Текст третьего квадрата первого блока")
  text_one_four = models.TextField(blank=True, null=True, verbose_name="Текст четвертого квадрата первого блока")
  item_one = models.TextField(blank=True, null=True, verbose_name="Список 1")
  item_two = models.TextField(blank=True, null=True, verbose_name="Список 2")
  item_three = models.TextField(blank=True, null=True, verbose_name="Список 3")
  director = models.TextField(blank=True, null=True, verbose_name="Цитата директора")
  director_image = models.ImageField(upload_to="home-page", blank=True, null=True, verbose_name="Фото директора")
  rev_one = models.TextField(blank=True, null=True, verbose_name="Отзывы 2 гис")
  rev_two = models.TextField(blank=True, null=True, verbose_name="Отзывы Яндекс")
  
  why_subtitle = models.CharField(max_length=250, blank=True, null=True, verbose_name="Как мы работаем подзаголвоок")
  why_title_card_one = models.CharField(max_length=250, blank=True, null=True, verbose_name="Заголовок 1 карточки")
  why_descr_card_one = models.CharField(max_length=250, blank=True, null=True, verbose_name="Описание 1 карточки")
  
  why_title_card_two = models.CharField(max_length=250, blank=True, null=True, verbose_name="Заголовок 2 карточки")
  why_descr_card_two = models.CharField(max_length=250, blank=True, null=True, verbose_name="Описание 2 карточки")
  
  why_title_card_three = models.CharField(max_length=250, blank=True, null=True, verbose_name="Заголовок 3 карточки")
  why_descr_card_three = models.CharField(max_length=250, blank=True, null=True, verbose_name="Описание 3 карточки")
  
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  
class Stock(models.Model):
  """Model"""
  title = models.CharField(max_length=250, blank=True, null=True, verbose_name="Название акции")
  description = models.TextField(blank=True, null=True, verbose_name="Описание акции")
  validity = models.DateTimeField(blank=True, null=True, help_text="После окончания акции, она перейдет в состояние не активна", verbose_name="Срок дейстия акции")
  status = models.BooleanField(default=True, verbose_name="Статус публикации")
  image = models.ImageField(upload_to="stock", null=True, blank=True, verbose_name="ФОтография акции")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="URL")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  slider_status = models.BooleanField(default=False, verbose_name="Слайдер на главной")

  def get_absolute_url(self):
      return reverse("stock_detail", kwargs={"slug": self.slug})
    
class GalleryCategory(models.Model):
  name = models.CharField(max_length=250, null=True, blank=True, verbose_name="Наименование")
  meta_h1 = models.CharField(max_length=350, null=True, blank=True, verbose_name="Заголовок первого уровня")
  meta_title = models.CharField(max_length=350, null=True, blank=True, verbose_name="Мета заголовок")
  meta_description = models.TextField(null=True, blank=True, verbose_name="Meta описание")
  meta_keywords = models.TextField(null=True, blank=True, verbose_name="Meta keywords")
  slug = models.SlugField(max_length=200, unique=True, blank=True, null=True, verbose_name="")
  home_view = models.BooleanField(default=False, verbose_name="Отображать на главной ?")
  image = models.ImageField(upload_to="gallery-category", null=True, blank=True, verbose_name="Фотография категории")
  
  def __str__(self):
    return self.name
  
  def get_absolute_url(self):
    return reverse("gal_cat_detail", kwargs={"slug": self.slug})
  
class Gallery(models.Model):
  category = models.ForeignKey(GalleryCategory, on_delete=models.CASCADE, null=True, default=None, related_name="categories")
  image = models.ImageField(upload_to="gallery-image", null=True, blank=True, verbose_name="Фотография")
  name = models.CharField(max_length=255, null=True, blank=True, verbose_name="Наименование пойдет в alt и title")
  cat_detail = models.BooleanField(default=False, verbose_name="Вывод в категорию")
  is_active = models.BooleanField(default=True, verbose_name="Выводить на сайт ?")
  
  
  def __str__(self):
    return self.name
  
class RobotsTxt(models.Model):
  content = models.TextField(default="User-agent: *\nDisallow: /admin/")
    
  def __str__(self):
    return "robots.txt"
