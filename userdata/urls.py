from .views import RegisterAPI
from django.urls import path
from knox import views as knox_views
from .views import LoginAPI
from django.urls import path , include
from . views import *
urlpatterns = [
    path('create_objects/', CreateObjectsView.as_view(), name='create_objects'),
    # SMS Create urls 
    path('create-sms/', create_sms, name='create_sms'),

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

]











# e7c3f6224b0addd2615ddf7e4c6e7192be7a63e047ff7eae4ee0c5dff2179f4a