# SMF Benchmark Types & Methodology

## Introduction: Why Formal Benchmark Types?

The Semantic Maturity Framework (SMF) evaluates Large Language Models (LLMs) across a diverse spectrum of capabilities, from logical reasoning to emotional intelligence. A "one-size-fits-all" benchmark task structure (e.g., multiple-choice questions) is insufficient to capture this nuance.

Different semantic capabilities require different forms of stress testing:
*   **Coherence** is best tested by comparing outputs to slightly varied inputs (Contrastive Evaluation).
*   **Reasoning** requires explicit step-by-step derivation (Question-Based Evaluation).
*   **Context Handling** needs multi-turn or fragmented inputs (Context Reconstruction).
*   **Creativity** demands open-ended, long-form generation (Long-Form Generation).

By explicitly defining **Benchmark Types (Task Archetypes)**, we achieve:

1.  **Prevention of Overfitting:** Models cannot just optimize for "answering questions." They must demonstrate stability, reconstruction, and generation capabilities.
2.  **Comparability:** We ensure that "Reasoning" is always tested via rigorous methods, while "Creativity" is tested via generative methods, preventing apples-to-oranges comparisons.
3.  **UI & Pipeline Integration:** The UI can render specialized views for each task type (e.g., side-by-side diffs for Contrastive Evaluation vs. markdown rendering for Long-Form Generation).

## Canonical Benchmark Types

### A) Question-Based Evaluation (QBE)
*   **Description:** Direct questions or tasks with clear success criteria.
*   **Focus:** Explicit answer quality, factuality, and logical derivation.
*   **Use Case:** Testing knowledge, logic, and simple instruction following.

### B) Contrastive Evaluation (CE)
*   **Description:** The model is presented with multiple related inputs (e.g., paraphrases, perturbations) and the outputs are compared.
*   **Focus:** Stability, consistency, and differentiation.
*   **Use Case:** Meaning Coherence (MCB), Robustness (RAS).

### C) Context Reconstruction Tasks (CRT)
*   **Description:** The model receives fragmented, implicit, or noisy context and must act coherently within it.
*   **Focus:** Internal state maintenance and inference.
*   **Use Case:** Context Integration (CIB), Social Intelligence (SSB).

### D) Long-Form Generation Tasks (LFG)
*   **Description:** Production of extended, structured artifacts (essays, codebases, stories).
*   **Focus:** Coherence over time, structure maintenance, and avoiding semantic drift.
*   **Use Case:** Long-Form Coherence (LFCB), Creativity (CCB).

### E) Reflexive & Meta-Cognitive Tasks (RMT)
*   **Description:** Tasks requiring the model to assess its own knowledge, uncertainty, or ethical boundaries.
*   **Focus:** Self-awareness and honesty.
*   **Use Case:** Query Grounding (QGB), Ethical Alignment (ELB).

### F) Stress & Boundary Tasks (SBT)
*   **Description:** Edge cases, paradoxes, adversarial inputs, and ethical dilemmas without clear "right" answers.
*   **Focus:** Behavior under pressure and safety alignment.
*   **Use Case:** Robustness (RAS), Ethical Benchmarks (ELB).

## Risk & Design Notes

### Why Limit Long-Form Tasks?
Not all categories support Long-Form Generation (LFG). For example, **Meaning Coherence (MCB)** is difficult to measure in long essays because minor variations in phrasing can naturally lead to vastly different narratives (the "butterfly effect"). MCB is better measured via short, controlled **Contrastive Evaluation (CE)** where variables are isolated.

### Determinism in Stress Benchmarks
**Stress & Boundary Tasks (SBT)** are inherently less deterministic than logic puzzles. A model might refuse a jailbreak in 5 different ways, all valid. Therefore, scoring for SBT relies heavily on **heuristic** and **integrative** evaluation (e.g., "Did it refuse?" vs. "How did it refuse?"), rather than strict string matching.

### Pipeline Influence
The Task Type determines the pipeline execution strategy:
*   **QBE:** Simple Input -> Output -> Score.
*   **CE:** Input A -> Output A; Input B -> Output B -> Compare(A, B).
*   **LFG:** Input -> Stream Output -> Chunked Analysis.
