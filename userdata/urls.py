from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path , include
from . views import *
urlpatterns = [
    
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', knox_views.LogoutView.as_view(), name='logout'),
    path('api/logoutall/', knox_views.LogoutAllView.as_view(), name='logoutall'),
    path('api/change-password/', ChangePasswordView.as_view(), name='change-password'),
    path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
    path('api/categories/', CategoryList.as_view(), name='category-list'),
    path('api/categories/<str:cat_name>/', CategoryDetail.as_view(), name='category-detail'),
    path('api/categories/<str:cat_name>/<str:sub_cat_name>/', SubCategoryDetail.as_view(), name='sub-category-detail'),
    path('api/sms/', SmsList.as_view(), name='sms-list'),
    path('api/langs/', LangList.as_view(), name='lang-list'),
    path('api/langs/<str:language>/', LangDetail.as_view(), name='lang-detail'),
    path('api/langs/<str:language>/<str:cat_name>/', LangDetail.as_view(), name='lang-detail'),
    path('api/langs/<str:language>/<str:cat_name>/<str:sub_cat_name>/', LangDetail.as_view(), name='lang-detail'),

]











# e7c3f6224b0addd2615ddf7e4c6e7192be7a63e047ff7eae4ee0c5dff2179f4a