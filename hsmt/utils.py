import json
import logging
from datetime import date, datetime
from copy import deepcopy

def is_suitable_change(detail, change, reverse=False):
    '''Check if detail and change are suitable'''

    if not (detail and change):
        return False
    list1 = [detail.get('type'), detail.get('value')]
    list2 = [change.get('type'), change.get('old'), change.get('new')]
    # check if any item in detail and change is None
    for item in list1+list2:
        if item is None:
            return False
    # check if values are not the same type
    if (list1[0] != list2[0]): return False
    if reverse:
        # check if value of detail and new value of change are not the same
        if (list1[1] != list2[2]): return False
    else:
        # check if value of detail and old value of change are not the same
        if (list1[1] != list2[1]): return False

    return True

def apply_change(content:dict, change_log:dict):
    '''Apply changes in change_log to content'''
    new_content = deepcopy(content) 
    for field, log in change_log.items():
        detail = new_content.get(field)

        if not is_suitable_change(detail, log): 
            logging.error('Content and Change_log are not suitable!!!')
            raise ValueError
        
        new_content[field]['value'] = log['new']
    return new_content

def reverse_change(content:dict, change_log:dict):
    '''Reverse changes in change_log from content'''
    new_content = deepcopy(content) 
    for field, log in change_log.items():
        detail = new_content.get(field)

        if not is_suitable_change(detail, log, reverse=True): 
            logging.error('Content and Change_log are not suitable!!!')
            raise ValueError
        
        new_content[field]['value'] = log['old']
    return new_content

def is_suitable_content(content1:dict, content2:dict):
    '''Check if content1 and content2 are same XFile type'''
    if content1.keys() != content2.keys():
        return False
    
    for field in content1.keys():
        if content1[field]['type'] != content2[field]['type']:
            return False

    return True

def get_xfile_changes(old_content:dict, new_content:dict):
    '''Get change_log of content'''
    if not is_suitable_content(old_content, new_content):
        logging.error('old_content and new_content are not the same Xfile type!!!')
        raise ValueError
    change = {}
    for field in old_content.keys():
        if old_content[field] != new_content[field]:
            change[field] = {}
            change[field]['type'] = old_content[field]['type']
            change[field]['old'] = old_content[field]['value']
            change[field]['new'] = new_content[field]['value']
    
    return change

def read_from_JSON(content, extra_content, ):
    '''Get dict-type content from json string'''
    return json.loads(content)

def save_to_JSON(content):
    '''Get json string from dict-type content'''
    return json.dumps(content)

def get_changes_brief_info(changes_obj):
    '''Get dict-type brief info from list of change object'''
    info = {}
    for change_obj in changes_obj:
        pass

def decode(content, key):
    return content


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