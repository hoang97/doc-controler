from copy import deepcopy
from django.urls.base import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User, Department, Position
from users.api_views import department_check_pwd

# Create your tests here.
def create_troly(department_id, username):
    department = Department.objects.get(id=department_id)
    position = Position.objects.get(alias='tl')
    return User.objects.create_user(username=username, password='test1805', department=department, position=position, first_name=username+'_name')

def create_truongphong(department_id, username):
    department = Department.objects.get(id=department_id)
    position = Position.objects.get(alias='tp')
    return User.objects.create_user(username=username, password='test1805', department=department, position=position, first_name=username+'_name')

def create_giamdoc(department_id, username):
    department = Department.objects.get(id=department_id)
    position = Position.objects.get(alias='gd')
    return User.objects.create_user(username=username, password='test1805', department=department, position=position, first_name=username+'_name')

class BaseTests(APITestCase):
    def setUp(self) -> None:
        self.chucvugd = Position.objects.create(name='giám đốc', alias='gd')
        self.chucvutp = Position.objects.create(name='trưởng phòng', alias='tp')
        self.chucvutl = Position.objects.create(name='trợ lý', alias='tl')
        self.phonggiamdoc = Department.objects.create_department(name='giám đốc', alias='giamdoc', password='abc')
        self.phong1 = Department.objects.create_department(alias='phong1', password='abc', name='phòng 1')
        self.phong2 = Department.objects.create_department(alias='phong2', password='abc', name='phòng 2')
        self.giamdoc = create_giamdoc(1, 'giamdoc')
        self.truongphong1 = create_truongphong(2, 'truongphong1')
        self.troly1 = create_troly(2, 'troly1')

    def user_login_jwt(self, username, password):
        data = {
            'username': username,
            'password': password
        }
        url = reverse('api_user_login')
        response = self.client.post(url, data, format='json')
        if response.status_code == 200:
            jwt_token = response.data
            credentials = deepcopy(self.client._credentials)
            credentials['HTTP_AUTHORIZATION'] = 'Login ' + jwt_token['access']
            self.client.credentials(**credentials)
        return response

    def department_login_jwt(self, department_id, password):
        data = {
            'department_id': department_id,
            'password': password
        }
        url = reverse('api_department_login')
        response = self.client.post(url, data, format='json')
        if response.status_code == 200:
            jwt_token = response.data
            credentials = deepcopy(self.client._credentials)
            credentials['HTTP_DAUTHORIZATION'] = jwt_token['access']
            self.client.credentials(**credentials)
        return response

class UserTests(BaseTests):

    def register_user_for_other(self, creator, username, position):
        response = self.user_login_jwt(creator.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = {
            'username': username,
            'password': 'test1805',
            'first_name': username+'1',
            'position': position.id
        }
        url = reverse('api_user_register_for_other')
        response = self.client.post(url, data, format='json')
        self.client.logout()
        return response

    def register_user_for_any(self, username, department):
        data = {
            'username': username,
            'password': 'test1805',
            'first_name': username+'1',
            'department': department.id
        }
        url = reverse('api_user_register')
        return self.client.post(url, data, format='json')

    def manage_user(self, manager, user, data):
        response = self.user_login_jwt(manager.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_user_manage', kwargs={'pk': user.id})
        response = self.client.patch(url, data, format='json')
        self.client.logout()
        return response

    def test_position_model(self):
        '''
        Ensure position model is working
        '''
        self.assertEqual(str(self.chucvutl), self.chucvutl.name)

    def test_user_model(self):
        '''
        Ensure position model is working
        '''
        self.assertEqual(str(self.troly1), f"Tài khoản {self.troly1.username}")

    def test_user_register_for_other(self):
        '''
        Ensure that User create new account for other:
        - new_user.department = user.department
        - new_user.position less important than user.position
        '''
        response = self.register_user_for_other(self.troly1, 'test_user', self.chucvutl)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_user = User.objects.get(username='test_user')
        self.assertEqual(new_user.department.alias, self.troly1.department.alias)
        self.assertEqual(new_user.position.alias, 'tl')
        response = self.register_user_for_other(self.troly1, 'test_user1', self.chucvutp)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_register_for_any(self):
        '''
        Ensure that Create new account for everyone:
        - new_user.position = tro ly
        '''
        response = self.register_user_for_any('test_user1', self.phong1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        new_user = User.objects.get(username='test_user1')
        self.assertEqual(new_user.department.alias, 'phong1')
        self.assertEqual(new_user.position.alias, 'tl')

    def test_user_manage(self):
        '''
        Ensure that can't set higher position than your position
        '''
        response = self.manage_user(self.truongphong1, self.troly1, {'position': self.chucvugd.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.manage_user(self.truongphong1, self.troly1, {'position': self.chucvutp.id, 'is_active': False, 'department': self.phonggiamdoc.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['position'], self.chucvutp.id)
        self.assertEqual(response.data['is_active'], False)
        self.assertEqual(response.data['department'], self.phonggiamdoc.id)
        response = self.manage_user(self.giamdoc, self.troly1, {'position': self.chucvutl.id, 'is_active': True, 'department': self.phong1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class DepartmentTests(BaseTests):

    def change_pwd_department(self, manager, data):
        response = self.user_login_jwt(manager.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        url = reverse('api_department_change_pwd')
        response = self.client.post(url, data, format='json')
        self.client.logout()
        return response

    def test_department_model(self):
        '''
        Ensure department model is working
        '''
        self.assertEqual(str(self.phong1), self.phong1.name)

    def test_department_check_pwd(self):
        '''
        Ensure department_check_pwd function is working
        '''
        self.assertTrue(department_check_pwd(self.phong1.id, 'abc'))

    def test_department_login(self):
        '''
        Ensure authenticated user can login to department
        '''
        response = self.department_login_jwt(self.phong1.id, 'abc')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        response = self.user_login_jwt(self.troly1.username, 'test1805')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.department_login_jwt(self.phong1.id, 'abc')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.department_login_jwt(self.phonggiamdoc.id, 'fake_password')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.client.logout()

    def test_department_change_pwd(self):
        '''
        Ensure that only truongphong of department can change password
        '''
        response = self.change_pwd_department(self.troly1, {'department_id': self.phong1.id, 'password_old': 'abc', 'password_new': 'xyz'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.change_pwd_department(self.truongphong1, {'department_id': self.phong2.id, 'password_old': 'abc', 'password_new': 'xyz'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        response = self.change_pwd_department(self.truongphong1, {'department_id': self.phong1.id, 'password_old': 'xyz', 'password_new': 'xyz'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.change_pwd_department(self.truongphong1, {'department_id': self.phong1.id, 'password_old': 'abc', 'password_new': 'abc'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)