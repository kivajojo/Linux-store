from django.urls import path
from . import views

app_name = 'health_records'

urlpatterns = [
    # 基础路由和老人管理
    path('', views.elderly_list, name='elderly_list'),
    path('elderly/create/', views.elderly_create, name='elderly_create'),
    path('elderly/<int:elderly_id>/', views.elderly_detail, name='elderly_detail'),
    path('elderly/<int:elderly_id>/update/', views.elderly_update, name='elderly_update'),
    
    # 健康记录管理
    path('elderly/<int:elderly_id>/record/create/', views.record_create, name='record_create'),
    path('record/<int:record_id>/', views.record_detail, name='record_detail'),
    path('record/<int:record_id>/update/', views.record_update, name='record_update'),
    
    # 健康记录扩展功能
    path('record/<int:record_id>/update-recommendation/', 
         views.update_recommendation, 
         name='update_recommendation'),
    path('elderly/<int:elderly_id>/analysis/', 
         views.health_analysis, 
         name='health_analysis'),
    path('elderly/<int:elderly_id>/record/<int:record_id>/delete/',
         views.delete_record,
         name='delete_record'),
    path('elderly/<int:elderly_id>/record/<int:record_id>/update/',
         views.record_update,
         name='record_update'),
    path('elderly/<int:elderly_id>/record/<int:record_id>/', 
         views.record_detail, 
         name='record_detail'),
]
