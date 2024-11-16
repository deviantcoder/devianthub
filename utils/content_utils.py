from django.utils import timezone
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def pagination(request, all_objects, results):
    paginator = Paginator(all_objects, results)
    page = request.GET.get('page', 1)

    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        objects = paginator.page(page)
    except EmptyPage:
        objects = paginator.page(paginator.num_pages)

    left_index = (int(page) - 2)
    if left_index < 1:
        left_index = 1

    right_index = (int(page) + 3)
    if right_index > paginator.num_pages:
        right_index = paginator.num_pages + 1

    custom_range = range(left_index, right_index)

    return objects, paginator, custom_range


def time_since_obj_posted(obj):
    time_diff = timezone.now() - obj.created
    time_diff = time_diff.total_seconds() / 3600

    week_hours = 24 * 7
    month_hours = 24 * 30

    data = {'type': '', 'num': 0}

    if time_diff < 1 / 60:
        data['type'] = 'now'
    elif time_diff < 1:
        data['type'] = 'minute'
        data['num'] = int(time_diff * 60)  # minutes
    elif time_diff < 24:
        data['type'] = 'hour'
        data['num'] = int(time_diff)  # hours
    elif 24 <= time_diff < week_hours:
        data['type'] = 'day'
        data['num'] = int(time_diff // 24)  # days
    elif week_hours <= time_diff < month_hours:
        data['type'] = 'week'
        data['num'] = int(time_diff / 24 / 7)  # weeks
    elif time_diff >= month_hours:
        data['type'] = 'month'
        data['num'] = int(time_diff / 24 / 30)  # months

    return data