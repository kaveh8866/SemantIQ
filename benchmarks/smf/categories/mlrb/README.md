# Multilingual & Linguistic Reasoning Benchmarks (MLRB)

## Conceptual Definition
Multilingual & Linguistic Reasoning Benchmarks test the model's proficiency across languages and its understanding of linguistic structures. It ensures that semantic capabilities (logic, nuance) transfer across language boundaries.

## Measured Capability
**Multilingualism:** The ability to understand and generate text fluently in multiple languages and code-switch effectively.

## What It Measures
*   **Translation Quality:** Accuracy and fluency of translation.
*   **Idiom Handling:** Translating meaning, not just words ("It's raining cats and dogs").
*   **Cross-Lingual Consistency:** Does the model give the same answer in English and Spanish?
*   **Low-Resource Languages:** Performance in languages with less training data.

## What It Explicitly Does NOT Measure
*   **Cultural Knowledge (SSB):** Knowing *how* to speak French vs. knowing French *culture*.

## Typical Failure Modes
*   **Hallucination:** Inventing words in the target language.
*   **Anglocentrism:** Translating idioms literally from English.
*   **Grammar Failures:** Incorrect gender/case agreement.

## Relation to Other Categories
*   **Contrast with MCB:** MLRB is MCB applied across languages.

## Expected Benchmark Formats
*   **Translation:** English -> Target -> English (Back-translation).
*   **Cross-Lingual QA:** Question in English, Answer in German.
*   **Linguistic Puzzles:** Grammar correction tasks.
