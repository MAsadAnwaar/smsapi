from knox.models import AuthToken
from .serializers import *
from .models import *
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from rest_framework import generics, permissions
from knox.auth import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.views import APIView
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
import requests
# Register API
class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
        "user": UserSerializer(user, context=self.get_serializer_context()).data,
        "token": AuthToken.objects.create(user)[1]
        })




class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginAPI, self).post(request, format=None)


 

class ChangePasswordView(generics.UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password updated successfully',
                'data': []
            }

            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from rest_framework.decorators import api_view

@api_view(['POST'])
def like_sms(request, sms_id):
    sms_obj = sms.objects.get(pk=sms_id)
    user = request.user

    if user in sms_obj.likes.all():
        sms_obj.likes.remove(user)
    else:
        sms_obj.likes.add(user)
        sms_obj.dislikes.remove(user)

    return Response({'detail': 'Action performed successfully.'})


@api_view(['POST'])
def dislike_sms(request, sms_id):
    sms_obj = sms.objects.get(pk=sms_id)
    user = request.user

    if user in sms_obj.dislikes.all():
        sms_obj.dislikes.remove(user)
    else:
        sms_obj.dislikes.add(user)
        sms_obj.likes.remove(user)

    return Response({'detail': 'Action performed successfully.'})




from django.db.models import Prefetch
class CategoryList(generics.ListAPIView):
    queryset = category.objects.prefetch_related('sub_category_set__sms_set')
    serializer_class = CategorySerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     data = serializer.data

    #     for category_data in data:
    #         category_obj = category.objects.get(cat_name__iexact=category_data['cat_name'])  # Case-insensitive lookup
    #         sub_cat_serializer = SubCategorySerializer(category_obj.sub_category_set.all(), many=True, context={'request': request})
    #         category_data['sub_categories'] = sub_cat_serializer.data
    #         category_data['cat_image_link'] = request.build_absolute_uri(category_obj.cat_image_link.url)

    #         for sub_cat_data in category_data['sub_categories']:
    #             sub_cat_objs = sub_category.objects.filter(sub_cat_name__iexact=sub_cat_data['sub_cat_name'], cat_name=category_obj)
    #             if sub_cat_objs.exists():
    #                 sms_objs = sub_cat_objs[0].sms_set.all()
    #                 sms_serializer = SmsSerializer(sms_objs, many=True, context={'request': request})
    #                 sub_cat_data['sms'] = sms_serializer.data

    #     return Response(data)
# class CategoryList(generics.ListAPIView):
#     queryset = category.objects.select_related('language').prefetch_related(
#         Prefetch('sub_category_set', queryset=sub_category.objects.prefetch_related('sms_set'))
#     )
#     serializer_class = CategorySerializer

    # def list(self, request, *args, **kwargs):
    #     queryset = self.get_queryset()
    #     serializer = self.get_serializer(queryset, many=True)
    #     data = serializer.data

    #     for category_data in data:
    #         category_obj = category.objects.get(cat_name__iexact=category_data['cat_name'])  # Case-insensitive lookup
    #         sub_cat_serializer = SubCategorySerializer(category_obj.sub_category_set.all(), many=True, context={'request': request})
    #         category_data['sub_categories'] = sub_cat_serializer.data
    #         category_data['cat_image_link'] = request.build_absolute_uri(category_obj.cat_image_link.url)

    #         for sub_cat_data in category_data['sub_categories']:
    #             sub_cat_objs = sub_category.objects.filter(sub_cat_name__iexact=sub_cat_data['sub_cat_name'], cat_name=category_obj)
    #             if sub_cat_objs.exists():
    #                 sms_objs = sub_cat_objs[0].sms_set.all()
    #                 sms_serializer = SmsSerializer(sms_objs, many=True, context={'request': request})
    #                 sub_cat_data['sms'] = sms_serializer.data

    #     return Response(data)




class SmsList(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication,]
    # permission_classes = [IsAuthenticated,]
    queryset = sms.objects.all()
    serializer_class = SmsSerializer


