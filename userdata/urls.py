from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path , include
from . views import *
from . import views

urlpatterns = [
    path('create_objects/', CreateObjectsView.as_view(), name='create_objects'),
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
    path('categories/<str:cat_name>/', CategoryDetail.as_view(), name='category-detail'),
    path('categories/<str:cat_name>/<str:sub_cat_name>/', SubCategoryDetail.as_view(), name='sub-category-detail'),
    path('sms/', SmsList.as_view(), name='sms-list'),
    path('langs/', LangList.as_view(), name='lang-list'),
    path('langs/<str:language>/', LangDetail.as_view(), name='lang-detail'),
    path('langs/<str:language>/<str:cat_name>/', LangDetail.as_view(), name='lang-detail'),
    path('langs/<str:language>/<str:cat_name>/<str:sub_cat_name>/', LangDetail.as_view(), name='lang-detail'),




    # save Quote Using Scrape MEthod 
    path('save_quotes/', save_quotes, name='save_quotes'),


    # Like and Dislike SMS 
    path('like-sms/<int:sms_id>/', views.like_sms, name='like-sms'),
    path('dislike-sms/<int:sms_id>/', views.dislike_sms, name='dislike-sms'),
]











# e7c3f6224b0addd2615ddf7e4c6e7192be7a63e047ff7eae4ee0c5dff2179f4a