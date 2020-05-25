import threading
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# 引用站点的User模型
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

# Create your models here.

class SendMail(threading.Thread):
    def __int__(self, subject, text, email, fail_silently=False):
        self.subject = subject
        self.text = text
        self.email = email
        self.fail_silently = fail_silently
        threading.Thread.__int__(self)
    def run(self):
        seng_mail(
            self.subject, 
            '', 
            self.settings.EMAIL_HOST_USER, 
            [self.email], 
            fail_silently=self.fail_silently,
            html_message=self.text
        )

class Comment(models.Model):
    # 评论对象 可关联任意对象 通过ContentType和GenericForeignKey(关联外键)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    text = models.TextField()
    comment_time = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, related_name="comments", on_delete=models.CASCADE)

    # 回复的顶级目录最根的
    root = models.ForeignKey('self', related_name="root_comment", null=True, on_delete=models.CASCADE)
    # parent_id = models.IntegerField(default=0)
    parent = models.ForeignKey('self', related_name="parent_comment", null=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(User, related_name="replies", null=True, on_delete=models.CASCADE)

    def send_mail(self):
        if comment.parent is None:
            # 评论我的博客 
            subject = '有人评论你的博客'
            email = comment.content_object.get_email()
        else:
            # 回复评论
            subject = '有人回复了你的评论'
            email = comment.reply_to.email
        if email != '':
            # text = ' %s\n<a href="%s">%s</a>' %(comment.text, comment.content_object.get_url(), '点击查看')
            context = {}
            context['comment_text'] = comment.text
            context['url'] = comment.content_object.get_url()
            text = render_to_string('comment/send_mail.html', context)
            send_mail = SendMail(subject, text, email)
            # send_mail = SendMail(subject, text, email)
            send_mail.start()

    def __str__(self):
        return self.text

    class Meta():
        ordering = ['comment_time']