from ...tests.utils import DBTestCase
from ...models import Challenge


class TestChallenge(DBTestCase):
    def test_challenge_creation(self):
        challenge = Challenge(
            name="Long name", short_name="short_name", description="description"
        )
        self.assertEqual(challenge.name, "Long name")
        self.assertEqual(challenge.short_name, "short_name")
        self.assertEqual(challenge.description, "description")

    def test_cannot_create_empty_challenge(self):
        with self.assertRaises(Exception):
            Challenge().save()
        with self.assertRaises(Exception):
            Challenge(name="Challenge number one").save()
        with self.assertRaises(Exception):
            Challenge(short_name="chall").save()

    def test_short_name_are_unique(self):
        Challenge(name="Challenge number one", short_name="chall").save()
        with self.assertRaises(Exception):
            Challenge(name="Challenge number two", short_name="chall").save()
