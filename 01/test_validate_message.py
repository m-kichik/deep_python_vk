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
    def test_model_call(self, mock_model):
        with patch.object(mock_model, "predict") as mock_predict:
            message = "Test message"
            mock_model.predict.return_value = 0.42
            predict_message_mood(message, mock_model)
            mock_predict.call_args.assert_called_once_with(message="Test message")

    @patch("validate_message.SomeModel")
    def test_messages(self, mock_model):
        with self.subTest("Test bad message"):
            mock_model.predict.return_value = 0.2
            message = "Bad message"
            result = predict_message_mood(message, mock_model)
            self.assertEqual(result, "неуд")

        with self.subTest("Test norm message"):
            mock_model.predict.return_value = 0.5
            message = "Normal message"
            result = predict_message_mood(message, mock_model)
            self.assertEqual(result, "норм")

        with self.subTest("Test good message"):
            mock_model.predict.return_value = 0.9
            message = "Good message"
            result = predict_message_mood(message, mock_model)
            self.assertEqual(result, "отл")

    @patch("validate_message.SomeModel")
    def test_thresholds(self, mock_model):
        with self.subTest("Test custom threshold with bad message"):
            mock_model.predict.return_value = 0.1
            message = "Not that good message"
            result = predict_message_mood(
                message, mock_model, bad_thresholds=0.25, good_thresholds=0.75
            )
            self.assertEqual(result, "неуд")

        with self.subTest("Test custom threshold with norm message"):
            mock_model.predict.return_value = 0.5
            message = "Average message"
            result = predict_message_mood(
                message, mock_model, bad_thresholds=0.25, good_thresholds=0.75
            )
            self.assertEqual(result, "норм")

        with self.subTest("Test custom threshold with good message"):
            mock_model.predict.return_value = 0.9
            message = "Good enough message"
            result = predict_message_mood(
                message, mock_model, bad_thresholds=0.25, good_thresholds=0.75
            )
            self.assertEqual(result, "отл")

        with self.subTest("Test bad_t = good_t with bad message"):
            mock_model.predict.return_value = 0.2
            message = "Strange bad message"
            result = predict_message_mood(
                message, mock_model, bad_thresholds=0.42, good_thresholds=0.42
            )
            self.assertEqual(result, "неуд")

        with self.subTest("Test bad_t = good_t with norm message"):
            mock_model.predict.return_value = 0.42
            message = "Strange norm message"
            result = predict_message_mood(
                message, mock_model, bad_thresholds=0.42, good_thresholds=0.42
            )
            self.assertEqual(result, "норм")

        with self.subTest("Test bad_t = good_t with good message"):
            mock_model.predict.return_value = 0.6
            message = "Strange good message"
            result = predict_message_mood(
                message, mock_model, bad_thresholds=0.42, good_thresholds=0.42
            )
            self.assertEqual(result, "отл")

        with self.subTest("Test value equal to lower threshold"):
            mock_model.predict.return_value = 0.3
            message = "Almost bad message"
            result = predict_message_mood(message, mock_model, bad_thresholds=0.3)
            self.assertEqual(result, "норм")

        with self.subTest("Test value equal to upper threshold"):
            mock_model.predict.return_value = 0.8
            message = "Almost good message"
            result = predict_message_mood(message, mock_model, good_thresholds=0.8)
            self.assertEqual(result, "норм")

        with self.subTest("Test value 1e-9 less than bad threshold"):
            mock_model.predict.return_value = 0.3 - 1e-9
            message = "This message tried"
            result = predict_message_mood(message, mock_model, bad_thresholds=0.3)
            self.assertEqual(result, "неуд")

        with self.subTest("Test value 1e-9 more than bad threshold"):
            mock_model.predict.return_value = 0.3 + 1e-9
            message = "This message passed"
            result = predict_message_mood(message, mock_model, bad_thresholds=0.3)
            self.assertEqual(result, "норм")

        with self.subTest("Test value 1e-9 less than good threshold"):
            mock_model.predict.return_value = 0.8 - 1e-9
            message = "Unhappy message"
            result = predict_message_mood(message, mock_model, good_thresholds=0.8)
            self.assertEqual(result, "норм")

        with self.subTest("Test value 1e-9 more than good threshold"):
            mock_model.predict.return_value = 0.8 + 1e-9
            message = "Sufficient message"
            result = predict_message_mood(message, mock_model, good_thresholds=0.8)
            self.assertEqual(result, "отл")


if __name__ == "__main__":
    unittest.main()
