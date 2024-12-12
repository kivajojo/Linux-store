from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Elderly, HealthRecord

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'phone', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('个人信息', {'fields': ('email', 'phone')}),
        ('权限', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('重要日期', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'phone'),
        }),
    )
    search_fields = ('username', 'email', 'phone')
    ordering = ('username',)

class ElderlyAdmin(admin.ModelAdmin):
    list_display = ('name', 'gender', 'birth_date', 'phone', 'emergency_contact')
    list_filter = ('gender',)
    search_fields = ('name', 'phone', 'emergency_contact')
    date_hierarchy = 'created_at'

class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('elderly', 'date', 'blood_pressure', 'heart_rate', 'blood_sugar', 'weight')
    list_filter = ('date', 'elderly')
    search_fields = ('elderly__name',)
    date_hierarchy = 'date'

admin.site.register(User, CustomUserAdmin)
admin.site.register(Elderly, ElderlyAdmin)
admin.site.register(HealthRecord, HealthRecordAdmin)

# 自定义管理站点
admin.site.site_header = '老年人健康档案平台'
admin.site.site_title = '健康档案管理'
admin.site.index_title = '管理面板'
