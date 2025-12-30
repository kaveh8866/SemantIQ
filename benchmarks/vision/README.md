# SemantIQ-Vision: Text-to-Image Benchmark Domain

**Version:** 0.1  
**Scope:** Semantic Correctness, Compositional Fidelity, Constraint Adherence

## Overview

SemantIQ-Vision is the third official domain of the SemantIQ-M-Benchmarks suite, designed to evaluate Text-to-Image (T2I) generation models. Unlike traditional benchmarks that often prioritize aesthetic quality or photorealism, SemantIQ-Vision strictly evaluates **semantic correctness**. It measures whether the generated image faithfully represents the logical and structural constraints defined in the prompt.

## Evaluation Philosophy

The core philosophy of SemantIQ-Vision is **"Truth over Beauty."**

*   **Semantic Correctness:** Does the image contain exactly what was asked for?
*   **Compositional Fidelity:** Are objects placed in the correct spatial relationship?
*   **Constraint Adherence:** Does the model respect negative constraints (e.g., "no red")?
*   **Reproducibility:** Evaluation relies on observable image properties, not subjective artistic merit.

## Key Differences from SMF & HACS

| Feature | SMF (Semantic Maturity) | HACS (Human-AI Comparison) | SemantIQ-Vision |
| :--- | :--- | :--- | :--- |
| **Input** | Text Prompts (QA) | Text Prompts (QA) | Text Prompts (T2I) |
| **Output** | Text | Text | Images |
| **Focus** | Reasoning, nuance, depth | Human-likeness, bias, stability | Semantic fidelity, spatial logic |
| **Scoring** | LLM-based / Heuristic | Comparative (Human vs AI) | VQA / Detection / Heuristic |

## Integration

SemantIQ-Vision integrates with the core pipeline:

*   **Pipeline:** Uses the standard SemantIQ execution flow.
*   **Caching:** Image outputs are hashed and cached to ensure reproducibility.
*   **UI Visualization:** Results are displayed with side-by-side prompt-image pairs and annotated bounding boxes (future VQA integration).

## Architecture & Risk Notes

### Why Semantic Correctness?
Current T2I models excel at aesthetics but struggle with complex logic (e.g., "a red cube on a blue sphere"). Focusing on semantics provides a more rigorous test of a model's "understanding" of language.

### Risks & Mitigations

1.  **Prompt Memorization:**
    *   *Risk:* Models trained on common benchmark prompts (e.g., COCO) may overfit.
    *   *Mitigation:* SemantIQ-Vision uses synthetic, combinatorially generated prompts to minimize overlap with training data.

2.  **Style Leakage:**
    *   *Risk:* Prompts asking for specific objects might trigger associated styles (e.g., "cyberpunk" style for "robot").
    *   *Mitigation:* Prompts are strictly neutral and minimal. No style tokens are used unless the category is explicitly `Style Stability`.

3.  **Vendor-Specific Defaults:**
    *   *Risk:* Models like Midjourney or DALL-E have strong default aesthetics that can mask semantic failures.
    *   *Mitigation:* Evaluation metrics (Rubrics) ignore style and focus solely on object presence, count, and attributes.

### Controlled Prompts
Prompts in this benchmark are **minimal and constrained**. They avoid "prompt engineering" tricks to expose the raw capability of the model. If a model requires complex engineering to produce a red box, it fails the "Attribute Binding" test.

---
*All technical artifacts, code, and documentation in this repository are maintained in English.*
