from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
    """管理员用户模型"""
    phone = models.CharField('联系电话', max_length=20, blank=True)
    
    class Meta:
        verbose_name = '管理员'
        verbose_name_plural = verbose_name

class Elderly(models.Model):
    """老年人信息模型"""
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    
    name = models.CharField('姓名', max_length=50)
    gender = models.CharField('性别', max_length=1, choices=GENDER_CHOICES)
    birth_date = models.DateField('出生日期')
    phone = models.CharField('联系电话', max_length=20, blank=True)
    address = models.CharField('居住地址', max_length=200, blank=True)
    medical_history = models.TextField('既往病史', blank=True)
    emergency_contact = models.CharField('紧急联系人', max_length=50)
    emergency_phone = models.CharField('紧急联系电话', max_length=20)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='创建者',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '老年人信息'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.name

class HealthRecord(models.Model):
    """健康记录模型"""
    elderly = models.ForeignKey(
        Elderly,
        on_delete=models.CASCADE,
        verbose_name='老年人',
        null=True,
        blank=True
    )
    date = models.DateField('记录日期')
    blood_pressure = models.CharField('血压', max_length=20)
    heart_rate = models.IntegerField('心率')
    blood_sugar = models.DecimalField('血糖', max_digits=5, decimal_places=2)
    weight = models.DecimalField('体重', max_digits=5, decimal_places=2)
    
    # 活动记录
    activity_type = models.CharField('活动类型', max_length=50, blank=True)
    activity_duration = models.IntegerField('活动时长(分钟)', null=True, blank=True)
    activity_level = models.CharField('活动强度', max_length=20, blank=True)
    sleep_hours = models.DecimalField('睡眠时长', max_digits=4, decimal_places=1, null=True, blank=True)
    
    # 饮食记录
    breakfast = models.CharField('早餐', max_length=200, blank=True)
    lunch = models.CharField('午餐', max_length=200, blank=True)
    dinner = models.CharField('晚餐', max_length=200, blank=True)
    water_intake = models.DecimalField('饮水量(升)', max_digits=3, decimal_places=1, null=True, blank=True)
    
    # 个性化建议
    recommendation = models.TextField('个性化建议', blank=True, null=True)
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='记录者',
        null=True,
        blank=True
    )
    created_at = models.DateTimeField('创建时间', default=timezone.now)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '健康记录'
        verbose_name_plural = verbose_name
        ordering = ['-date']

    def __str__(self):
        return f"{self.elderly.name} - {self.date}"

class MedicalHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    condition = models.CharField('病症', max_length=200)
    diagnosis_date = models.DateField('诊断日期')
    treatment = models.TextField('治疗方案')

    class Meta:
        verbose_name = '病史记录'
        verbose_name_plural = verbose_name

class HealthRecommendation(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='用户'
    )
    date = models.DateField('日期', auto_now_add=True)
    recommendation = models.TextField('建议')
    risk_level = models.CharField('风险等级', max_length=20)

    class Meta:
        verbose_name = '健康建议'
        verbose_name_plural = verbose_name