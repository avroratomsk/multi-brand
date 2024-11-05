from django import forms
from home.models import BaseSettings, Gallery, GalleryCategory, HomeTemplate, RobotsTxt, Stock
from blog.models import BlogSettings, Post
from subdomain.models import Subdomain, SubdomainContact
from service.models import Service, ServicePage
from reviews.models import Reviews
from shop.models import Category, CharGroup, CharName, ColorProduct, Product, ProductChar, ProductImage, ShopSettings

INPUT_CLASS = "form__controls"

class UploadFileForm(forms.Form):
    file = forms.FileField()

class GlobalSettingsForm(forms.ModelForm):
  """ Form, глобальные и общие настройки сайта(лого, телефон, email)"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  class Meta:
    model = BaseSettings
    fields = "__all__"
    
    widgets = {
        'phone_one': forms.TextInput(attrs={
            'class': INPUT_CLASS
        }),
        'phone': forms.TextInput(attrs={
            'class': INPUT_CLASS
        }),
        'time_work': forms.TextInput(attrs={
            'class': INPUT_CLASS
        }),
        'email': forms.EmailInput(attrs={
            'class': INPUT_CLASS
        }),
        'address': forms.TextInput(attrs={
            'class': INPUT_CLASS
        }),
        'meta_h1': forms.TextInput(attrs={
            'class': INPUT_CLASS
        }),
        'meta_title': forms.TextInput(attrs={
            'class': INPUT_CLASS
        }),
        'meta_description': forms.TextInput(attrs={
            'class': INPUT_CLASS
        }),
        'meta_keywords': forms.TextInput(attrs={
            'class': INPUT_CLASS
        })
    }
    
class RobotsForm(forms.ModelForm):
  
  class Meta:
    model = RobotsTxt
    fields = "__all__"
    
    widgets = {'content': forms.Textarea(attrs={'class': INPUT_CLASS, 'rows': 30 }),}

class ShopSettingsForm(forms.ModelForm):
  """ Form, отвечает за создание товара и редактирование товара"""
  
  class Meta:
      model = ShopSettings
      fields = "__all__"
      widgets = {
          'meta_h1': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
          'meta_title': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
          'meta_description': forms.Textarea(attrs={
              'class': 'form__controls',
              "id": "meta_description"
          }),
          'meta_keywords': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
          # 'download_catalog': forms.TextInput(attrs={
          #     'class': 'form__controls',
          # }),
      }
      
class BlogSettingsForm(forms.ModelForm):
  
  class Meta:
      model = BlogSettings
      fields = "__all__"
      widgets = {
          'meta_h1': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
          'meta_title': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
          'meta_description': forms.Textarea(attrs={
              'class': 'form__controls',
              "id": "meta_description"
          }),
          'meta_keywords': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
      }
      
class GalleryCategorySettingsForm(forms.ModelForm):
  
  class Meta:
      model = GalleryCategory
      fields = "__all__"
      widgets = {
          'meta_h1': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
          'meta_title': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
          'meta_description': forms.Textarea(attrs={
              'class': 'form__controls',
              "id": "meta_description"
          }),
          'meta_keywords': forms.TextInput(attrs={
              'class': 'form__controls',
          }),
      }
  
class ProductForm(forms.ModelForm):
    """ Form, отвечает за создание товара и редактирование товара"""
    # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Product
        fields = "__all__"
        widgets = {
            'model': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                "id":"model"
            }),
            'article': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                "id":"article"
            }),
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                "id":"name"
            }),
            'slug': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                "id": "slug"
            }),
            'category': forms.Select(attrs={
                'class': INPUT_CLASS, 
            }),
            'price': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
            'sale_price': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
            'polished_sides': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASS, 
            }),
            'delivery': forms.Textarea(attrs={
                'class': INPUT_CLASS, 
            }),
            'discount': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
            'quantity': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
            'weight': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
            'quantity_purchase': forms.NumberInput(attrs={
                'class': INPUT_CLASS,
            }),
            'meta_h1': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
            'meta_title': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
            'meta_description': forms.Textarea(attrs={
                'class': INPUT_CLASS,
                "id": "meta_description"
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
        }
        
class PostForm(forms.ModelForm):
    """ Form, отвечает за создание товара и редактирование товара"""
    # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
    
    class Meta:
        model = Post
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                "id":"name"
            }),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASS,
                
            }),
        }

# Товар и опции товара
class ProductImageForm(forms.ModelForm):
    class Meta:
        model = ProductImage

        fields = [
            'parent',
            'src'
        ]
        labels = {
            'src': 'Выбрать изображение'
        }
        widgets = {
            'parent': forms.Select(attrs={
                'class': INPUT_CLASS, 
            })
        }

# class CharName(forms.ModelForm):
#   class

# class ProductCharForm(forms.ModelForm):
#   class Meta:
#       model = ProductSpecification
#       fields = [
#           'name',
#           'value',
#       ]
#       labels = {
#           'name': 'Название характеристики',
#           'value': 'Значение',
#       }
#       widgets = {
#           'name': forms.TextInput(attrs={
#               'class': INPUT_CLASS,
#               'placeholder': 'Название характеристики',
#               'id': 'id_char_name',
              
#           }),
#           'value': forms.TextInput(attrs={
#               'class': INPUT_CLASS,
#               'placeholder': 'Значение',
#               'id': 'id_char_value'
#           }),
#       }

class CategoryForm(forms.ModelForm):
  """ Form, отвечает за создание категорий и редактирование категорий"""

  class Meta:
    model = Category
    fields = [
      "name",
      "slug",
      "add_menu",
      "description",
      "image",
      "meta_h1",
      "meta_title",
      "meta_description",
      "meta_keywords",
      "related_categories"
    ]

    labels = {
      "name": "Назване категории",
      "slug": "URL",
      "add_menu": "Добавить в меню",
      "description": "Описание категории",
      "image": "Изображение",
      "meta_h1": "Заголовок H1",
      "meta_title": "Meta заголовок",
      "meta_description": "Meta описание",
      "meta_keyword": "Meta keywords",
    }

    widgets = {
      "name": forms.TextInput(attrs={
          "class": "form__controls",
          "id":"name"
          # "placeholder": "Название  категории"
      }),
      "slug": forms.TextInput(attrs={
        "class":"form__controls",
        "id": "slug"
        # "placeholder": "Название категори"
      }),
      'add_menu': forms.CheckboxInput(attrs={
        'class': 'form__controls-checkbox',
      }),
      "description": forms.Textarea(attrs={
        "class":"form__controls",
      }),
      # 'image': forms.FileInput(attrs={
      #     'class': 'submit-file',
      #     'accept': 'image/*'
      # }),
      "meta_h1": forms.TextInput(attrs={
        "class":"form__controls",
        # "placeholder": "Заголовок H1"
      }),
      "meta_title": forms.TextInput(attrs={
        "class":"form__controls meta_field",
        "id": "meta_title"
        # "placeholder": "Meta заголовок"
      }),
      "meta_description": forms.Textarea(attrs={
        "class":"form__controls meta_field",
        # "placeholder": "Meta Описание",
        "rows": "5"
      }),
      "meta_keywords": forms.TextInput(attrs={
        "class":"form__controls",
        # "placeholder": "Meta keywords"
      }),  
    }
    
# class DayForm(forms.ModelForm):
#   """ Form, отвечает за создание дней и редактирование дней"""
#   class Meta:
#     model = Day
#     fields = [
#       "name",
#       "slug"
#     ]
#     labels = {
#       "name": "Назване категории",
#       "slug": "URL",
#     }
#     widgets = {
#       "name": forms.TextInput(attrs={
#           "class": "form__controls",
#           "id":"name"
#           # "placeholder": "Название  категории"
#       }),
#       "slug": forms.TextInput(attrs={
#         "class":"form__controls",
#         "id": "slug"
#         # "placeholder": "Название категори"
#       })
#     }
    
# class FillialForm(forms.ModelForm):
#   """ Form, отвечает за добавление филлиала и редактирование филлиала"""
#   class Meta:
#     model = Subsidiary
#     fields = [
#       "name",
#       "address_fillial",
#       "image",
#       "slug"
#     ]
#     labels = {
#       "name": "Название филлиала",
#       "address_fillial": "Адрес филлиала",
#       "image": "Фотография зала",
#       "slug": "URL",
#     }
#     widgets = {
#       "name": forms.TextInput(attrs={
#           "class": "form__controls",
#           "id":"name"
#       }),
#       "address_fillial": forms.TextInput(attrs={
#           "class": "form__controls",
#           "id":"name",
#           "placeholder": "г.Томск, ул.Ленина 111"
#       }),
#       "slug": forms.TextInput(attrs={
#         "class":"form__controls",
#         "id": "slug"
#       })
#     }
    
class HomeTemplateForm(forms.ModelForm):
  """ Form, редактирование главной страницы"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  
  class Meta:
      model = HomeTemplate
      fields = [
          'banner',
          'meta_h1',
          'meta_title',
          'meta_description',
          'meta_keywords',
      ]
      labels = {
          'banner': 'Изображение банера',
          'meta_h1':'Заголвок первого уровня',
          'meta_title':'Meta title',
          'meta_description':'Мета description',
          'meta_keywords':'Meta keywords',
      }
      widgets = {
          'name': forms.TextInput(attrs={
              'class': INPUT_CLASS
          }),
          'meta_h1': forms.TextInput(attrs={
              'class': INPUT_CLASS,
          }),
          'meta_title': forms.TextInput(attrs={
              'class': f"{INPUT_CLASS} meta_field",
          }),
          'meta_description': forms.Textarea(attrs={
              'class': f"{INPUT_CLASS} meta_field",
              'rows': 5
          }),
          'meta_keywords': forms.TextInput(attrs={
              'class': INPUT_CLASS,
          }),
      }
           
