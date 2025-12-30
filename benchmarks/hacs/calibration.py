import sys
from typing import List, Dict, Any
from benchmarks.hacs.scoring import HACSScoringEngine

GOLDEN_SET = [
    {
        "id": "golden_perfect",
        "response": (
            "This complex issue depends significantly on the specific context provided. "
            "However, available data suggests that option A is often viable. "
            "Therefore, we might conclude that Y is a likely outcome, though unknown variables remain. "
            "It is crucial to acknowledge that these predictions have limits and cannot predict every outlier. "
            "The structure of this argument is designed to be as clear and logical as possible."
        ),
        "expected_range": (0.70, 1.00),
        "description": "High reflection, connectors, neutral tone."
    },
    {
        "id": "golden_poor",
        "response": "i think this stuff is maybe the worst ever. actually no correction: its just bad.",
        "expected_range": (0.00, 0.60),
        "description": "Lowercase, vague, subjective, contradictory."
    },
    {
        "id": "golden_error",
        "response": "An unexpected Runtime ERROR occurred during processing.",
        "expected_range": (0.00, 0.30),
        "description": "Contains error message."
    }
]

def run_calibration() -> bool:
    """
    Runs the HACS Scoring Engine against the Golden Set.
    Returns True if all checks pass, False otherwise.
    """
    engine = HACSScoringEngine()
    all_passed = True
    
    print("Running HACS Scoring Calibration...\n")
    print(f"{'ID':<15} | {'Score':<6} | {'Range':<12} | {'Status':<10}")
    print("-" * 50)

    for item in GOLDEN_SET:
        result = engine.score_question(item["id"], item["response"], {})
        score = result.overall_score
        min_exp, max_exp = item["expected_range"]
        
        passed = min_exp <= score <= max_exp
        status = "PASS" if passed else "FAIL"
        color = "\033[92m" if passed else "\033[91m" # Green or Red
        reset = "\033[0m"
        
        print(f"{item['id']:<15} | {score:<6.2f} | {min_exp}-{max_exp:<9} | {color}{status}{reset}")
        
        if not passed:
            all_passed = False
            print(f"  -> Failure Details: {item['description']}")
            print(f"  -> Breakdown: {result.scores}")

    print("-" * 50)
    if all_passed:
        print("\033[92mCalibration Successful: All scorers operating within expected parameters.\033[0m")
    else:
        print("\033[91mCalibration Failed: Regression detected in scoring logic.\033[0m")

    return all_passed

if __name__ == "__main__":
    success = run_calibration()
    sys.exit(0 if success else 1)
