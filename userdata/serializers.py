from rest_framework import serializers
from django.contrib.auth.models import User

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'], validated_data['email'], validated_data['password'])

        return user

from rest_framework import serializers
from django.contrib.auth.models import User

class ChangePasswordSerializer(serializers.Serializer):
    model = User

    """
    Serializer for password change endpoint.
    """
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)







from rest_framework import serializers
from .models import category, sub_category, sms , lang
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username',)

class SmsSerializer(serializers.ModelSerializer):
    sub_cat_name = serializers.CharField(source='sub_cat_name.sub_cat_name', read_only=True)
    # user = UserSerializer(read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = sms
        fields = ('sub_cat_name', 'sms', 'user_name')


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

# Serializers For SMS Create 

from rest_framework import serializers
from .models import lang, category, sub_category, sms

class SMSSerializer(serializers.ModelSerializer):
    language = serializers.PrimaryKeyRelatedField(queryset=lang.objects.all())
    cat_name = serializers.PrimaryKeyRelatedField(queryset=category.objects.all())
    sub_cat_name = serializers.PrimaryKeyRelatedField(queryset=sub_category.objects.all())
    sms = serializers.CharField(max_length=160)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = sms
        fields = ['language', 'cat_name', 'sub_cat_name', 'sms', 'user_name']

    # def create(self, validated_data):
    #     language = validated_data['language']
    #     cat_name = validated_data['cat_name']
    #     sub_cat_name = validated_data['sub_cat_name']
    #     sms_text = validated_data['sms']

    #     selected_cat = category.objects.get(pk=cat_name.id, language=language)
    #     selected_sub_cat = sub_category.objects.get(pk=sub_cat_name.id, cat_name=selected_cat)

    #     new_sms = sms(sub_cat_name=selected_sub_cat, sms=sms_text)
    #     new_sms.save()
    #     return new_sms
