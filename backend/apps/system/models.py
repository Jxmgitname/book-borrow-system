from django.db import models


class Department(models.Model):
    name = models.CharField('部门名称', max_length=50)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='上级部门',
    )
    sort = models.IntegerField('排序', default=0)
    leader = models.CharField('负责人', max_length=50, blank=True, default='')
    phone = models.CharField('联系电话', max_length=20, blank=True, default='')
    status = models.BooleanField('启用状态', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'sys_department'
        verbose_name = '部门'
        verbose_name_plural = verbose_name
        ordering = ['sort', 'id']

    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField('角色名称', max_length=50)
    code = models.CharField('角色编码', max_length=50, unique=True)
    description = models.CharField('描述', max_length=200, blank=True, default='')
    status = models.BooleanField('启用状态', default=True)
    menus = models.ManyToManyField(
        'Menu',
        blank=True,
        related_name='roles',
        verbose_name='菜单权限',
    )
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'sys_role'
        verbose_name = '角色'
        verbose_name_plural = verbose_name
        ordering = ['id']

    def __str__(self):
        return self.name


class Menu(models.Model):
    MENU_TYPE_CHOICES = (
        ('catalog', '目录'),
        ('menu', '菜单'),
        ('button', '按钮'),
    )

    name = models.CharField('菜单名称', max_length=50)
    path = models.CharField('路由路径', max_length=200, blank=True, default='')
    component = models.CharField('组件路径', max_length=200, blank=True, default='')
    icon = models.CharField('图标', max_length=50, blank=True, default='')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='children',
        verbose_name='上级菜单',
    )
    menu_type = models.CharField('类型', max_length=20, choices=MENU_TYPE_CHOICES, default='menu')
    permission = models.CharField('权限标识', max_length=100, blank=True, default='')
    sort = models.IntegerField('排序', default=0)
    visible = models.BooleanField('是否显示', default=True)
    status = models.BooleanField('启用状态', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        db_table = 'sys_menu'
        verbose_name = '菜单'
        verbose_name_plural = verbose_name
        ordering = ['sort', 'id']

    def __str__(self):
        return self.name
