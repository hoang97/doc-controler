import json
from django.urls.base import reverse
from rest_framework import status
from users.tests import BaseTests, create_troly, create_giamdoc, create_truongphong
from hsmt.models import *

xfile_fake_content = {
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

def create_type(name, content):
    example_content = json.dumps(content)
    return XFileType.objects.create(name=name, example_content=example_content)

def create_target(name, type, description=''):
    return Target.objects.create(name=name, type=type, description=description)

class XFileTests(BaseTests):
    def setUp(self) -> None:
        super().setUp()
        self.troly11 = create_troly(self.phong1.id, 'troly11')
        self.troly12 = create_troly(self.phong1.id, 'troly12')
        self.troly2 = create_troly(self.phong2.id, 'troly2')
        self.truongphong2 = create_truongphong(self.phong2.id, 'truongphong2')
        self.xfiletype1 = create_type('xfiletype1', xfile_fake_content)
        self.xfiletype2 = create_type('xfiletype2', xfile_fake_content)
        self.target1 = create_target('target1', TARGET_TYPES.AREA)
        self.target2 = create_target('target2', TARGET_TYPES.DIRECTION)
        self.target3 = create_target('target3', TARGET_TYPES.GROUP)
        xfile1_data = {
            'code': 'test_code_1',
            'description': '',
            'type': self.xfiletype1.id,
            'targets': [self.target1.id, self.target2.id, self.target3.id],
            'editors': [self.troly11.id, self.troly12.id],
            'checkers': [self.troly1.id],
            'approvers': [self.truongphong1.id]
        }
        response = self.create_xfile(self.troly1, xfile1_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.xfile1 = XFile.objects.get(code=xfile1_data['code'])
        xfile2_data = {
            'code': 'test_code_2',
            'description': '',
            'type': self.xfiletype2.id,
            'targets': [self.target1.id, self.target2.id, self.target3.id],
            'editors': [self.troly11.id],
            'checkers': [self.troly1.id],
            'approvers': [self.truongphong1.id]
        }
        response = self.create_xfile(self.troly1, xfile2_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.xfile2 = XFile.objects.get(code=xfile2_data['code'])
        xfile3_data = {
            'code': 'test_code_3',
            'description': '',
            'type': self.xfiletype1.id,
            'targets': [self.target1.id, self.target2.id, self.target3.id],
            'editors': [self.troly2.id],
            'checkers': [self.troly2.id],
            'approvers': [self.truongphong2.id]
        }
        response = self.create_xfile(self.troly2, xfile3_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.xfile3 = XFile.objects.get(code=xfile3_data['code'])

    #------------------API function---------------------------------#

    def create_xfile(self, creator, data):
        response = self.user_login_jwt(creator.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_C')
        response = self.client.post(url, data, format='json')
        self.client.logout()
        return response

    def list_xfile(self, viewer):
        response = self.user_login_jwt(viewer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_L')
        response = self.client.get(url, format='json')
        self.client.logout()
        return response

    def destroy_xfile(self, destroyer, xfile_id):
        response = self.user_login_jwt(destroyer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_RD_general', kwargs={'pk': xfile_id})
        response = self.client.delete(url, format='json')
        self.client.logout()
        return response

    def change_perm_xfile(self, manager, xfile_id, data):
        response = self.user_login_jwt(manager.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_U_perm', kwargs={'pk': xfile_id})
        response = self.client.patch(url, data, format='json')
        self.client.logout()
        return response

    def list_xfile_perm(self, viewer, xfile_id):
        response = self.user_login_jwt(viewer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_perm', kwargs={'pk': xfile_id})
        response = self.client.get(url, format='json')
        self.client.logout()
        return response

    def create_change_xfile(self, editor, xfile_id, data):
        response = self.user_login_jwt(editor.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('hsmt-create-change', kwargs={'pk': xfile_id})
        response = self.client.put(url, data, format='json')
        self.client.logout()
        return response

    def cancel_change_xfile(self, editor, xfile_id):
        response = self.user_login_jwt(editor.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('hsmt-cancel-change', kwargs={'pk': xfile_id})
        response = self.client.put(url, format='json')
        self.client.logout()
        return response

    def submit_change_xfile(self, editor, xfile_id):
        response = self.user_login_jwt(editor.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('hsmt-submit', kwargs={'pk': xfile_id})
        response = self.client.put(url, format='json')
        self.client.logout()
        return response

    def check_change_xfile(self, checker, xfile_id):
        response = self.user_login_jwt(checker.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('hsmt-check', kwargs={'pk': xfile_id})
        response = self.client.put(url, format='json')
        self.client.logout()
        return response

    def reject_check_xfile(self, checker, xfile_id):
        response = self.user_login_jwt(checker.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('hsmt-reject-check', kwargs={'pk': xfile_id})
        response = self.client.put(url, format='json')
        self.client.logout()
        return response

    def approve_change_xfile(self, approver, xfile_id):
        response = self.user_login_jwt(approver.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('hsmt-approve', kwargs={'pk': xfile_id})
        response = self.client.put(url, format='json')
        self.client.logout()
        return response

    def reject_approve_xfile(self, approver, xfile_id):
        response = self.user_login_jwt(approver.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('hsmt-reject-approve', kwargs={'pk': xfile_id})
        response = self.client.put(url, format='json')
        self.client.logout()
        return response

    def update_general_xfile(self, editor, xfile_id, data):
        response = self.user_login_jwt(editor.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_U_general', kwargs={'pk': xfile_id})
        response = self.client.patch(url, data, format='json')
        self.client.logout()
        return response

    def retrieve_content_xfile(self, viewer, xfile_id, department_id=None):
        response = self.user_login_jwt(viewer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if department_id:
            response = self.department_login_jwt(department_id, 'abc')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_RU_content', kwargs={'pk': xfile_id})
        response = self.client.get(url, format='json')
        self.client.logout()
        return response

    def update_content_xfile(self, editor, xfile_id, data, department_id=None):
        response = self.user_login_jwt(editor.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if department_id:
            response = self.department_login_jwt(department_id, 'abc')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_RU_content', kwargs={'pk': xfile_id})
        response = self.client.put(url, data, format='json')
        self.client.logout()
        return response

    def list_comment_xfile(self, viewer, xfile_id):
        response = self.user_login_jwt(viewer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_L_comment', kwargs={'pk': xfile_id})
        response = self.client.get(url, format='json')
        self.client.logout()
        return response

    def create_comment_xfile(self, creator, xfile_id, data):
        response = self.user_login_jwt(creator.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_C_comment', kwargs={'pk': xfile_id})
        response = self.client.post(url, data, format='json')
        self.client.logout()
        return response

    def retrieve_comment_xfile(self, viewer, xfile_id, comment_id):
        response = self.user_login_jwt(viewer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_RUD_comment', kwargs={'pk': xfile_id, 'comment_id': comment_id})
        response = self.client.get(url, format='json')
        self.client.logout()
        return response

    def destroy_comment_xfile(self, destroyer, xfile_id, comment_id):
        response = self.user_login_jwt(destroyer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_RUD_comment', kwargs={'pk': xfile_id, 'comment_id': comment_id})
        response = self.client.delete(url, format='json')
        self.client.logout()
        return response

    def update_comment_xfile(self, editor, xfile_id, comment_id, data):
        response = self.user_login_jwt(editor.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_RUD_comment', kwargs={'pk': xfile_id, 'comment_id': comment_id})
        response = self.client.put(url, data, format='json')
        self.client.logout()
        return response

    def list_attacklog_xfile(self, viewer, xfile_id, department_id=None):
        response = self.user_login_jwt(viewer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if department_id:
            response = self.department_login_jwt(department_id, 'abc')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_L_attacklog', kwargs={'pk': xfile_id})
        response = self.client.get(url, format='json')
        self.client.logout()
        return response

    def retrieve_attacklog_xfile(self, viewer, xfile_id, attacklog_id, department_id=None):
        response = self.user_login_jwt(viewer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if department_id:
            response = self.department_login_jwt(department_id, 'abc')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_RUD_attacklog', kwargs={'pk': xfile_id, 'attacklog_id': attacklog_id})
        response = self.client.get(url, format='json')
        self.client.logout()
        return response

    def update_attacklog_xfile(self, editor, xfile_id, attacklog_id, data, department_id=None):
        response = self.user_login_jwt(editor.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if department_id:
            response = self.department_login_jwt(department_id, 'abc')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_RUD_attacklog', kwargs={'pk': xfile_id, 'attacklog_id': attacklog_id})
        response = self.client.patch(url, data, format='json')
        self.client.logout()
        return response

    def destroy_attacklog_xfile(self, destroyer, xfile_id, attacklog_id, department_id=None):
        response = self.user_login_jwt(destroyer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if department_id:
            response = self.department_login_jwt(department_id, 'abc')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_RUD_attacklog', kwargs={'pk': xfile_id, 'attacklog_id': attacklog_id})
        response = self.client.delete(url, format='json')
        self.client.logout()
        return response

    #---------------------test functions--------------------------------------#

    def test_create_xfile(self):
        '''
        Ensure only troly can create xfile
        XFile after created -> 
        status=init, department=user.department, creator=user, content=example_content
        '''
        xfile_data = {
            'code': 'test_code_4',
            'description': '',
            'type': self.xfiletype1.id,
            'targets': [self.target1.id, self.target2.id, self.target3.id],
            'editors': [self.troly11.id],
            'checkers': [self.troly1.id],
            'approvers': [self.truongphong1.id]
        }
        response = self.create_xfile(self.truongphong1, xfile_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.create_xfile(self.troly1, xfile_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_xfile = XFile.objects.get(code=xfile_data['code'])
        self.assertEqual(new_xfile.status, STATUS.INIT)
        self.assertEqual(new_xfile.department.id, self.troly1.department.id)
        self.assertEqual(new_xfile.creator.id, self.troly1.id)
        self.assertEqual(new_xfile.content, self.xfiletype1.example_content)

        xfile_data['code'] = 'fake'
        xfile_data.pop('type')
        response = self.create_xfile(self.troly1, xfile_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_xfile(self):
        '''
        Ensure that:
        - troly only can see xfiles, which he can edit and check
        - truongphong can see all department's xfiles
        - giamdoc can see all xfiles
        '''
        response = self.list_xfile(self.troly1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.troly1.xfiles_can_edit.count()+self.troly1.xfiles_can_check.count())
        response = self.list_xfile(self.troly12)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), self.troly12.xfiles_can_edit.count()+self.troly12.xfiles_can_check.count())
        response = self.list_xfile(self.truongphong1)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), XFile.objects.filter(department=self.truongphong1.department).count())
        response = self.list_xfile(self.giamdoc)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), XFile.objects.count())

    def test_retrieve_destroy_xfile(self):
        '''
        Ensure that only giamdoc can delete xfile
        '''
        xfile_data = {
            'code': 'test_code_for_destroy',
            'description': '',
            'type': self.xfiletype1.id,
            'targets': [self.target1.id, self.target2.id, self.target3.id],
            'editors': [self.troly11.id],
            'checkers': [self.troly1.id],
            'approvers': [self.truongphong1.id]
        }
        response = self.create_xfile(self.troly1, xfile_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        xfile_for_destroy = XFile.objects.get(code=xfile_data['code'])
        response = self.destroy_xfile(self.troly1, xfile_for_destroy.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.destroy_xfile(self.truongphong1, xfile_for_destroy.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.destroy_xfile(self.giamdoc, xfile_for_destroy.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_update_perm_xfile(self):
        '''
        Ensure that only truongphong can change editors, checkers, approvers
        '''
        xfile_data = {
            'code': 'test_code_for_perm_change',
            'description': '',
            'type': self.xfiletype1.id,
            'targets': [self.target1.id, self.target2.id, self.target3.id],
            'editors': [self.troly11.id],
            'checkers': [self.troly1.id],
            'approvers': [self.truongphong1.id]
        }
        response = self.create_xfile(self.troly1, xfile_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        xfile_for_perm_change = XFile.objects.get(code=xfile_data['code'])

        data_for_perm_change = {
            'editors': [self.troly1.id]
        }
        response = self.change_perm_xfile(self.troly1, xfile_for_perm_change.id, data_for_perm_change)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.change_perm_xfile(self.giamdoc, xfile_for_perm_change.id, data_for_perm_change)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.change_perm_xfile(self.truongphong2, xfile_for_perm_change.id, data_for_perm_change)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.change_perm_xfile(self.truongphong1, xfile_for_perm_change.id, data_for_perm_change)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_xfile_perm(self):
        '''
        Ensure that any authenticated account can get list xfile perm
        '''
        response = self.list_xfile_perm(self.troly1, self.xfile3.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.list_xfile_perm(self.troly2, self.xfile3.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.list_xfile_perm(self.truongphong1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.list_xfile_perm(self.giamdoc, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_xfile_update_general(self):
        '''
        Ensure that only editors can update xfile general when status=EDITING
        '''
        xfile_data = {
            'code': 'test_code_for_update_general',
            'description': '',
            'type': self.xfiletype1.id,
            'targets': [self.target1.id, self.target2.id, self.target3.id],
            'editors': [self.troly11.id],
            'checkers': [self.troly1.id],
            'approvers': [self.truongphong1.id]
        }
        data_for_update_general = {
            'description': 'updated',
            'targets': [self.target1.id, self.target2.id]
        }
        data_changes = {
            "targets": {"type": "target", "old": [1, 2, 3], "new": [1, 2]}, 
            "description": {"type": "string", "old": "", "new": "updated"}
        }
        response = self.create_xfile(self.troly1, xfile_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        xfile_for_update_general = XFile.objects.get(code=xfile_data['code'])
        response = self.update_general_xfile(self.troly11, xfile_for_update_general.id, data_for_update_general)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.create_change_xfile(self.troly11, xfile_for_update_general.id, {'change_name': 'test_create_change'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(xfile_for_update_general.changes.count(), 1)
        response = self.update_general_xfile(self.troly1, xfile_for_update_general.id, data_for_update_general)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.update_general_xfile(self.troly11, xfile_for_update_general.id, data_for_update_general)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(xfile_for_update_general.changes.first().content), data_changes)

    def test_xfile_retrieve_update_content(self):
        '''
        Ensure that:
        - only user can View xfile and logged in department can retrieve xfile.content
        - only editors who logged-in department can edit xfile.content when status=EDITING
        '''
        xfile_data = {
            'code': 'test_code_for_update_content',
            'description': '',
            'type': self.xfiletype1.id,
            'targets': [self.target1.id, self.target2.id, self.target3.id],
            'editors': [self.troly11.id],
            'checkers': [self.troly1.id],
            'approvers': [self.truongphong1.id]
        }
        xfile_fake1_content = deepcopy(xfile_fake_content)
        xfile_fake1_content['1. Tên gọi và các tên gọi khác']['value'] = 'updated test_name'
        data_for_update_content = {
            'content': json.dumps(xfile_fake1_content),
        }
        data_changes = {
            "1. Tên gọi và các tên gọi khác": {"type": "string", "old": "", "new": "updated test_name"}
        }
        response = self.create_xfile(self.troly1, xfile_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        xfile_for_update_content = XFile.objects.get(code=xfile_data['code'])

        #-----------------------------retrieve content---------------------------#
        response = self.retrieve_content_xfile(self.truongphong1, xfile_for_update_content.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.retrieve_content_xfile(self.troly12, xfile_for_update_content.id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        response = self.retrieve_content_xfile(self.troly1, xfile_for_update_content.id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #-----------------------------update content---------------------------#
        response = self.update_content_xfile(self.troly1, xfile_for_update_content.id, data_for_update_content, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.update_content_xfile(self.troly11, xfile_for_update_content.id, data_for_update_content, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # create change
        response = self.create_change_xfile(self.troly11, xfile_for_update_content.id, {'change_name': 'test_create_change'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # --------------
        response = self.update_content_xfile(self.troly11, xfile_for_update_content.id, data_for_update_content, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(xfile_for_update_content.changes.first().content), data_changes)

    def test_xfile_list_comment(self):
        '''
        Ensure that only user, who can view xfile, can view xfile.comments
        '''
        response = self.list_comment_xfile(self.troly2, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.list_comment_xfile(self.truongphong2, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.list_comment_xfile(self.troly11, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.list_comment_xfile(self.troly1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.list_comment_xfile(self.truongphong1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.list_comment_xfile(self.giamdoc, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_xfile_create_comment(self):
        '''
        Ensure that only user, who can view xfile, can create xfile.comments
        '''
        data_for_create_comment = {
            'body': 'test create comment'
        }
        response = self.create_comment_xfile(self.troly2, self.xfile1.id, data_for_create_comment)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.create_comment_xfile(self.truongphong2, self.xfile1.id, data_for_create_comment)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.create_comment_xfile(self.troly11, self.xfile1.id, data_for_create_comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.create_comment_xfile(self.troly1, self.xfile1.id, data_for_create_comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.create_comment_xfile(self.truongphong1, self.xfile1.id, data_for_create_comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.create_comment_xfile(self.giamdoc, self.xfile1.id, data_for_create_comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_xfile_retrieve_update_destroy_comment(self):
        '''
        Ensure that only user, who can view xfile, can retrieve/update/destroy xfile.comments
        '''
        data_for_create_comment = {
            'body': 'test update comment 1'
        }
        data_for_update_comment = {
            'body': 'test update comment 2'
        }
        response = self.create_comment_xfile(self.troly11, self.xfile1.id, data_for_create_comment)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        comment = self.xfile1.comments.get(body=data_for_create_comment['body'])

        #----------------------trieve comment---------------------------------#
        response = self.retrieve_comment_xfile(self.troly2, self.xfile1.id, comment.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.retrieve_comment_xfile(self.troly11, self.xfile1.id, comment.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.retrieve_comment_xfile(self.troly1, self.xfile1.id, comment.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.retrieve_comment_xfile(self.truongphong1, self.xfile1.id, comment.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.retrieve_comment_xfile(self.giamdoc, self.xfile1.id, comment.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #----------------------update comment---------------------------------#
        response = self.update_comment_xfile(self.troly2, self.xfile1.id, comment.id, data_for_update_comment)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.update_comment_xfile(self.troly11, self.xfile1.id, comment.id, data_for_update_comment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.update_comment_xfile(self.troly1, self.xfile1.id, comment.id, data_for_update_comment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.update_comment_xfile(self.truongphong1, self.xfile1.id, comment.id, data_for_update_comment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.update_comment_xfile(self.giamdoc, self.xfile1.id, comment.id, data_for_update_comment)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        comment = self.xfile1.comments.get(id=comment.id)
        self.assertEqual(comment.body, data_for_update_comment['body'])
        #----------------------delete comment---------------------------------#
        response = self.destroy_comment_xfile(self.troly2, self.xfile1.id, comment.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.destroy_comment_xfile(self.troly11, self.xfile1.id, comment.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_xfile_list_attacklog(self):
        '''
        Ensure that only user, who can view xfile + logged in department, can view list attacklog
        '''
        response = self.list_attacklog_xfile(self.troly2, self.xfile1.id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.list_attacklog_xfile(self.troly11, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.list_attacklog_xfile(self.giamdoc, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.list_attacklog_xfile(self.troly11, self.xfile1.id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.list_attacklog_xfile(self.truongphong1, self.xfile1.id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.list_attacklog_xfile(self.giamdoc, self.xfile1.id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def create_attacklog_xfile(self, creator, xfile_id, data, department_id=None):
        response = self.user_login_jwt(creator.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if department_id:
            response = self.department_login_jwt(department_id, 'abc')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_C_attacklog', kwargs={'pk': xfile_id})
        response = self.client.post(url, data, format='json')
        self.client.logout()
        return response

    def test_xfile_create_attacklog(self):
        '''
        Ensure that only editors, who is logged in department, can create attacklog when status=EDITING
        '''
        xfile_data = {
            'code': 'test_code_for_create_attacklog',
            'description': '',
            'type': self.xfiletype1.id,
            'targets': [self.target1.id, self.target2.id, self.target3.id],
            'editors': [self.troly11.id],
            'checkers': [self.troly1.id],
            'approvers': [self.truongphong1.id]
        }
        data_for_create_attacklog = {
            'timestamp': '2021-09-12',
            'result': 'test create result',
            'process': 'test create process',
            'attacker': self.troly1.id
        }
        response = self.create_xfile(self.troly1, xfile_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        xfile_for_create_attacklog = XFile.objects.get(code=xfile_data['code'])

        response = self.create_attacklog_xfile(self.troly2, xfile_for_create_attacklog.id, data_for_create_attacklog, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.create_attacklog_xfile(self.troly11, xfile_for_create_attacklog.id, data_for_create_attacklog)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.create_attacklog_xfile(self.giamdoc, xfile_for_create_attacklog.id, data_for_create_attacklog)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.create_attacklog_xfile(self.truongphong1, xfile_for_create_attacklog.id, data_for_create_attacklog, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.create_attacklog_xfile(self.giamdoc, xfile_for_create_attacklog.id, data_for_create_attacklog, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.create_attacklog_xfile(self.troly11, xfile_for_create_attacklog.id, data_for_create_attacklog, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #create xfilechange => status -> EDITING
        response = self.create_change_xfile(self.troly11, xfile_for_create_attacklog.id, {'change_name': 'test_create_change'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #---------------------------------------
        response = self.create_attacklog_xfile(self.troly11, xfile_for_create_attacklog.id, data_for_create_attacklog, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        data_changes = {
            "attack_logs": {"type": "attacklog", "old": [], "new": [response.data['id']]}
        }
        self.assertEqual(json.loads(xfile_for_create_attacklog.changes.first().content), data_changes)

    def test_xfile_retrieve_update_destroy_attacklog(self):
        '''
        Ensure that only editors, who is logged in department, can update, destroy attacklog when status=EDITING 
        '''
        xfile_data = {
            'code': 'test_code_for_update_destroy_attacklog',
            'description': '',
            'type': self.xfiletype1.id,
            'targets': [self.target1.id, self.target2.id, self.target3.id],
            'editors': [self.troly11.id],
            'checkers': [self.troly1.id],
            'approvers': [self.truongphong1.id]
        }
        data_for_create_attacklog = {
            'timestamp': '2021-09-12',
            'result': 'test update destroy result 1',
            'process': 'test update destroy process 1',
            'attacker': self.troly1.id
        }
        data_for_update_attacklog = {
            'result': 'test update destroy result 2',
            'process': 'test update destroy process 2',
            'attacker': self.troly11.id
        }
        response = self.create_xfile(self.troly1, xfile_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        xfile_for_update_destroy_attacklog = XFile.objects.get(code=xfile_data['code'])

        #----------------create xfilechange => status -> EDITING--------------#
        response = self.create_change_xfile(self.troly11, xfile_for_update_destroy_attacklog.id, {'change_name': 'test_create_change'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #----------------create attacklog---------------------#
        response = self.create_attacklog_xfile(self.troly11, xfile_for_update_destroy_attacklog.id, data_for_create_attacklog, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        attacklog_id = response.data['id']
        #----------------retrieve attacklog---------------------#
        response = self.retrieve_attacklog_xfile(self.troly2, xfile_for_update_destroy_attacklog.id, attacklog_id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.retrieve_attacklog_xfile(self.troly11, xfile_for_update_destroy_attacklog.id, attacklog_id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.retrieve_attacklog_xfile(self.truongphong1, xfile_for_update_destroy_attacklog.id, attacklog_id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        #----------------update attacklog---------------------#
        response = self.update_attacklog_xfile(self.troly2, xfile_for_update_destroy_attacklog.id, attacklog_id, data_for_update_attacklog, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.update_attacklog_xfile(self.troly11, xfile_for_update_destroy_attacklog.id, attacklog_id, data_for_update_attacklog)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.update_attacklog_xfile(self.giamdoc, xfile_for_update_destroy_attacklog.id, attacklog_id, data_for_update_attacklog)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.update_attacklog_xfile(self.truongphong1, xfile_for_update_destroy_attacklog.id, attacklog_id, data_for_update_attacklog, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.update_attacklog_xfile(self.giamdoc, xfile_for_update_destroy_attacklog.id, attacklog_id, data_for_update_attacklog, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.update_attacklog_xfile(self.troly11, xfile_for_update_destroy_attacklog.id, attacklog_id, data_for_update_attacklog, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['result'], data_for_update_attacklog['result'])
        #----------------destroy attacklog---------------------#
        response = self.destroy_attacklog_xfile(self.troly2, xfile_for_update_destroy_attacklog.id, attacklog_id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.destroy_attacklog_xfile(self.troly11, xfile_for_update_destroy_attacklog.id, attacklog_id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.destroy_attacklog_xfile(self.giamdoc, xfile_for_update_destroy_attacklog.id, attacklog_id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.destroy_attacklog_xfile(self.truongphong1, xfile_for_update_destroy_attacklog.id, attacklog_id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.destroy_attacklog_xfile(self.giamdoc, xfile_for_update_destroy_attacklog.id, attacklog_id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.destroy_attacklog_xfile(self.troly11, xfile_for_update_destroy_attacklog.id, attacklog_id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def list_change_xfile(self, viewer, xfile_id, department_id=None):
        response = self.user_login_jwt(viewer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if department_id:
            response = self.department_login_jwt(department_id, 'abc')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_L_change', kwargs={'pk': xfile_id})
        response = self.client.get(url, format='json')
        self.client.logout()
        return response

    def retrieve_change_xfile(self, viewer, xfile_id, version, department_id=None):
        response = self.user_login_jwt(viewer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if department_id:
            response = self.department_login_jwt(department_id, 'abc')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_RU_change', kwargs={'pk': xfile_id, 'version': version})
        response = self.client.get(url, format='json')
        self.client.logout()
        return response

    def update_change_xfile(self, viewer, xfile_id, version, data, department_id=None):
        response = self.user_login_jwt(viewer.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        if department_id:
            response = self.department_login_jwt(department_id, 'abc')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_xfile_RU_change', kwargs={'pk': xfile_id, 'version': version})
        response = self.client.put(url, data, format='json')
        self.client.logout()
        return response

    def test_xfile_workflow(self):
        '''
        Ensure that:
        - only editors can create xfile_change when xfile.status=INIT/DONE
        - only users, who can view xfile and logged-in department, can view or update change_name when status=EDITING
        - only editors can submit/cancel_change xfile when xfile.status=EDITING
        - only checkers can check/reject_check xfile when xfile.status=CHECKING
        - only approvers can approve/reject_approve xfile when xfile.status=APPROVING
        '''
        #---------------create_change--------------------#
        response = self.create_change_xfile(self.troly1, self.xfile1.id, {'change_name': 'test_create_change'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.create_change_xfile(self.truongphong1, self.xfile1.id, {'change_name': 'test_create_change'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.create_change_xfile(self.giamdoc, self.xfile1.id, {'change_name': 'test_create_change'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.create_change_xfile(self.troly11, self.xfile1.id, {'change_name': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.create_change_xfile(self.troly11, self.xfile1.id, {'change_name': 'test_create_change'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.create_change_xfile(self.troly11, self.xfile1.id, {'change_name': 'test_create_change2'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #---------------retrieve_change/update change_name--------------------#
        self.xfile1 = XFile.objects.get(id=self.xfile1.id)
        response = self.list_change_xfile(self.truongphong2, self.xfile1.id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.list_change_xfile(self.troly1, self.xfile1.id, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.retrieve_change_xfile(self.troly2, self.xfile1.id, self.xfile1.version, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.retrieve_change_xfile(self.troly1, self.xfile1.id, self.xfile1.version, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.update_change_xfile(self.troly1, self.xfile1.id, self.xfile1.version, {'name': 'test_change_name'}, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.update_change_xfile(self.troly11, self.xfile1.id, self.xfile1.version, {'name': 'test_change_name'}, self.phong1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test_change_name')
        #---------------cancel_change--------------------#
        response = self.cancel_change_xfile(self.troly1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.cancel_change_xfile(self.truongphong1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.cancel_change_xfile(self.giamdoc, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.cancel_change_xfile(self.troly12, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.cancel_change_xfile(self.troly12, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #---------------submit_change--------------------#
        response = self.create_change_xfile(self.troly11, self.xfile1.id, {'change_name': 'test_create_change2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.submit_change_xfile(self.troly1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.submit_change_xfile(self.truongphong1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.submit_change_xfile(self.giamdoc, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.submit_change_xfile(self.troly12, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.submit_change_xfile(self.troly12, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #---------------reject_check_change--------------------#
        response = self.reject_check_xfile(self.troly11, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.reject_check_xfile(self.truongphong1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.reject_check_xfile(self.giamdoc, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.reject_check_xfile(self.troly1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.reject_check_xfile(self.troly1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #---------------check_change--------------------#
        response = self.submit_change_xfile(self.troly12, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.check_change_xfile(self.troly11, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.check_change_xfile(self.truongphong1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.check_change_xfile(self.giamdoc, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.check_change_xfile(self.troly1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.check_change_xfile(self.troly1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #---------------reject_approve_change--------------------#
        response = self.reject_approve_xfile(self.troly11, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.reject_approve_xfile(self.troly1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.reject_approve_xfile(self.giamdoc, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.reject_approve_xfile(self.truongphong1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.reject_approve_xfile(self.truongphong1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #---------------approve_change_change--------------------#
        response = self.check_change_xfile(self.troly1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.approve_change_xfile(self.troly11, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.approve_change_xfile(self.troly1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.approve_change_xfile(self.giamdoc, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.approve_change_xfile(self.truongphong1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.approve_change_xfile(self.truongphong1, self.xfile1.id)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        #---------------create_change--------------------#
        response = self.create_change_xfile(self.troly11, self.xfile1.id, {'change_name': 'test_create_change3'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

# '{"1. T\u00ean g\u1ecdi v\u00e0 c\u00e1c t\u00ean g\u1ecdi kh\u00e1c": {"type": "string", "value": ""}, "2a. Th\u1eddi gian t\u1ed5 ch\u1ee9c th\u00e0nh l\u1eadp": {"type": "datetime", "value": ""}, "2b. Th\u1eddi gian xu\u1ea5t hi\u1ec7n tr\u00ean KGM": {"type": "datetime", "value": ""}, "3. M\u1ee5c ti\u00eau tr\u00ean m\u1ea1ng": {"type": "string", "value": ""}, "4. N\u1ec1n t\u1ea3ng \u1ee9ng d\u1ee5ng (b\u1ed5 sung)": {"type": "string", "value": ""}, "5. \u0110\u1ecba ch\u1ec9 v\u00e0 s\u1ed1 \u0111i\u1ec7n tho\u1ea1i": {"type": "string", "value": ""}, "6. T\u00f4n ch\u1ec9, m\u1ee5c \u0111\u00edch": {"type": "string", "value": ""}, "7. Qu\u00e1 tr\u00ecnh h\u00ecnh th\u00e0nh, ho\u1ea1t \u0111\u1ed9ng": {"type": "string", "value": ""}, "8. N\u1ed9i dung \u0111\u0103ng t\u1ea3i ch\u1ee7 y\u1ebfu": {"type": "string", "value": ""}}'

# print(json.dumps(content))