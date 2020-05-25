from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.http import JsonResponse
from .models import Comment
from .forms import CommentForm

# Create your views here.

def update_comment(request):
    '''
    referer = request.META.get('HTTP_REFERER', reverse('home'))

    # 数据检查
    if not request.user.is_authenticated:
        return render(request, 'error.html', {'message':'请登入用户', 'redirect_to': referer})

    text = request.POST.get('text', '').strip() # strip()会把前后多余的空格去掉
    if text == '':
        return render(request, 'error.html', {'message':'评论内容为空', 'redirect_to': referer})

    try:
        content_type = request.POST.get('content_type', '')
        object_id = int(request.POST.get('object_id', ''))
        model_class = ContentType.objects.get(model=content_type).model_class()
        model_obj = model_class.objects.get(pk=object_id) # Blog.objects.get(pk=object_id)
    except Exception as e:
        return render(request, 'error.html', {'message':'评论对象不存在', 'redirect_to': referer})

        # 检查通过，保存数据
    comment = Comment()
    comment.user = user
    comment.text = text
    comment.content_object = model_obj
    comment.save()
    return redirect(referer)
    '''

    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}

    if comment_form.is_valid():
        # 检查通过，保存数据
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']

        parent = comment_form.cleaned_data['parent']
        if not parent is None:
            comment.root = parent.root if not parent.root is None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        # return redirect(referer) #非异步请求


        # 发送邮件通知
        # comment.send_mail()
        # if comment.parent is None:
        #     # 评论我的博客 
        #     subject = '有人评论你的博客'
        #     # text = comment.text + reverse('blog_detail', args=[comment.content_object.pk])
        #     # text = comment.text + '\n' + reverse('blog_detail', kwargs={'blog_pk': comment.content_object.pk})
        #     # text = comment.text + '\n' + comment.content_object.get_url()
        #     email = comment.content_object.get_email()

        # else:
        #     # 回复评论
        #     subject = '有人回复了你的评论'
        #     email = comment.reply_to.email

        # if email != '':
        #     text = comment.text + '\n' + comment.content_object.get_url()
        #     send_mail(subject, text, settings.EMAIL_HOST_USER, [email], fail_silently=False)
        

        # 返回数据
        data['status'] = 'SUCCESS'
        # data['username'] = comment.user.username
        data['username'] = comment.user.get_nickname_or_username()
        # data['comment_time'] = comment.comment_time.strftime('%Y-%m-%d %H:%M:%S')
        data['comment_time'] = comment.comment_time.timestamp()
        data['text'] = comment.text
        data['content_type'] = ContentType.objects.get_for_model(Comment).model

        if not parent is None:
            # data['reply_to'] = comment.reply_to.username
            data['reply_to'] = comment.reply_to.get_nickname_or_username()
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if not comment.root is None else ''
    else:
        # return render(request, 'error.html', {'message':comment_form.errors, 'redirect_to': referer})
        data['status'] = 'ERROR'
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)