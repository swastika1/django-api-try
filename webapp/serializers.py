from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class EmployeeSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    
    class Meta:

        model = Employee
        fields = ('name', 'user', 'phone')



class EmployeeCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employee
        fields = ['name','phone','nationality']  


    def validate(self, data):
        if len(data.get('phone'))> 10:
            raise serializers.ValidationError("Phone number should be less than 10 digit")
        return data


class NationalitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Nationality
        fields = ['id','name']

class EmployeeTokenMatchSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False)
    password = serializers.CharField(allow_blank=False)

    def validate(self, data):
        username = data.get('username')
        print(username,1111111111)
        password = data.get('password')
        print(password)
        # print(secret_key,1111111111)
        # user = User.objects.filter(
        # Q(username=username) &
        # Q(password=password)
        # ).distinct()
        user = authenticate(username=username, password=password)
        if not user:
            raise serializers.ValidationError({'status': 'This Username or Key is not Valid'})
        return data

class UserSerializers(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()

        return user

    class Meta:
        model = User
        fields = ("username", "password")


class BlogSerialiizer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields =['name' , 'tagline']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields =['name', 'email']
      


class EntryManySerializer(serializers.ModelSerializer):

    class Meta:
        model = Entry
        fields =['blog', 'headline', 'body_text']


class UserSignUpSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields=['username', 'password1', 'password2']

    def validate(self, data):
        # password1 = self.validated_data.get('password1')
        # password2 = self.validated_data.get('password2')
        print(data)
        password1 = data.get('password1')
        password2 = data.get('password2')
        print(password1, password2)
        if not password2:
            raise serializers.ValidationError({"password2":"You must confirm your password"})
        if password1 != password2:
            print("asdf")
            raise serializers.ValidationError({"password2":"Your passwords do not match"})

        return data


class EmployeeSignUpSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    phone = serializers.CharField()
    nationality = serializers.IntegerField()
    password1 = serializers.CharField()
    password2 = serializers.CharField()

    class Meta:
        model = User
        fields=['username','password1', 'password2','name', 'phone', 'nationality']

        def validate_password2(self, password2):
            password1 = data.get('password1')
            password2 = data.get('password2')
            if not password2:
                raise serializers.ValidationError("you must confirm yur password")
            if password1!=password2:
                raise serializers.ValidationError("your password donot match")

            return password2


class UserTokenMatchSerializer(serializers.Serializer):
    username = serializers.CharField(allow_blank=False)
    secret_key = serializers.CharField(allow_blank=False)

    # class Meta:
    #     model = UserKey
    #     fields = ['user', 'secret_key','username']


    def validate(self, data):
        user_obj = None
        username = data.get('username', None)
        secret_key = data.get('secret_key')
        user = UserKey.objects.filter(
            Q(user__username=username) &
            Q(secret_key=secret_key)
        ).distinct()
        print(user,111111111)
        if user.exists() and user.count() == 1:
            user_obj = user.first()
        else:
            raise ValidationError({'status': 'This Username or Key is not Valid'})
        return data


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields =['is_bokmarked', 'blog', 'user']



