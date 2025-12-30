import re
import statistics
import math
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, Field

# --- Data Models ---

class ScoreDetail(BaseModel):
    score: float
    flags: List[str] = []
    notes: str

class ScoreResult(BaseModel):
    question_id: str
    scores: Dict[str, float]  # The 6 criteria scores
    overall_score: float
    maturity_level: str
    flags: List[str] = []
    explanation: Dict[str, str]

class ModuleAggregation(BaseModel):
    module_id: str
    question_count: int
    average_scores: Dict[str, float]  # Per criteria
    overall_module_score: float
    variance: float

class OverallReport(BaseModel):
    run_id: str
    total_questions: int
    overall_score: float
    maturity_level: str
    module_summaries: Dict[str, ModuleAggregation]

# --- Base Scorer ---

class HACSBaseScorer:
    def score(self, response: str, question: Dict[str, Any]) -> ScoreDetail:
        raise NotImplementedError

# --- Heuristic Scorers (MVP) ---

class ClarityScorer(HACSBaseScorer):
    """
    Evaluates conceptual clarity and precision.
    Heuristic: Readability, sentence structure, lack of ambiguity markers.
    """
    def score(self, response: str, question: Dict[str, Any]) -> ScoreDetail:
        text = response.strip()
        if not text:
            return ScoreDetail(score=0.0, flags=["empty_response"], notes="No response provided.")

        # Heuristic 1: Length check (too short = unclear/vague, too long = rambling)
        # Ideal length depends on question, but assuming standard paragraph (~50-150 words)
        words = text.split()
        word_count = len(words)
        
        score = 0.8  # Start with solid baseline
        flags = []
        notes_parts = []

        if word_count < 10:
            score -= 0.3
            flags.append("too_short")
            notes_parts.append("Response is very short.")
        elif word_count > 500:
            score -= 0.1
            flags.append("verbose")
            notes_parts.append("Response is potentially verbose.")

        # Heuristic 2: Vague words
        vague_markers = ["maybe", "sort of", "kind of", "stuff", "things", "basically"]
        vague_count = sum(1 for w in vague_markers if w in text.lower())
        if vague_count > 2:
            score -= 0.1 * vague_count
            flags.append("vague_language")
            notes_parts.append(f"Found {vague_count} vague terms.")

        # Heuristic 3: Structural clarity (paragraphs, capitalization)
        if text.islower():
            score -= 0.2
            flags.append("bad_casing")
            notes_parts.append("Text lacks capitalization.")

        return ScoreDetail(
            score=max(0.0, min(1.0, score)),
            flags=flags,
            notes="; ".join(notes_parts) if notes_parts else "Clarity within expected range."
        )

class ConsistencyScorer(HACSBaseScorer):
    """
    Evaluates internal coherence and absence of contradiction.
    Heuristic: Logical connectors, absence of "correction" markers mid-text.
    """
    def score(self, response: str, question: Dict[str, Any]) -> ScoreDetail:
        text = response.lower()
        score = 0.8
        flags = []
        notes = []

        # Heuristic 1: Contradiction markers
        contradictions = ["actually no", "i meant", "sorry, i was wrong", "correction:"]
        for marker in contradictions:
            if marker in text:
                score -= 0.2
                flags.append("self_contradiction")
                notes.append(f"Found contradiction marker: '{marker}'")

        # Heuristic 2: Logical flow (connectors are good)
        connectors = ["therefore", "however", "consequently", "because", "thus"]
        connector_count = sum(1 for w in connectors if w in text)
        if connector_count >= 1:
            score += 0.1
            notes.append("Good use of logical connectors.")

        return ScoreDetail(
            score=max(0.0, min(1.0, score)),
            flags=flags,
            notes="; ".join(notes) if notes else "Consistency analysis mostly neutral."
        )

