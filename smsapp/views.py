from django.shortcuts import render
from rest_framework import generics
from .models import category, sub_category, sms
from .serializers import CategorySerializer, SubCategorySerializer, SmsSerializer
from rest_framework import status
from rest_framework.response import Response
from django.conf import settings
from django.http import Http404


class CategoryList(generics.ListAPIView):
    queryset = category.objects.all()
    serializer_class = CategorySerializer


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
