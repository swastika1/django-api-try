from django.contrib import admin
from django.conf.urls import url, include
from .views import *

app_name='webapp'

urlpatterns = [

	
	url(r'^$', Home.as_view(), name='home'),

    url(r'^user/list$', UserList.as_view(), name='userlist'),
    url(r'^user/create', UserCreateAPIView.as_view(), name='usercreate'),
    url(r'^user/update/(?P<pk>\d+)/$',
        UserUpdateAPIView.as_view(), name='userupdate'),
    url(r'^user/detail/(?P<username>\w+)/$',
        UserDetailAPIView.as_view(), name='userdetail'),
    url(r'^user/secret-key/$', UserTokenMatchAPIView.as_view(), name = 'secret_key'),

    url(r'^employee/list', EmployeeListAPIView.as_view(), name='employeelist'),
    url(r'^employee/create', EmployeeCreateAPIView.as_view(), name='employee_create'),
    url(r'^nationality', NationalityListAPIView.as_view(), name='nationality_list'),
    url(r'^user/login-key/$', EmployeeTokenMatchAPIView.as_view(), name='secret_key'),
    url(r'^create/user', UserCreateAPIView.as_view(), name='user_create'),
    # path('employee/', views.EmployeeList.as_view())


    url(r'^create/blog', BlogCreateAPIView.as_view(), name='blogcreate'),
    url(r'^list/blog', BlogListAPIView.as_view(), name='bloglist'),
    url(r'^update/(?P<pk>\d+)/blog', BlogUpdateAPIView.as_view(), name='blogupdate'),
    url(r'^delete/(?P<pk>\d+)/blog', BlogDeleteAPIView.as_view(), name='blogdelete'),

    url(r'^create/entry', EntryCreateAPIView.as_view(), name='entrycreate'),
    url(r'^list/entry', EntryListAPIView.as_view(), name='entrylist'), 
    url(r'^list/author', AuthorListAPIView.as_view(), name='authorlist'), 

    url(r'^signup/user', SignUp.as_view(), name='signup'),
    url(r'^signup/employee', EmployeeSignUp.as_view(), name='employeesignup'),
    url(r'^bookmark/blog/(?P<blog_id>\d+)/$', BookMarkView.as_view(), name='bookmark'),  


    url(r'^bookmark-template', BookmarkTemplateView.as_view(), name='bookmark_template'),
    url(r'^logout/', Logout.as_view(), name='logout'),

    url(r'^usertype/chart/$', UserTypeChart.as_view(), name='usertype'),

    url(r'^group/chart/$', GroupChart.as_view(), name='groupchart'),
]
