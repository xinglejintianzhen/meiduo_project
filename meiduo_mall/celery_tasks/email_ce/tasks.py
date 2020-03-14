# 定义任务
from django.core.mail import send_mail
from django.conf import settings

from celery_tasks.main import celery_app

# 使用装饰器装饰任务保证celery识别任务,name参数的目的在于为任务命名,否则celery会自动命名特别长
@celery_app.task(bind=True, name='send_verify_email', retry_backoff=3)
def send_verify_email(self, to_email, verify_url):
    subject = "美多商城邮箱验证"
    html_message = '<p>尊敬的用户您好！</p>' \
                   '<p>感谢您使用美多商城。</p>' \
                   '<p>您的邮箱为：%s 。请点击此链接激活您的邮箱：</p>' \
                   '<p><a href="%s">%s<a></p>' % (to_email, verify_url, verify_url)
    try:
        send_mail(subject, "", settings.EMAIL_FROM, [to_email], html_message=html_message)
    except Exception as e:
        # 有异常自动重试三次
        raise self.retry(exc=e, max_retries=3)
