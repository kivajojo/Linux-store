from django.core.mail import send_mail
from django.conf import settings

class NotificationService:
    @staticmethod
    def send_health_alert(user, message):
        """发送健康警告"""
        subject = '健康状况提醒'
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
    
    @staticmethod
    def create_notification(user, message, level='info'):
        """创建系统内部通知"""
        return Notification.objects.create(
            user=user,
            message=message,
            level=level
        )