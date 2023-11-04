from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path , include
from . views import *
from . import views

urlpatterns = [
    # path('create_objects/', CreateObjectsView.as_view(), name='create_objects'),
    # SMS Create urls 
    path('create-sms/', create_sms, name='create_sms'),
    path('update_sms/<int:sms_id>/', update_sms, name='create_sms'),
    path('delete_sms/<int:sms_id>/',delete_sms, name='delete_sms'),
    # Complaint Box 
    path('complaints/', ComplaintCreateView.as_view(), name='complaint-create'),
    # Knox Login & Signup 
    path('register/', RegisterAPI.as_view(), name='register'),
    path('login/', LoginAPI.as_view(), name='login'),
    path('logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    # for view all models 
    path('categories/', CategoryList.as_view(), name='category-list'),
    # path('categories/<str:cat_name>/', CategoryDetail.as_view(), name='category-detail'),
    # path('categories/<str:cat_name>/<str:sub_cat_name>/', SubCategoryDetail.as_view(), name='sub-category-detail'),
    path('categories/<int:cat_id>/', CategoryDetail.as_view(), name='category-detail'),
    path('categories/<int:cat_id>/<int:sub_cat_id>/', SubCategoryDetail.as_view(), name='sub-category-detail'),
    path('categories/<int:cat_id>/<int:sub_cat_id>/<int:sms_id>/', SmsDetail.as_view(), name='sms-detail'),
    path('sms/', SmsList.as_view(), name='sms-list'),
    # path('langs/', LangList.as_view(), name='lang-list'),
    # path('langs/<str:language>/', LangDetail.as_view(), name='lang-detail'),
    # path('langs/<str:language>/<str:cat_name>/', LangDetail.as_view(), name='lang-detail'),
    # path('langs/<str:language>/<str:cat_name>/<str:sub_cat_name>/', LangDetail.as_view(), name='lang-detail'),




    # save Quote Using Scrape MEthod 
    path('save_quotes/', save_quotes, name='save_quotes'),


    # Like and Dislike SMS 
    path('like-sms/<int:sms_id>/', views.like_sms, name='like-sms'),
    path('dislike-sms/<int:sms_id>/', views.dislike_sms, name='dislike-sms'),


    # Login and Logout 

    path('Login/', views.login_view, name='Login'),
    path('logout/', views.logout_view, name='logout'),

    # images 
    path('images/<int:sub_category_id>/', ImageListBySubCategory.as_view(), name='image-list-by-subcategory'),
    # Stickers 
    path('stickers/<int:sub_category_id>/', StickerListBySubCategory.as_view(), name='Sticker-list-by-subcategory'),

    # Upload images
    path('upload/', upload_images, name='upload_images'),

    # Upload sticker
    path('upload_sticker/', upload_sticker, name='upload_sticker'),

]

