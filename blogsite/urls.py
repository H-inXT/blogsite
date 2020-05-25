"""blogsite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
# 从外层  向里导入一般
from django.conf import settings
from django.conf.urls.static import static

# from blog.views import blog_list
from . import views

urlpatterns = [
    # path('', blog_list, name='home'),
    path ('', views.home, name='home'),
    path('admin/', admin.site.urls),
    path('ckeditor', include('ckeditor_uploader.urls')),
    path('blog/', include('blog.urls')),
    path('comment', include('comment.urls')),
    path('likes', include('likes.urls')),
    path('user', include('user.urls')),
]

# 设置一个路径指向到哪个位置
# urlpatterns += static('/media/', document_root=settings.MEDOA_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)