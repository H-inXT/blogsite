from django.db import models
from django.contrib.auth.models import User

# from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from read_statistics.models import ReadNumExpandMethod, ReadDetail
from django.contrib.contenttypes.fields import GenericRelation
from django.urls import reverse
# Create your models here.


        

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name


class Blog(models.Model, ReadNumExpandMethod): # 如果之前有定义的字段，但是现在不需要 在数据迁移的时候会自动删除
    title = models.CharField(max_length=50)
    # blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, relate_name='blog_blog') # 最后的参数是对这个字段的外键的重命名
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE)
    # content = models.TextField() # 之前 普通文本
    # content = RichTextField() # 富文本 但不允许上传文件
    content = RichTextUploadingField()
    author = models.ForeignKey(User,  on_delete=models.CASCADE) # 删除外键的时候不影响blog本身
    read_details = GenericRelation(ReadDetail)
    # readed_num = models.IntegerField(default=0) # 计数方法一
    created_time = models.DateTimeField(auto_now_add=True)
    last_updated_time = models.DateTimeField(auto_now=True)

    '''
    def get_read_num(self): # 方法二
        try:
            return self.readnum.read_num
        # except Exception as e:
        except exceptions.ObjectDoesNotExist:
            # 返回0篇博客
            return 0
    '''
    

    def get_url(self):
        return comment.text + '\n' + reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_email(self):
        return self.author.email

    def __str__(self):
        return "<Blog: %s>" % self.title



    class Meta:
        ordering = ['-created_time'] # '-'号是倒叙

'''
class ReadNum(models.Model): # 计数方法二
    read_num = models.IntegerField(default=0)
    # blog = models.ForeignKey(blog, on_delete=DO_NOTHING)
    blog = models.OneToOneField(Blog, on_delete=models.CASCADE)
'''