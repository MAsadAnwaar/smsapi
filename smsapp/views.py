from django.shortcuts import render
from rest_framework import generics
from .models import category, sub_category, sms , lang
from .serializers import CategorySerializer, SubCategorySerializer, SmsSerializer , LangSerializer
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from django.http import Http404


class CategoryList(generics.ListAPIView):
    queryset = category.objects.all()
    serializer_class = CategorySerializer

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
    queryset = sms.objects.all()
    serializer_class = SmsSerializer


class CategoryDetail(generics.RetrieveAPIView):
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


class LangList(generics.ListAPIView):
    queryset = lang.objects.all()
    serializer_class = LangSerializer

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        data = serializer.data

        for lang_data in data:
            lang_obj = lang.objects.get(language__iexact=lang_data['language'])  # Case-insensitive lookup
            cats = lang_obj.category_set.all()
            cat_serializer = CategorySerializer(cats, many=True, context={'request': request})
            lang_data['categories'] = cat_serializer.data

            # serialize related sub_cat and sms objects for each category object
            for cat_data in lang_data['categories']:
                cat_obj = category.objects.get(cat_name__iexact=cat_data['cat_name'], language=lang_obj)
                sub_cats = cat_obj.sub_category_set.all()
                sub_cat_serializer = SubCategorySerializer(sub_cats, many=True, context={'request': request})
                cat_data['sub_categories'] = sub_cat_serializer.data
                cat_data['cat_image_link'] = request.build_absolute_uri(cat_obj.cat_image_link.url)

                for sub_cat_data in cat_data['sub_categories']:
                    sub_cat_obj = sub_category.objects.get(sub_cat_name__iexact=sub_cat_data['sub_cat_name'], cat_name=cat_obj)
                    sms_objs = sms.objects.filter(sub_cat_name=sub_cat_obj)
                    sms_serializer = SmsSerializer(sms_objs, many=True, context={'request': request})
                    sub_cat_data['sms'] = sms_serializer.data

        return Response(data)
from .models import category, sms, lang


class LangDetail(generics.RetrieveAPIView):
    serializer_class = LangSerializer

    def get_object(self):
        language = self.kwargs['language'].lower()  # Convert to lowercase
        try:
            obj = lang.objects.get(language__iexact=language)  # Case-insensitive lookup
            return obj
        except lang.DoesNotExist:
            raise Http404

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        categories = instance.category_set.all()
        cat_serializer = CategorySerializer(categories, many=True, context={'request': request})
        response_data = serializer.data
        response_data['categories'] = cat_serializer.data

        # serialize sub-categories and SMS for each category object
        for cat_data in response_data['categories']:
            cat_obj = category.objects.get(cat_name__iexact=cat_data['cat_name'], language=instance)
            sub_cats = cat_obj.sub_category_set.all()
            sub_cat_serializer = SubCategorySerializer(sub_cats, many=True, context={'request': request})
            cat_data['sub_categories'] = sub_cat_serializer.data
            cat_data['cat_image_link'] = request.build_absolute_uri(cat_obj.cat_image_link.url)

            for sub_cat_data in cat_data['sub_categories']:
                sub_cat_obj = sub_category.objects.get(sub_cat_name__iexact=sub_cat_data['sub_cat_name'], cat_name=cat_obj)
                sms_objs = sms.objects.filter(sub_cat_name=sub_cat_obj)
                sms_serializer = SmsSerializer(sms_objs, many=True, context={'request': request})
                sub_cat_data['sms'] = sms_serializer.data

        return Response(response_data)

