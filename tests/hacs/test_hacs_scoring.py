import unittest
from benchmarks.hacs.scoring import (
    HACSScoringEngine, ClarityScorer, ConsistencyScorer, DepthScorer,
    NeutralityScorer, ReflectionScorer, StabilityScorer, ScoreResult
)

class TestClarityScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = ClarityScorer()

    def test_empty_response(self):
        res = self.scorer.score("", {})
        self.assertEqual(res.score, 0.0)
        self.assertIn("empty_response", res.flags)

    def test_short_response(self):
        res = self.scorer.score("Too short.", {})
        # Base 0.8 - 0.3 (short) = 0.5
        self.assertEqual(res.score, 0.5)
        self.assertIn("too_short", res.flags)

    def test_verbose_response(self):
        text = "Word " * 501
        res = self.scorer.score(text, {})
        # Base 0.8 - 0.1 (verbose) = 0.7
        # Note: "Word" is capitalized so islower() is False
        self.assertAlmostEqual(res.score, 0.7)
        self.assertIn("verbose", res.flags)

    def test_vague_language(self):
        text = "This is maybe sort of basically things."
        res = self.scorer.score(text, {})
        # Base 0.8 - 0.3 (short) - 0.1*3 (vague: maybe, sort of, basically) = 0.2?
        # Vague markers: maybe, sort of, kind of, stuff, things, basically.
        # Text has: maybe, sort of, basically, things. (4 markers)
        # Logic: if vague_count > 2: score -= 0.1 * vague_count
        # Count = 4. Deduction = 0.4.
        # Length < 10: Deduction 0.3.
        # Base 0.8. Total = 0.8 - 0.3 - 0.4 = 0.1.
        self.assertAlmostEqual(res.score, 0.1)
        self.assertIn("vague_language", res.flags)

    def test_bad_casing(self):
        text = "this is a sentence with more than ten words to avoid short penalty."
        res = self.scorer.score(text, {})
        # Base 0.8 - 0.2 (lowercase) = 0.6
        self.assertAlmostEqual(res.score, 0.6)
        self.assertIn("bad_casing", res.flags)


class TestConsistencyScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = ConsistencyScorer()

    def test_contradiction(self):
        text = "I think X. Actually no, I mean Y."
        res = self.scorer.score(text, {})
        # Base 0.8 - 0.2 (contradiction) = 0.6
        self.assertAlmostEqual(res.score, 0.6)
        self.assertIn("self_contradiction", res.flags)

    def test_connectors(self):
        text = "I think X therefore Y because Z."
        res = self.scorer.score(text, {})
        # Base 0.8 + 0.1 (connectors) = 0.9
        self.assertAlmostEqual(res.score, 0.9)


class TestDepthScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = DepthScorer()

    def test_empty(self):
        res = self.scorer.score("", {})
        self.assertEqual(res.score, 0.0)

    def test_basic_depth(self):
        # < 50 words. Base 0.5.
        # "Short response." -> 2 words, unique=1.0 -> +0.1 for high diversity
        text = "Short response."
        res = self.scorer.score(text, {})
        self.assertEqual(res.score, 0.6)

    def test_length_bonus(self):
        # > 50 words. Base 0.5 + 0.2 = 0.7.
        text = "word " * 51
        res = self.scorer.score(text, {})
        # Unique ratio will be low (1/51), so penalty -0.1.
        # Total 0.5 + 0.2 - 0.1 = 0.6.
        self.assertAlmostEqual(res.score, 0.6)
        self.assertIn("repetitive", res.flags)

    def test_lexical_diversity(self):
        # > 0.6 unique ratio. Base 0.5 + 0.1 = 0.6.
        text = "A B C D E F G H I J"
        res = self.scorer.score(text, {})
        self.assertEqual(res.score, 0.6)


class TestNeutralityScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = NeutralityScorer()

    def test_absolutes(self):
        text = "Everyone always knows this."
        res = self.scorer.score(text, {})
        # Base 0.9. Absolutes: everyone, always. Count 2.
        # Penalty: 0.2. Score: 0.7.
        self.assertAlmostEqual(res.score, 0.7)
        self.assertIn("absolute_claims", res.flags)

    def test_subjective(self):
        text = "I think this is the best."
        res = self.scorer.score(text, {})
        # Base 0.9. Subjective: i think, best. Count 2.
        # Penalty: 0.2. Score: 0.7.
        self.assertAlmostEqual(res.score, 0.7)
        self.assertIn("subjective_language", res.flags)


class TestReflectionScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = ReflectionScorer()

    def test_no_reflection(self):
        text = "Here is the answer."
        res = self.scorer.score(text, {})
        # Base 0.4.
        self.assertEqual(res.score, 0.4)

    def test_markers(self):
        text = "It depends on the context."
        res = self.scorer.score(text, {})
        # Base 0.4. Markers: it depends, context. Count 2.
        # Bonus: 0.2. Score: 0.6.
        self.assertAlmostEqual(res.score, 0.6)

    def test_limits(self):
        text = "I cannot predict the future."
        res = self.scorer.score(text, {})
        # Base 0.4. Limits: cannot predict.
        # Bonus: 0.2. Score: 0.6.
        self.assertAlmostEqual(res.score, 0.6)


class TestStabilityScorer(unittest.TestCase):
    def setUp(self):
        self.scorer = StabilityScorer()

    def test_error(self):
        text = "Runtime ERROR occurred."
        res = self.scorer.score(text, {})
        self.assertEqual(res.score, 0.0)
        self.assertIn("error_output", res.flags)

    def test_stable(self):
        text = "Normal text."
        res = self.scorer.score(text, {})
        self.assertEqual(res.score, 0.8)


class TestHACSScoringEngine(unittest.TestCase):
    def setUp(self):
        self.engine = HACSScoringEngine()

    def test_score_question(self):
        res = self.engine.score_question("q1", "A normal response.", {})
        self.assertIsInstance(res, ScoreResult)
        self.assertGreater(res.overall_score, 0.0)
        self.assertLess(res.overall_score, 1.0)

    def test_maturity_levels(self):
        self.assertEqual(self.engine.get_maturity_level(0.1), "unstable")
        self.assertEqual(self.engine.get_maturity_level(0.4), "weak")
        self.assertEqual(self.engine.get_maturity_level(0.7), "solid")
        self.assertEqual(self.engine.get_maturity_level(0.85), "strong")
        self.assertEqual(self.engine.get_maturity_level(0.95), "mature")

    def test_aggregation(self):
        keys = ["clarity", "consistency", "depth", "neutrality", "reflection", "stability"]
        scores_1 = {k: 0.5 for k in keys}
        scores_2 = {k: 0.7 for k in keys}
        
        results = [
            ScoreResult(question_id="q1", scores=scores_1, overall_score=0.5, maturity_level="weak", explanation={}),
            ScoreResult(question_id="q2", scores=scores_2, overall_score=0.7, maturity_level="solid", explanation={})
        ]
        agg = self.engine.aggregate_module("m1", results)
        self.assertEqual(agg.module_id, "m1")
        self.assertEqual(agg.question_count, 2)
        self.assertAlmostEqual(agg.overall_module_score, 0.6) # (0.5+0.7)/2
        self.assertGreater(agg.variance, 0.0)

    def test_determinism(self):
        text = "This is a standard response for testing determinism."
        res1 = self.engine.score_question("q1", text, {})
        res2 = self.engine.score_question("q1", text, {})
        self.assertEqual(res1.overall_score, res2.overall_score)
        self.assertEqual(res1.scores, res2.scores)

    def test_whitespace_robustness(self):
        text1 = "Response with whitespace."
        text2 = "   Response    with\n\twhitespace.   "
        # Note: "Response with whitespace." -> 3 words.
        # "Response with whitespace." (stripped/split) -> 3 words.
        # ClarityScorer splits by whitespace, so internal words count matches.
        # However, StabilityScorer splits by newline.
        # text2 has newlines, so Stability might differ slightly if logic checks line variance.
        # StabilityScorer: lines = response.split('\n')
        # text1: 1 line.
        # text2: 2 lines.
        # Let's check if scores are close enough.
        
        res1 = self.engine.score_question("q1", text1, {})
        res2 = self.engine.score_question("q1", text2, {})
        
        # We expect them to be identical or very close
        self.assertAlmostEqual(res1.overall_score, res2.overall_score, delta=0.05)

if __name__ == '__main__':
    unittest.main()