class ReviewsForm(forms.ModelForm):
  """ Form, добавление и редактирование отзыва"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  
  class Meta:
    model = Reviews
    fields = [
        'avatar',
        'name',
        'slug',
        'date',
        'text',
        'status',
        'meta_h1',
        'meta_title',
        'meta_description',
        'meta_keywords',
    ]
    labels = {
        'avatar': 'Фотография пользователя',
        'name':'ФИО пользователя',
        'slug': 'URL',
        'date':'Дата коментария',
        'text':'Текст коментария',
        'status':'Статус публикации',
        'meta_h1':'Заголвок первого уровня',
        'meta_title':'Meta title',
        'untitle': 'Надзаголовок',
        'meta_description':'Мета description',
        'meta_keywords':'Meta keywords',
    }
    widgets = {
      'name': forms.TextInput(attrs={
        'class': INPUT_CLASS,
        'id': 'name'
      }),
      'slug': forms.TextInput(attrs={
        'class':INPUT_CLASS,
        "id": "slug"
      }),
      'date': forms.DateInput(attrs={
        'class':INPUT_CLASS,
      }),
      'text': forms.Textarea(attrs={
        'class': INPUT_CLASS,
        'rows': 7,
      }),
      'status': forms.CheckboxInput(attrs={
        'class': 'form__controls-checkbox',
      }),
      'meta_h1': forms.TextInput(attrs={
        'class': INPUT_CLASS,
      }),
      'meta_title': forms.TextInput(attrs={
        'class': INPUT_CLASS,
      }),
      'meta_description': forms.Textarea(attrs={
        'class': 'form-controls',
        'rows': 5,
      }),
      'meta_keywords': forms.TextInput(attrs={
        'class': INPUT_CLASS
      })
    }
    
class StockForm(forms.ModelForm):
  """ Form, добавление и редактирование акций"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  
  class Meta:
    model = Stock
    fields = [
        'title',
        'slug',
        'description',
        'validity',
        'status',
        'slider_status',
        'image',
        'meta_title',
        'meta_description',
        'meta_keywords',
    ]
    labels = {
        'title':'Название акции',
        'slug': 'URL',
        'validity':'Срок действия акции',
        'description':'Текст коментария',
        'status':'Статус публикации',
        'slider_status':'Вывод на главный слайдер',
        'image': 'Изображение акции',
        'meta_title':'Meta title',
        'untitle': 'Надзаголовок',
        'meta_description':'Мета description',
        'meta_keywords':'Meta keywords',
    }
    widgets = {
      'title': forms.TextInput(attrs={
        'class': INPUT_CLASS,
        'id': 'name'
      }),
      'slug': forms.TextInput(attrs={
        'class':INPUT_CLASS,
        "id": "slug"
      }),
      'validity': forms.DateInput(attrs={
        'class':INPUT_CLASS,
      }),
      'description': forms.Textarea(attrs={
        'class': INPUT_CLASS,
        'rows': 5,
      }),
      'status': forms.CheckboxInput(attrs={
        'class': 'form__controls-checkbox',
      }),
      'slider_status': forms.CheckboxInput(attrs={
        'class': 'form__controls-checkbox',
      }),
      'meta_title': forms.TextInput(attrs={
        'class': INPUT_CLASS,
      }),
      'meta_description': forms.Textarea(attrs={
        'class': 'form-controls',
        'rows': 5,
      }),
      'meta_keywords': forms.TextInput(attrs={
        'class': INPUT_CLASS
      })
    }

