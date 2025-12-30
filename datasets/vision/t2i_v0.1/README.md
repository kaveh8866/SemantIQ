# SemantIQ-Vision T2I Prompt Set v0.1

## Purpose
This dataset contains the official **SemantIQ-Vision T2I Prompt Set v0.1**. It is designed to evaluate Text-to-Image models on **semantic correctness**, **constraint adherence**, and **compositional fidelity**.

Unlike aesthetic benchmarks, this set ignores "beauty" or "artistic merit". Instead, it asks: *Did the model draw exactly what was requested, and nothing else?*

## Dataset Structure
The dataset consists of **30 canonical prompts** distributed evenly across 6 categories (5 prompts each):

1.  **Single-Object Fidelity (SOF):** Testing basic object generation in isolation.
2.  **Multi-Object Composition (MOC):** Testing the ability to handle multiple distinct entities.
3.  **Spatial Relations (SPR):** Testing geometric understanding (on, under, left, right).
4.  **Attribute Binding & Counting (ABC):** Testing precise counting and attribute assignment.
5.  **Negation & Exclusion (NEX):** Testing the ability to *not* generate specific elements.
6.  **Style & Stability (SAS):** Testing adherence to style constraints independent of content.

## Evaluation Methodology
Each prompt includes:
*   **Intent:** What specific capability is being tested.
*   **Constraints:** Explicit, binary conditions for success (e.g., "Must be green").
*   **Expected Visual Properties:** Observable features required for a high score.
*   **Typical Failure Modes:** Common errors to watch for (e.g., "object fusion", "leakage").

## Usage
This dataset is intended for use with the SemantIQ benchmarking pipeline.
```bash
# List all prompts
bench vision list-prompts

# Filter by category
bench vision list-prompts --category spatial_relations
```

## Limitations
*   **Visual-Only:** Does not evaluate text rendering (OCR) or complex reasoning.
*   **English-Only:** All prompts are in English to ensure cross-model comparability.
*   **Static:** This is a fixed "Golden Set" for v0.1. Future versions may introduce dynamic templates.
