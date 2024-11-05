from home.models import BaseSettings
from shop.models import Category, ShopSettings 
 
def load_settings(request):
    return {'site_settings': BaseSettings.load()}

def category_menu(request):
    return {'category_menu': Category.objects.filter(add_menu=True)}