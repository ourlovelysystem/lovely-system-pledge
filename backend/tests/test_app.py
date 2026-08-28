import importlib
from datetime import datetime, timezone
import json
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


class PledgeStateTests(unittest.TestCase):
    now = datetime(2026, 8, 28, 1, 30, tzinfo=timezone.utc)

    def record(self, **changes):
        value = {
            "submission_id": "6de7a7b0-43c7-4c25-a049-4779a9091f72",
            "catalogue": "who_are_you",
            "catalogue_decision": "usable",
            "borrowing_starts_at": "2026-08-28T01:00:00Z",
            "expires_at": "2026-08-29T01:00:00Z",
            "audio_object_reference": "audio/id/source.webm",
            "audio_media_type": "audio/webm",
            "minimum_uses": 0,
            "completed_uses": 0,
        }
        value.update(changes)
        return value

    def test_no_usable_history_is_bootstrap(self):
        state = app.derive_pledge_state([], self.now)
        self.assertEqual(state["mode"], "bootstrap")

    def test_eligible_voice_changes_state_to_normal(self):
        state = app.derive_pledge_state([self.record()], self.now)
        self.assertEqual(state["mode"], "normal")
        self.assertEqual(state["selected"]["catalogue_decision"], "usable")

    def test_expired_usable_voice_changes_state_to_sulk(self):
        expired = self.record(expires_at="2026-08-28T01:15:00Z")
        state = app.derive_pledge_state([expired], self.now)
        self.assertEqual(state["mode"], "sulk")

    def test_unusable_voice_does_not_end_bootstrap(self):
        unusable = self.record(catalogue_decision="unusable")
        state = app.derive_pledge_state([unusable], self.now)
        self.assertEqual(state["mode"], "bootstrap")


if __name__ == "__main__":
    unittest.main()