from django.db.models import Prefetch
class CategoryDetail(generics.RetrieveAPIView):
    serializer_class = CategorySerializer

    def get_object(self):
        cat_id = self.kwargs['cat_id']
        try:
            obj = category.objects.prefetch_related(
                'sub_category_set__sms_set'
            ).get(id=cat_id)
            return obj
        except category.DoesNotExist:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        sub_cat_serializer = SubCategorySerializer(instance.sub_category_set.all(), many=True, context={'request': request})
        response_data = serializer.data
        response_data['sub_categories'] = sub_cat_serializer.data
        response_data['cat_image_link'] = request.build_absolute_uri(instance.cat_image_link.url)

        return Response(response_data)



from django.db.models import Prefetch
class SubCategoryDetail(generics.RetrieveAPIView):
    serializer_class = SubCategorySerializer

    def get_object(self):
        cat_id = self.kwargs['cat_id']
        sub_cat_id = self.kwargs['sub_cat_id']
        try:
            obj = sub_category.objects.select_related('cat_name').prefetch_related(
                'sms_set__user', 'sms_set__likes', 'sms_set__dislikes'
            ).get(cat_name__id=cat_id, id=sub_cat_id)
            return obj
        except sub_category.DoesNotExist:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        response_data = serializer.data
        response_data['cat_image_link'] = request.build_absolute_uri(instance.cat_name.cat_image_link.url)

        sms_objs = instance.sms_set.all()
        sms_serializer = SmsSerializer(sms_objs, many=True, context={'request': request})
        response_data['sms'] = sms_serializer.data

        return Response(response_data)


from django.shortcuts import get_object_or_404

class SmsDetail(generics.RetrieveAPIView):
    serializer_class = SmsSerializer

    def get_object(self):
        cat_id = self.kwargs['cat_id']
        sub_cat_id = self.kwargs['sub_cat_id']
        sms_id = self.kwargs['sms_id']
        try:
            obj = sms.objects.select_related(
                'sub_cat_name__cat_name', 'user'
            ).prefetch_related('likes', 'dislikes').get(
                sub_cat_name__cat_name__id=cat_id,
                sub_cat_name__id=sub_cat_id,
                id=sms_id
            )
            return obj
        except sms.DoesNotExist:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        response_data = serializer.data
        response_data['cat_name'] = instance.sub_cat_name.cat_name.cat_name
        response_data['sub_cat_name'] = instance.sub_cat_name.sub_cat_name

        return Response(response_data)

# SMS Create View


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_sms(request):
    try:
        # Get language, category, and subcategory names from the request data
        # language = request.data['lang']['language']
        # # Defult use
        # language = 'English'      
        cat_name = request.data['category']['cat_name']
        sub_cat_name = request.data['sub_category']['sub_cat_name']
        sms_text = request.data['sms']['sms']

        # Get the language, category, and subcategory objects
        # selected_lang = lang.objects.get(language=language)
        selected_cat = category.objects.get(cat_name=cat_name)
        selected_sub_cat = sub_category.objects.get(cat_name=selected_cat, sub_cat_name=sub_cat_name)

        # Create a new SMS object with the subcategory, SMS text, and current user, and save it to the database
        new_sms = sms(sub_cat_name=selected_sub_cat, sms=sms_text, user=request.user)
        new_sms.save()

        # Serialize the new SMS and return it in the response
        sms_serializer = SmsSerializer(new_sms)
        return Response(sms_serializer.data, status=status.HTTP_201_CREATED)

    except ( category.DoesNotExist, sub_category.DoesNotExist):
        return Response("Invalid language, category, or subcategory name", status=status.HTTP_400_BAD_REQUEST)

# json form which is used to create sms 
# {
#     "category": {
#         "cat_name": "Quotes"
#     },
#     "sub_category": {
#         "cat_name": "Quotes",
#         "sub_cat_name": "Good Morning Wishes"
#     },
#     "sms": {
#         "sub_cat_name": "Good Morning Wishes",
#         "sms": "Good Morning"
#     }
# }




