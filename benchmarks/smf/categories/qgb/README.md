# Query & Grounding Benchmarks (QGB)

## Conceptual Definition
Query & Grounding Benchmarks evaluate the model's ability to anchor its responses in reality or provided source material. It measures the reduction of hallucinations and the accuracy of citations.

## Measured Capability
**Knowledge Grounding:** The ability to distinguish fact from fiction and cite sources.

## What It Measures
*   **Hallucination Rate:** Frequency of invented facts.
*   **RAG Fidelity:** Answering *only* using the provided documents.
*   **Citation:** Correctly attributing information to its source.
*   **Knowledge Boundaries:** Admitting "I don't know" when appropriate.

## What It Explicitly Does NOT Measure
*   **Reasoning (RFB):** QGB is about *facts*, not *derivation*.
*   **Creativity (CCB):** QGB penalizes invention.

## Typical Failure Modes
*   **Hallucination:** "The Eiffel Tower is in London."
*   **Citation Fabrication:** Citing a real paper that doesn't contain the claim.
*   **Sycophancy:** Agreeing with a user's false premise.

## Relation to Other Categories
*   **Contrast with MCB:** MCB is about consistency; QGB is about truth.

## Expected Benchmark Formats
*   **Fact Checking:** "Is this statement true?"
*   **RAG Tasks:** "Answer using only this text."
*   **Unanswerable Questions:** "Who is the president of the moon?" (Should say unknown).
