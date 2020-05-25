from django.shortcuts import get_object_or_404, render
# from django.shortcuts import render_to_response, get_object_or_404
from .models import Blog, BlogType
# , ReadNum
from django.conf import settings
from django.db.models import Count
from django.contrib.contenttypes.models import ContentType
from django.core.paginator import Paginator
from read_statistics.utils import read_statistics_once_read
from comment.models import Comment
from comment.forms import CommentForm
# from user.forms import LoginForm

# from datetime import datetime

# Create your views here.
# 

# each_pageblogs_number = 2

def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 每each_pageblogs_number篇进行分页
    page_num = request.GET.get('page', 1)# 获取页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number# 获取当前页码
    # 获取当前页码前后各两页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))# 后面的是+2+1取开区间的最大值
    # 加上省略页码标记
    if page_range[0] - 1 >=2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页的按钮页数
    if page_range[0] != 1:
        page_range.insert(0, 1)# 将1插入到【0】
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    # 获取博客分类的对应博客数量
    # BlogType.objects.aannotate(Count('blog_blog')) # 拓展查询字段
    # BlogType.objects.annotate(blog_count=Count('blog')) # 可以查询一下annotate函数的作用
    '''
    blog_types = BlogType.objects.all()
    blog_types_list = []
    for blog_type in blog_types: # blog_type 是一个实例化的对象 blog_types是集合
        blog_type.blog_count = Blog.objects.filter(blog_type=blog_type).count()
        blog_types_list.append(blog_type) # 将三个分类的数量存储到列表里(暂时不对，仅参考)
    '''
    # 获取日期归档对应的博客数量
    # 第二种方法
    # blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")\
    #                     .annotate(lbog_count=Count('created_time'))
    # blog_dates_dict = {}
    # for blog_date in blog_dates[::2]:


    # 第一种方法
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year, 
                                        created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    # 
    # 
    context = {}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    # context['blog_types'] = BlogType.objects.all()
    # context['blog_types'] = blog_types_list
    # 直接操作数据库 真正使用前不会占用内存 而上一种方法则是在内存中进行
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog')) 
    context['page_range'] = page_range
    # context['blog_dates'] = Blog.objects.dates('created_time', 'month', order = 'DESC')
    context['blog_dates'] = blog_dates_dict
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog/blog_list.html', context)

def blog_list_beifen(request):
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 每each_pageblogs_number篇进行分页
    page_num = request.GET.get('page', 1)# 获取页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number# 获取当前页码
    # 获取当前页码前后各两页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))# 后面的是+2+1取开区间的最大值
                # [currentr_page_num, currentr_page_num + 1, currentr_page_num + 2 ]
    # list(range(min(currentr_page_num + 2, page_of_blogs.number), currentr_page_num + 1))
    # 
    # 加上省略页码标记
    if page_range[0] - 1 >=2:
        page_range.insert(0, '...')
    # if page_range[-1] + 1< paginator.num_pages:
    # if page_range[-1] <= paginator.num_pages -2:
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页的按钮页数
    if page_range[0] != 1:
        page_range.insert(0, 1)# 将1插入到【0】
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    #两种方法都可以
    # context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    # context['blogs'] = Blog.objects.all() # 二
    context['blog_types'] = BlogType.objects.all()
    # content['blogs_count'] = Blog.objects.all().count() # 统计博客数量
    # blogs = Blog.objects.all() # 一
    context['page_range'] = page_range
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order = 'DESC') # 最后一个是倒叙
    
    # return render_to_response('blog_list.html', context) #3.0应该是不支持
    # return render(request, 'blog_list.html', {'blogs':blogs}) #一
    return render(request, 'blog/blog_list.html', context) # 二