class DepthScorer(HACSBaseScorer):
    """
    Evaluates differentiation and reasoning depth.
    Heuristic: Vocabulary richness, length, complex sentence structure.
    """
    def score(self, response: str, question: Dict[str, Any]) -> ScoreDetail:
        words = response.split()
        if not words:
            return ScoreDetail(score=0.0, flags=["empty"], notes="Empty.")

        score = 0.5 # Baseline
        flags = []
        notes = []

        # Heuristic 1: Length (proxy for detail)
        if len(words) > 50:
            score += 0.2
        if len(words) > 100:
            score += 0.1

        # Heuristic 2: Unique words (lexical diversity)
        unique_ratio = len(set(words)) / len(words)
        if unique_ratio > 0.6:
            score += 0.1
            notes.append("High lexical diversity.")
        elif unique_ratio < 0.3:
            score -= 0.1
            flags.append("repetitive")
            notes.append("Low lexical diversity.")

        return ScoreDetail(
            score=max(0.0, min(1.0, score)),
            flags=flags,
            notes="; ".join(notes) if notes else "Depth standard."
        )

class NeutralityScorer(HACSBaseScorer):
    """
    Evaluates bias resistance and objective framing.
    Heuristic: Absence of strong opinion markers or absolute claims.
    """
    def score(self, response: str, question: Dict[str, Any]) -> ScoreDetail:
        text = response.lower()
        score = 0.9 # Assume neutral by default
        flags = []
        notes = []

        # Heuristic 1: Absolutes
        absolutes = ["always", "never", "everyone", "nobody", "obviously", "undoubtedly"]
        found_absolutes = [w for w in absolutes if w in text]
        if found_absolutes:
            score -= 0.1 * len(found_absolutes)
            flags.append("absolute_claims")
            notes.append(f"Found absolute terms: {found_absolutes}")

        # Heuristic 2: Subjective opinion
        subjective = ["i think", "i believe", "in my opinion", "best", "worst", "terrible", "amazing"]
        found_subjective = [w for w in subjective if w in text]
        if found_subjective:
            score -= 0.1 * len(found_subjective)
            flags.append("subjective_language")
            notes.append(f"Found subjective terms: {found_subjective}")

        return ScoreDetail(
            score=max(0.0, min(1.0, score)),
            flags=flags,
            notes="; ".join(notes) if notes else "Neutral tone maintained."
        )

class ReflectionScorer(HACSBaseScorer):
    """
    Evaluates self-correction and awareness of limits.
    Heuristic: Presence of epistemic markers.
    """
    def score(self, response: str, question: Dict[str, Any]) -> ScoreDetail:
        text = response.lower()
        score = 0.4 # Baseline low, must earn reflection
        flags = []
        notes = []

        # Heuristic 1: Uncertainty markers (Positive for Reflection)
        markers = ["it depends", "not sure", "unclear", "arguably", "context", "might", "potentially"]
        found_markers = [w for w in markers if w in text]
        
        if found_markers:
            score += 0.1 * len(found_markers)
            flags.append("reflection_markers")
            notes.append(f"Found reflection markers: {found_markers}")
        
        # Heuristic 2: explicit limit acknowledgement
        limits = ["limit", "constraint", "unknown", "cannot predict"]
        if any(w in text for w in limits):
            score += 0.2
            notes.append("Acknowledged limits.")

        return ScoreDetail(
            score=max(0.0, min(1.0, score)),
            flags=flags,
            notes="; ".join(notes) if notes else "Low reflection signals."
        )

class StabilityScorer(HACSBaseScorer):
    """
    Evaluates consistency across structure and tone.
    Heuristic: Formatting consistency, absence of sudden shifts.
    """
    def score(self, response: str, question: Dict[str, Any]) -> ScoreDetail:
        # Without multi-shot history, we check structural stability
        score = 0.8
        flags = []
        notes = []

        lines = response.split('\n')
        if len(lines) > 1:
            # Check if lines have widely different lengths (e.g. erratic formatting)
            lengths = [len(l) for l in lines if l.strip()]
            if lengths:
                mean_len = statistics.mean(lengths)
                variance = statistics.variance(lengths) if len(lengths) > 1 else 0
                if variance > 1000: # High variance might indicate erratic formatting
                    # Not necessarily bad, but potentially unstable structure
                    pass 

        # Placeholder: Stability is hard to measure on single turn without history
        # We assume high stability unless formatted weirdly
        if "ERROR" in response or "Exception" in response:
            score = 0.0
            flags.append("error_output")
            notes.append("Response contains error message.")

        return ScoreDetail(
            score=score,
            flags=flags,
            notes="; ".join(notes) if notes else "Output appears stable."
        )

