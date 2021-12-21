from datetime import datetime

from ...commands import instance_cli
from ...models import User, Challenge, ResourceInstance, ChallengeResource
from ...tests.utils import CliTestCase


# noinspection DuplicatedCode
class TestInstanceCommands(CliTestCase):

    @staticmethod
    def create_instance(identifier=0):
        challenge = Challenge(
            name="Challenge", short_name=f"challenge_short_name{identifier}"
        ).save()
        user = User(
            username=f"username{identifier}",
            email=f"username{identifier}@email.com",
        ).save()
        resource = ChallengeResource(
            type="terraform", args="", start_duration=10, challenge=challenge
        ).save()
        ResourceInstance(
            status="started",
            resource=resource,
            expiration=datetime.now(),
            user=user,
            number=identifier,
        ).save()

    def test_list_empty_instances(self):
        result = self.runner.invoke(instance_cli, ["list"])
        self.assertEqual(result.stdout.split("\n")[2], "")

    def test_list_one_instance(self):
        self.create_instance()
        result = self.runner.invoke(instance_cli, ["list"])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertEqual(
            result.stdout.split("\n")[2],
            " 0   |  started   |    username0     | challenge_short_name0",
        )

    def test_list_many_instance(self):
        count = 10
        for i in range(count):
            self.create_instance(i)
        result = self.runner.invoke(instance_cli, ["list"])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertEqual(len(result.stdout.split("\n")), count + 3)

    def test_clean_expired_instances(self):
        self.create_instance()
        result = self.runner.invoke(instance_cli, ["clean", "--expired"])
        self.assertEqual(result.exit_code, 0, msg=result.exception)
        self.assertIn("Instance stopped for user username0\n", result.stdout)
