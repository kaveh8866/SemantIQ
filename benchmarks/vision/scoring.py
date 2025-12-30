import json
import os
import hashlib
import random
from typing import Dict, List, Any, Optional, Union
from pydantic import BaseModel, Field
import yaml
from datetime import datetime

# --- Data Models ---

class ScoreResult(BaseModel):
    prompt_id: str
    image_id: str
    scores: Dict[str, float]
    overall_score: float
    flags: List[str] = []
    explanations: Dict[str, str] = {}

class CategorySummary(BaseModel):
    category_id: str
    mean_score: float
    prompt_scores: Dict[str, float]
    rubric_scores: Dict[str, float]
    violation_rate: float

class RunReport(BaseModel):
    run_id: str
    timestamp: str
    provider: str
    model: str
    overall_score: float
    category_summaries: Dict[str, CategorySummary]
    notes: Optional[str] = None

# --- Interfaces ---

class BaseScorer:
    """Base class for rubric scorers."""
    def score(self, image_path: str, prompt_data: Dict[str, Any]) -> float:
        raise NotImplementedError

    def explain(self, score: float, prompt_data: Dict[str, Any]) -> str:
        raise NotImplementedError

# --- Mock Scorers (Deterministic Heuristics) ---

class DeterministicMockScorer(BaseScorer):
    """
    A mock scorer that generates deterministic scores based on the image filename/hash.
    This simulates a functioning scorer for pipeline validation without needing CV models.
    """
    def __init__(self, rubric_name: str):
        self.rubric_name = rubric_name

    def score(self, image_path: str, prompt_data: Dict[str, Any]) -> float:
        # Use image filename hash to seed random generator for determinism
        filename = os.path.basename(image_path)
        seed_str = f"{filename}_{self.rubric_name}"
        seed_val = int(hashlib.sha256(seed_str.encode('utf-8')).hexdigest(), 16)
        random.seed(seed_val)
        
        # Bias towards high scores to simulate "good" models, but with variance
        base_score = 0.7 + (random.random() * 0.3) # 0.7 - 1.0
        
        # Introduce occasional failures
        if random.random() < 0.1:
            base_score = random.random() * 0.5 # 0.0 - 0.5
            
        return round(base_score, 2)

    def explain(self, score: float, prompt_data: Dict[str, Any]) -> str:
        if score > 0.8:
            return f"High adherence to {self.rubric_name} requirements."
        elif score > 0.5:
            return f"Moderate issues detected in {self.rubric_name}."
        else:
            return f"Significant failure in {self.rubric_name}."

# --- Engine ---