def blog_detail(request, blog_pk):
    # 计数
    blog = get_object_or_404(Blog, pk=blog_pk)
    read_cookie_key = read_statistics_once_read(request, blog)
    # 去掉的原因一样
    # blog_content_type = ContentType.objects.get_for_model(blog)
    # comments = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk, parent=None)
    # 判断书否有缓存
    '''
    if not request.COOKIES.get('blog_%s_readed' % blog_pk):
        # blog.readed_num += 1
        # blog.save()
        
        ct = ContentType.objects.get_for_model(Blog)

        if ReadNum.objects.filter(content_type=ct, object_id=blog.pk).count():
            # 存在对应的记录
            readnum = ReadNum.objects.get(content_type=ct, object_id=blog.pk)
        else:
            # 不存在对应的记录
            readnum = ReadNum(content_type=ct, object_id=blog.pk)

        # 计数加1并保存
        readnum.read_num += 1
        readnum.save()
        '''

        
    context = {}
    # blog = get_object_or_404(Blog, pk=blog_pk)
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first
    context['blog'] = blog
    # context['login_form'] = LoginForm() # 公用了
    # context['comment_count'] = Comment.objects.filter(content_type=blog_content_type, object_id=blog.pk).count()
    # 应为模板包去掉
    # context['comments'] = comments.order_by('-comment_time')
    # date = {}
    # data['content_typs'] = blog_content_type.model
    # data['object_id'] = blog_pk
    # context['comment_form'] = CommentForm(initial=data)
    # 因为引用模板包重复定义所以将此注释
    # context['comment_form'] = CommentForm(initial={'content_type':blog_content_type.model, 'object_id':blog_pk, 'reply_comment_id': 0})
    response = render(request, 'blog/blog_detail.html', context) # 响应
    # 阅读cookie的标记
    response.set_cookie(read_cookie_key, 'true') # 默认的清除cookie的时候是关闭浏览器的时候
    # response.set_cookie('blog_%s_readed' % blog_pk, 'true', max_age=60)
    return response


def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blog_type_pk)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blog_type
    # context['blogs'] = page_of_blogs.object_list
    return render(request, 'blog/blogs_with_type.html', context)

def blogs_with_type_bieben(request,blog_type_pk):
    # context = {}
    blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    # context['blog_type'] = blog_type
    # context['blogs'] = Blog.objects.filter(blog_type=blog_type_pk)
    # context['blog_types'] = BlogType.objects.all()

    blogs_all_list = Blog.objects.filter(blog_type=blog_type_pk)
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 每each_pageblogs_number篇进行分页
    page_num = request.GET.get('page', 1)# 获取页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number# 获取当前页码
    # 获取当前页码前后各两页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))# 后面的是+2+1取开区间的最大值
                # [currentr_page_num, currentr_page_num + 1, currentr_page_num + 2 ]
    # list(range(min(currentr_page_num + 2, page_of_blogs.number), currentr_page_num + 1))
    # 
    # 加上省略页码标记
    if page_range[0] - 1 >=2:
        page_range.insert(0, '...')
    # if page_range[-1] + 1< paginator.num_pages:
    # if page_range[-1] <= paginator.num_pages -2:
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页的按钮页数
    if page_range[0] != 1:
        page_range.insert(0, 1)# 将1插入到【0】
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)


    context = {}
    # blog_type = get_object_or_404(BlogType, pk=blog_type_pk)
    context['blog_type'] = blog_type
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order = 'DESC')
    return render(request, 'blog/blogs_with_type.html', context)


def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' %(year, month)
    # context['blogs'] = page_of_blogs.object_list
    return render(request, 'blog/blogs_with_date.html', context)


def blogs_with_date_beifen(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    paginator = Paginator(blogs_all_list, settings.EACH_PAGE_BLOGS_NUMBER) # 每each_pageblogs_number篇进行分页
    page_num = request.GET.get('page', 1)# 获取页面参数（GET请求）
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number# 获取当前页码
    # 获取当前页码前后各两页的页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))# 后面的是+2+1取开区间的最大值
    # 加上省略页码标记
    if page_range[0] - 1 >=2:
        page_range.insert(0, '...')
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append('...')
    # 加上首页和尾页的按钮页数
    if page_range[0] != 1:
        page_range.insert(0, 1)# 将1插入到【0】
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)

    context = {}
    context['blogs_with_date'] = '%s年%s月' %(year, month)
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.all()
    context['blog_dates'] = Blog.objects.dates('created_time', 'month', order = 'DESC')
    return render(request, 'blog/blogs_with_date.html', context)






        
