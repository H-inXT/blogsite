from django.db import models
from django.db.models.fields import exceptions
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
 #         .工具
from django.utils import timezone


# Create your models here.

class ReadNum(models.Model): # 计数方法三
    read_num = models.IntegerField(default=0)

    # 此段信息可在官网查到-contenttypes
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

class ReadNumExpandMethod():
    def get_read_num(self):
        try:
            ct = ContentType.objects.get_for_model(self)# 获取到博客类， 这个是ContentType的一个方法
            readnum = ReadNum.objects.get(content_type=ct, object_id=self.pk)
            return readnum.read_num
        except exceptions.ObjectDoesNotExist:
            return 0       
        return readnum.read_num


class ReadDetail(models.Model):
    date = models.DateField(default=timezone.now) # 
    read_num = models.IntegerField(default=0)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id') # 通用的外键 可以访问到相应的模型
    pass
