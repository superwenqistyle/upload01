from django.db import models
# Django里面的用户表
from django.contrib.auth.models import AbstractUser


# Create your models here.

class BlogUser(AbstractUser):
    nickname = models.CharField(max_length=20, verbose_name='昵称', default='')


class EmailVerifyRecord(models.Model):
    code = models.CharField(verbose_name='邮箱验证码', max_length=50, default='')
    email = models.EmailField(max_length=50, verbose_name='邮箱')
    send_type = models.CharField(max_length=200, verbose_name='验证码类型',
                                 choices=(('forget', '找回密码'), ('register', '注册'), ('update_email', '修改邮箱')))
    send_time = models.DateTimeField(auto_now_add=True, verbose_name='发送时间')

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return '{}--{}'.format(self.code, self.email)
