from knox.models import AuthToken
from .serializers import *
from .models import *
from django.shortcuts import render
from django.conf import settings
from django.http import Http404
from rest_framework import generics, permissions
from .models import Complaint, sms
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
from rest_framework.permissions import IsAuthenticated  
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





class CategoryList(generics.ListAPIView):
    queryset = category.objects.all()
    serializer_class = CategorySerializer
    # authentication_classes = [TokenAuthentication,]
    # permission_classes = [IsAuthenticated,]

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        for category_data in data:
            category_obj = category.objects.get(cat_name__iexact=category_data['cat_name'])  # Case-insensitive lookup
            sub_cats = category_obj.sub_category_set.all()
            sub_cat_serializer = SubCategorySerializer(sub_cats, many=True, context={'request': request})
            category_data['sub_categories'] = sub_cat_serializer.data
            category_data['cat_image_link'] = request.build_absolute_uri(category_obj.cat_image_link.url)

            # serialize related sms for each sub_cat object
            for sub_cat_data in category_data['sub_categories']:
                sub_cat_obj = sub_category.objects.get(sub_cat_name__iexact=sub_cat_data['sub_cat_name'], cat_name=category_obj)
                sms_objs = sms.objects.filter(sub_cat_name=sub_cat_obj)
                sms_serializer = SmsSerializer(sms_objs, many=True, context={'request': request})
                sub_cat_data['sms'] = sms_serializer.data

        return Response(data)



class SmsList(generics.ListAPIView):
    # authentication_classes = [TokenAuthentication,]
    # permission_classes = [IsAuthenticated,]
    queryset = sms.objects.all()
    serializer_class = SmsSerializer


class CategoryDetail(generics.RetrieveAPIView):
    # authentication_classes = [TokenAuthentication,]
    # permission_classes = [IsAuthenticated,]
    serializer_class = CategorySerializer

    def get_object(self):
        cat_name = self.kwargs['cat_name'].lower()  # Convert to lowercase
        try:
            obj = category.objects.get(cat_name__iexact=cat_name)  # Case-insensitive lookup
            return obj
        except category.DoesNotExist:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        sub_cats = instance.sub_category_set.all()
        sub_cat_serializer = SubCategorySerializer(sub_cats, many=True, context={'request': request})
        response_data = serializer.data
        response_data['sub_categories'] = sub_cat_serializer.data
        response_data['cat_image_link'] = request.build_absolute_uri(instance.cat_image_link.url)

        # serialize related sms for each sub_cat object
        for sub_cat_data in response_data['sub_categories']:
            sub_cat_obj = sub_category.objects.get(sub_cat_name__iexact=sub_cat_data['sub_cat_name'], cat_name=instance)
            sms_objs = sms.objects.filter(sub_cat_name=sub_cat_obj)
            sms_serializer = SmsSerializer(sms_objs, many=True, context={'request': request})
            sub_cat_data['sms'] = sms_serializer.data

        return Response(response_data)


class SubCategoryDetail(generics.RetrieveAPIView):
    # authentication_classes = [TokenAuthentication,]
    # permission_classes = [IsAuthenticated,]
    serializer_class = SubCategorySerializer

    def get_object(self):
        cat_name = self.kwargs['cat_name'].lower()  # Convert to lowercase
        sub_cat_name = self.kwargs['sub_cat_name'].lower()  # Convert to lowercase
        try:
            obj = sub_category.objects.get(cat_name__cat_name__iexact=cat_name, sub_cat_name__iexact=sub_cat_name)  # Case-insensitive lookup
            return obj
        except sub_category.DoesNotExist:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        response_data = serializer.data
        response_data['cat_image_link'] = request.build_absolute_uri(instance.cat_name.cat_image_link.url)

        sms_objs = sms.objects.filter(sub_cat_name=instance)
        sms_serializer = SmsSerializer(sms_objs, many=True, context={'request': request})
        response_data['sms'] = sms_serializer.data

        return Response(response_data)


# from rest_framework.response import Response
# from rest_framework import generics
# from .serializers import LangSerializer, CategorySerializer, SubCategorySerializer, SmsSerializer
# from .models import lang, category, sub_category, sms

from rest_framework import generics
from rest_framework.response import Response
from .serializers import LangSerializer, CategorySerializer, SubCategorySerializer, SmsSerializer
from .models import lang, category, sub_category, sms

