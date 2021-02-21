from django.conf.urls import url
from . import views
from django.urls import path, re_path
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView, PasswordResetView, \
    PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from .views import SignUpView
from rest_framework.urlpatterns import format_suffix_patterns

app_name = 'portfolio'
urlpatterns = [

    path('', views.home, name='home'),
    path('password-change/',
         PasswordChangeView.as_view(template_name='registration/password-change.html'),
         name='password-change'),
    path('password_change/done/',
         PasswordChangeDoneView.as_view(template_name='registration/password-change-success.html'),
         name='password-change-success'),
    re_path(r'^password_reset/$',
            PasswordResetView.as_view(template_name='registration/password_reset.html'),
            name='password_reset'),
    re_path(r'^password_reset/done/$',
            PasswordResetDoneView.as_view(template_name='registration/password_reset_done.html'),
            name='password_reset_done'),
    re_path(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
            PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirmation.html'),
            name='password_reset_confirmation'),
    re_path(r'^password/reset/complete/$',
            PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
            name='password_reset_complete'),
    url(r'^home/$', views.home, name='home'),
    url(r'^accounts/login/$', views.login, name='login'),
    url(r'^accounts/logout/$', views.logout, name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('customer_list', views.customer_list, name='customer_list'),
    path('customer/create/', views.customer_new, name='customer_new'),
    path('customer/<int:pk>/edit/', views.customer_edit, name='customer_edit'),
    path('customer/<int:pk>/delete/', views.customer_delete, name='customer_delete'),
    path('stock_list', views.stock_list, name='stock_list'),
    path('stock/create/', views.stock_new, name='stock_new'),
    path('stock/<int:pk>/edit/', views.stock_edit, name='stock_edit'),
    path('stock/<int:pk>/delete/', views.stock_delete, name='stock_delete'),
    path('investment_list', views.investment_list, name='investment_list'),
    path('investment/create/', views.investment_new, name='investment_new'),
    path('investment/<int:pk>/edit/', views.investment_edit, name='investment_edit'),
    path('investment/<int:pk>/delete/', views.investment_delete, name='investment_delete'),
    path('customer/<int:pk>/portfolio/', views.portfolio, name='portfolio'),
    path('mutual_fund_list', views.mutual_fund_list, name='mutual_fund_list'),
    path('mutual_fund/<int:pk>/edit/', views.mutual_fund_edit, name='mutual_fund_edit'),
    path('mutual_fund/<int:pk>/delete/', views.mutual_fund_delete, name='mutual_fund_delete'),
    path('mutual_fund/create/', views.mutual_fund_new, name='mutual_fund_new'),
    url(r'^customers_json/', views.CustomerList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
