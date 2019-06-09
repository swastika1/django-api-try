from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
# from rest_framework.decorators import APIView
from rest_framework.response import Response
from .models import *
from .serializers import *
from rest_framework.generics import *
from rest_framework.views import APIView
from django.http import JsonResponse
from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from braces.views import (LoginRequiredMixin, GroupRequiredMixin, SuperuserRequiredMixin)
from rest_framework import permissions, exceptions
from rest_framework import pagination
from django.utils.crypto import get_random_string
from django.views.generic import TemplateView
# Create your views here.
class ExamplePagination(pagination.PageNumberPagination):
    page_size = 2


# class EmployeeList(APIView):
#     def get(self, request):
#         employee1 = Employee.objects.all()
#         serializer = EmployeeSerializer(employee1, many=True)
#         return Response(serializer.data)

#     def post():
#         pass
class UserPermission(permissions.BasePermission):
    message = 'Adding customers not allowed.'

    def has_permission(self, request, view):
        print(request.user.groups.first().name,11111111)
        _permissions = [group.name for group in request.user.groups.all() ]

        if 'special' in _permissions and 'normal' in _permissions:
            print('asdfasdfa')
            return 'ok'
        raise exceptions.PermissionDenied()
        # if not (request.user.groups.first().name =="special" ):
        #     raise exceptions.PermissionDenied()
        # return "ok"

class EmployeePermission(permissions.BasePermission):
    message ='you donot have access'

    def has_permission(self, request, view):
        if request.user.groups.first().name =="employee":
            return 'ok'
        raise exceptions.PermissionDenied()

# class SpecialRequiredMixin(GroupRequiredMixin):
#     group_required =  ['special']


class UserList(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    # def get_queryset(self, *args, **kwargs):
    #     return User.objects.filter(username=self.request.user.username)


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserUpdateAPIView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetailAPIView(RetrieveAPIView):
    lookup_field ="username"
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[AllowAny]



class EmployeeListAPIView(ListAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    pagination_class=ExamplePagination
    permission_classes=[AllowAny]

    # def get(self, request, *args, **kwargs):
    #   employer = Employee.objects.all()
    #   toRet = []
    #   for emp in employer:
    #       toAdd = {}
    #       toAdd['name'] = emp.name
    #       toAdd['phone'] = emp.phone
    #       toAdd['user'] = {
    #           'username': emp.user.username
    #       }
    #       toRet.append(toAdd)
    #   return Response(toRet)


class EmployeeCreateAPIView(CreateAPIView):
    serializer_class = EmployeeCreateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        user = User.objects.get(username='rita')
        serializer.save(user=user)


class NationalityListAPIView(ListAPIView):
    serializer_class = NationalitySerializer
    queryset = Nationality.objects.all()


class EmployeeTokenMatchAPIView(APIView):
    serializer_class = EmployeeTokenMatchSerializer
    # permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # return HttpResponse('a')
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.filter(username=username).first()

        if user:
            token, created = Token.objects.get_or_create(user=user)
            print(token)
            print(created)
            return Response({
                'token': token.key,
                'user_id': user.pk,
                'username': user.username,
            })
        return Response({
            'status': 'Username or Key is not Valid'
        })


class CreateUserAPIView(CreateAPIView):
    model = User
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class BlogListAPIView(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerialiizer
    permission_classes = [AllowAny]


class BlogCreateAPIView(CreateAPIView):
    serializer_class = BlogSerialiizer
    permission_classes = [IsAuthenticated]


class BlogUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = BlogSerialiizer
    queryset = Blog.objects.all()


class BlogDeleteAPIView(DestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerialiizer

class AuthorListAPIView(ListAPIView):
    queryset = Author.objects.all()

    def get(self, request, *args, **kwargs):
        authors = Author.objects.all()
        toList=[]
        for author in authors:
            toAdd={}
            toAdd['name']= author.name
            toAdd['email'] = author.email
            toList.append(toAdd)
        return Response(toList)


class EntryCreateAPIView(CreateAPIView):
    serializer_class= EntryManySerializer

class EntryListAPIView(ListAPIView):
    serializer_class = EntryManySerializer
    queryset = Entry.objects.all()


class SignUp(APIView):
    serializer_class = UserSignUpSerializer
    permission_classes= [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserSignUpSerializer(data = request.data)
        print(serializer)
        if serializer.is_valid():
            # user = User()
            username = serializer.validated_data.get('username')
            password =serializer.validated_data.get('password1')
            user = User.objects.create(username=username)

            user.set_password(password)
            key = UserKey.objects.create(user=user, secret_key=get_random_string(64))
            key.save()

            # user.set_password(password)
            user.save()
            group =Group.objects.get(name="normal")
            user.groups.add(group)
            return Response(serializer.data, status=200)
        return Response(serializer.errors)


        # if serializer.is_valid():
        #     print(serializer.data)
        #     return Response(serializer.data, status=200)
        # return Response(serializer.errors)


class EmployeeSignUp(APIView):
    permission_classes=[AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = EmployeeSignUpSerializer(data= request.data)
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            phone = serializer.validated_data.get('phone')
            nationality = serializer.validated_data.get('nationality')

            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password1')
            user = User.objects.create(username=username)
            user.set_password(password)
            
            employee = Employee.objects.create(name=name, nationality_id=nationality, phone=phone)
            employee.save()
            user.save()
            group =Group.objects.get(name="employee")
            user.groups.add(group)
            return Response(serializer.data, status=200)
        return Response(serializer.errors)



class UserTokenMatchAPIView(APIView):
    serializer_class = UserTokenMatchSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # return HttpResponse('a')
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        user = User.objects.filter(username=username).first() 

        if user:
            secret_key, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': secret_key.key,
                'user_id': user.pk, 
                'username':user.username,  
            })
        return Response({
                'status': 'Username or Key is not Valid'
            })



class BookMarkView(APIView):
    serializer_class = BookmarkSerializer
    permission_classes = [AllowAny]

    def get(self, request, **kwargs):
        userId=self.request.user.id
        blogObj = Blog.objects.get(id = self.kwargs.get('blog_id'))

        # Bookmark.objects.create(user_id = userId, blog = blogObj, is_bookmarked=True)
        bookmark, created = Bookmark.objects.get_or_create(user_id=userId, blog=blogObj)
        if bookmark.is_bookmarked:
            bookmark.is_bookmarked = False
            bookmark.save()
            return Response({'bookmarked':False})
        else:
            bookmark.is_bookmarked=True
            bookmark.save()
            return Response({'bookmarked':True})


class BookmarkTemplateView(TemplateView):
    template_name = 'bookmark/index.html'
        










    