class LangList(generics.ListAPIView):
    queryset = lang.objects.all()
    serializer_class = LangSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        for lang_data in data:
            lang_obj = lang.objects.get(language__iexact=lang_data['language'])  # Case-insensitive lookup
            cats = category.objects.filter(lang=lang_obj)
            cat_serializer = CategorySerializer(cats, many=True, context={'request': request})
            lang_data['categories'] = cat_serializer.data

            for cat_data in lang_data['categories']:
                cat_obj = category.objects.get(cat_name__iexact=cat_data['cat_name'], lang=lang_obj)
                sub_cats = sub_category.objects.filter(cat_name=cat_obj)
                sub_cat_serializer = SubCategorySerializer(sub_cats, many=True, context={'request': request})
                cat_data['sub_categories'] = sub_cat_serializer.data
                cat_data['cat_image_link'] = request.build_absolute_uri(cat_obj.cat_image_link.url) if cat_obj.cat_image_link else None

                for sub_cat_data in cat_data['sub_categories']:
                    sub_cat_obj = sub_category.objects.get(sub_cat_name__iexact=sub_cat_data['sub_cat_name'], cat_name=cat_obj)
                    sms_objs = sms.objects.filter(sub_cat_name=sub_cat_obj)
                    sms_serializer = SmsSerializer(sms_objs, many=True, context={'request': request})
                    sub_cat_data['sms'] = sms_serializer.data

        return Response(data)



# class LangDetail(generics.RetrieveAPIView):
#     # authentication_classes = [TokenAuthentication,]
#     # permission_classes = [IsAuthenticated,]
#     serializer_class = LangSerializer

#     def get_object(self):
#         language = self.kwargs['language'].lower()  # Convert to lowercase
#         try:
#             obj = lang.objects.get(language__iexact=language)  # Case-insensitive lookup
#             return obj
#         except lang.DoesNotExist:
#             raise Http404

#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         serializer = self.get_serializer(instance)

#         categories = instance.category_set.all()
#         cat_serializer = CategorySerializer(categories, many=True, context={'request': request})
#         response_data = serializer.data
#         response_data['categories'] = cat_serializer.data

#         # serialize sub-categories and SMS for each category object
#         for cat_data in response_data['categories']:
#             cat_obj = category.objects.get(cat_name__iexact=cat_data['cat_name'], language=instance)
#             sub_cats = cat_obj.sub_category_set.all()
#             sub_cat_serializer = SubCategorySerializer(sub_cats, many=True, context={'request': request})
#             cat_data['sub_categories'] = sub_cat_serializer.data
#             cat_data['cat_image_link'] = request.build_absolute_uri(cat_obj.cat_image_link.url)

#             for sub_cat_data in cat_data['sub_categories']:
#                 sub_cat_obj = sub_category.objects.get(sub_cat_name__iexact=sub_cat_data['sub_cat_name'], cat_name=cat_obj)
#                 sms_objs = sms.objects.filter(sub_cat_name=sub_cat_obj)
#                 sms_serializer = SmsSerializer(sms_objs, many=True, context={'request': request})
#                 sub_cat_data['sms'] = sms_serializer.data

#         return Response(response_data)







# class CreateObjectsView(APIView):
#     serializer_classes = {
#         'lang': LangSerializer,
#         'category': CategorySerializer,
#         'sub_category': SubCategorySerializer,
#         'sms': SmsSerializer
#     }

#     def post(self, request, format=None):
#         # Extract data from the request
#         lang_data = request.data.get('lang', None)
#         category_data = request.data.get('category', None)
#         sub_category_data = request.data.get('sub_category', None)
#         sms_data = request.data.get('sms', None)

#         # Create objects
#         if lang_data:
#             lang_serializer = LangSerializer(data=lang_data)
#             if lang_serializer.is_valid():
#                 lang_obj = lang_serializer.save()
#             else:
#                 return Response(lang_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         if category_data:
#             category_data['language'] = lang_obj.id
#             category_serializer = CategorySerializer(data=category_data)
#             if category_serializer.is_valid():
#                 category_obj = category_serializer.save()
#             else:
#                 return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         if sub_category_data:
#             sub_category_data['cat_name'] = category_obj.id
#             sub_category_serializer = SubCategorySerializer(data=sub_category_data)
#             if sub_category_serializer.is_valid():
#                 sub_category_serializer.save()
#             else:
#                 return Response(sub_category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         if sms_data:
#             sms_data['sub_cat_name'] = sub_category_obj.id
#             sms_serializer = SmsSerializer(data=sms_data)
#             if sms_serializer.is_valid():
#                 sms_serializer.save()
#             else:
#                 return Response(sms_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#         return Response(status=status.HTTP_201_CREATED)




# SMS Create View


@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_sms(request):
    try:
        # Get language, category, and subcategory names from the request data
        language = request.data['lang']['language']
        cat_name = request.data['category']['cat_name']
        sub_cat_name = request.data['sub_category']['sub_cat_name']
        sms_text = request.data['sms']['sms']

        # Get the language, category, and subcategory objects
        selected_lang = lang.objects.get(language=language)
        selected_cat = category.objects.get(cat_name=cat_name)
        selected_sub_cat = sub_category.objects.get(cat_name=selected_cat, sub_cat_name=sub_cat_name)

        # Create a new SMS object with the subcategory, SMS text, and current user, and save it to the database
        new_sms = sms(sub_cat_name=selected_sub_cat, sms=sms_text, user=request.user)
        new_sms.save()

        # Serialize the new SMS and return it in the response
        sms_serializer = SmsSerializer(new_sms)
        return Response(sms_serializer.data, status=status.HTTP_201_CREATED)

    except (lang.DoesNotExist, category.DoesNotExist, sub_category.DoesNotExist):
        return Response("Invalid language, category, or subcategory name", status=status.HTTP_400_BAD_REQUEST)

