from rest_framework import serializers
from .models import category, sub_category, sms


class SmsSerializer(serializers.ModelSerializer):
    sub_cat_name = serializers.CharField(source='sub_cat_name.sub_cat_name', read_only=True)

    class Meta:
        model = sms
        fields = ('sub_cat_name', 'sms')


class SubCategorySerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source='cat_name.cat_name', read_only=True)

    class Meta:
        model = sub_category
        fields = ('cat_name', 'sub_cat_name')


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = category
        fields = ('cat_name', 'cat_image_link', 'cat_added_date', 'sub_categories')