# --- Engine ---

class HACSScoringEngine:
    def __init__(self):
        self.scorers = {
            "clarity": ClarityScorer(),
            "consistency": ConsistencyScorer(),
            "depth": DepthScorer(),
            "neutrality": NeutralityScorer(),
            "reflection": ReflectionScorer(),
            "stability": StabilityScorer()
        }

    def get_maturity_level(self, score: float) -> str:
        if score < 0.30: return "unstable"
        if score < 0.60: return "weak"
        if score < 0.80: return "solid"
        if score < 0.90: return "strong"
        return "mature"

    def score_question(self, question_id: str, response: str, question_data: Dict[str, Any]) -> ScoreResult:
        scores = {}
        explanation = {}
        all_flags = []

        for name, scorer in self.scorers.items():
            result = scorer.score(response, question_data)
            scores[name] = round(result.score, 2)
            explanation[name] = result.notes
            all_flags.extend(result.flags)

        overall = statistics.mean(scores.values())
        
        # Critical Failure Check
        if "error_output" in all_flags:
            overall = 0.0
            explanation["system"] = "Critical Failure: Error output detected. Score set to 0.0."

        return ScoreResult(
            question_id=question_id,
            scores=scores,
            overall_score=round(overall, 2),
            maturity_level=self.get_maturity_level(overall),
            flags=list(set(all_flags)),
            explanation=explanation
        )

    def aggregate_module(self, module_id: str, results: List[ScoreResult]) -> ModuleAggregation:
        if not results:
            return ModuleAggregation(
                module_id=module_id,
                question_count=0,
                average_scores={},
                overall_module_score=0.0,
                variance=0.0
            )

        # Average per criteria
        criteria_sums = {k: 0.0 for k in self.scorers.keys()}
        for res in results:
            for k, v in res.scores.items():
                criteria_sums[k] += v
        
        count = len(results)
        avg_scores = {k: round(v / count, 2) for k, v in criteria_sums.items()}
        
        # Overall module score (mean of means)
        overall = statistics.mean(avg_scores.values())
        
        # Variance of overall scores
        overalls = [r.overall_score for r in results]
        variance = statistics.variance(overalls) if len(overalls) > 1 else 0.0

        return ModuleAggregation(
            module_id=module_id,
            question_count=count,
            average_scores=avg_scores,
            overall_module_score=round(overall, 2),
            variance=round(variance, 4)
        )

    def generate_report(self, run_id: str, results: List[ScoreResult], module_map: Dict[str, str]) -> OverallReport:
        # Group by module
        module_results = {}
        for r in results:
            # We need to look up module_id from question_id or pass it in.
            # Assuming question_id starts with "h1", "h2" etc or we use the map
            # simple heuristic: h1_q_01 -> h1
            mod_id = r.question_id.split('_')[0]
            if mod_id not in module_results:
                module_results[mod_id] = []
            module_results[mod_id].append(r)

        summaries = {}
        module_scores = []
        
        for mod_id, res_list in module_results.items():
            agg = self.aggregate_module(mod_id, res_list)
            summaries[mod_id] = agg
            module_scores.append(agg.overall_module_score)

        overall_total = statistics.mean(module_scores) if module_scores else 0.0

        return OverallReport(
            run_id=run_id,
            total_questions=len(results),
            overall_score=round(overall_total, 2),
            maturity_level=self.get_maturity_level(overall_total),
            module_summaries=summaries
        )
