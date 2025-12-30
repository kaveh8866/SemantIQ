from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from .schema import ScoreResult, BenchmarkTestCase

class BaseScorer(ABC):
    @abstractmethod
    def score(self, case: BenchmarkTestCase, model_output: str) -> ScoreResult:
        """
        Evaluate the model output against the test case.
        """
        pass

class ExactMatchScorer(BaseScorer):
    def score(self, case: BenchmarkTestCase, model_output: str) -> ScoreResult:
        expected = case.expected
        if not expected:
            return ScoreResult(score=0.0, metrics={"exact_match": False}, details="No expected output provided")

        # Normalize strings for comparison
        output_norm = model_output.strip()
        
        # Handle different types of expected output
        match = False
        if isinstance(expected, str):
            match = output_norm == expected.strip()
        elif isinstance(expected, list):
            match = output_norm in [e.strip() for e in expected]
            
        return ScoreResult(
            score=1.0 if match else 0.0,
            metrics={"exact_match": match},
            details=f"Expected: {expected}, Got: {output_norm}" if not match else "Match"
        )

class HeuristicScorer(BaseScorer):
    """
    A deterministic heuristic scorer for code generation.
    Checks for basic properties like non-emptiness, presence of expected tokens (if simple), etc.
    """
    def score(self, case: BenchmarkTestCase, model_output: str) -> ScoreResult:
        metrics = {}
        score = 0.0
        details = []

        # Metric 1: Not Empty
        if model_output and model_output.strip():
            metrics["not_empty"] = True
            score += 0.5
        else:
            metrics["not_empty"] = False
            details.append("Output is empty")

        # Metric 2: Contains expected snippet (weak match)
        expected = case.expected
        if expected and isinstance(expected, str):
            if expected.strip() in model_output:
                metrics["contains_expected"] = True
                score += 0.5
            else:
                metrics["contains_expected"] = False
                details.append(f"Output does not contain expected snippet: '{expected}'")
        elif expected:
             # If expected is list/dict, skip this heuristic for MVP or implement smarter logic
             pass
        else:
             # If no expected, give partial credit just for generating something
             score += 0.5

        return ScoreResult(
            score=min(score, 1.0),
            metrics=metrics,
            details="; ".join(details) if details else "Passed heuristics"
        )

class ScorerFactory:
    @staticmethod
    def get_scorer(scorer_type: str) -> BaseScorer:
        if scorer_type == "exact_match":
            return ExactMatchScorer()
        elif scorer_type == "heuristic":
            return HeuristicScorer()
        else:
            raise ValueError(f"Unknown scorer type: {scorer_type}")