# json form which is used to create sms 
# {
#     "lang": {
#         "language": "English"
#     },
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



from .models import category, lang, sub_category, sms

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import lang, category, sub_category, sms
from bs4 import BeautifulSoup
import requests

# @login_required
# def save_quotes(request):
#     if request.method == 'POST':
#         url = request.POST.get('url')  # Assuming you have a form input with name 'url'
#         headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#         r = requests.get(url, headers=headers)
#         soup = BeautifulSoup(r.content, "html.parser")
#         title = soup.find('h1').get_text()
        
#         cat, created = category.objects.get_or_create(cat_name="Quotes")
#         lang_obj, created = lang.objects.get_or_create(category=cat, language="English")  # Use the 'category' field to link the language to the category

#         # for https://hamariweb.com/mobiles/good_morning_sms_messages20/ datascrape
#         quotes = soup.find_all(class_="quote_text")    

#         for quote in quotes:
#             quote_text = quote.get_text().replace('\n', '')
#             if quote_text:
#                 sub_cat, created = sub_category.objects.get_or_create(cat_name=cat, sub_cat_name=title)
#                 # Check if an SMS with the same content already exists
#                 existing_sms = sms.objects.filter(sub_cat_name=sub_cat, sms=quote_text).exists()
#                 if not existing_sms:
#                     sms.objects.create(sub_cat_name=sub_cat, sms=quote_text, user=request.user)
        
#         return render(request, 'success.html')  # Assuming you have a template called 'success.html'

#     return render(request, 'save_quotes.html')



from .models import lang, category, sub_category, sms

@login_required
def save_quotes(request):
    languages = lang.objects.all()  # Get all available languages
    categories = category.objects.all()  # Get all available categories

    if request.method == 'POST':
        url = request.POST.get('url')  # Assuming you have a form input with name 'url'
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        r = requests.get(url, headers=headers)
        soup = BeautifulSoup(r.content, "html.parser")
        title = soup.find('h1').get_text()

        selected_lang_id = request.POST.get('language')  # Get selected language ID from the form
        selected_cat_id = request.POST.get('category')  # Get selected category ID from the form

        selected_lang = lang.objects.get(pk=selected_lang_id)  # Get the selected language object
        selected_cat = category.objects.get(pk=selected_cat_id)  # Get the selected category object

        quotes = soup.find_all(class_="quote_text")

        for quote in quotes:
            quote_text = quote.get_text().replace('\n', '')
            if quote_text:
                sub_cat, created = sub_category.objects.get_or_create(cat_name=selected_cat, language=selected_lang, sub_cat_name=title)
                # Check if an SMS with the same content already exists
                existing_sms = sms.objects.filter(sub_cat_name=sub_cat, sms=quote_text).exists()
                if not existing_sms:
                    sms.objects.create(sub_cat_name=sub_cat, sms=quote_text, user=request.user)

        return render(request, 'success.html')  # Assuming you have a template called 'success.html'

    context = {
        'languages': languages,
        'categories': categories
    }
    return render(request, 'save_quotes.html', context)  # Assuming you have a template called 'save_quotes.html'

# def save_quotes(request):
#     languages = lang.objects.all()  # Get all available languages
#     categories = category.objects.all()  # Get all available categories

#     if request.method == 'POST':
#         url = request.POST.get('url')  # Assuming you have a form input with name 'url'
#         headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#         r = requests.get(url, headers=headers)
#         soup = BeautifulSoup(r.content, "html.parser")
#         title = soup.find('h1').get_text()

#         selected_lang_id = request.POST.get('language')  # Get selected language ID from the form
#         selected_cat_id = request.POST.get('category')  # Get selected category ID from the form

#         selected_lang = lang.objects.get(pk=selected_lang_id)  # Get the selected language object
#         selected_cat = category.objects.get(pk=selected_cat_id)  # Get the selected category object

#         quotes = soup.find_all(class_="quote_text")

#         for quote in quotes:
#             quote_text = quote.get_text().replace('\n', '')
#             if quote_text:
#                 sub_cat, created = sub_category.objects.get_or_create(cat_name=selected_cat, sub_cat_name=title)
#                 # Check if an SMS with the same content already exists
#                 existing_sms = sms.objects.filter(sub_cat_name=sub_cat, sms=quote_text).exists()
#                 if not existing_sms:
#                     sms.objects.create(sub_cat_name=sub_cat, sms=quote_text, user=request.user)

#         return render(request, 'success.html')  # Assuming you have a template called 'success.html'

#     context = {
#         'languages': languages,
#         'categories': categories
#     }
#     return render(request, 'save_quotes.html', context)  # Assuming you have a template called 'save_quotes.html'

