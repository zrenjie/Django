from django.conf.urls import url
from . import views
import django.contrib.auth.views as auth_views

app_name = 'collector'
urlpatterns = [
    url('create/', views.ImageRecordCreateView.as_view(), name='create_record'),
    url(r'(?P<pk>\d+)/update', views.ImageRecordUpdateView.as_view(), name='update_record'),
    url(r'login/', auth_views.LoginView.as_view(template_name='collector/login.html'), name='login'),
    url(r'logout/$', auth_views.LogoutView.as_view(), name="logout"),
    url('', views.ImageRecordListView.as_view(), name='home'),
    
]
