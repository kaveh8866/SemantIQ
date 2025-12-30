# Negation & Exclusion (NEX)

**Category ID:** `nex`

## Purpose
This category measures the model's ability to process negative constraints—what should *not* be in the image. T2I models notoriously struggle with negation, often focusing on the noun (e.g., "no elephants") and generating it anyway.

## What This Category Measures
*   **Exclusion Adherence:** Is the forbidden object truly absent?
*   **Negative Constraint Fidelity:** Are "without" attributes respected (e.g., "a landscape without trees")?
*   **Replacement Logic:** If an object is negated, is the space filled logically or left as a void?

## What It Does NOT Measure
*   **Positive Fidelity:** We care less about what *is* there, as long as the *forbidden* thing is not.
*   **Aesthetics:** A blank room is a valid output for "a room with no furniture".

## Typical Failure Modes
*   **Ironic Generation:** The model sees the token "elephant" in "no elephant" and generates an elephant.
*   **Ghosting:** Traces or outlines of the negated object appear.
*   **Attribute Persistence:** "A red ball not made of rubber" might still look rubbery.

## Relation to Other Categories
*   **Inverse of SOF/MOC:** Tests absence rather than presence.
*   **Advanced Logic:** Requires understanding semantic negation, not just visual recognition.

## Relation to SMF / HACS
*   **SMF:** Strongly related to "Reasoning" and "Instruction Following".
*   **HACS:** Relates to "Neutrality" (avoiding bias towards generating common objects despite negation) and "Reflection".
