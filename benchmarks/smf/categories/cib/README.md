# Context Integration Benchmarks (CIB)

## Conceptual Definition
Context Integration measures the model's ability to maintain a coherent mental model of a conversation or document over time. It evaluates how well the model integrates new information with previously established facts and how effectively it switches between different contexts without "bleeding" information.

## Measured Capability
**Context Handling:** The ability to retain, recall, and update state information across a sequence of interactions.

## What It Measures
*   **Retention:** Remembering facts stated early in a long context.
*   **Context Switching:** Cleanly moving from Topic A to Topic B without confusion.
*   **Implicit Context:** Understanding unstated but implied information based on previous turns.
*   **Resolution:** Resolving pronouns ("it", "he") correctly based on history.

## What It Explicitly Does NOT Measure
*   **Long-Context Capacity (Raw):** While related to token limits, CIB focuses on the *logic* of context, not just the *volume* (though LFCB overlaps here). CIB is often conversational; LFCB is often document-based.
*   **Factuality:** It measures internal consistency with the *provided* context, not external truth.

## Typical Failure Modes
*   **Catastrophic Forgetting:** Losing track of earlier instructions.
*   **Context Bleed:** Mixing up details from two distinct scenarios presented in the same session.
*   **Recency Bias:** Over-weighting the most recent input while ignoring established constraints.

## Relation to Other Categories
*   **Contrast with LFCB:** CIB focuses on dynamic, interactive context (chat); LFCB focuses on static, long-form coherence (documents).
*   **Contrast with MCB:** MCB is static (single turn coherence); CIB is dynamic (multi-turn coherence).

## Expected Benchmark Formats
*   **Multi-turn Dialogues:** Simulating a conversation with evolving constraints.
*   **State Tracking:** "I have 3 apples." ... (distractor) ... "I eat one." -> "How many left?"
*   **Role Switching:** "Act as a pirate." ... "Now act as a doctor." (Check for pirate slang in doctor response).
