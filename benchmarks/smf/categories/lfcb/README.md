# Long-Form & Coherence Benchmarks (LFCB)

## Conceptual Definition
Long-Form & Coherence Benchmarks test the model's ability to construct and maintain valid mental models over extended texts. It evaluates narrative arcs, argument structures, and the retrieval of details from long contexts.

## Measured Capability
**Long-Context Coherence:** The ability to generate and process extended sequences without losing structure or detail.

## What It Measures
*   **Narrative Consistency:** Does the character's eye color stay the same in Chapter 10?
*   **Global Coherence:** Does the essay have a unified thesis?
*   **Needle in a Haystack:** Retrieving specific facts from large inputs.
*   **Summarization:** Condensing long texts without losing key points.

## What It Explicitly Does NOT Measure
*   **Short-Context Integration (CIB):** LFCB is about *scale*.
*   **Creativity (CCB):** LFCB focuses on *structure* and *consistency*.

## Typical Failure Modes
*   **Lost in the Middle:** Forgetting information in the middle of the context window.
*   **Wandering:** Losing the thread of the argument.
*   **Repetition:** Looping content when context gets too long.

## Relation to Other Categories
*   **Contrast with CIB:** See CIB.

## Expected Benchmark Formats
*   **Book Summarization:** "Summarize this 50-page PDF."
*   **Long-Form Generation:** "Write a 2000-word article."
*   **Retrieval:** "What was the code mentioned on page 4?"
