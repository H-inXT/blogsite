from django.contrib import admin
from .models import Comment

# Register your models here.

@admin.register(Comment) # 注册
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'text', 'comment_time', 'user')