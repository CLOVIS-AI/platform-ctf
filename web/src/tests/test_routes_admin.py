from .utils import PopulatedDBTestCase


# noinspection DuplicatedCode
class TestRoutesAdmin(PopulatedDBTestCase):
    def login(self, username, password):
        return self.client.post(
            "/login",
            data=dict(username=username, password=password),
            follow_redirects=True,
        )

    def logout(self):
        return self.client.get("/logout", follow_redirects=True)

    def test_admin_page_is_inaccessible_when_not_connected(self):
        response = self.client.get("/admin")
        self.assertRedirects(response, "/login?next=%2Fadmin")

    def test_admin_page_is_inaccessible_when_not_admin(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/admin")
            self.assert403(response)

    def test_admin_challenge_page_is_inaccessible_when_not_connected(self):
        response = self.client.get("/admin/challenges")
        self.assertRedirects(response, "/login?next=%2Fadmin%2Fchallenges")

    def test_admin_challenge_page_is_inaccessible_when_not_admin(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/admin/challenges")
            self.assert403(response)

    def test_admin_user_page_is_inaccessible_when_not_connected(self):
        response = self.client.get("/admin/users")
        self.assertRedirects(response, "/login?next=%2Fadmin%2Fusers")

    def test_admin_user_page_is_inaccessible_when_not_admin(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/admin/users")
            self.assert403(response)

    def test_admin_instances_page_is_inaccessible_when_not_connected(self):
        response = self.client.get("/admin/instances")
        self.assertRedirects(response, "/login?next=%2Fadmin%2Finstances")

    def test_admin_instances_page_is_inaccessible_when_not_admin(self):
        with self.client:
            self.login("logged_user", "logged_password")
            response = self.client.get("/admin/instances")
            self.assert403(response)
