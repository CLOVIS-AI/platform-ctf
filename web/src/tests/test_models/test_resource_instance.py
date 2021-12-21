from ...tests.utils import DBTestCase
from ...models import ResourceInstance, Challenge, ChallengeResource, User


# noinspection DuplicatedCode
class TestResourceInstance(DBTestCase):
    def test_resource_instance_creation(self):
        user = User(username="username", email="email@email.com").save()
        Challenge(name="Long name", short_name="short_name").save()
        challenge_resource = ChallengeResource(type="file", args="filename.txt").save()
        resource_instance = ResourceInstance(
            resource=challenge_resource, user=user
        ).save()
        self.assertEqual(resource_instance.user, user)
        self.assertEqual(resource_instance.resource, challenge_resource)

    def test_resource_instance_instantiation(self):
        user = User(username="username", email="email@email.com").save()
        challenge_resource = ChallengeResource(type="terraform", args="test").save()
        challenge_resource.instantiate(user)
