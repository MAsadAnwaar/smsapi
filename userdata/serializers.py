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
# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('username',)

class SMSSerializer(serializers.ModelSerializer):
    language = serializers.PrimaryKeyRelatedField(queryset=lang.objects.all())
    cat_name = serializers.PrimaryKeyRelatedField(queryset=category.objects.all())
    sub_cat_name = serializers.PrimaryKeyRelatedField(queryset=sub_category.objects.all())
    sms = serializers.CharField(max_length=160)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = sms
        fields = ['id', 'language', 'cat_name', 'sub_cat_name', 'sms', 'user_name', 'status']


class SubCategorySerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source='cat_name.cat_name', read_only=True)

    class Meta:
        model = sub_category
        fields = ('id', 'cat_name', 'sub_cat_name')


class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = category
        fields = ('id', 'cat_name', 'cat_image_link', 'sub_categories')


class LangSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    sub_categories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = lang
        fields = ('id', 'language', 'categories', 'sub_categories')


class SmsSerializer(serializers.ModelSerializer):
    # sub_cat_name = SubCategorySerializer(read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = sms
        fields = ('id', 'sms', 'user_name', 'status')
    # sub_cat_name = SubCategorySerializer(read_only=True)
    # user_name = serializers.CharField(source='user.username', read_only=True)

    # class Meta:
    #     model = sms
    #     fields = ('id', 'sub_cat_name', 'sms', 'user_name', 'status')

   
 

# Complant BOX 
from .models import *
from rest_framework import serializers
from .models import Complaint

from rest_framework import serializers
from .models import Complaint

class ComplaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Complaint
        fields = ('sms', 'user', 'complaint_text')
        read_only_fields = ('user',)  # user should be set in view

    def validate(self, attrs):
        # Check if the user has already made a complaint for this SMS
        user = self.context['request'].user
        if Complaint.objects.filter(sms=attrs['sms'], user=user).exists():
            raise serializers.ValidationError('You have already complained about this SMS.')
        
        # Check if the user has reached the complaint limit for this SMS
        num_complaints = Complaint.objects.filter(sms=attrs['sms'], user=user).count()
        # max_complaints = attrs['sms'].max_complaints
        # if num_complaints >= max_complaints:
        #     raise serializers.ValidationError('You have reached the complaint limit for this SMS.')
        
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        complaint = Complaint.objects.create(**validated_data)
        return complaint



