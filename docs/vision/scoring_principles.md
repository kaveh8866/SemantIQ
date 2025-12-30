# SemantIQ-Vision: Scoring Principles

## Core Philosophy
The SemantIQ-Vision benchmark prioritizes **semantic correctness** and **reproducibility** over aesthetic quality. Our scoring system is designed to be:

1.  **Observable**: Based on concrete visual evidence (e.g., "Is the red ball present?"), not subjective feeling.
2.  **Rule-Based & Deterministic**: Identical inputs and visual states yield identical scores.
3.  **Explainable**: Every score comes with a rationale or breakdown.
4.  **Non-Aesthetic**: We do not evaluate "beauty," "artistic merit," or "photorealism" unless explicitly requested by the prompt style.

## Canonical Rubrics
Scores are normalized to the range `[0.0, 1.0]`.

| Rubric | Description |
| :--- | :--- |
| `object_presence` | Is the requested object recognizable in the scene? |
| `attribute_fidelity` | Do objects match their described attributes (color, shape, material)? |
| `semantic_coherence` | Does the scene make logical sense (e.g., gravity, scale)? |
| `compositional_accuracy` | Are multiple objects arranged without unnatural blending? |
| `object_count` | Is the number of objects approximately correct? |
| `attribute_binding` | Are attributes correctly bound to their respective objects (no leakage)? |
| `relation_correctness` | Are specified relationships (X holding Y) depicted accurately? |
| `spatial_consistency` | Are spatial prepositions (left of, behind) respected? |
| `counting_accuracy` | Is the exact count of objects correct (strict)? |
| `negation_handling` | Are excluded elements truly absent? |
| `constraint_adherence` | Are all explicit constraints met? |
| `style_consistency` | Does the image adhere to the requested artistic style? |
| `stability_across_runs` | (Aggregation only) Variance metric across repeated runs. |

## Scoring Architecture
The scoring pipeline uses a modular "Scorer" architecture. Each scorer focuses on a specific aspect of the image.

### Levels of Evaluation
1.  **Prompt Level**: Aggregation of active rubrics for a single generated image.
2.  **Category Level**: Mean of all Prompt scores within a category.
3.  **Run Level**: Macro-average of Category scores.

## Limitations & Ethics
- **Automated Evaluation**: While we strive for determinism, automated CV models (VQA, Detection) have their own biases and error modes.
- **Pixel Identity**: We do not require pixel-perfect reproduction, but semantic reproduction.
- **Usage**: This benchmark is for regression testing and semantic capability measurement, NOT for ranking artistic capability.
