from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField('昵称', max_length=50, blank=True, default='')
    phone = models.CharField('手机号', max_length=20, blank=True, null=True, unique=True)
    avatar = models.URLField('头像', blank=True, default='')
    status = models.BooleanField('启用状态', default=True)
    department = models.ForeignKey(
        'system.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users',
        verbose_name='部门',
    )
    roles = models.ManyToManyField(
        'system.Role',
        blank=True,
        related_name='users',
        verbose_name='角色',
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'sys_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name
        ordering = ['-id']

    def __str__(self):
        return self.username
