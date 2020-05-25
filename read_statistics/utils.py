import datetime
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.db.models import Sum # 求和函数
from .models import ReadNum, ReadDetail

def read_statistics_once_read(request, obj):
    ct = ContentType.objects.get_for_model(obj)
    key = "%s_%s_read" %(ct.model, obj.pk)

    if not request.COOKIES.get(key):
        # if ReadNum.objects.filter(content_type=ct, object_id=obj.pk).count():
        #     # 存在对应的记录
        #     readnum = ReadNum.objects.get(content_type=ct, object_id=obj.pk)
        # else:
        #     # 不存在对应的记录
        #     readnum = ReadNum(content_type=ct, object_id=obj.pk)
        # 总阅读数+1   
        readnum, created = ReadNum.objects.get_or_create(content_type=ct, object_id=obj.pk)
        # 计数加1并保存
        readnum.read_num += 1
        readnum.save()


        # 当天阅读数 +1
        date = timezone.now().date()
        # if ReadDetail.objects.filter(content_type=ct, object_id=obj.pk, date=date).count():
        #     readDetail = ReadDetail.objects.get(content_type=ct, object_id=obj.pk, date=date)
        # else:
        #     # 实例化对象
        #     readDetail = ReadDetail(content_type=ct, object_id=obj.pk, date=date)
        #           判断是否创建 True或False
        readDetail, created = ReadDetail.objects.get_or_create(content_type=ct,object_id=obj.pk, date=date)
        readDetail.read_num +=1
        readDetail.save()
    return key

def get_seven_days_read_data(content_type):
    today = timezone.now().date()
    #                时间差量
    # today - datetime.timedelta(days=1)
    read_nums = []
    dates = []
    for i in range(7, 0, -1):
        date = today - datetime.timedelta(days=i)
        # 要将日期型转换成字符串
        dates.append(date.strftime('%m/%d'))
        read_details = ReadDetail.objects.filter(content_type=content_type, date=date)
        #           聚合
        result = read_details.aggregate(read_num_sum=Sum('read_num'))
        read_nums.append(result['read_num_sum'] or 0)
    return read_nums, dates

def get_today_hot_data(content_type):
    today = timezone.now().date()
    read_details = ReadDetail.objects.filter(content_type=content_type, date=today).order_by('-read_num') # 排序由大到小
    return read_details[:7]

def get_yesterday_hot_data(content_type):
    today = timezone.now().date()
    yesterday = today - datetime.timedelta(days=1)
    read_details = ReadDetail.objects.filter(content_type=content_type, date=yesterday).order_by('-read_num') # 排序由大到小
    return read_details[:7]

# def get_7_days_hot_data(content_type):
#     today = timezone.now().date()
#     date = today - datetime.timedelta(days=7)
#     read_details = ReadDetail.objects \
#                                 .filter(content_type=content_type, date__lt=today, date__gt=date) \
#                                 .annotate(read_num_sum=Sum('read_num')) \
#                                 .order_by('-read_num_sum') # 排序由大到小
#     return read_details[:7]

# .values('content_type', 'object_id') \


