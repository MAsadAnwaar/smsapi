from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

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










class SubCategorySerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source='cat_name.cat_name', read_only=True)

    class Meta:
        model = sub_category
        fields = ('id', 'cat_name', 'sub_cat_name','Sub_cat_image')
class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'
class StickerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sticker
        fields = '__all__'
class CategorySerializer(serializers.ModelSerializer):
    sub_categories = SubCategorySerializer(many=True, read_only=True)
    
    class Meta:
        model = category
        fields = ('id', 'cat_name', 'cat_image_link', 'sub_categories')



class SmsSerializer(serializers.ModelSerializer):
    sub_cat_name = serializers.CharField(source='sub_cat_name.sub_cat_name', read_only=True)
    cat_name = serializers.CharField(source='sub_cat_name.cat_name.cat_name', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    like_count = serializers.SerializerMethodField()
    dislike_count = serializers.SerializerMethodField()

    class Meta:
        model = sms
        fields = ('id', 'cat_name', 'sub_cat_name', 'sms', 'user_name', 'status', 'like_count', 'dislike_count')

    def get_like_count(self, obj):
        return obj.likes.count()

    def get_dislike_count(self, obj):
        return obj.dislikes.count()

   
 
 

# # Complant BOX 
# from .models import Complaint

# class ComplaintSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Complaint
#         fields = ('sms', 'user', 'complaint_text')
#         read_only_fields = ('user',)  # user should be set in view

#     def validate(self, attrs):
#         # Check if the user has already made a complaint for this SMS
#         user = self.context['request'].user
#         if Complaint.objects.filter(sms=attrs['sms'], user=user).exists():
#             raise serializers.ValidationError('You have already complained about this SMS.')
        
#         # Check if the user has reached the complaint limit for this SMS
#         num_complaints = Complaint.objects.filter(sms=attrs['sms'], user=user).count()
        
#         return attrs

#     def create(self, validated_data):
#         user = self.context['request'].user
#         validated_data['user'] = user
#         complaint = Complaint.objects.create(**validated_data)
#         return complaint


# Complant BOX 
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
        
        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['user'] = user
        complaint = Complaint.objects.create(**validated_data)
        return complaint

