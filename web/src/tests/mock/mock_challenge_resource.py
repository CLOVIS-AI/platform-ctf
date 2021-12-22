from ...models import ChallengeResource


class MockChallengeResource(ChallengeResource):
    __mapper_args__ = {"polymorphic_identity": "mock"}

    def __init__(self):
        super().__init__()
        self.actions = []

    def instantiate(self, user):
        self.actions.append("instantiate")
        return super().instantiate(user)