class VisionScoringEngine:
    def __init__(self, mapping_path: str = "benchmarks/vision/scoring_mapping.yaml"):
        self.mapping = self._load_mapping(mapping_path)
        self.scorers = {
            "object_presence": DeterministicMockScorer("object_presence"),
            "attribute_fidelity": DeterministicMockScorer("attribute_fidelity"),
            "semantic_coherence": DeterministicMockScorer("semantic_coherence"),
            "compositional_accuracy": DeterministicMockScorer("compositional_accuracy"),
            "object_count": DeterministicMockScorer("object_count"),
            "attribute_binding": DeterministicMockScorer("attribute_binding"),
            "relation_correctness": DeterministicMockScorer("relation_correctness"),
            "spatial_consistency": DeterministicMockScorer("spatial_consistency"),
            "counting_accuracy": DeterministicMockScorer("counting_accuracy"),
            "negation_handling": DeterministicMockScorer("negation_handling"),
            "constraint_adherence": DeterministicMockScorer("constraint_adherence"),
            "style_consistency": DeterministicMockScorer("style_consistency"),
            "stability_across_runs": DeterministicMockScorer("stability_across_runs"),
        }

    def _load_mapping(self, path: str) -> Dict[str, Any]:
        if not os.path.exists(path):
            raise FileNotFoundError(f"Mapping file not found: {path}")
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        return data.get("mappings", {})

    def score_image(self, image_path: str, prompt_data: Dict[str, Any]) -> ScoreResult:
        category_id = prompt_data.get("category_id")
        mapping = self.mapping.get(category_id)
        
        if not mapping:
            # Fallback or error
            rubrics = ["object_presence", "semantic_coherence"]
        else:
            rubrics = mapping.get("primary_rubrics", []) + mapping.get("secondary_rubrics", [])

        scores = {}
        explanations = {}
        flags = []
        
        total_score = 0.0
        count = 0

        for rubric in rubrics:
            scorer = self.scorers.get(rubric)
            if scorer:
                s = scorer.score(image_path, prompt_data)
                scores[rubric] = s
                explanations[rubric] = scorer.explain(s, prompt_data)
                
                total_score += s
                count += 1
                
                if s < 0.5:
                    flags.append(f"low_{rubric}")
            else:
                # Missing scorer implementation
                scores[rubric] = 0.0
                explanations[rubric] = "Scorer not implemented"
        
        overall = round(total_score / count, 2) if count > 0 else 0.0
        
        return ScoreResult(
            prompt_id=prompt_data.get("prompt_id"),
            image_id=os.path.basename(image_path),
            scores=scores,
            overall_score=overall,
            flags=flags,
            explanations=explanations
        )

    def score_run(self, run_id: str) -> RunReport:
        run_dir = os.path.join("runs", "vision", run_id)
        images_dir = os.path.join(run_dir, "images")
        meta_path = os.path.join(run_dir, "metadata", "IMAGE_METADATA.json")
        run_meta_path = os.path.join(run_dir, "metadata", "RUN_METADATA.json")
        
        if not os.path.exists(meta_path):
            raise FileNotFoundError(f"Metadata not found for run {run_id}")
            
        with open(meta_path, "r") as f:
            image_metadata_list = json.load(f)
            
        run_meta = {}
        if os.path.exists(run_meta_path):
             with open(run_meta_path, "r") as f:
                run_meta = json.load(f)

        # Group by category
        category_results: Dict[str, List[ScoreResult]] = {}
        
        for meta in image_metadata_list:
            prompt_id = meta.get("prompt_id")
            prompt_hash = meta.get("prompt_hash")
            # Find image file (assuming png or jpg)
            image_filename = None
            for ext in [".png", ".jpg", ".jpeg"]:
                fname = f"{prompt_id}_{prompt_hash}{ext}"
                if os.path.exists(os.path.join(images_dir, fname)):
                    image_filename = fname
                    break
            
            if not image_filename:
                continue # Skip missing images
                
            image_path = os.path.join(images_dir, image_filename)
            
            result = self.score_image(image_path, meta)
            
            cat_id = meta.get("category_id", "unknown")
            if cat_id not in category_results:
                category_results[cat_id] = []
            category_results[cat_id].append(result)
            
        # Aggregate
        category_summaries = {}
        total_run_score = 0.0
        cat_count = 0
        
        for cat_id, results in category_results.items():
            mean_score = sum(r.overall_score for r in results) / len(results) if results else 0.0
            
            # Rubric breakdown
            rubric_sums = {}
            rubric_counts = {}
            for r in results:
                for k, v in r.scores.items():
                    rubric_sums[k] = rubric_sums.get(k, 0.0) + v
                    rubric_counts[k] = rubric_counts.get(k, 0) + 1
            
            rubric_means = {k: round(v / rubric_counts[k], 2) for k, v in rubric_sums.items()}
            
            # Prompt scores
            prompt_scores = {r.prompt_id: r.overall_score for r in results}
            
            # Violation rate (flagged < 0.5)
            violation_count = sum(1 for r in results if r.flags)
            violation_rate = round(violation_count / len(results), 2) if results else 0.0
            
            category_summaries[cat_id] = CategorySummary(
                category_id=cat_id,
                mean_score=round(mean_score, 2),
                prompt_scores=prompt_scores,
                rubric_scores=rubric_means,
                violation_rate=violation_rate
            )
            
            total_run_score += mean_score
            cat_count += 1
            
        overall_run_score = round(total_run_score / cat_count, 2) if cat_count > 0 else 0.0
        
        report = RunReport(
            run_id=run_id,
            timestamp=datetime.now().isoformat(),
            provider=run_meta.get("provider", "unknown"),
            model=run_meta.get("model", "unknown"),
            overall_score=overall_run_score,
            category_summaries=category_summaries
        )
        
        # Save Report
        report_dir = os.path.join("reports", "vision", "runs", run_id)
        os.makedirs(report_dir, exist_ok=True)
        
        with open(os.path.join(report_dir, "overall_summary.json"), "w") as f:
            json.dump(report.model_dump(), f, indent=2)
            
        # Per-prompt details
        prompt_scores_export = {}
        for cat_id, results in category_results.items():
            for r in results:
                prompt_scores_export[r.prompt_id] = r.model_dump()
                
        with open(os.path.join(report_dir, "prompt_scores.json"), "w") as f:
            json.dump(prompt_scores_export, f, indent=2)
            
        return report

