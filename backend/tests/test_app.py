import importlib
import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock, patch


os.environ.setdefault("SUBMISSIONS_BUCKET", "test-bucket")
os.environ.setdefault("PROCESSING_QUEUE_URL", "https://example.invalid/queue")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

fake_boto3 = types.SimpleNamespace(client=lambda _name: MagicMock())
sys.modules.setdefault("boto3", fake_boto3)
app = importlib.import_module("src.app")


class IntakeLoggingTests(unittest.TestCase):
    def test_unexpected_intake_failure_is_logged(self):
        event = {"routeKey": "POST /submissions"}

        with patch.object(app, "create_submission", side_effect=RuntimeError("boom")):
            with self.assertLogs("src.app", level="ERROR") as captured:
                result = app.lambda_handler(event, None)

        self.assertEqual(result["statusCode"], 500)
        self.assertIn("Submission intake failed", captured.output[0])
        self.assertIn("RuntimeError: boom", captured.output[0])


if __name__ == "__main__":
    unittest.main()
