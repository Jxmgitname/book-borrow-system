from django.contrib import admin
from django.urls import include, path#从 Django 的 urls 模块里，拿出 include 和 path 这两个函数。include （把某个 app 的路由接进来）。，path （定义一条网址是用来定义 URL 路径的）

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('system.urls')),
    path('api/', include('library.urls')),#访问以 /api/ 开头的地址时，转到 library/urls.py 里继续匹配
]
