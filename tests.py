import unittest
from main import find_best_threshold

class TestFindBestThreshold(unittest.TestCase):

    def test_basic_case(self):
        # One threshold clearly has the highest precision among those meeting recall ≥0.9
        data = {
            0.3: {'tp': 90, 'fn': 10, 'fp': 20},
            0.4: {'tp': 95, 'fn': 5, 'fp': 5},
            0.5: {'tp': 80, 'fn': 20, 'fp': 0},
        }
        self.assertEqual(find_best_threshold(data), 0.4)

    def test_tie_in_precision(self):
        # Two thresholds meet recall ≥0.9 with the same precision; pick the higher threshold
        data = {
            0.6: {'tp': 90, 'fn': 10, 'fp': 10},
            0.7: {'tp': 90, 'fn': 10, 'fp': 10},
            0.5: {'tp': 95, 'fn': 5, 'fp': 20},
        }
        self.assertEqual(find_best_threshold(data), 0.7)

    def test_no_threshold_meets_recall(self):
        # All thresholds have recall <0.9; return None
        data = {
            0.3: {'tp': 80, 'fn': 20, 'fp': 20},
            0.4: {'tp': 85, 'fn': 15, 'fp': 15},
        }
        self.assertIsNone(find_best_threshold(data))

    def test_exact_recall(self):
        # Threshold with exactly 0.9 recall should be included
        data = {
            0.5: {'tp': 90, 'fn': 10, 'fp': 5},
            0.6: {'tp': 85, 'fn': 15, 'fp': 0},
        }
        self.assertEqual(find_best_threshold(data), 0.5)

    def test_skip_invalid_recall(self):
        # Threshold with TP+FN=0 (invalid) is skipped; valid threshold is selected
        data = {
            0.5: {'tp': 0, 'fn': 0, 'fp': 5},
            0.6: {'tp': 90, 'fn': 10, 'fp': 5},
        }
        self.assertEqual(find_best_threshold(data), 0.6)

    def test_zero_precision_denominator(self):
        # Edge case: TP=0 and FP=0 (precision=0.0), but recall is 0 (skipped)
        data = {
            0.5: {'tp': 0, 'fn': 10, 'fp': 0},
            0.6: {'tp': 90, 'fn': 10, 'fp': 5},
        }
        self.assertEqual(find_best_threshold(data), 0.6)

    def test_incorrect_data_type(self):
        # When values are not int/float
        data = {
            0.6: {'tp': '90.0', 'fn': 10.0, 'fp': 10},
            0.7: {'tp': 90, 'fn': 10, 'fp': [10]},
            0.5: {'tp': 95, 'fn': '5', 'fp': 20},
        }
        self.assertEqual(find_best_threshold(data), 0.6)

    def test_no_data(self):
        # When no values are provided
        data = {
        }
        self.assertEqual(find_best_threshold(data), None)

    def test_missing_values(self):
        # When values are not int/float
        data = {
            0.6: {'tp': 90, 'fn': 10},
            0.7: {'tp': 90, 'fp': [10]},
            0.5: {'fn': '5', 'fp': 20},
        }
        self.assertEqual(find_best_threshold(data), None)

if __name__ == '__main__':

    unittest.main()