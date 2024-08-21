from django.test import TestCase
from core.models import Feedback


class FeedbackTestCase(TestCase):
    def test_group_feedback_by_branch_service(self):
        results = Feedback.group_feedback_by_branch_service()
        self.assertIsInstance(results, list)
        self.assertGreater(len(results), 0)
