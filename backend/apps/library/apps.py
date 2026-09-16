from django.apps import AppConfig#从 Django 的 apps 模块里，拿出 AppConfig （应用配置）这个类

class LibraryConfig(AppConfig):#定义一个叫 LibraryConfig 的类，并继承 AppConfig
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'library'#定义一个叫 name 的属性，值为 'library'， app 的内部名字，必须等于文件夹名 library
    verbose_name = '图书馆借阅管理'
