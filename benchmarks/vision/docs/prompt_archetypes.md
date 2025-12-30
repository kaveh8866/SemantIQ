# SemantIQ-Vision T2I Prompt Archetypes

## 1. Introduction: Why Prompt Archetypes?

In the SemantIQ-Vision framework, we deviate from the common practice of using unstructured, "wild" prompts for benchmarking. Instead, we introduce **Prompt Archetypes** as the fundamental unit of evaluation.

### 1.1 The Problem with Raw Prompts
Raw, unstructured prompts suffer from several benchmarking weaknesses:
*   **Memorization & Contamination:** Popular benchmarks (like COCO or parti-prompts) are often included in training datasets, allowing models to "recall" the image rather than "generate" it.
*   **Ambiguity:** A prompt like "a beautiful sunset" has no objective truth condition. Evaluation becomes subjective (aesthetic) rather than objective (semantic).
*   **Vendor Bias:** Prompts optimized for Midjourney v6 may fail on DALL-E 3 simply due to syntax preferences, not semantic capability.

### 1.2 The Archetype Solution
A **Prompt Archetype** is an abstract template or structural pattern that defines a specific semantic task (e.g., "draw exactly two objects," "draw X inside Y"). It is **content-agnostic** but **structure-rigid**.

By evaluating Archetypes, we measure a model's **underlying semantic engine** rather than its pattern matching on specific phrases.

## 2. Core Concepts

### 2.1 Definitions
*   **Prompt Archetype:** The abstract task definition (e.g., "Single Object Isolation"). Defines the *structure* and *constraints*.
*   **Concrete Prompt:** A specific instantiation of an archetype (e.g., "A photo of a red ceramic mug on a white table").
*   **Scoring Rubric:** The measurement criteria applied to the output (e.g., "Is the mug red?", "Is there only one mug?").

### 2.2 Enabling Scalability & Fairness
Archetypes enable:
*   **Controlled Variation:** We can instantiate the "Counting" archetype with 100 different objects to test robustness, rather than relying on a single "three cats" prompt.
*   **Cross-Model Comparison:** All models face the same *structural* challenges, leveling the playing field regarding prompt syntax.
*   **Dataset Scaling:** We can algorithmically generate thousands of test cases from a single archetype definition.

## 3. Risk & Design Notes

### 3.1 Style vs. Semantics Isolation
We deliberately isolate **Style Archetypes (SAS)** from semantic ones.
*   *Why?* Models often trade off semantic adherence for aesthetic style. By separating them, we can measure "Can it draw a cat?" independently of "Can it draw an oil painting?"
*   If a prompt asks for "a cyberpunk cat," a failure might be due to the complex style overriding the object definition. Isolating them pinpoints the failure mode.

### 3.2 Anti-Gaming Measures
To prevent "gaming" the benchmark (optimizing for specific test prompts):
*   **No Artist Names:** We do not use "in the style of Greg Rutkowski". This tests training data memorization, not style generalization.
*   **No Camera Models:** We avoid "shot on Sony A7R IV" to prevent triggering vendor-specific photographic biases.
*   **No Vendor Defaults:** We avoid syntax specific to one model (e.g., `--v 6.0` or `::2` weights).

### 3.3 Limits of Visual Evaluation
We acknowledge that purely visual evaluation (without human aesthetic judgment) has limits.
*   Archetypes focus on **observable properties** (counts, colors, positions).
*   They do **not** measure "beauty," "creativity," or "impact."
*   SemantIQ-Vision is a measure of **correctness**, not art.
