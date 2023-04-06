from django.urls import path
from .views import CategoryList, CategoryDetail, SmsList, SubCategoryDetail

urlpatterns = [
    path('categories/', CategoryList.as_view(), name='category-list'),
    path('categories/<str:cat_name>/', CategoryDetail.as_view(), name='category-detail'),
    path('categories/<str:cat_name>/<str:sub_cat_name>/', SubCategoryDetail.as_view(), name='sub-category-detail'),
    path('sms/', SmsList.as_view(), name='sms-list'),
]
