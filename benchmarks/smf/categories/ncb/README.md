# Nuance & Complexity Benchmarks (NCB)

## Conceptual Definition
Nuance & Complexity benchmarks test the model's ability to discern subtle distinctions in meaning, intent, and tone. A mature model should distinguish between "frugal" and "cheap," or between a polite request and a passive-aggressive demand.

## Measured Capability
**Nuance Detection:** The sensitivity to fine-grained semantic differences and subtext.

## What It Measures
*   **Subtext Recognition:** Identifying implied meaning (reading between the lines).
*   **Tonal Sensitivity:** Detecting and generating specific emotional tones.
*   **Complexity Handling:** Following multi-part instructions where constraints might conflict or require prioritization.
*   **Irony/Sarcasm:** Detecting non-literal meaning.

## What It Explicitly Does NOT Measure
*   **Logical Reasoning (RFB):** NCB is about *interpretation*, not necessarily formal deduction.
*   **Emotional Intelligence (EEB):** NCB identifies the nuance; EEB acts on it with empathy (though they are related).

## Typical Failure Modes
*   **Literalism:** Taking idioms or sarcasm literally.
*   **Flattening:** Ignoring subtle distinctions and treating related concepts as identical.
*   **Instruction Skipping:** Missing one part of a complex, multi-clause instruction.

## Relation to Other Categories
*   **Contrast with MCB:** MCB checks if A == A'. NCB checks if A != A'' (where A'' is slightly different).
*   **Contrast with RFB:** RFB is binary (valid/invalid). NCB is spectral (shades of meaning).

## Expected Benchmark Formats
*   **Distinction Tasks:** "Explain the difference between 'regret' and 'remorse'."
*   **Subtext Analysis:** "What did the speaker imply by saying 'That's a... brave choice'?"
*   **Complex Instruction Following:** Prompts with 5+ interacting constraints.
