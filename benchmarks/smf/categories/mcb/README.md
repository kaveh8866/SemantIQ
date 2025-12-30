# Meaning Coherence Benchmarks (MCB)

## Conceptual Definition
Meaning Coherence measures the stability and internal consistency of a model's understanding across semantic variations. A semantically mature model should recognize that "The cat sat on the mat" and "The feline rested on the floor covering" convey the same core proposition, despite surface-level differences.

## Measured Capability
**Semantic Coherence:** The ability to maintain invariant meaning across rephrasing, structural changes, or minor noise injection.

## What It Measures
*   **Definition Stability:** Does the model define concepts consistently?
*   **Paraphrase Recognition:** Can it identify equivalent statements?
*   **Ambiguity Handling:** Does it resolve or flag ambiguous inputs consistently?
*   **Semantic Purity:** Does the model avoid hallucinating unrelated meanings into a focused concept?

## What It Explicitly Does NOT Measure
*   **Creativity:** It does not reward novel or flowery language if the core meaning shifts.
*   **Factual Accuracy:** It measures *consistency*, not necessarily truth (though truth is often coherent). A consistently wrong model is coherent, though factually incorrect (handled by QGB).

## Typical Failure Modes
*   **Drift:** The model changes its stance or definition when the question is phrased slightly differently.
*   **Hallucination:** Adding details that were not present in the source premise during paraphrasing.
*   **Fragility:** Failing to understand a concept because of a typo or unusual syntax.

## Relation to Other Categories
*   **Contrast with CCB (Creativity):** MCB values stability; CCB values divergence.
*   **Contrast with NCB (Nuance):** MCB focuses on *sameness* (equivalence); NCB focuses on *difference* (distinction).

## Expected Benchmark Formats
*   **Paraphrase Equivalence Tasks:** "Are these two sentences synonymous?"
*   **Definition Consistency:** Define X, then Define X (phrased differently). Compare.
*   **Perturbation Tests:** Input X -> Output Y. Input X' (noisy) -> Output Y' (should be close to Y).
