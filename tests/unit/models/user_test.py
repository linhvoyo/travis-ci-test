from models.user import UserModel
from tests.unit.base_test_unit import UnitBaseTest

class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test', 'abcd')

        self.assertEqual(user.username, 'test')
        self.assertEqual(user.password, 'abcd')