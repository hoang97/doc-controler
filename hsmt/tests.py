from django.test import TestCase
from .utils import apply_change, reverse_change, get_changes_brief_info, get_xfile_changes

# Create your tests here.
content = {
    '1. Tên gọi và các tên gọi khác': {
        'type': 'string',
        'value' : 'Tổ chức B',
    },
    '2a. Thời gian tổ chức thành lập': {
        'type': 'datetime',
        'value' : 'Jun 1 2005  1:33PM',
    },
    '2b. Thời gian xuất hiện trên KGM': {
        'type': 'datetime',
        'value' : 'Jun 1 2005  1:33PM',
    },
    '3. Địa chỉ và số điện thoại': {
        'type': 'string',
        'value' : '+84123456789',
    },
}

change_log_1 = {
    '2b. Thời gian xuất hiện trên KGM': {
        'type': 'datetime',
        'old' : 'Jun 1 2005  1:33PM',
        'new' : 'Jun 1 2015  1:33PM',
    },
    '3. Địa chỉ và số điện thoại': {
        'type': 'string',
        'old' : '+84123456789',
        'new' : '+74123456789',
    },
}

a = apply_change(content, change_log_1)
print(a)
b = reverse_change(a, change_log_1)
# print(b)
change = get_xfile_changes(a,b)
print(change)
# print(save_to_JSON(a))