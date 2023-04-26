from rest_framework import serializers
from .models import category, sub_category, sms , lang


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
        fields = ('cat_name', 'cat_image_link', 'sub_categories')
class LangSerializer(serializers.ModelSerializer):
    
    categories = CategorySerializer(many=True, read_only=True)
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = lang
        fields = ('id', 'language', 'categories','sub_categories')