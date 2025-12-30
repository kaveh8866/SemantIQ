import unittest
import numpy as np
import pandas as pd
from evaluation.reliability.icc import calculate_icc
from evaluation.reliability.krippendorff import calculate_krippendorff_alpha

class TestReliabilityMetrics(unittest.TestCase):

    def test_icc_perfect_agreement(self):
        # 3 subjects, 3 raters, perfect agreement
        data = pd.DataFrame({
            'R1': [1, 2, 3],
            'R2': [1, 2, 3],
            'R3': [1, 2, 3]
        })
        icc = calculate_icc(data, icc_type='icc2k')
        self.assertAlmostEqual(icc, 1.0)

    def test_icc_poor_agreement(self):
        # Random data where raters disagree but not pathologically
        # R1 says 1,1,1; R2 says 3,3,3. They disagree on levels but are consistent internally.
        # But we want poor reliability.
        data = pd.DataFrame({
            'R1': [1, 1, 1],
            'R2': [3, 3, 3],
            'R3': [2, 2, 2]
        })
        # Between-subject variance is 0 (all subjects are 1,3,2 -> mean 2).
        # So ICC should be 0.
        icc = calculate_icc(data, icc_type='icc2k')
        self.assertLess(icc, 0.1)

    def test_krippendorff_perfect(self):
        # Rows=Raters, Cols=Subjects (but our function takes Subjects x Raters if we follow utils.py, 
        # BUT calculate_krippendorff_alpha expects a matrix. 
        # Let's check my implementation again.
        # My implementation: matrix = np.array(data).T (Transposes Input).
        # Input expected: Rows=Subjects, Cols=Raters.
        # Transposed: Rows=Raters, Cols=Subjects.
        # Logic follows.
        
        data = [
            [1, 1], # Subject 1: Rater 1=1, Rater 2=1
            [2, 2], # Subject 2: Rater 1=2, Rater 2=2
            [3, 3]  # Subject 3: Rater 1=3, Rater 2=3
        ]
        alpha = calculate_krippendorff_alpha(data)
        self.assertAlmostEqual(alpha, 1.0)

    def test_krippendorff_disagreement(self):
        data = [
            [1, 3],
            [2, 2],
            [3, 1]
        ]
        alpha = calculate_krippendorff_alpha(data)
        # Should be low, possibly negative if disagreement is worse than chance
        self.assertLess(alpha, 0.5)

    def test_krippendorff_missing_data(self):
        # Using np.nan
        data = [
            [1, 1],
            [2, np.nan],
            [3, 3]
        ]
        alpha = calculate_krippendorff_alpha(data)
        # Should still be high as existing data agrees perfectly
        self.assertAlmostEqual(alpha, 1.0)

if __name__ == '__main__':
    unittest.main()