@api_view(['PUT'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def update_sms(request, sms_id):
    try:
        # Get the SMS object and check that it belongs to the current user
        selected_sms = sms.objects.get(pk=sms_id, user=request.user)

        # Update the SMS text if provided in the request data
        if 'sms' in request.data:
            selected_sms.sms = request.data['sms']
            selected_sms.save()

        # Serialize the updated SMS and return it in the response
        sms_serializer = SmsSerializer(selected_sms)
        return Response(sms_serializer.data)

    except sms.DoesNotExist:
        return Response("Invalid SMS ID", status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def delete_sms(request, sms_id):
    try:
        # Get the SMS object and check that it belongs to the current user
        selected_sms = sms.objects.get(pk=sms_id, user=request.user)

        # Delete the SMS from the database
        selected_sms.delete()

        # Return a success response
        return Response("SMS deleted successfully")

    except sms.DoesNotExist:
        return Response("Invalid SMS ID", status=status.HTTP_400_BAD_REQUEST)


# complain box 


class ComplaintCreateView(generics.CreateAPIView):
    serializer_class = ComplaintSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        # No need to set the user field here since it's already set in the serializer
        serializer.save()


# class ComplaintViewSet(viewsets.ModelViewSet):
#     queryset = Complaint.objects.all()
#     serializer_class = ComplaintSerializer

#     def create(self, request):
#         serializer = self.get_serializer(data=request.data)
#         if serializer.is_valid():
#             sms = SMS.objects.get(id=request.data['sms'])
#             user = request.user
#             num_complaints = Complaint.objects.filter(sms=sms, user=user).count()
#             if num_complaints >= serializer.validated_data['max_complaints']:
#                 sms.delete()
#                 return Response({'message': 'Max complaints reached, SMS deleted'}, status=status.HTTP_400_BAD_REQUEST)
#             serializer.save(user=user)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateObjectsView(APIView):
    serializer_classes = {
        'category': CategorySerializer,
        'sub_category': SubCategorySerializer,
        'sms': SmsSerializer
    }

    def post(self, request, format=None):
        # Extract data from the request
        category_data = request.data.get('category', None)
        sub_category_data = request.data.get('sub_category', None)
        sms_data = request.data.get('sms', None)

        # Create objects

        if category_data:
            category_serializer = CategorySerializer(data=category_data)
            if category_serializer.is_valid():
                category_obj = category_serializer.save()
            else:
                return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if sub_category_data:
            sub_category_data['cat_name'] = category_obj.id
            sub_category_serializer = SubCategorySerializer(data=sub_category_data)
            if sub_category_serializer.is_valid():
                sub_category_serializer.save()
            else:
                return Response(sub_category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        if sms_data:
            sms_data['sub_cat_name'] = sub_category_obj.id
            sms_serializer = SmsSerializer(data=sms_data)
            if sms_serializer.is_valid():
                sms_serializer.save()
            else:
                return Response(sms_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_201_CREATED)






import FCMManager as fcm
from .models import category, sub_category, sms
@login_required(login_url='Login')
# @login_required
def save_quotes(request):
    # languages = lang.objects.all()  # Get all available languages
    categories = category.objects.all()  # Get all available categories

    if request.method == 'POST':
        url = request.POST.get('url')  # Assuming you have a form input with name 'url'
        website = request.POST.get('website')
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        title = soup.find('h1').get_text()

        # selected_lang_id = request.POST.get('language')  # Get selected language ID from the form
        selected_cat_id = request.POST.get('category')  # Get selected category ID from the form

        # selected_lang = lang.objects.get(pk=selected_lang_id)  # Get the selected language object
        selected_cat = category.objects.get(pk=selected_cat_id)  # Get the selected category object
        if website == "hamariweb.com":
            # for https://hamariweb.com/mobiles/good_morning_sms_messages20/ datascrape

            quotes = soup.find_all(class_= "quote_text")  

        elif website == "www.brainyquote.com":
            # for https://www.brainyquote.com/topics/life-quotes qoutes scrape

            quotes = soup.find_all(class_= "b-qt qt_109542 oncl_q")
        elif website == "www.goodreads.com":
            # for https://www.goodreads.com/quotes quotes scrape

            quotes = soup.find_all(class_= "quoteText")
        elif website == "www.fluentin3months.com":
            # for https://www.fluentin3months.com/chinese-proverbs/ quotes scrape

            quotes = soup.find_all(class_= "wp-block-heading")
        elif website == "www.goodhousekeeping.com":
           # for https://www.goodhousekeeping.com/life/g5080/life-quotes/ quotes scrape
            quotes = soup.find_all(class_= "css-18vfmjb et3p2gv0")

        elif website == "www.143greetings.com":
        #     # for https://www.143greetings.com/goodluck/messages.html?utm_content=expand_article quotes scrape
            quotes = soup.find_all(class_= "message") 

        elif website == "blog.rescuetime.com":
            # for https://blog.rescuetime.com/time-management-quotes/ quotes scrape
            quotes = soup.find_all(class_ = "wp-block-quote")
        # elif website == "www.fi.edu":
        #     # for https://www.fi.edu/en/benjamin-franklin/famous-quotes quotes scrape
        #     quotes = soup.find_all(dir="ltr")
        elif website == "www.berries.com":
            
            # for https://www.berries.com/blog/positive-quotes quotes scrape
            quotes = soup.find_all(class_="has-text-align-center filter-box-quote")
        elif website == "www.keepinspiring.me":
            # for https://www.keepinspiring.me/famous-quotes/ quotes scrape
            quotes = soup.find_all(class_="wp-block-quote is-style-large")
        for quote in quotes:
            quote_text = quote.get_text().replace('\n', '')
            if quote_text:
                sub_cat, created = sub_category.objects.get_or_create(cat_name=selected_cat, sub_cat_name=title)
                # Check if an SMS with the same content already exists
                existing_sms = sms.objects.filter(sub_cat_name=sub_cat, sms=quote_text).exists()
                if not existing_sms:
                    sms.objects.create(sub_cat_name=sub_cat, sms=quote_text, user=request.user)

        # keyword = request.data.get('keyword')
        # message = request.data.get('message')
        keyword = title
        message = ("SMS Updates")
        tokens = [
                "cPhEglgmQ62VzMWlPpN47L:APA91bFbXcOTYz0ThEu1Oleja3wLb-TI1KBasm-ki2OEa13K1xZzOLKWCrwn6QuseI0i7zZXF46mCWdIr8S--ZAHxv8aZ8mrlKjbUZ4b3QVlqZDYn_EoYANZOMkv8ZyUvMB8XmurDytX",
                "cHrgv6txT9ac-_La0F6uSz:APA91bFlFwvRsOFYq3xUZ7Odw6MyAQA2my6Q4C39XWtJsCgcQT0hkkDyWMVuwb8jDqazM02j8l_KDC3V0B3j1jf8yvg3kXZUaDWnrf5whQTKiLwSMaCG_mPgxEZgmCvVFOJy93QqjzBn",
                "dyu0cpTUTmCBqxwWlSn4ua:APA91bGWAe_GUMY7qyjiuUcc91uzHBz-i7YXxjnVuvEknh5aulUBMhrUABqb0KGXNtK57454xV-MqXChehWi3AngQcbJ8H-9PgYPv0Jm6SSAY_Yf_uNIPT7Z6AUNAAeFF5fmtxA-AzA4",
                "fwQ7q_VqQ9mvNUa5IBkIst:APA91bEzGAQJ71Mca3cfhyDOEdE5LDeBht98q4WvAA8znPqj4SREp5QEBCwK8pJcedrt05fEUEZnJKgebZvZMJhbz63ENvYVE0Z4eKAmH1oYBRO4KPbzCCsAO98KOUQ5tkO5gfHFUTan",
                "du3CXja2RPC2QQK73-2sr5:APA91bGKX1p5VcOU19Dmv4GaZgFhgc0BKVy9SgnorTUW_lk3R7JdEe-0B0XsUljYI0aWuJ-hUFHpLCFZUtMrX7j8mQ8cM-ozyeMXT5HPK9XAKomTy9b8ZQmdTwLVyKkzYlO_O_d8j654",

                ]
        for token in tokens:
                fcm.sendPush(keyword, message, [token])
        # fcm.sendPush(keyword, message, tokens)
        if not keyword or not message:
    # sendPush to all available tokens
            for token in tokens:
                fcm.sendPush(keyword, message, [token])
        else:
            fcm.sendPush(keyword, message, tokens)

        # # Find all users who have searched for the given keyword
        # users = search.objects.filter(keywords=keyword).values_list('user', flat=True)

        # # # Check if the keyword already exists
        # # existing_keyword = search.objects.filter(keywords=keyword).exists()
        # # if existing_keyword:
        # #     notifications = []
        # #     for user_id in users:
        # #         notification = Notifications(user_id=user_id, message=message)
        # #         notifications.append(notification)

        # #     # Bulk create the notifications
        # #     Notifications.objects.bulk_create(notifications)

        # #     # return Response("Notifications sent successfully And Keyword  Existing", status=status.HTTP_200_OK)

        # # Create notifications for each user
        # notifications = []
        # for user_id in users:
        #     notification = Notifications(user_id=user_id, message=message)
        #     notifications.append(notification)

        # # Bulk create the notifications
        # Notifications.objects.bulk_create(notifications)

        # return Response("Notifications sent successfully", status=status.HTTP_200_OK)

        messages.success(request, 'SMS Update Successfully')
        # return render(request, 'success.html')  # Assuming you have a template called 'success.html'

    context = {
        # 'languages': languages,
        'categories': categories
    }
    return render(request, 'save_quotes.html', context)  # Assuming you have a template called 'save_quotes.html'




from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect


def login_view(request):
    if request.user.is_authenticated:
        return redirect('save_quotes')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # messages.success(request, 'Login Successful')
            return redirect('save_quotes')  # Replace 'home' with the desired URL name for the home page
        else:
            # messages.error(request, f'Error creating theme: {str(e)}')
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login/login.html')





def logout_view(request):
    logout(request)
    return redirect('Login')


# Search Method 


from django.db.models import Q
from django.shortcuts import get_object_or_404

class SubCategorySearchView(APIView):
    authentication_classes = [TokenAuthentication,]
    permission_classes = [IsAuthenticated,]

    def get(self, request):
        query = request.GET.get('query')

        if not query:
            return Response("Please provide a search query", status=status.HTTP_400_BAD_REQUEST)

        # Perform the case-insensitive search query to filter the SMS objects by subcategory name
        sms_objects = sms.objects.filter(Q(sub_cat_name__sub_cat_name__icontains=query) | Q(sub_cat_name__sub_cat_name__iexact=query))

      

        serializer = SmsSerializer(sms_objects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ImageListBySubCategory(generics.ListAPIView):
    serializer_class = ImageSerializer

    def get_queryset(self):
        sub_category_id = self.kwargs['sub_category_id']
        return Image.objects.filter(sub_category_id=sub_category_id)



class StickerListBySubCategory(generics.ListAPIView):
    serializer_class = StickerSerializer

    def get_queryset(self):
        sub_category_id = self.kwargs['sub_category_id']
        return Sticker.objects.filter(sub_category_id=sub_category_id)  
    

from django.shortcuts import render, redirect
from .forms import ImageUploadForm, StickerUploadForm
from django.contrib import messages
@login_required(login_url='Login')
def upload_images(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            sub_category = form.cleaned_data['sub_category']
            images = request.FILES.getlist('image')
            thumbnails = request.FILES.getlist('thumbnail')

            for image, thumbnail in zip(images, thumbnails):
                Image.objects.create(sub_category=sub_category, image=image, thumbnail=thumbnail)
            messages.success(request, 'Images and thumbnails uploaded successfully!')
            return redirect('upload_images')  # Redirect to a success page
    else:
        form = ImageUploadForm()

    return render(request, 'upload_images.html', {'form': form})

@login_required(login_url='Login')
def upload_sticker(request):
    if request.method == 'POST':
        form = StickerUploadForm(request.POST, request.FILES)
        if form.is_valid():
            sub_category = form.cleaned_data['sub_category']
            sticker = request.FILES.getlist('sticker')

            for uploaded_sticker in sticker:
                Sticker.objects.create(sub_category=sub_category, sticker=uploaded_sticker)
            messages.success(request, 'Images uploaded successfully!')
            return redirect('upload_sticker')  # Redirect to a success page
    else:
        form = StickerUploadForm()

    return render(request, 'upload_sticker.html', {'form': form})

