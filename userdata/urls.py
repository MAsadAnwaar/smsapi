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


    # Login and Logout 

    path('Login/', views.login_view, name='Login'),
    path('logout/', views.logout_view, name='logout'),




    # Search MEthod 
    path('search/', SubCategorySearchView.as_view(), name='sub_category_search'),



    # Notifications 
    path('notifications/', NotificationsCreateView.as_view(), name='notifications-create'),
    path('notifications/user/', UserNotificationsListView.as_view(), name='notifications-user-list'),
    path('notifications/<int:pk>/', NotificationsRetrieveUpdateView.as_view(), name='notifications-retrieve-update'),
    path('notifications/<int:pk>/delete/', NotificationsRetrieveUpdateView.as_view(), name='notifications-delete'),
    path('send-notification/', SendNotificationView.as_view(), name='send_notification'),

]

