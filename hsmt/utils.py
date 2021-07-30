import json
import logging
from datetime import date, datetime
from copy import deepcopy
from asgiref.sync import async_to_sync

from channels.layers import get_channel_layer
from notifications.models import Log

def decode(content, key):
    return content

def notify(actor, target, verb, notify_to):
    '''
    Create new log and publish notification to channel
    '''
    channel_layer = get_channel_layer()
    new_log = Log.objects.create(actor=actor, target=target, verb=verb)
    new_log.notify_to.set(notify_to)
    for notification in new_log.notification_set.all():
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'notify.user',
                'notification_id': notification.id,
                'seen': notification.seen,
                'user_id': notification.recipient.id,
                'message': str(notification.log),
                'timestamp': datetime.strftime(notification.log.timestamp, '%b %d, %Y, %I:%M %p'),
            }
        )


if __name__ == '__main__':
    # Test
    content = {
        '1. Tên gọi và các tên gọi khác': {
            'type': 'string',
            'value' : '',
        },
        '2a. Thời gian tổ chức thành lập': {
            'type': 'datetime',
            'value' : '',
        },
        '2b. Thời gian xuất hiện trên KGM': {
            'type': 'datetime',
            'value' : '',
        },
        '3. Mục tiêu trên mạng': {
            'type': 'string',
            'value': '',
        },
        '4. Nền tảng ứng dụng (bổ sung)': {
            'type': 'string',
            'value': '',
        },
        '5. Địa chỉ và số điện thoại': {
            'type': 'string',
            'value' : '',
        },
        '6. Tôn chỉ, mục đích': {
            'type': 'string',
            'value': '',
        },
        '7. Quá trình hình thành, hoạt động': {
            'type': 'string',
            'value': '',
        },
        '8. Nội dung đăng tải chủ yếu': {
            'type': 'string',
            'value': '',
        },
    }
    content1 = {
        '1. Tên gọi và các tên gọi khác': {
            'type': 'string',
            'value' : '',
        },
        '2a. Thời gian tổ chức thành lập': {
            'type': 'datetime',
            'value' : '',
        },
        '2b. Thời gian xuất hiện trên KGM': {
            'type': 'datetime',
            'value' : '',
        },
        '3. Địa chỉ và số điện thoại': {
            'type': 'string',
            'value' : '',
        },
        '4. Mục tiêu trên mạng': {
            'type': 'string',
            'value': '',
        },
        '5a. Cơ cấu tổ chức, các bộ phận, chi nhánh': {
            'type': 'string',
            'value': '',
        },
        '5b. Lãnh đạo/quản trị, thành viên chủ chốt': {
            'type': 'string',
            'value': '',
        },
        '5c. Số lượng thành viên': {
            'type': 'string',
            'value': '',
        },
        '5d. Cách thức, quy trình tuyển chọn thành viên': {
            'type': 'string',
            'value': '',
        },
        '5e. Địa bàn hoạt động': {
            'type': 'string',
            'value': '',
        },
        '6. Tôn chỉ, mục đích': {
            'type': 'string',
            'value': '',
        },
        '7a. Đặc điểm, quy luật, nội dung, thủ đoạn, các hoạt động chống phá': {
            'type': 'string',
            'value': '',
        },
        '7b. Tần suất, lưu lượng đăng tải, mức độ quan tâm': {
            'type': 'string',
            'value': '',
        },
        '7c. Tổ chức/cá nhân chỉ đạo, tài trợ': {
            'type': 'string',
            'value': '',
        },
        '7d. Các tổ chức, mục tiêu có liên quan': {
            'type': 'string',
            'value': '',
        },
    }
    content2 = {
        '1. Tên gọi và các tên gọi khác (bí danh/nickname trên mạng)': {
            'type': 'string',
            'value' : '',
        },
        'Ngày sinh': {
            'type': 'datetime',
            'value' : '',
        },
        'Quê quán': {
            'type': 'string',
            'value' : '',
        },
        'Trú quán': {
            'type': 'string',
            'value' : '',
        },
        'Dân tộc': {
            'type': 'string',
            'value' : '',
        },
        'Quốc tịch': {
            'type': 'string',
            'value' : '',
        },
        'Tôn giáo': {
            'type': 'string',
            'value' : '',
        },
        'Địa chỉ': {
            'type': 'string',
            'value' : '',
        },
        
    }

    change_log_1 = {
        'code': {
            'type': 'string',
            'value' : '456LOL/VN',
        },
        '3. Địa chỉ và số điện thoại': {
            'type': 'string',
            'old' : '+84123456789',
            'new' : '+74123456789',
        },
    }

    content_test = {
        'type': {
            'type': 'target',
            'value': [1,2,3,4]
        },
        'department': {
            'type': 'department',
            'value': 2
        },
        'phần 2 mục 2':{
            'type': 'event',
            'value': [
                {'datetime':'1/1/1997','text':'bú hút với a K )))'},
                {'datetime':'2/1/1997','text':'bú hút tiếp với Tùng'},
                {'datetime':'default','text':'chơi thêm mai thúy mà méo biết từ bao giờ'}
            ]
        }
    }
    # a = apply_change(content, change_log_1)
    # print(a)
    # b = reverse_change(a, change_log_1)
    # print(b)
    # change = get_xfile_changes(a,b)
    # print(change)
    # print(save_to_JSON(a))
    # string_content = json.dumps(content)
    # print(string_content)
    # print(json.loads(string_content))
    # print(datetime.strptime('Jan 1 0001', '%b %d %Y'))

    # list1 = set(content1.keys())
    # list2 = set(content2.keys())
    # print(list1)
    # print(list2)
    # for item in list1 | list2:
    #     print(item)
    # from hsmt import models
    # xfile1 = models.XFile.objects.get(id = 2)
    # xfile2 = models.XFile.objects.get(id = 3)

    # print(xfile1.get_change_content(xfile2))
    for i in range(1, 0 , -1):
        print(i)