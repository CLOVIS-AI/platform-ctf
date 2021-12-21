from ...tests.utils import DBTestCase
from ...models import Challenge, ChallengeResource


# noinspection DuplicatedCode
class TestChallengeResource(DBTestCase):
    def test_challenge_resource_creation(self):
        Challenge(name="Long name", short_name="short_name").save()
        challenge_resource = ChallengeResource(type="file", args="filename.txt").save()
        self.assertEqual(challenge_resource.type, "file")
        self.assertEqual(challenge_resource.args, "filename.txt")
