from django.contrib import admin
from .models import LikeRecord, LikeCount

# Register your models here.

@admin.register(LikeRecord) # 注册
class LikeRecordAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object','user')

@admin.register(LikeCount) # 注册
class LikeCountAdmin(admin.ModelAdmin):
    list_display = ('id', 'content_object', 'liked_num')