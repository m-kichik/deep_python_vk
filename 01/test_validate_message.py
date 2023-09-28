import unittest
from unittest.mock import patch

from validate_message import SomeModel, predict_message_mood


class TestPredictMessageMood(unittest.TestCase):
    def test_default(self):
        model = SomeModel()
        message = "Volcano"
        result = predict_message_mood(message, model)
        self.assertEqual(result, "неуд")

    @patch("validate_message.SomeModel")
    def test_call_predict(self, mock_model):
        with patch.object(mock_model, "predict") as mock_predict:
            message = "Test message"
            mock_model.predict.return_value = 0.2
            predict_message_mood(message, mock_model)
            mock_predict.assert_called_once()

    @patch("validate_message.SomeModel")
    def test_bad_message(self, mock_model):
        mock_model.predict.return_value = 0.2
        message = "Bad message"
        result = predict_message_mood(message, mock_model)
        self.assertEqual(result, "неуд")

    @patch("validate_message.SomeModel")
    def test_norm_message(self, mock_model):
        mock_model.predict.return_value = 0.5
        message = "Normal message"
        result = predict_message_mood(message, mock_model)
        self.assertEqual(result, "норм")

    @patch("validate_message.SomeModel")
    def test_good_message(self, mock_model):
        mock_model.predict.return_value = 0.9
        message = "Good message"
        result = predict_message_mood(message, mock_model)
        self.assertEqual(result, "отл")

    @patch("validate_message.SomeModel")
    def test_custom_thresholds(self, mock_model):
        mock_model.predict.return_value = 0.42
        message = "Average message"
        result = predict_message_mood(
            message, mock_model, bad_thresholds=0.2, good_thresholds=0.7
        )
        self.assertEqual(result, "норм")


if __name__ == "__main__":
    unittest.main()
