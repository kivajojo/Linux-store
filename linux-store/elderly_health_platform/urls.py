from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.views import LogoutView, LoginView
from health_records import views as health_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('health_records.urls')),
    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        redirect_field_name='next',
      
    ), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('record/<int:elderly_id>/<int:record_id>/', health_views.record_detail, name='record_detail'),
]
