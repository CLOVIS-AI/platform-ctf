from ...tests.utils import DBTestCase
from ...models import ChallengeStep


class TestChallengeStep(DBTestCase):
    def test_challenge_step_creation(self):
        step = ChallengeStep(
            description="Un challenge",
            points=10,
            validation_type="string",
            validation_arg="flag{test}",
        )
        self.assertEqual(step.description, "Un challenge")
        self.assertEqual(step.points, 10)
        self.assertEqual(step.validation_type, "string")
        self.assertEqual(step.validation_arg, "flag{test}")
