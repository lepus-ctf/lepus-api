from django.test import TestCase
from lepus.models import Team


class TeamModelTests(TestCase):

    def test_password(self):
        team = Team(name="team")

        # 空パスワードで認証されないことを確認
        self.assertFalse(team.check_password(""))

        # パスワードを設定
        team.set_password("password")
        self.assertFalse(team.check_password("invalid"))
        self.assertTrue(team.check_password("password"))

        # パスワードの変更
        team.set_password("newpassword")
        self.assertFalse(team.check_password("invalid"))
        self.assertFalse(team.check_password("password"))
        self.assertTrue(team.check_password("newpassword"))
