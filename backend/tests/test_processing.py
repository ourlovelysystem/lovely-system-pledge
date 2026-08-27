import importlib
import os
from pathlib import Path
import sys
import types
import unittest
from unittest.mock import MagicMock


os.environ.setdefault("SUBMISSIONS_BUCKET", "test-bucket")
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

fake_boto3 = types.SimpleNamespace(client=lambda _name: MagicMock())
sys.modules.setdefault("boto3", fake_boto3)
processing = importlib.import_module("src.processing")


class SemanticEvaluationTests(unittest.TestCase):
    def test_direct_question_is_usable(self):
        result = processing.semantic_evaluation("Who are you?")
        self.assertEqual(result["catalogue_decision"], "usable")
        self.assertEqual(result["semantic_match_score"], 1.0)

    def test_humorous_variant_is_usable(self):
        result = processing.semantic_evaluation("Who are you, dickwad?")
        self.assertEqual(result["catalogue_decision"], "usable")

    def test_name_request_is_usable(self):
        result = processing.semantic_evaluation("Sing me your name.")
        self.assertEqual(result["catalogue_decision"], "usable")

    def test_ambiguous_identity_language_requires_review(self):
        result = processing.semantic_evaluation("Identity unknown.")
        self.assertEqual(result["catalogue_decision"], "review_required")

    def test_unrelated_speech_is_unusable(self):
        result = processing.semantic_evaluation("The weather is pleasant.")
        self.assertEqual(result["catalogue_decision"], "unusable")


class TranscriptTests(unittest.TestCase):
    def test_average_confidence_uses_pronunciation_items(self):
        document = {
            "results": {
                "items": [
                    {"type": "pronunciation", "alternatives": [{"confidence": "0.8"}]},
                    {"type": "punctuation", "alternatives": [{"confidence": "0.1"}]},
                    {"type": "pronunciation", "alternatives": [{"confidence": "1.0"}]},
                ]
            }
        }
        self.assertEqual(processing.average_confidence(document), 0.9)

    def test_transcript_text_handles_empty_result(self):
        self.assertEqual(processing.transcript_text({"results": {}}), "")


if __name__ == "__main__":
    unittest.main()
