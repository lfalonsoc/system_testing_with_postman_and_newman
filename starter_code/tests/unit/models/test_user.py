from starter_code.models.user import UserModel
from starter_code.tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self) -> None:
        user: UserModel = UserModel('test', 'abcd')
        
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, 'abcd')
