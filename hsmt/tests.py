from django.test import TestCase
import json
content = {
    "1. Tên gọi và các tên gọi khác": {
        "type": "string",
        "value": ""
    },
    "2a. Thời gian tổ chức thành lập": {
        "type": "datetime",
        "value": ""
    },
    "2b. Thời gian xuất hiện trên KGM": {
        "type": "datetime",
        "value": ""
    },
    "3. Mục tiêu trên mạng": {
        "type": "string",
        "value": ""
    },
    "4. Nền tảng ứng dụng (bổ sung)": {
        "type": "string",
        "value": ""
    },
    "5. Địa chỉ và số điện thoại": {
        "type": "string",
        "value": ""
    },
    "6. Tôn chỉ, mục đích": {
        "type": "string",
        "value": ""
    },
    "7. Quá trình hình thành, hoạt động": {
        "type": "string",
        "value": ""
    },
    "8. Nội dung đăng tải chủ yếu": {
        "type": "string",
        "value": ""
    }
}

'{"1. T\u00ean g\u1ecdi v\u00e0 c\u00e1c t\u00ean g\u1ecdi kh\u00e1c": {"type": "string", "value": ""}, "2a. Th\u1eddi gian t\u1ed5 ch\u1ee9c th\u00e0nh l\u1eadp": {"type": "datetime", "value": ""}, "2b. Th\u1eddi gian xu\u1ea5t hi\u1ec7n tr\u00ean KGM": {"type": "datetime", "value": ""}, "3. M\u1ee5c ti\u00eau tr\u00ean m\u1ea1ng": {"type": "string", "value": ""}, "4. N\u1ec1n t\u1ea3ng \u1ee9ng d\u1ee5ng (b\u1ed5 sung)": {"type": "string", "value": ""}, "5. \u0110\u1ecba ch\u1ec9 v\u00e0 s\u1ed1 \u0111i\u1ec7n tho\u1ea1i": {"type": "string", "value": ""}, "6. T\u00f4n ch\u1ec9, m\u1ee5c \u0111\u00edch": {"type": "string", "value": ""}, "7. Qu\u00e1 tr\u00ecnh h\u00ecnh th\u00e0nh, ho\u1ea1t \u0111\u1ed9ng": {"type": "string", "value": ""}, "8. N\u1ed9i dung \u0111\u0103ng t\u1ea3i ch\u1ee7 y\u1ebfu": {"type": "string", "value": ""}}'

print(json.dumps(content))