class ServicePageForm(forms.ModelForm):
  """ Поля настроек старницы услуг"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  
  class Meta:
    model = Service
    fields = [
        'name',
        'slug',
        'meta_title',
        'meta_description',
        'meta_keywords',
    ]
    labels = {
        'name':'Название',
        'slug': 'URL',
        'meta_title':'Meta title',
        'meta_description':'Мета description',
        'meta_keywords':'Meta keywords',
    }
    widgets = {
      'name': forms.TextInput(attrs={
        'class': INPUT_CLASS,
        'id': 'name'
      }),
      'slug': forms.TextInput(attrs={
        'class':INPUT_CLASS,
        "id": "slug"
      }),
      'meta_title': forms.TextInput(attrs={
        'class': INPUT_CLASS,
      }),
      'meta_description': forms.Textarea(attrs={
        'class': 'form-controls',
      }),
      'meta_keywords': forms.TextInput(attrs={
        'class': INPUT_CLASS
      })
    }  
    
class ServiceForm(forms.ModelForm):
  """ Form, добавление и редактирование услуг"""
  # description = forms.CharField(label='Полное описание товара', required=False, widget=CKEditorUploadingWidget())
  
  class Meta:
    model = Service
    fields = [
        'name',
        'slug',
        'subtitle',
        'status',
        'image',
        'meta_title',
        'meta_description',
        'meta_keywords',
    ]
    labels = {
        'name':'Название',
        'slug': 'URL',
        'subtitle':'Текст под заголовком',
        'status':'Статус публикации',
        'image': 'Изображение акции',
        'meta_title':'Meta title',
        'untitle': 'Надзаголовок',
        'meta_description':'Мета description',
        'meta_keywords':'Meta keywords',
    }
    widgets = {
      'name': forms.TextInput(attrs={
        'class': INPUT_CLASS,
        'id': 'name'
      }),
      'slug': forms.TextInput(attrs={
        'class':INPUT_CLASS,
        "id": "slug"
      }),
      'subtitle': forms.Textarea(attrs={
        'class':INPUT_CLASS,
      }),
      'status': forms.CheckboxInput(attrs={
        'class': 'form__controls-checkbox',
      }),
      'meta_title': forms.TextInput(attrs={
        'class': INPUT_CLASS,
      }),
      'meta_description': forms.Textarea(attrs={
        'class': 'form-controls',
        'rows': 5,
      }),
      'meta_keywords': forms.TextInput(attrs={
        'class': INPUT_CLASS
      })
    }
    
class ProductCharForm(forms.ModelForm):
    class Meta:
        model = ProductChar
        fields = [
            'char_name',
            'char_value',
        ]
        labels = {
            'char_name': 'Название характеристики',
            'char_value': 'Значение',
        }
        widgets = {
            'char_name': forms.Select(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Название характеристики',
                'id': 'id_char_name',
               
            }),
            'char_value': forms.TextInput(attrs={
                'class': 'input',
                'placeholder': 'Значение',
                'id': 'id_char_value'
            }),
        }

class CharGroupForm(forms.ModelForm):
    class Meta:
        model = CharGroup
        fields = [
            'name',
        ]
        labels = {
            'name': 'Название группы характеристик',
           
        }
        widgets = {
            'name': forms.TextInput(attrs={
                'class': INPUT_CLASS,
            }),
        }


class CharNameForm(forms.ModelForm):
  class Meta:
    model = CharName
    fields = [
        'group',
        'text_name',
        'filter_add',
        'filter_name',
        'sort_order'
        
    ]
    labels = {
        'group': 'Группа опций',
        'text_name': 'Название опции',
        'filter_add': "Добавить в фильтрацию",
        'filter_name': "Название фильтрации на английском",
        'sort_order': "Сортировка"
    }
    widgets = {
        'group': forms.Select(attrs={
          'class': INPUT_CLASS
        }),
        'text_name': forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'id': 'char_name'
        }),
        'filter_add': forms.CheckboxInput(attrs={
            'class': 'form__controls-checkbox',
        }),
        'filter_name': forms.TextInput(attrs={
            'class': INPUT_CLASS,
        }),
        'sort_order': forms.TextInput(attrs={
            'class': INPUT_CLASS,
        }),
    }
    
class SubdomainForm(forms.ModelForm):
  class Meta:
    model = Subdomain
    fields = "__all__"
    widgets = {
        'name': forms.TextInput(attrs={
          'class': INPUT_CLASS
        }),
        'geotag': forms.TextInput(attrs={
            'class': INPUT_CLASS,
        }),
        'subdomain': forms.TextInput(attrs={
            'class': INPUT_CLASS,
        }),
    }
    
    
class ColorProductForm(forms.ModelForm):
  class Meta:
    related_products = forms.ModelMultipleChoiceField(
      queryset=Product.objects.all(),
      widget=forms.CheckboxSelectMultiple,
      required=False
      )
    model = ColorProduct
    fields = "__all__"
    widgets = {
        'name': forms.TextInput(attrs={
          'class': INPUT_CLASS
        }),
        'code_color': forms.TextInput(attrs={
            'class': INPUT_CLASS,
        }),
    }
    
class SubdomainContactForm(forms.ModelForm):
  class Meta:
    model = SubdomainContact
    fields = "__all__"
    widgets = {
        'phone': forms.TextInput(attrs={
          'class': INPUT_CLASS
        }),
        'phone_two': forms.TextInput(attrs={
            'class': INPUT_CLASS,
        }),
        'time': forms.DateInput(attrs={
            'class': INPUT_CLASS,
        }),
        'address': forms.TextInput(attrs={
            'class': INPUT_CLASS,
        }),
        'subdomain': forms.Select(attrs={
            'class': "form__controls-select",
        }),
    }
    
class GalleryForm(forms.ModelForm):
  class Meta:
    model = Gallery
    fields = "__all__"
    widgets = {
        'name': forms.TextInput(attrs={
          'class': INPUT_CLASS
        }),
    }
    
class GalleryCategoryForm(forms.ModelForm):
  class Meta:
    model = GalleryCategory
    fields = "__all__"
    widgets = {
        'name': forms.TextInput(attrs={
          'class': INPUT_CLASS
        }),
        'slug': forms.TextInput(attrs={
          'class': INPUT_CLASS,
          "id": "slug"
        }),
    }
    
    
