from django.test import TestCase
from django.urls import reverse, reverse_lazy
from account.tests.test_modelmixintestcase import ModelMixinTestCase


class TestUserLogin(ModelMixinTestCase, TestCase):
    def test_auth_login_view_uses_correct_template(self):
        self.assertTemplateUsed(
            self.client.get(reverse("login")), "registration/login.html"
        )

    def test_auth_login_view_uses_correct_template_after_successful_login(
        self,
    ):
        self.client.login(**self.credentials)
        response = self.client.get(reverse("dashboard"), follow=True)
        self.assertTemplateUsed(response, "account/dashboard.html")


class TestLogoutView(ModelMixinTestCase, TestCase):
    def test_auth_logout_view_uses_correct_template(self):
        self.assertTemplateUsed(
            self.client.get(reverse("logout")),
            "registration/logged_out.html",
        )

    def test_auth_logout_view_uses_correct_template_after_successful_logout(
        self,
    ):
        self.client.login(**self.credentials)
        self.client.logout
        response = self.client.get(reverse("dashboard"), follow=True)
        self.assertTemplateUsed(response, "account/dashboard.html")


class TestPasswordChangeView(ModelMixinTestCase, TestCase):
    def test_auth_password_change_view_uses_correct_template(self):
        self.client.login(**self.credentials)
        self.assertTemplateUsed(
            self.client.get(reverse("password_change")),
            "registration/password_change_form.html",
        )

    def test_auth_password_change_done_view_uses_correct_template(self):
        self.client.login(**self.credentials)
        self.assertTemplateUsed(
            self.client.get(reverse("password_change_done")),
            "registration/password_change_done.html",
        )


class TestRegisterView(TestCase):
    def test_register_view_uses_correct_template_for_unsuccessful_registration(
        self,
    ):
        response = self.client.get(
            reverse("register"),
            {
                "username": "athiqur@gmail.com",
                "first_name": "athiqur",
                "email": "athiqurking@gmail.com",
                "password": "123",
                "password2": "123",
            },
        )
        self.assertTemplateUsed(response, "account/register.html")

    def test_register_view_uses_success_view_after_successful_registration(
        self,
    ):
        response = self.client.post(
            reverse("register"),
            {
                "username": "athiqur@gmail.com",
                "first_name": "athiqur",
                "email": "athiqurking@gmail.com",
                "password": "123",
                "password2": "123",
            },
        )
        self.assertTemplateUsed(response, "account/register_done.html")

    def test_edit_view_uses_success_view_after_editing(self):
        response = self.client.post(
            reverse("register"),
            {
                "username": "athiqur@gmail.com",
                "first_name": "athiqur",
                "email": "athiqurking@gmail.com",
                "password": "123",
                "password2": "123",
            },
        )
        self.assertTemplateUsed(response, "account/register_done.html")


class UserListView(ModelMixinTestCase, TestCase):
    def test_user_list_view_returns_success_view(self):

        self.client.login(**self.credentials)
        response = self.client.get(reverse("user_list"))

        self.assertTemplateUsed(response, "account/user/list.html")


class UserDetailView(ModelMixinTestCase, TestCase):
    def test_detail_view_returns_success_view_for_the_valid_user(self):

        self.client.login(**self.credentials)
        response = self.client.get(reverse("user_detail", args=[self.user]))

        self.assertTemplateUsed(response, "account/user/detail.html")

    def test_detail_view_returns_404_for_invalid_user(self):

        self.client.login(**self.credentials)
        response = self.client.get(
            reverse("user_detail", args=["invalid-user"])
        )

        self.assertEqual(response.status_code, 404)


class UserFollowView(ModelMixinTestCase, TestCase):
    def test_user_follow_view_succeeds_follow_when_the_request_is_ajax(self):
        self.client.login(**self.credentials)
        self.client.get(reverse("user_detail", args=[self.user.username]))
        response = self.client.post(
            reverse("user_follow"),
            {"id": self.user.pk, "action": "follow"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertJSONEqual(response.content, {"status": "ok"})

    def test_user_follow_view_succeeds_unfollow_when_the_request_is_ajax(self):
        self.client.login(**self.credentials)
        self.client.get(reverse("user_detail", args=[self.user.username]))
        self.client.post(
            reverse("user_follow"),
            {"id": self.user.pk, "action": "follow"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        response = self.client.post(
            reverse("user_follow"),
            {"id": self.user.pk, "action": "unfollow"},
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertJSONEqual(response.content, {"status": "ok"})

    def test_user_follow_view_returns_status_error_when_the_action_is_invalid(
        self,
    ):
        self.client.login(**self.credentials)
        self.client.get(reverse("user_detail", args=[self.user.username]))
        response = self.client.post(
            reverse("user_follow"),
            {
                "id": self.user.pk,
                "action": "actionum venaam reactionum venaam",
            },
            **{"HTTP_X_REQUESTED_WITH": "XMLHttpRequest"}
        )
        self.assertJSONEqual(response.content, {"status": "error"})
