from django.urls import path

from . import views


urlpatterns = [
    path('', views.admin, name="admin"),
    
    #URl - отвечающие за загрузку данных
    path('upload-goods/', views.upload_goods, name="upload_goods"),
    path('upload-succes/', views.upload_succes, name="upload-succes"),
    
    #URl - отвечающие за отображение категорий, редактирование и удаление категории
    path('category/', views.admin_category, name='admin_category'),
    path('category/add/', views.category_add, name='category_add'),
    path('category/edit/<int:pk>/', views.category_edit, name='category_edit'),
    path('category/delete/<int:pk>/', views.category_delete, name='category_delete'),
    
    
    
    #URl - отвечающие за отображение дня недели, редактирование и удаление дня недели
    path('days/', views.day_product, name='admin_day'),
    path('days/add/', views.day_add, name='days_add'),
    path('days/edit/<int:pk>/', views.day_edit, name='days_edit'),
    # path('days/delete/<int:pk>/', views.day_delete, name='days_delete'),
    
    #URl - отвечающие за отображение товаров, редактирование и удаление товара
    path('product/', views.admin_product, name='admin_product'),
    path('product/add/', views.product_add, name='product_add'),
    path('product/edit/<int:pk>/', views.product_edit, name='product_edit'),
    path('product/delete/<int:pk>/', views.product_delete, name='product_delete'),
    
      
    #URl - отвечающие за отображение характиристик, редактирование и удаление характеристик
    path('char/', views.admin_char, name='admin_char'),
    path('char/char-add/', views.char_add, name='char_add'),
    path('char/char-edit/<int:pk>', views.char_edit, name='char_edit'),
    path('char/char-delete/<int:pk>', views.char_delete, name='char_delete'),
    
    
    path('char/group/add/', views.char_group_add, name='char_group_add'),
    path('char/group/edit/<int:pk>', views.char_group_edit, name='char_group_edit'),
    path('char/group/delete/<int:pk>', views.char_group_delete, name='char_group_delete'),
    
    #URl - отвечающие за отображение филлиалов, редактирование и удаление филлиала
    path('fillial/', views.admin_fillial, name='admin_fillial'),
    path('fillial/add/', views.fillial_add, name='fillial_add'),
    path('fillial/edit/<int:pk>/', views.fillial_edit, name='fillial_edit'),
    # path('fillial/delete/<int:pk>/', views.fillial_delete, name='fillial_delete'),
    
    #URl - отвечающие за отображение отзывов, редактирование и удаление отзывов
    path('admin-reviews/', views.admin_reviews, name='admin_reviews'),
    path('admin-reviews/add/', views.admin_reviews_add, name='admin_reviews_add'),
    path('admin-reviews/edit/<int:pk>/', views.admin_reviews_edit, name='admin_reviews_edit'),
    path('admin_reviews/delete/<int:pk>/', views.admin_reviews_delete, name='admin_reviews_delete'),
    
    #URl - отвечающие за отображение акций, редактирование и удаление акций
    path('stock/', views.admin_stock, name='admin_stock'),
    path('stock/add/', views.stock_add, name='stock_add'),
    path('stock/edit/<int:pk>/', views.stock_edit, name='stock_edit'),
    path('stock/delete/<int:pk>/', views.stock_delete, name='stock_delete'),
    
    #URl - отвечающие за отображение услуг, редактирование и удаление услуг
    path('service-page/', views.admin_service_page, name='admin_service_page'),
    path('serv/', views.admin_service, name='admin_service'),
    path('serv/add/', views.service_add, name='service_add'),
    path('serv/edit/<int:pk>/', views.service_edit, name='service_edit'),
    path('serv/delete/<int:pk>/', views.service_delete, name='service_delete'),
    
    #URl - Шаблон главной страницы
    path('home/', views.admin_home, name='admin_home'),
    
    #URl - Шаблон общих настроек сайта
    path('settings/', views.admin_settings, name='admin_settings'),
    path('robots/', views.robots, name='robots'),
    
    path('home-page/', views.admin_home_page, name='admin_home_page'),
    
    path('admin-shop/', views.admin_shop, name='admin_shop'),
    
    #URl - субдомены
    path('subdomain/', views.admin_subdomain, name='admin_subdomain'),
    path('subdomain/add/', views.subdomain_add, name='subdomain_add'),
    path('subdomain/edit/<int:pk>/', views.subdomain_edit, name='subdomain_edit'),
    # path('subdomain/delete/<int:pk>/', views.subdomain_delete, name='subdomain_delete'),
    
    #URl - цвета памятников
    path('color-product/', views.admin_color, name='admin_color'),
    path('color-product/add/', views.admin_color_add, name='admin_color_add'),
    path('color-product/edit/<int:pk>/', views.admin_color_edit, name='admin_color_edit'),
    # path('subdomain/delete/<int:pk>/', views.subdomain_delete, name='subdomain_delete'),
    
    #URl - цвета памятников
    path('gallery-settings/', views.gallery_settings, name='gallery_settings'),
    path('gallery/', views.admin_gallery, name='admin_gallery'),
    path('gallery/add/', views.admin_gallery_add, name='admin_gallery_add'),
    path('gallery/edit/<int:pk>/', views.admin_gallery_edit, name='admin_gallery_edit'),
    # path('subdomain/delete/<int:pk>/', views.subdomain_delete, name='subdomain_delete'),
    
    #URl - отвечающие за отображение категории Галлереи, редактирование и удаление категории
    path('gallery-category/', views.admin_gallery_category, name='admin_gallery_category'),
    path('gallery-category/add/', views.gallery_category_add, name='gallery_category_add'),
    path('gallery-category/edit/<int:pk>/', views.gallery_category_edit, name='gallery_category_edit'),
    path('gallery-category/delete/<int:pk>/', views.gallery_category_delete, name='gallery_category_delete'),
    
    #URl - отвечающие за отображение категории Страниц блога, редактирование и удаление категории
    path('blog-settings/', views.blog_settings, name='blog_settings'),
    path('article/', views.article, name='article'),
    path('article/add/', views.article_add, name='article_add'),
    path('article/edit/<int:pk>/', views.article_edit, name='article_edit'),
    path('article/delete/<int:pk>/', views.article_delete, name='article_delete'),
]